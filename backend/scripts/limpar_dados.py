import asyncio
import re
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select, delete
from app.core.database import AsyncSessionLocal
from app.models.anuncio import Anuncio
from app.scraper.extractor import extrair_specs

TERMOS_INVALIDOS = [
    'defeito', 'sucata', 'nao funciona', 'não funciona', 'nao liga', 'não liga',
    'para retirada', 'retirada de pecas', 'retirada de peças', 'pecas ou conserto',
    'peças ou conserto', 'conserto', 'quebrado', 'quebrada', 'quebrados',
    'trincado', 'trincada', 'apenas troca', 'so troca', 'só troca', 'aceito troca',
    'hot wheels', 'carrinho', 'miniatura', 'brinquedo', 'boneco', 'camisa', 'tenis',
    'lote de', 'lote com'
]

def normalizar_gpu(nome):
    if not nome:
        return None
    nome = nome.upper().strip()
    nome = re.sub(r'^(PLACA DE V[IÍ]DEO\s*|VGA\s*|GEFORCE\s*|NVIDIA\s*|AMD\s*|RADEON\s*)+', '', nome).strip()
    return nome

async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Anuncio))
        todos = res.scalars().all()
        total_inicial = len(todos)
        
        removidos_motivo = {
            'sem_preco_ou_invalido': 0,
            'defeito_ou_sucata': 0,
            'fora_de_escopo': 0,
            'preco_outlier': 0
        }
        
        ids_para_deletar = []
        validos = 0
        
        for a in todos:
            texto = f"{a.titulo} {a.descricao or ''}".lower()
            
            # 1. Verifica termos inválidos
            termo_invalido = next((t for t in TERMOS_INVALIDOS if t in texto), None)
            if termo_invalido:
                if any(x in termo_invalido for x in ['hot wheels', 'carrinho', 'miniatura', 'brinquedo', 'boneco', 'camisa', 'tenis']):
                    removidos_motivo['fora_de_escopo'] += 1
                else:
                    removidos_motivo['defeito_ou_sucata'] += 1
                ids_para_deletar.append(a.id)
                continue
                
            # 2. Preço
            if a.preco is None and a.preco_texto:
                nums = re.sub(r'[^\d,]', '', a.preco_texto).replace(',', '.')
                try:
                    val = float(nums)
                    if 50 <= val <= 35000:
                        a.preco = val
                except:
                    pass
                        
            if a.preco is None or a.preco <= 50:
                removidos_motivo['sem_preco_ou_invalido'] += 1
                ids_para_deletar.append(a.id)
                continue
                
            if a.preco > 35000:
                removidos_motivo['preco_outlier'] += 1
                ids_para_deletar.append(a.id)
                continue
                
            # 3. Resgata e normaliza specs
            specs = extrair_specs(a.titulo, a.descricao, categoria_forcada=a.categoria)
            if not a.categoria and specs.get('categoria'):
                a.categoria = specs['categoria']
                
            if specs.get('gpu'):
                a.gpu = normalizar_gpu(specs['gpu'])
            if specs.get('gpu_vram_gb') and not getattr(a, 'gpu_vram_gb', None):
                a.gpu_vram_gb = specs['gpu_vram_gb']
            if specs.get('cpu_linha') and not a.cpu_linha:
                a.cpu_linha = specs['cpu_linha']
            if specs.get('cpu_geracao') and not a.cpu_geracao:
                a.cpu_geracao = specs['cpu_geracao']
            if specs.get('ram_gb') and not a.ram_gb:
                a.ram_gb = specs['ram_gb']
            if specs.get('ram_tipo') and not a.ram_tipo:
                a.ram_tipo = specs['ram_tipo']
            if specs.get('ano_lancamento') and not getattr(a, 'ano_lancamento', None):
                a.ano_lancamento = specs['ano_lancamento']
                
            validos += 1

        if ids_para_deletar:
            for i in range(0, len(ids_para_deletar), 100):
                lote = ids_para_deletar[i:i+100]
                await db.execute(delete(Anuncio).where(Anuncio.id.in_(lote)))
            await db.commit()
            
        print('\n' + '='*60)
        print('RELATÓRIO DE LIMPEZA E AUDITORIA DE DADOS (FASE 2)')
        print('='*60)
        print(f'Total coletado inicialmente:       {total_inicial:>5}')
        print(f'Total de registros removidos:      {len(ids_para_deletar):>5}')
        print(f'  - Sem preço / preço zero / nulo: {removidos_motivo["sem_preco_ou_invalido"]:>5}')
        print(f'  - Peças com defeito / sucatas:   {removidos_motivo["defeito_ou_sucata"]:>5}')
        print(f'  - Fora de escopo (não hardware): {removidos_motivo["fora_de_escopo"]:>5}')
        print(f'  - Outliers absurdos (> R$35k):   {removidos_motivo["preco_outlier"]:>5}')
        print(f'Total VÁLIDO após limpeza:         {validos:>5}')
        print('='*60)

if __name__ == '__main__':
    asyncio.run(main())
