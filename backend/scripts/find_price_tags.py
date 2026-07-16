from scrapling.parser import Adaptor

html = open('debug_olx.html', encoding='utf-8').read()
page = Adaptor(html, url="http://olx.com.br")

print("Procurando elementos com R$ no texto:")
for el in page.find_all('*'):
    txt = el.text or ''
    # Apenas se for um elemento que contem R$ diretamente e nao for muito longo
    if 'R$' in txt and len(txt) < 50:
        print(f"Tag: {el.tag}, Attrs: {el.attrib}, Text: {txt.strip()}")
