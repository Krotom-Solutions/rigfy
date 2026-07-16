"""
Parser HTML usando Scrapling Adaptor.
Scrapling é usado APENAS como parser — o fetch é feito pelo ZenRows.
"""
import re
import logging
from scrapling.parser import Adaptor
from app.schemas.anuncio import AnuncioRaw

logger = logging.getLogger(__name__)


def extrair_olx_id(url: str) -> str:
    """Extrai o ID único do anúncio da URL da OLX."""
    # URLs da OLX têm formato: .../item/titulo-do-anuncio-IDXXXXXXXX.html
    match = re.search(r'-(\d+)(?:\.html)?$', url)
    return match.group(1) if match else url.split('/')[-1]


def limpar_preco(texto: str | None) -> float | None:
    """Converte 'R$ 1.750' → 1750.0"""
    if not texto:
        return None
    # Remove tudo exceto dígitos e vírgula
    numeros = re.sub(r'[^\d,]', '', texto)
    if not numeros:
        return None
    # Trata milhar com ponto e decimal com vírgula (padrão BR)
    numeros = numeros.replace(',', '.')
    # Se tiver múltiplos pontos, mantém só o último como decimal
    partes = numeros.split('.')
    if len(partes) > 2:
        numeros = ''.join(partes[:-1]) + '.' + partes[-1]
    try:
        valor = float(numeros)
        # Filtro básico: preços absurdos (< R$100 ou > R$50.000) são outliers
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

    # Estratégia 1: links de anúncio individual (mais robusto que depender de classe CSS)
    links_anuncio = page.find_all(
        'a',
        filters=[lambda el: '/item/' in (el.attrib.get('href') or '')]
    )

    # Deduplicar por href (a OLX às vezes repete o mesmo link com wrappers diferentes)
    hrefs_vistos = set()
    links_unicos = []
    for link in links_anuncio:
        href = link.attrib.get('href', '')
        if href and href not in hrefs_vistos:
            hrefs_vistos.add(href)
            links_unicos.append(link)

    logger.info(f"Links de anúncio encontrados: {len(links_unicos)}")

    for link in links_unicos:
        href = link.attrib.get('href', '')
        if not href:
            continue

        # URL completa
        if href.startswith('/'):
            href = f"https://www.olx.com.br{href}"

        # Container do card (parent do link)
        card = link.parent

        # Título — tenta h2, h3, ou o texto do link
        titulo_el = (
            card.find('h2') or
            card.find('h3') or
            link
        )
        titulo = titulo_el.text.strip() if titulo_el else ""

        if not titulo or len(titulo) < 5:
            continue

        # Preço — busca elemento com "R$"
        preco_el = card.find(
            filters=[lambda el: el.text and 'R$' in el.text and len(el.text) < 30]
        )
        preco_texto = preco_el.text.strip() if preco_el else None

        # Localização
        local_el = card.find(
            filters=[lambda el: el.attrib.get('aria-label', '').lower().startswith('local')]
        )
        if not local_el:
            # fallback: elemento com vírgula que parece "Cidade, UF"
            local_el = card.find(
                filters=[lambda el: el.text and re.search(r'[A-Z]{2}$', el.text.strip())]
            )
        localizacao = local_el.text.strip() if local_el else None

        # Data de publicação
        data_el = card.find('time') or card.find(
            filters=[lambda el: el.text and any(
                x in el.text.lower() for x in ['hoje', 'ontem', 'dias', 'hora']
            )]
        )
        data_texto = data_el.text.strip() if data_el else None

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

    # Descrição completa
    desc_el = (
        page.find('[data-ds-component="DS-Text"]') or
        page.find('.description') or
        page.find('#description')
    )
    descricao = desc_el.text.strip() if desc_el else ""

    # Specs em tabela (OLX às vezes estrutura como lista de características)
    specs_els = page.find_all('li', filters=[lambda el: ':' in el.text])
    specs_lista = [el.text.strip() for el in specs_els if el.text]

    return {
        "descricao": descricao,
        "specs_raw": "\n".join(specs_lista),
    }
