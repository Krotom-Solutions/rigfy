from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.anuncio import Anuncio
import logging

logger = logging.getLogger(__name__)


async def anuncio_existe(db: AsyncSession, olx_id: str) -> bool:
    result = await db.execute(
        select(func.count()).where(Anuncio.olx_id == olx_id)
    )
    return result.scalar() > 0


async def salvar_anuncio(db: AsyncSession, dados: dict) -> Anuncio:
    anuncio = Anuncio(**dados)
    db.add(anuncio)
    await db.commit()
    await db.refresh(anuncio)
    return anuncio


async def buscar_sem_descricao(db: AsyncSession, limite: int = 50) -> list[Anuncio]:
    result = await db.execute(
        select(Anuncio)
        .where(Anuncio.descricao.is_(None))
        .limit(limite)
    )
    return result.scalars().all()


async def atualizar_descricao(
    db: AsyncSession,
    olx_id: str,
    descricao: str,
    specs: dict,
) -> None:
    result = await db.execute(select(Anuncio).where(Anuncio.olx_id == olx_id))
    anuncio = result.scalar_one_or_none()
    if anuncio:
        anuncio.descricao = descricao
        for campo, valor in specs.items():
            if hasattr(anuncio, campo):
                setattr(anuncio, campo, valor)
        await db.commit()


async def contar_anuncios(db: AsyncSession) -> dict:
    total = await db.execute(select(func.count()).select_from(Anuncio))
    com_preco = await db.execute(
        select(func.count()).where(Anuncio.preco.isnot(None))
    )
    com_specs = await db.execute(
        select(func.count()).where(Anuncio.specs_extraidas == True)  # noqa: E712
    )
    return {
        "total": total.scalar(),
        "com_preco": com_preco.scalar(),
        "com_specs_extraidas": com_specs.scalar(),
    }
