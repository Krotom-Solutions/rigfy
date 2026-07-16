from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.config import settings
from app.core.database import AsyncSessionLocal
from app.scraper.pipeline import executar_coleta, enriquecer_anuncios_sem_descricao
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def job_coleta_diaria():
    logger.info("=== JOB DIÁRIO INICIADO ===")
    async with AsyncSessionLocal() as db:
        resumo = await executar_coleta(db)
        logger.info(f"Coleta: {resumo}")
        await enriquecer_anuncios_sem_descricao(db, limite=30)
    logger.info("=== JOB DIÁRIO FINALIZADO ===")


def iniciar_scheduler():
    scheduler.add_job(
        job_coleta_diaria,
        trigger=CronTrigger(
            hour=settings.scraper_schedule_hour,
            minute=settings.scraper_schedule_minute,
        ),
        id="coleta_diaria",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        f"Scheduler iniciado — job diário às "
        f"{settings.scraper_schedule_hour:02d}:{settings.scraper_schedule_minute:02d}"
    )
