"""Cria as tabelas no PostgreSQL. Rodar uma vez antes de iniciar o serviço."""
import asyncio
from app.core.database import engine, Base
from app.models.anuncio import Anuncio  # noqa: F401 — importar para registrar o model


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso.")
    await engine.dispose()


asyncio.run(init())
