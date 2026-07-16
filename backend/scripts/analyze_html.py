"""Analisa o HTML salvo para descobrir o padrão de URL dos anúncios da OLX."""
import re

html = open('debug_olx.html', encoding='utf-8').read()

# Pega todos os hrefs
hrefs = re.findall(r'href="(https?://[^"]{10,200})"', html)
olx_hrefs = [h for h in hrefs if 'olx.com.br' in h]
olx_hrefs_unicos = list(dict.fromkeys(olx_hrefs))

print('=== URLs únicas da OLX encontradas ===')
for h in olx_hrefs_unicos[:40]:
    print(h)

print(f'\nTotal de hrefs OLX únicos: {len(olx_hrefs_unicos)}')

# Verifica padrões de anúncio
padroes = ['/d/', '/anuncio/', 'listing', '/ad/', 'produto', '/item/', 'notebook', 'computador']
print('\n=== Contagem por padrão ===')
for p in padroes:
    count = sum(1 for h in olx_hrefs_unicos if p in h)
    print(f'  {p!r}: {count} links')

# Mostra um trecho do HTML em torno de um link de card
print('\n=== Trecho HTML ao redor do primeiro link não-nav ===')
# Pega links que parecem ser de anúncio (não são nav/header)
candidatos = [h for h in olx_hrefs_unicos if not any(
    x in h for x in ['conta.olx', 'ajuda', 'anunciar', 'cadastro', 'login', 'categoria']
)]
print(f'Candidatos a anúncio: {len(candidatos)}')
for c in candidatos[:10]:
    print(f'  {c}')
