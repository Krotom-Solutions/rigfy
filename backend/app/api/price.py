from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.api import PriceRequest, PriceResponse
from app.ml.pipeline import carregar_modelo, prever_faixa_preco
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/price", tags=["price"])

# Cache local do modelo
_modelo_cache = None

def obter_modelo(request: Request = None):
    global _modelo_cache
    if request and hasattr(request.app.state, "modelo_ml") and request.app.state.modelo_ml:
        return request.app.state.modelo_ml
    if _modelo_cache is None:
        _modelo_cache = carregar_modelo()
    return _modelo_cache

@router.post("/predict", response_model=PriceResponse)
async def estimar_preco_post(
    req: PriceRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    modelo = obter_modelo(request)
    if not modelo:
        return PriceResponse(
            preco_estimado=None,
            preco_minimo=None,
            preco_maximo=None,
            preco_mediano=None,
            total_anuncios_similares=0,
            confianca="insuficiente",
            filtros_usados=req.model_dump(),
        )

    dados_input = req.model_dump()
    predicao = prever_faixa_preco(modelo, dados_input)
    
    return PriceResponse(
        preco_estimado=predicao["preco_estimado"],
        preco_minimo=predicao["preco_minimo"],
        preco_maximo=predicao["preco_maximo"],
        preco_mediano=predicao["preco_estimado"],
        total_anuncios_similares=100, # 100 estimadores no ensemble
        confianca="alta",
        filtros_usados=dados_input,
    )

@router.get("/predict", response_model=PriceResponse)
async def estimar_preco_get(
    request: Request,
    categoria: str = Query(None, description="notebook | desktop | gpu | cpu"),
    marca: str = Query(None),
    cpu_linha: str = Query(None),
    cpu_geracao: str = Query(None),
    ram_gb: int = Query(None),
    storage_tipo: str = Query(None),
    gpu: str = Query(None),
    gpu_vram_gb: int = Query(None),
    db: AsyncSession = Depends(get_db),
):
    req = PriceRequest(
        categoria=categoria,
        marca=marca,
        cpu_linha=cpu_linha,
        cpu_geracao=cpu_geracao,
        ram_gb=ram_gb,
        storage_tipo=storage_tipo,
        gpu=gpu,
    )
    return await estimar_preco_post(req, request, db)
