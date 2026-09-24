import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, AsyncSessionLocal
from app.core.config import settings
from app.scheduler.jobs import iniciar_scheduler, scheduler
from app.scraper.pipeline import executar_coleta
from app.crud.anuncio import contar_anuncios
from app.ml.pipeline import carregar_modelo

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
    # Inicializa scheduler
    iniciar_scheduler()
    
    # Carrega modelo de Machine Learning
    logger.info("Carregando modelo Random Forest...")
    app.state.modelo_ml = carregar_modelo()
    if app.state.modelo_ml:
    else:
        logger.warning("⚠️ Nenhum modelo treinado encontrado em app/ml/")
        
    yield
    scheduler.shutdown()


app = FastAPI(
    title="Rigfy API",
    description="Backend de precificação inteligente de hardware usado via Machine Learning.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(listings_router)
app.include_router(stats_router)
app.include_router(price_router)


@app.get("/", tags=["health"])
async def root():
    return {"status": "online", "service": "rigfy-api", "version": "1.0.0"}


@app.get("/health", tags=["health"])
async def health():
    """Endpoint de healthcheck para o Render."""
    return {"status": "healthy", "database": "connected", "ml_model": app.state.modelo_ml is not None}


@app.get("/status", tags=["health"])
async def status(db: AsyncSession = Depends(get_db)):
    contagem = await contar_anuncios(db)
    job = scheduler.get_job("coleta_diaria")
    return {
        "status": "online",
        "database": contagem,
        "ml_model_loaded": app.state.modelo_ml is not None,
        "scheduler": {
            "jobs": [j.id for j in scheduler.get_jobs()],
            "proximo_job": str(job.next_run_time) if job else None,
        },
    }


async def _tarefa_coleta_background():
    async with AsyncSessionLocal() as db:
        await executar_coleta(db)


@app.post("/collect/trigger", tags=["scraper"])
async def trigger_coleta(background_tasks: BackgroundTasks):
    """Dispara a coleta em background sem bloquear a resposta da requisição."""
    logger.info("Coleta em background agendada via API")
    background_tasks.add_task(_tarefa_coleta_background)
    return {"message": "Coleta iniciada em background com sucesso"}
