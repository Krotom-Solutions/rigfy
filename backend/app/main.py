import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.scheduler.jobs import iniciar_scheduler, scheduler
from app.scraper.pipeline import executar_coleta
from app.crud.anuncio import contar_anuncios

# Routers da API
from app.api.listings import router as listings_router
from app.api.stats import router as stats_router
from app.api.price import router as price_router

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Rigfy API",
    description=(
        "Backend de coleta e precificação inteligente de hardware usado.\n\n"
        "## Endpoints principais\n"
        "- **GET /listings** — lista anúncios com filtros\n"
        "- **GET /listings/opcoes** — valores disponíveis para filtros\n"
        "- **GET /stats/mercado** — estatísticas de preço por grupo\n"
        "- **GET /stats/resumo** — resumo rápido da coleta\n"
        "- **POST /price/predict** — estima preço de um hardware\n"
        "- **POST /collect/trigger** — dispara coleta manualmente\n"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ─── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(listings_router)
app.include_router(stats_router)
app.include_router(price_router)


# ─── Rotas base ──────────────────────────────────────────────────────────────
@app.get("/", tags=["health"])
async def root():
    return {"status": "online", "service": "rigfy-api", "version": "1.0.0"}


@app.get("/status", tags=["health"])
async def status(db: AsyncSession = Depends(get_db)):
    """Retorna estatísticas do banco + próximo job agendado."""
    contagem = await contar_anuncios(db)
    job = scheduler.get_job("coleta_diaria")
    return {
        "status": "online",
        "database": contagem,
        "scheduler": {
            "jobs": [j.id for j in scheduler.get_jobs()],
            "proximo_job": str(job.next_run_time) if job else None,
        },
    }


@app.post("/collect/trigger", tags=["scraper"])
async def trigger_coleta(db: AsyncSession = Depends(get_db)):
    """Dispara a coleta manualmente (para testes ou recoleta sob demanda)."""
    logger.info("Coleta disparada manualmente via API")
    resumo = await executar_coleta(db)
    return {"message": "Coleta concluída", "resumo": resumo}
