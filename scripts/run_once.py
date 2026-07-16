"""Roda o scraper uma vez para testar. Útil durante desenvolvimento."""
import asyncio
from app.core.database import AsyncSessionLocal
from app.scraper.pipeline import executar_coleta


async def main():
    async with AsyncSessionLocal() as db:
        resumo = await executar_coleta(db)
        print(f"\nResumo da coleta:\n{resumo}")


asyncio.run(main())
