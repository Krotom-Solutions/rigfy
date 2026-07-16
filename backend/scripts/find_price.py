import re

html = open('debug_olx.html', encoding='utf-8').read()
indices = [m.start() for m in re.finditer(r'R\$', html)]
print(f'Ocorrencias de R$: {len(indices)}')
for idx in indices[:10]:
    trecho = html[max(0,idx-150):idx+80]
    print('---')
    print(trecho)
