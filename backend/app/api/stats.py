"""
Endpoint GET /stats/mercado — estatísticas de mercado para o dashboard.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text

from app.core.database import get_db
from app.models.anuncio import Anuncio
from app.schemas.api import MercadoStatsResponse, EstatisticaGrupo

router = APIRouter(prefix="/stats", tags=["stats"])


async def _stats_por_coluna(db: AsyncSession, coluna) -> list[EstatisticaGrupo]:
    """Calcula min/média/max/mediana de preço agrupado por uma coluna."""
    result = await db.execute(
        select(
            coluna.label("grupo"),
            func.count().label("total"),
            func.min(Anuncio.preco).label("minimo"),
            func.avg(Anuncio.preco).label("medio"),
            func.max(Anuncio.preco).label("maximo"),
            func.percentile_cont(0.5)
            .within_group(Anuncio.preco)
            .label("mediano"),
        )
        .where(coluna.isnot(None))
        .where(Anuncio.preco.isnot(None))
        .group_by(coluna)
        .order_by(func.count().desc())
        .limit(15)
    )
    rows = result.fetchall()
    return [
        EstatisticaGrupo(
            grupo=str(row.grupo),
            total_anuncios=row.total,
            preco_minimo=round(row.minimo, 2) if row.minimo else None,
            preco_medio=round(row.medio, 2) if row.medio else None,
            preco_maximo=round(row.maximo, 2) if row.maximo else None,
            preco_mediano=round(row.mediano, 2) if row.mediano else None,
        )
        for row in rows
    ]


@router.get("/mercado", response_model=MercadoStatsResponse)
async def estatisticas_mercado(db: AsyncSession = Depends(get_db)):
    """
    Retorna estatísticas de preço agrupadas por categoria, CPU, RAM e marca.
    Usado pelo dashboard do frontend para montar os gráficos.
    """
    # Totais gerais
    total_result = await db.execute(select(func.count()).select_from(Anuncio))
    total = total_result.scalar()

    com_preco_result = await db.execute(
        select(func.count()).where(Anuncio.preco.isnot(None))
    )
    com_preco = com_preco_result.scalar()

    return MercadoStatsResponse(
        total_anuncios=total,
        total_com_preco=com_preco,
        por_categoria=await _stats_por_coluna(db, Anuncio.categoria),
        por_cpu_linha=await _stats_por_coluna(db, Anuncio.cpu_linha),
        por_ram_gb=await _stats_por_coluna(db, Anuncio.ram_gb),
        por_marca=await _stats_por_coluna(db, Anuncio.marca),
    )


@router.get("/resumo")
async def resumo_coleta(db: AsyncSession = Depends(get_db)):
    """Resumo rápido para o card de status no dashboard."""
    total = await db.execute(select(func.count()).select_from(Anuncio))
    com_preco = await db.execute(
        select(func.count()).where(Anuncio.preco.isnot(None))
    )
    com_specs = await db.execute(
        select(func.count()).where(Anuncio.specs_extraidas == True)  # noqa: E712
    )
    preco_medio = await db.execute(
        select(func.avg(Anuncio.preco)).where(Anuncio.preco.isnot(None))
    )
    return {
        "total_anuncios": total.scalar(),
        "com_preco": com_preco.scalar(),
        "com_specs": com_specs.scalar(),
        "preco_medio_geral": round(preco_medio.scalar() or 0, 2),
    }
