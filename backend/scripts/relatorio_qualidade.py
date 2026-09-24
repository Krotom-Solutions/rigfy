"""
Gera relatório de qualidade dos dados coletados.
Execute: PYTHONPATH=. .venv/Scripts/python scripts/relatorio_qualidade.py
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select, func, text
from app.core.database import AsyncSessionLocal
from app.models.anuncio import Anuncio


async def main():
    async with AsyncSessionLocal() as db:
        # Totais gerais
        total       = (await db.execute(select(func.count()).select_from(Anuncio))).scalar()
        com_preco   = (await db.execute(select(func.count()).where(Anuncio.preco.isnot(None)))).scalar()
        com_gpu     = (await db.execute(select(func.count()).where(Anuncio.gpu.isnot(None)))).scalar()
        com_vram    = (await db.execute(select(func.count()).where(Anuncio.gpu_vram_gb.isnot(None)))).scalar()
        com_lancam  = (await db.execute(select(func.count()).where(Anuncio.ano_lancamento.isnot(None)))).scalar()

        print("\n" + "="*60)
        print("RELATÓRIO DE QUALIDADE DOS DADOS")
        print("="*60)
        print(f"Total de anúncios:          {total:>6}")
        print(f"Com preço:                  {com_preco:>6}  ({100*com_preco/max(total,1):.1f}%)")
        print(f"Com GPU extraída:           {com_gpu:>6}  ({100*com_gpu/max(total,1):.1f}%)")
        print(f"Com VRAM extraída:          {com_vram:>6}  ({100*com_vram/max(total,1):.1f}%)")
        print(f"Com ano_lancamento:         {com_lancam:>6}  ({100*com_lancam/max(total,1):.1f}%)")

        # Por categoria
        print("\n--- Por categoria ---")
        cats = await db.execute(
            select(Anuncio.categoria, func.count(), func.avg(Anuncio.preco))
            .where(Anuncio.categoria.isnot(None))
            .group_by(Anuncio.categoria)
            .order_by(func.count().desc())
        )
        for row in cats:
            media = f"R$ {row[2]:.0f}" if row[2] else "sem preço"
            print(f"  {str(row[0]):<12} {row[1]:>5} anúncios | preço médio: {media}")

        # Top GPU modelos (peças avulsas)
        print("\n--- Top GPUs avulsas (categoria=gpu) ---")
        gpus = await db.execute(
            select(Anuncio.gpu, func.count(), func.avg(Anuncio.preco))
            .where(Anuncio.categoria == 'gpu')
            .where(Anuncio.gpu.isnot(None))
            .group_by(Anuncio.gpu)
            .order_by(func.count().desc())
            .limit(15)
        )
        for row in gpus:
            media = f"R$ {row[2]:.0f}" if row[2] else "sem preço"
            print(f"  {str(row[0]):<30} {row[1]:>4} | {media}")

        # Top CPUs avulsas
        print("\n--- Top CPUs avulsas (categoria=cpu) ---")
        cpus = await db.execute(
            select(Anuncio.cpu_linha, Anuncio.cpu_geracao, func.count(), func.avg(Anuncio.preco))
            .where(Anuncio.categoria == 'cpu')
            .where(Anuncio.cpu_linha.isnot(None))
            .group_by(Anuncio.cpu_linha, Anuncio.cpu_geracao)
            .order_by(func.count().desc())
            .limit(15)
        )
        for row in cpus:
            media = f"R$ {row[3]:.0f}" if row[3] else "sem preço"
            gen = f" Gen{row[1]}" if row[1] else ""
            print(f"  {str(row[0])}{gen:<35} {row[2]:>4} | {media}")

        # Top modelos de notebook/desktop por cpu_linha
        print("\n--- Notebooks/Desktops por CPU linha ---")
        nbs = await db.execute(
            select(Anuncio.categoria, Anuncio.cpu_linha, func.count(), func.avg(Anuncio.preco))
            .where(Anuncio.categoria.in_(['notebook', 'desktop']))
            .where(Anuncio.cpu_linha.isnot(None))
            .group_by(Anuncio.categoria, Anuncio.cpu_linha)
            .order_by(func.count().desc())
            .limit(15)
        )
        for row in nbs:
            media = f"R$ {row[3]:.0f}" if row[3] else "sem preço"
            print(f"  {str(row[0]):<10} {str(row[1]):<15} {row[2]:>4} | {media}")

        print("\n" + "="*60)


asyncio.run(main())
