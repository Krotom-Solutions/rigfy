"""
Endpoint GET /listings — lista anúncios com filtros e paginação.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.models.anuncio import Anuncio
from app.schemas.api import AnuncioListItem, ListingsResponse

router = APIRouter(prefix="/listings", tags=["listings"])


@router.get("", response_model=ListingsResponse)
async def listar_anuncios(
    # Filtros
    categoria: str | None = Query(None, description="notebook | desktop"),
    marca: str | None = Query(None),
    cpu_linha: str | None = Query(None, description="Core i5, Ryzen 7 etc."),
    ram_gb: int | None = Query(None),
    storage_tipo: str | None = Query(None, description="SSD | SSD NVMe | HDD"),
    preco_min: float | None = Query(None),
    preco_max: float | None = Query(None),
    apenas_com_preco: bool = Query(False),
    # Paginação
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Lista anúncios com filtros opcionais e paginação."""

    # Monta filtros dinâmicos
    filtros = []
    if categoria:
        filtros.append(Anuncio.categoria == categoria)
    if marca:
        filtros.append(Anuncio.marca == marca)
    if cpu_linha:
        filtros.append(Anuncio.cpu_linha == cpu_linha)
    if ram_gb:
        filtros.append(Anuncio.ram_gb == ram_gb)
    if storage_tipo:
        filtros.append(Anuncio.storage_tipo == storage_tipo)
    if preco_min is not None:
        filtros.append(Anuncio.preco >= preco_min)
    if preco_max is not None:
        filtros.append(Anuncio.preco <= preco_max)
    if apenas_com_preco:
        filtros.append(Anuncio.preco.isnot(None))

    where_clause = and_(*filtros) if filtros else True

    # Contagem total
    count_result = await db.execute(
        select(func.count()).select_from(Anuncio).where(where_clause)
    )
    total = count_result.scalar()

    # Página de resultados
    offset = (page - 1) * per_page
    result = await db.execute(
        select(Anuncio)
        .where(where_clause)
        .order_by(Anuncio.coletado_em.desc())
        .offset(offset)
        .limit(per_page)
    )
    items = result.scalars().all()

    return ListingsResponse(
        total=total,
        page=page,
        per_page=per_page,
        items=[AnuncioListItem.model_validate(item) for item in items],
    )


@router.get("/opcoes", tags=["listings"])
async def opcoes_filtro(db: AsyncSession = Depends(get_db)):
    """Retorna os valores únicos disponíveis para cada filtro."""

    async def valores_distintos(coluna):
        result = await db.execute(
            select(coluna)
            .where(coluna.isnot(None))
            .distinct()
            .order_by(coluna)
        )
        return [r[0] for r in result.fetchall()]

    return {
        "categorias":    await valores_distintos(Anuncio.categoria),
        "marcas":        await valores_distintos(Anuncio.marca),
        "cpu_linhas":    await valores_distintos(Anuncio.cpu_linha),
        "ram_opcoes":    await valores_distintos(Anuncio.ram_gb),
        "storage_tipos": await valores_distintos(Anuncio.storage_tipo),
    }
