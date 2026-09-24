import os
import asyncio
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.anuncio import Anuncio
from app.ml.pipeline import criar_pipeline_ml, preparar_dataframe, prever_faixa_preco

VAL_DIR = "validation"
SEED = 42
np.random.seed(SEED)

async def main():
    print("1. Carregando anúncios limpos do banco...")
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Anuncio).where(Anuncio.preco.isnot(None)))
        anuncios = res.scalars().all()
        
    dados = []
    for a in anuncios:
        dados.append({
            "id": a.id,
            "titulo": a.titulo,
            "descricao": (a.descricao or "")[:200],
            "preco_real": a.preco,
            "categoria": a.categoria or "outro",
            "marca": a.marca,
            "cpu_linha": a.cpu_linha,
            "cpu_geracao": a.cpu_geracao,
            "ram_gb": a.ram_gb,
            "ram_tipo": a.ram_tipo,
            "storage_gb": a.storage_gb,
            "storage_tipo": a.storage_tipo,
            "gpu": a.gpu,
            "gpu_vram_gb": getattr(a, "gpu_vram_gb", None),
            "gpu_memoria_tipo": getattr(a, "gpu_memoria_tipo", None),
            "ano_lancamento": getattr(a, "ano_lancamento", None),
        })
        
    df = pd.DataFrame(dados)
    print(f"Total de anúncios disponíveis: {len(df)}")
    
    # 2. Separação Estratificada do Hold-Out (30 anúncios)
    amostras_teste = []
    for cat in ["gpu", "cpu", "notebook", "desktop"]:
        sub = df[df["categoria"] == cat]
        qtd = min(len(sub), 7 if cat in ["gpu", "cpu"] else 8)
        if qtd > 0:
            amostras_teste.append(sub.sample(n=qtd, random_state=SEED))
            
    df_teste = pd.concat(amostras_teste).drop_duplicates(subset=["id"])
    if len(df_teste) < 30:
        restantes = df[~df["id"].isin(df_teste["id"])].sample(n=30 - len(df_teste), random_state=SEED)
        df_teste = pd.concat([df_teste, restantes])
        
    df_teste = df_teste.head(30).reset_index(drop=True)
    df_treino = df[~df["id"].isin(df_teste["id"])].reset_index(drop=True)
    
    print(f"Conjunto de Treino: {len(df_treino)} anúncios")
    print(f"Conjunto de Teste (Hold-out): {len(df_teste)} anúncios")
    
    # 3. Treina o Rigfy apenas no conjunto de treino
    y_treino = df_treino["preco_real"]
    X_treino = preparar_dataframe(df_treino)
    
    pipeline = criar_pipeline_ml()
    pipeline.fit(X_treino, y_treino)
    
    # 4. Baseline 1: Mediana simples por categoria
    mediana_categoria = df_treino.groupby("categoria")["preco_real"].median().to_dict()
    mediana_geral = df_treino["preco_real"].median()
    
    # 5. Avaliação no conjunto de Teste
    predicoes_rigfy = []
    predicoes_min = []
    predicoes_max = []
    predicoes_baseline = []
    
    for _, row in df_teste.iterrows():
        input_row = row.to_dict()
        pred = prever_faixa_preco(pipeline, input_row)
        predicoes_rigfy.append(pred["preco_estimado"])
        predicoes_min.append(pred["preco_minimo"])
        predicoes_max.append(pred["preco_maximo"])
        
        base_val = mediana_categoria.get(row["categoria"], mediana_geral)
        predicoes_baseline.append(base_val)
        
    df_teste["previsto_rigfy"] = predicoes_rigfy
    df_teste["faixa_min"] = predicoes_min
    df_teste["faixa_max"] = predicoes_max
    df_teste["previsto_baseline"] = predicoes_baseline
    
    # Salvar resultados preliminares
    df_teste.to_csv(os.path.join(VAL_DIR, "resultados.csv"), index=False)
    
    # 6. Gerar Formulário Cego para Avaliação Humana
    df_form = df_teste[["id", "categoria", "titulo", "descricao", "gpu", "cpu_linha", "ram_gb"]].copy()
    df_form["estimativa_humana_R$"] = ""
    df_form.to_csv(os.path.join(VAL_DIR, "formulario_humano.csv"), index=False)
    print("✅ Formulário cego gerado em validation/formulario_humano.csv")
    
    # 7. Cálculo de Métricas (Rigfy vs Baseline)
    y_true = df_teste["preco_real"].values
    y_rigfy = np.array(predicoes_rigfy)
    y_base = np.array(predicoes_baseline)
    
    def calcular_metricas(real, pred):
        mae = float(np.mean(np.abs(real - pred)))
        rmse = float(np.sqrt(np.mean((real - pred)**2)))
        mape = float(np.mean(np.abs((real - pred) / real)) * 100)
        ss_res = np.sum((real - pred)**2)
        ss_tot = np.sum((real - np.mean(real))**2)
        r2 = float(1 - (ss_res / ss_tot)) if ss_tot != 0 else 0.0
        acuracia_10 = float(np.mean(np.abs((real - pred) / real) <= 0.10) * 100)
        acuracia_20 = float(np.mean(np.abs((real - pred) / real) <= 0.20) * 100)
        return mae, rmse, mape, r2, acuracia_10, acuracia_20

    m_rigfy = calcular_metricas(y_true, y_rigfy)
    m_base = calcular_metricas(y_true, y_base)
    
    cobertura_faixa = float(np.mean((y_true >= np.array(predicoes_min)) & (y_true <= np.array(predicoes_max))) * 100)
    
    # 8. Gerar Tabela Markdown
    tabela_md = f"""# Resultados de Validação Experimental - Rigfy

Data da execução: 2026-09-24  
Tamanho do conjunto Hold-out: 30 anúncios (estratificados)  
Total de amostras de treino: {len(df_treino)} anúncios  
Seed de reprodutibilidade: {SEED}

## Tabela Comparativa de Métricas

| Métrica de Avaliação | Rigfy (Random Forest) | Baseline Estatístico (Mediana) | Estimativa Humana (Painel)* |
| :--- | :---: | :---: | :---: |
| **MAE (Erro Médio Absoluto)** | **R$ {m_rigfy[0]:.2f}** | R$ {m_base[0]:.2f} | *Aguardando participantes* |
| **RMSE (Raiz do Erro Quadrático)** | **R$ {m_rigfy[1]:.2f}** | R$ {m_base[1]:.2f} | *Aguardando participantes* |
| **MAPE (Erro Médio Percentual)** | **{m_rigfy[2]:.2f}%** | {m_base[2]:.2f}% | *Aguardando participantes* |
| **Coeficiente R²** | **{m_rigfy[3]:.3f}** | {m_base[3]:.3f} | *Aguardando participantes* |
| **Acurácia dentro de ±10%** | **{m_rigfy[4]:.1f}%** | {m_base[4]:.1f}% | *Aguardando participantes* |
| **Acurácia dentro de ±20%** | **{m_rigfy[5]:.1f}%** | {m_base[5]:.1f}% | *Aguardando participantes* |
| **Cobertura da Faixa Mín-Máx** | **{cobertura_faixa:.1f}%** | N/A | N/A |

*\*Nota: O formulário cego está disponível em `validation/formulario_humano.csv` para aplicação com pelo menos 5 pessoas.*
"""
    with open(os.path.join(VAL_DIR, "metricas.md"), "w", encoding="utf-8") as f:
        f.write(tabela_md)
    print("✅ Tabela de métricas salva em validation/metricas.md")
    
    # 9. Gerar Gráficos em Alta Resolução (P&B / Escala de Cinza)
    plt.style.use("grayscale")
    
    # Gráfico 1: Previsto vs Real
    plt.figure(figsize=(7, 6), dpi=300)
    plt.scatter(y_true, y_rigfy, color="black", alpha=0.7, edgecolors="black", label="Rigfy (Random Forest)")
    lim_max = max(float(np.max(y_true)), float(np.max(y_rigfy)))
    plt.plot([0, lim_max], [0, lim_max], "k--", linewidth=1.5, label="Predição Ideal (y = x)")
    plt.title("Valores Reais vs. Valores Previstos pelo Rigfy (Hold-out)", fontsize=11, fontweight="bold")
    plt.xlabel("Preço Real do Anúncio (R$)", fontsize=10)
    plt.ylabel("Preço Previsto (R$)", fontsize=10)
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(VAL_DIR, "previsto_vs_real.png"))
    plt.close()
    
    # Gráfico 2: Barras de MAE
    plt.figure(figsize=(6, 5), dpi=300)
    metodos = ["Rigfy (ML)", "Baseline (Mediana)"]
    maes = [m_rigfy[0], m_base[0]]
    bars = plt.bar(metodos, maes, color=["#404040", "#909090"], width=0.5, edgecolor="black")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f"R$ {yval:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    plt.title("Comparativo de Erro Médio Absoluto (MAE)", fontsize=11, fontweight="bold")
    plt.ylabel("MAE em Reais (R$)", fontsize=10)
    plt.ylim(0, max(maes) * 1.25)
    plt.tight_layout()
    plt.savefig(os.path.join(VAL_DIR, "barras_mae.png"))
    plt.close()
    
    # Gráfico 3: Boxplot do Erro Percentual
    plt.figure(figsize=(6, 5), dpi=300)
    erro_pct_rigfy = np.abs((y_true - y_rigfy) / y_true) * 100
    erro_pct_base = np.abs((y_true - y_base) / y_true) * 100
    plt.boxplot([erro_pct_rigfy, erro_pct_base], tick_labels=["Rigfy (ML)", "Baseline (Mediana)"], patch_artist=True,
                boxprops=dict(facecolor="#d0d0d0", color="black"), medianprops=dict(color="black", linewidth=2))
    plt.title("Distribuição do Erro Percentual Absoluto (MAPE)", fontsize=11, fontweight="bold")
    plt.ylabel("Erro Absoluto (%)", fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(VAL_DIR, "boxplot_erros.png"))
    plt.close()
    
    print("✅ Gráficos acadêmicos em escala de cinza gerados com sucesso em validation/!")

if __name__ == "__main__":
    asyncio.run(main())
