import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings
from app.scheduler.jobs import iniciar_scheduler, scheduler
from app.scraper.pipeline import executar_coleta
from app.crud.anuncio import contar_anuncios

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
    title="Rigfy Scraper API",
    description="Backend de coleta de dados do Rigfy",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"status": "online", "service": "rigfy-scraper"}


@app.get("/status")
async def status(db: AsyncSession = Depends(get_db)):
    """Retorna estatísticas do banco de dados."""
    contagem = await contar_anuncios(db)
    return {
        "status": "online",
        "database": contagem,
        "scheduler": {
            "jobs": [job.id for job in scheduler.get_jobs()],
            "proximo_job": str(scheduler.get_job("coleta_diaria").next_run_time),
        },
    }


@app.post("/collect/trigger")
async def trigger_coleta(db: AsyncSession = Depends(get_db)):
    """Dispara a coleta manualmente (para testes)."""
    logger.info("Coleta disparada manualmente via API")
    resumo = await executar_coleta(db)
    return {"message": "Coleta concluída", "resumo": resumo}
