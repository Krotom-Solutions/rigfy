"""
Orquestra o pipeline completo: fetch → parse → extract → save.
"""
import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.scraper.fetcher import fetch_pagina, fetch_detalhe_anuncio, OLX_URLS
from app.scraper.parser import parse_listagem, parse_detalhe
from app.scraper.extractor import extrair_specs
from app.crud.anuncio import salvar_anuncio, anuncio_existe
from app.core.config import settings

logger = logging.getLogger(__name__)


async def executar_coleta(db: AsyncSession) -> dict:
    """
    Pipeline principal. Roda todas as categorias e páginas configuradas.
    Retorna resumo da execução.
    """
    total_novos = 0
    total_duplicatas = 0
    total_erros = 0

    for categoria, url_base in OLX_URLS.items():
        logger.info(f"=== Iniciando coleta: {categoria} ===")

        for pagina in range(1, settings.scraper_pages_per_run + 1):
            # 1. FETCH — ZenRows busca e renderiza a página
            html = await fetch_pagina(url_base, pagina)
            if not html:
                logger.warning(f"Página {pagina} de {categoria} retornou vazia")
                total_erros += 1
                continue

            # 2. PARSE — Scrapling extrai os dados da listagem
            anuncios_raw = parse_listagem(html, url_base)
            if not anuncios_raw:
                logger.warning(f"Nenhum anúncio parseado na página {pagina} de {categoria}")
                continue

            # 3. PROCESSAR cada anúncio
            for anuncio_raw in anuncios_raw:
                # Verificar duplicata
                if await anuncio_existe(db, anuncio_raw.olx_id):
                    total_duplicatas += 1
                    continue

                # 4. EXTRACT — regex extrai specs do título
                specs = extrair_specs(
                    titulo=anuncio_raw.titulo,
                    descricao=anuncio_raw.descricao,
                )

                # 5. SAVE — persiste no PostgreSQL
                dados_completos = {
                    **anuncio_raw.model_dump(),
                    **specs,
                    "plataforma": "olx",
                }
                await salvar_anuncio(db, dados_completos)
                total_novos += 1

            # Pausa entre páginas para não sobrecarregar
            await asyncio.sleep(settings.scraper_delay_seconds)

    resumo = {
        "novos": total_novos,
        "duplicatas": total_duplicatas,
        "erros": total_erros,
        "total_processados": total_novos + total_duplicatas,
    }
    logger.info(f"Coleta finalizada: {resumo}")
    return resumo


async def enriquecer_anuncios_sem_descricao(db: AsyncSession, limite: int = 50):
    """
    Busca os detalhes dos anúncios que ainda não têm descrição completa.
    Roda separado da coleta principal para não travar o pipeline.
    """
    from app.crud.anuncio import buscar_sem_descricao, atualizar_descricao

    anuncios = await buscar_sem_descricao(db, limite=limite)
    logger.info(f"Enriquecendo {len(anuncios)} anúncios sem descrição...")

    for anuncio in anuncios:
        html = await fetch_detalhe_anuncio(anuncio.url)
        if not html:
            continue

        detalhes = parse_detalhe(html, anuncio.url)
        if detalhes.get("descricao"):
            # Re-extrair specs com a descrição completa
            specs = extrair_specs(anuncio.titulo, detalhes["descricao"])
            await atualizar_descricao(db, anuncio.olx_id, detalhes["descricao"], specs)

        await asyncio.sleep(1)  # pausa gentil entre detalhes
