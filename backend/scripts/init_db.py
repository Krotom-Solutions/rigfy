"""
Cria todas as tabelas no banco (idempotente — não destrói dados existentes).
Execute: .venv/Scripts/python scripts/init_db.py
"""
import asyncio
from dotenv import load_dotenv
load_dotenv()

from app.core.database import engine, Base
from app.models.anuncio import Anuncio  # noqa: importa o model para registrar metadata


async def main():
    print("Criando tabelas...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("OK - tabelas criadas/verificadas.")
    await engine.dispose()


asyncio.run(main())
