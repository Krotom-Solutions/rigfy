import os
import pandas as pd
import numpy as np
from scipy import stats

VAL_DIR = "validation"
res_path = os.path.join(VAL_DIR, "resultados.csv")
form_path = os.path.join(VAL_DIR, "formulario_humano.csv")

if not os.path.exists(form_path):
    print("❌ Arquivo validation/formulario_humano.csv não encontrado.")
    exit(1)

df_form = pd.read_csv(form_path)
df_res = pd.read_csv(res_path)

# Verifica se a coluna de estimativa foi preenchida
colunas_humanas = [c for c in df_form.columns if "estimativa" in c.lower() or "humano" in c.lower() or "participante" in c.lower()]
if not colunas_humanas or df_form[colunas_humanas[0]].dropna().empty:
    print("⚠️ As estimativas humanas ainda não foram preenchidas no CSV.")
    print("Preencha a coluna 'estimativa_humana_R$' em validation/formulario_humano.csv com os valores dos participantes.")
    exit(0)

# Média das estimativas se houver múltiplas colunas de participantes
estimativas_humanas = df_form[colunas_humanas].mean(axis=1).values
y_true = df_res["preco_real"].values
y_rigfy = df_res["previsto_rigfy"].values

mae_humano = float(np.mean(np.abs(y_true - estimativas_humanas)))
rmse_humano = float(np.sqrt(np.mean((y_true - estimativas_humanas)**2)))
mape_humano = float(np.mean(np.abs((y_true - estimativas_humanas) / y_true)) * 100)
acuracia_10 = float(np.mean(np.abs((y_true - estimativas_humanas) / y_true) <= 0.10) * 100)
acuracia_20 = float(np.mean(np.abs((y_true - estimativas_humanas) / y_true) <= 0.20) * 100)

print("\n" + "="*50)
print("MÉTRICAS DO PAINEL HUMANO")
print("="*50)
print(f"MAE Humano:    R$ {mae_humano:.2f}")
print(f"RMSE Humano:   R$ {rmse_humano:.2f}")
print(f"MAPE Humano:   {mape_humano:.2f}%")
print(f"Acerto em ±10%: {acuracia_10:.1f}%")
print(f"Acerto em ±20%: {acuracia_20:.1f}%")

# Teste Pareado de Wilcoxon (Rigfy vs Humano)
erro_rigfy = np.abs(y_true - y_rigfy)
erro_humano = np.abs(y_true - estimativas_humanas)

try:
    stat, p_val = stats.wilcoxon(erro_rigfy, erro_humano)
    print(f"\nTeste de Postos Sinalizados de Wilcoxon:")
    print(f"  Estatística W: {stat:.2f}")
    print(f"  p-valor:       {p_val:.4f}")
    if p_val < 0.05:
        print("  -> Diferença estatisticamente significativa ao nível de 5% (p < 0.05)!")
    else:
        print("  -> Não há evidência estatística de diferença significativa ao nível de 5% (p >= 0.05).")
except Exception as e:
    print(f"Erro ao computar teste pareado: {e}")
