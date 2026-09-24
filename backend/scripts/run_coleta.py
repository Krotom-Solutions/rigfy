import asyncio, sys, logging
from dotenv import load_dotenv
load_dotenv()
from app.core.database import AsyncSessionLocal
from app.scraper.fetcher import OLX_URLS, CATEGORIA_TIPO, fetch_pagina
from app.scraper.parser import parse_listagem
from app.scraper.extractor import extrair_specs
from app.crud.anuncio import salvar_anuncio, anuncio_existe
from app.core.config import settings
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def main():
    total_novos = total_duplicatas = total_erros = total_sem_preco = 0
    async with AsyncSessionLocal() as db:
        for chave, url_base in OLX_URLS.items():
            tipo = CATEGORIA_TIPO.get(chave)
            logger.info(f"CATEGORIA: {chave} | tipo={tipo}")
            for pagina in range(1, settings.scraper_pages_per_run + 1):
                logger.info(f"  Pagina {pagina}/{settings.scraper_pages_per_run}")
                html = await fetch_pagina(url_base, pagina)
                if not html:
                    logger.warning(f"  Pagina {pagina} vazia")
                    total_erros += 1
                    continue
                anuncios_raw = parse_listagem(html, url_base)
                logger.info(f"  Parseados: {len(anuncios_raw)}")
                novos_p = 0
                for a in anuncios_raw:
                    if await anuncio_existe(db, a.olx_id):
                        total_duplicatas += 1
                        continue
                    if a.preco is None:
                        total_sem_preco += 1
                    specs = extrair_specs(a.titulo, a.descricao, categoria_forcada=tipo)
                    await salvar_anuncio(db, {**a.model_dump(), **specs, "plataforma": "olx"})
                    total_novos += 1
                    novos_p += 1
                logger.info(f"  Novos salvos: {novos_p}")
                await asyncio.sleep(settings.scraper_delay_seconds)
    logger.info(f"COLETA FINALIZADA: novos={total_novos} dup={total_duplicatas} erros={total_erros} sem_preco={total_sem_preco}")

asyncio.run(main())