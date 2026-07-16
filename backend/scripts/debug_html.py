"""
Debug: salva o HTML retornado pelo ZenRows para inspeção local.
Roda com: $env:PYTHONPATH="."; python scripts/debug_html.py
"""
import asyncio
import sys
import os

# Garante que o .env é carregado
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scraper.fetcher import fetch_pagina, OLX_URLS
from scrapling.parser import Adaptor


async def main():
    url = OLX_URLS["notebooks"]
    print(f"Buscando: {url}")

    html = await fetch_pagina(url, pagina=1)

    if not html:
        print("ERRO: ZenRows retornou vazio ou falhou.")
        return

    print(f"\nHTML recebido: {len(html)} caracteres")

    # Salva o HTML para inspeção
    with open("debug_olx.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML salvo em: debug_olx.html")

    # Testa os seletores
    page = Adaptor(html, url=url)

    print("\n--- Testando seletores ---")

    # 1. Links com /item/
    links = page.find_all('a[href*="/item/"]')
    print(f"a[href*='/item/']: {len(links)} encontrados")

    # 2. Todos os links <a>
    todos_links = page.find_all('a')
    print(f"Todos <a>: {len(todos_links)} encontrados")

    # Mostra os primeiros hrefs para análise
    hrefs_com_item = [
        a.attrib.get('href', '') for a in todos_links
        if '/item/' in (a.attrib.get('href') or '')
    ]
    print(f"\nLinks com /item/ (manual): {len(hrefs_com_item)}")
    for h in hrefs_com_item[:5]:
        print(f"  {h[:100]}")

    # 3. Padrões alternativos de URL da OLX
    for padrao in ['a[href*="olx.com.br"]', 'article', 'li[data-listing]', '[data-ds-component]']:
        els = page.find_all(padrao)
        print(f"  {padrao}: {len(els)}")

    # 4. Mostra primeiros 2000 chars do HTML para análise
    print("\n--- Início do HTML (500 chars) ---")
    print(html[:500])

    print("\n--- Trecho do HTML com 'item' ---")
    idx = html.find('/item/')
    if idx > 0:
        print(html[max(0, idx-200):idx+300])
    else:
        print("String '/item/' NÃO encontrada no HTML")
        # Procura por padrões alternativos
        for termo in ['anuncio', 'listing', 'product', 'card', 'ad-']:
            idx2 = html.lower().find(termo)
            if idx2 > 0:
                print(f"\nEncontrou '{termo}' na posição {idx2}:")
                print(html[max(0, idx2-100):idx2+200])
                break


asyncio.run(main())
