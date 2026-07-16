"""
Endpoint POST /price/predict — estimativa de preço baseada nos dados coletados.

Estratégia atual: busca anúncios similares no banco e retorna estatísticas.
Próxima versão: modelo Random Forest treinado com scikit-learn.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.database import get_db
from app.models.anuncio import Anuncio
from app.schemas.api import PriceRequest, PriceResponse

router = APIRouter(prefix="/price", tags=["price"])


def _nivel_confianca(total: int) -> str:
    if total >= 20:
        return "alta"
    if total >= 8:
        return "media"
    if total >= 3:
        return "baixa"
    return "insuficiente"


@router.post("/predict", response_model=PriceResponse)
async def estimar_preco(
    req: PriceRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Estima o preço de mercado de um hardware com base nos anúncios coletados.
    Aplica filtros progressivos: do mais específico ao mais amplo,
    garantindo sempre uma resposta útil.
    """

    # Lista de filtros em ordem decrescente de especificidade
    # Tentamos do mais completo ao mais genérico até encontrar anúncios suficientes
    filtros_tentativas = [
        # Tentativa 1 — máxima especificidade
        {k: v for k, v in {
            "categoria": req.categoria,
            "cpu_linha": req.cpu_linha,
            "ram_gb": req.ram_gb,
            "storage_tipo": req.storage_tipo,
            "marca": req.marca,
        }.items() if v is not None},

        # Tentativa 2 — sem marca
        {k: v for k, v in {
            "categoria": req.categoria,
            "cpu_linha": req.cpu_linha,
            "ram_gb": req.ram_gb,
            "storage_tipo": req.storage_tipo,
        }.items() if v is not None},

        # Tentativa 3 — só CPU + RAM
        {k: v for k, v in {
            "categoria": req.categoria,
            "cpu_linha": req.cpu_linha,
            "ram_gb": req.ram_gb,
        }.items() if v is not None},

        # Tentativa 4 — só CPU
        {k: v for k, v in {
            "categoria": req.categoria,
            "cpu_linha": req.cpu_linha,
        }.items() if v is not None},

        # Tentativa 5 — só categoria
        {k: v for k, v in {
            "categoria": req.categoria,
        }.items() if v is not None},
    ]

    resultado = None
    filtros_usados = {}

    for filtros in filtros_tentativas:
        if not filtros:
            continue

        # Monta cláusulas WHERE
        clausulas = [Anuncio.preco.isnot(None)]
        for campo, valor in filtros.items():
            clausulas.append(getattr(Anuncio, campo) == valor)

        where = and_(*clausulas)

        # Busca estatísticas
        stats = await db.execute(
            select(
                func.count().label("total"),
                func.min(Anuncio.preco).label("minimo"),
                func.avg(Anuncio.preco).label("medio"),
                func.max(Anuncio.preco).label("maximo"),
                func.percentile_cont(0.5)
                .within_group(Anuncio.preco)
                .label("mediano"),
            ).where(where)
        )
        row = stats.fetchone()

        if row and row.total >= 3:
            resultado = row
            filtros_usados = filtros
            break

    if not resultado or resultado.total == 0:
        return PriceResponse(
            preco_estimado=None,
            preco_minimo=None,
            preco_maximo=None,
            preco_mediano=None,
            total_anuncios_similares=0,
            confianca="insuficiente",
            filtros_usados={},
        )

    return PriceResponse(
        preco_estimado=round(resultado.mediano, 2),   # mediana é mais robusta que média
        preco_minimo=round(resultado.minimo, 2),
        preco_maximo=round(resultado.maximo, 2),
        preco_mediano=round(resultado.mediano, 2),
        total_anuncios_similares=resultado.total,
        confianca=_nivel_confianca(resultado.total),
        filtros_usados=filtros_usados,
    )
