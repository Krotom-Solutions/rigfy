"""Testa o parser corrigido contra o HTML já salvo (sem gastar créditos ZenRows)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scraper.parser import parse_listagem

html = open('debug_olx.html', encoding='utf-8').read()
url_base = "https://www.olx.com.br/brasil/informatica/computadores-e-acessorios/notebooks-e-netbooks"

html = open('debug_olx.html', encoding='utf-8').read()
url_base = "https://www.olx.com.br/brasil/informatica/computadores-e-acessorios/notebooks-e-netbooks"

anuncios = parse_listagem(html, url_base)

print(f"\nAnuncios encontrados: {len(anuncios)}")
for a in anuncios[:10]:
    print(f"\n  ID: {a.olx_id}")
    print(f"  Titulo: {a.titulo[:80]}")
    print(f"  Preco: {a.preco_texto} -> {a.preco}")
    print(f"  Local: {a.localizacao}")
    print(f"  URL: {a.url[:80]}")

