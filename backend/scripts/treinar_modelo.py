import asyncio
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.anuncio import Anuncio
from app.ml.pipeline import criar_pipeline_ml, preparar_dataframe, salvar_modelo

async def treinar():
    print("Buscando anúncios limpos do banco Supabase...")
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Anuncio).where(Anuncio.preco.isnot(None)))
        anuncios = res.scalars().all()
        
    print(f"Total de registros carregados: {len(anuncios)}")
    
    dados = []
    for a in anuncios:
        dados.append({
            "preco": a.preco,
            "categoria": a.categoria,
            "marca": a.marca,
            "cpu_linha": a.cpu_linha,
            "cpu_geracao": a.cpu_geracao,
            "ram_gb": a.ram_gb,
            "ram_tipo": a.ram_tipo,
            "storage_gb": a.storage_gb,
            "storage_tipo": a.storage_tipo,
            "gpu": a.gpu,
            "gpu_vram_gb": a.gpu_vram_gb,
            "gpu_memoria_tipo": a.gpu_memoria_tipo,
            "ano_lancamento": a.ano_lancamento,
        })
        
    df = pd.DataFrame(dados)
    y = df["preco"]
    X = preparar_dataframe(df)
    
    print("Treinando Random Forest Regressor (100 árvores)... Esperando convergência...")
    pipeline = criar_pipeline_ml()
    pipeline.fit(X, y)
    
    salvar_modelo(pipeline)

if __name__ == "__main__":
    asyncio.run(treinar())
