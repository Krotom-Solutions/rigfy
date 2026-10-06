import asyncio
import asyncpg
from collections import Counter
import pandas as pd

async def main():
    conn = await asyncpg.connect(
        host='aws-1-sa-east-1.pooler.supabase.com',
        port=5432,
        user='postgres.zoxzmbsuzycskzdfdspk',
        password='#@Rigfy2026#@',
        database='postgres',
        ssl='require',
        timeout=15,
    )
    rows = await conn.fetch('''
        SELECT id, categoria, cpu_fabricante, cpu_linha, cpu_geracao, gpu, ram_gb, ram_tipo, storage_gb, preco, titulo
        FROM anuncios
    ''')
    await conn.close()
    
    print(f"Total de registros analisados: {len(rows)}")
    
    df = pd.DataFrame([dict(r) for r in rows])
    
    print("\n" + "="*50)
    print("1. DISTRIBUIÇÃO POR CATEGORIA")
    print("="*50)
    print(df['categoria'].value_counts(dropna=False))
    
    print("\n" + "="*50)
    print("2. TOP 12 PLACAS DE VÍDEO (GPU)")
    print("="*50)
    print(df['gpu'].dropna().value_counts().head(12))

    print("\n" + "="*50)
    print("3. TOP 12 PROCESSADORES (CPU)")
    print("="*50)
    cpu_series = df.apply(
        lambda r: f"{r['cpu_fabricante'] or ''} {r['cpu_linha'] or ''} {r['cpu_geracao'] or ''}".strip(),
        axis=1
    )
    cpu_series = cpu_series[cpu_series != '']
    print(cpu_series.value_counts().head(12))

    print("\n" + "="*50)
    print("4. TOP MEMÓRIAS RAM")
    print("="*50)
    ram_series = df.apply(
        lambda r: f"{r['ram_gb']}GB {r['ram_tipo'] or ''}".strip() if pd.notnull(r['ram_gb']) else None,
        axis=1
    )
    print(ram_series.dropna().value_counts().head(8))

    print("\n" + "="*50)
    print("5. COMBINAÇÕES MAIS COMUNS (GPU + CPU + RAM)")
    print("="*50)
    combos = df.apply(
        lambda r: f"GPU: {r['gpu'] or 'N/A'} | CPU: {r['cpu_linha'] or 'N/A'} | RAM: {r['ram_gb'] or 'N/A'}GB | Cat: {r['categoria'] or 'N/A'}",
        axis=1
    )
    print(combos.value_counts().head(10))

    print("\n" + "="*50)
    print("6. MÉDIA E MEDIANA DE PREÇOS REAIS DOS HARDWARES MAIS FREQUENTES")
    print("="*50)
    top_gpus = df['gpu'].dropna().value_counts().head(5).index
    for g in top_gpus:
        sub = df[df['gpu'] == g]['preco'].dropna()
        print(f"GPU {g:15s} -> Qtd: {len(sub):2d} | Preço Médio: R$ {sub.mean():.2f} | Mediana: R$ {sub.median():.2f} | Min: R$ {sub.min():.2f} | Max: R$ {sub.max():.2f}")

if __name__ == '__main__':
    asyncio.run(main())
