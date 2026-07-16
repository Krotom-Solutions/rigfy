"""
Parser HTML usando Scrapling Adaptor.
Scrapling é usado APENAS como parser — o fetch é feito pelo ZenRows.
Scrapling 0.2.9: find/find_all aceitam CSS selectors como strings.

PADRÃO ATUAL DAS URLs OLX (2025):
  https://[uf].olx.com.br/[regiao]/informatica/[categoria]/[titulo]-[ID]
  Ex: https://sp.olx.com.br/sao-paulo-e-regiao/informatica/notebooks/notebook-dell-1518502735
"""
import re
import logging
from scrapling.parser import Adaptor
from app.schemas.anuncio import AnuncioRaw

logger = logging.getLogger(__name__)

# Regex para detectar URLs de anúncio da OLX:
# - Subdomínio de estado (sp, rj, mg, etc.) OU www
# - Termina com um ID numérico de 7-10 dígitos
OLX_AD_URL_PATTERN = re.compile(
    r'https?://(?:[a-z]{2}|www)\.olx\.com\.br/.+-(\d{7,12})(?:\.html)?$'
)


def extrair_olx_id(url: str) -> str:
    """Extrai o ID único do anúncio da URL da OLX."""
    match = OLX_AD_URL_PATTERN.search(url)
    if match:
        return match.group(1)
    # Fallback: último segmento numérico da URL
    match2 = re.search(r'(\d{7,12})(?:\.html)?$', url)
    return match2.group(1) if match2 else url.split('/')[-1]


def is_url_anuncio(href: str) -> bool:
    """Verifica se a URL é de um anúncio individual da OLX."""
    return bool(OLX_AD_URL_PATTERN.match(href))


def limpar_preco(texto: str | None) -> float | None:
    """Converte 'R$ 1.750' → 1750.0"""
    if not texto:
        return None
    numeros = re.sub(r'[^\d,]', '', texto)
    if not numeros:
        return None
    numeros = numeros.replace(',', '.')
    partes = numeros.split('.')
    if len(partes) > 2:
        numeros = ''.join(partes[:-1]) + '.' + partes[-1]
    try:
        valor = float(numeros)
        return valor if 100 <= valor <= 50_000 else None
    except ValueError:
        return None


def parse_listagem(html: str, url_base: str) -> list[AnuncioRaw]:
    """
    Parseia a página de listagem da OLX.
    Retorna lista de AnuncioRaw com dados básicos (sem specs técnicas).
    """
    if not html:
        return []

    page = Adaptor(html, url=url_base)
    anuncios = []

    # Busca todos os <a> e filtra por URL de anúncio em Python
    todos_links = page.find_all('a')
    logger.info(f"Total de <a> encontrados: {len(todos_links)}")

    # Deduplicar por href, mantendo apenas URLs de anúncio
    hrefs_vistos = set()
    links_anuncio = []
    for link in todos_links:
        href = link.attrib.get('href', '')
        if href and href not in hrefs_vistos and is_url_anuncio(href):
            hrefs_vistos.add(href)
            links_anuncio.append(link)

    logger.info(f"Links de anúncio encontrados: {len(links_anuncio)}")

    for link in links_anuncio:
        href = link.attrib.get('href', '')

        # Container do card (parent.parent do link)
        card = link.parent.parent


        # Título — tenta h2, h3, depois o texto do link
        titulo_el = card.find('h2') or card.find('h3') or link
        titulo = titulo_el.text.strip() if titulo_el else ""

        # Fallback: texto do próprio link
        if not titulo or len(titulo) < 5:
            titulo = (link.text or '').strip()
        if not titulo or len(titulo) < 5:
            continue

        # Preço — busca no card inteiro
        preco_texto = None
        for el in card.find_all('h3') + card.find_all('p') + card.find_all('span'):
            txt = (el.text or '').strip()
            if 'R$' in txt and len(txt) < 40 and 'x de' not in txt.lower():
                preco_texto = txt
                break

        # Localização — busca padrão "Cidade, UF"
        localizacao = None
        for el in card.find_all('span') + card.find_all('p'):
            txt = (el.text or '').strip()
            if txt and re.search(r',\s*[A-Z]{2}$', txt) and len(txt) < 80:
                localizacao = txt
                break

        # Data de publicação
        data_texto = None
        data_el = card.find('time')
        if data_el:
            data_texto = data_el.text.strip()
        else:
            for el in card.find_all('span'):
                txt = (el.text or '').lower()
                if any(x in txt for x in ['hoje', 'ontem', 'dias', 'hora', 'min']):
                    data_texto = el.text.strip()
                    break

        anuncio = AnuncioRaw(
            olx_id=extrair_olx_id(href),
            url=href,
            titulo=titulo,
            preco_texto=preco_texto,
            preco=limpar_preco(preco_texto),
            localizacao=localizacao,
            data_publicacao_texto=data_texto,
        )
        anuncios.append(anuncio)

    logger.info(f"Anúncios parseados com sucesso: {len(anuncios)}")
    return anuncios


def parse_detalhe(html: str, url: str) -> dict:
    """
    Parseia a página de detalhe de um anúncio individual.
    Retorna a descrição completa para extração de specs.
    """
    if not html:
        return {}

    page = Adaptor(html, url=url)

    descricao = ""
    for seletor in [
        '[data-ds-component="DS-Text"]',
        '#description',
        '.description',
        'div[class*="description"]',
        'section[class*="description"]',
    ]:
        desc_el = page.find(seletor)
        if desc_el and desc_el.text:
            descricao = desc_el.text.strip()
            break

    specs_lista = []
    for el in page.find_all('li'):
        txt = el.text or ''
        if ':' in txt:
            specs_lista.append(txt.strip())

    return {
        "descricao": descricao,
        "specs_raw": "\n".join(specs_lista),
    }
