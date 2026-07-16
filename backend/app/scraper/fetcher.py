"""
Cliente ZenRows via httpx async.
ZenRows resolve o Cloudflare e renderiza o JavaScript da OLX automaticamente.
Documentação: https://www.zenrows.com/docs
"""
import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# URLs de busca da OLX por categoria
OLX_URLS = {
    "notebooks": "https://www.olx.com.br/brasil/informatica/computadores-e-acessorios/notebooks-e-netbooks",
    "desktops": "https://www.olx.com.br/brasil/informatica/computadores-e-acessorios/computadores",
}


async def fetch_pagina(url: str, pagina: int = 1) -> str | None:
    """
    Busca uma página da OLX via ZenRows.
    Retorna o HTML renderizado ou None em caso de erro.
    """
    url_paginada = f"{url}?o={pagina}" if pagina > 1 else url

    params = {
        "apikey": settings.zenrows_api_key,
        "url": url_paginada,
        "js_render": "true",       # renderiza JavaScript (essencial para OLX)
        "wait": "3000",            # aguarda 3s para o React carregar
        "premium_proxy": "true",   # proxy residencial — melhor contra Cloudflare
        "proxy_country": "br",     # IP brasileiro — OLX mostra preços em BRL
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            logger.info(f"Fetching página {pagina}: {url_paginada}")
            response = await client.get(settings.zenrows_base_url, params=params)

            if response.status_code == 200:
                logger.info(f"OK — {len(response.text)} chars recebidos")
                return response.text

            # ZenRows retorna 422 quando a key está inválida
            # e 429 quando excede o limite do plano
            logger.error(f"ZenRows erro {response.status_code}: {response.text[:200]}")
            return None

        except httpx.TimeoutException:
            logger.error(f"Timeout ao buscar {url_paginada}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return None


async def fetch_detalhe_anuncio(url: str) -> str | None:
    """
    Busca a página de detalhe de um anúncio individual.
    Usado para extrair a descrição completa e specs técnicas.
    """
    params = {
        "apikey": settings.zenrows_api_key,
        "url": url,
        "js_render": "true",
        "wait": "2000",
        "premium_proxy": "true",
        "proxy_country": "br",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(settings.zenrows_base_url, params=params)
            return response.text if response.status_code == 200 else None
        except Exception as e:
            logger.error(f"Erro ao buscar detalhe {url}: {e}")
            return None
