import asyncio
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import select, delete
from app.core.database import AsyncSessionLocal
from app.models.anuncio import Anuncio
from app.scraper.extractor import extrair_specs

TERMOS_BANIDOS = [
    'apartamento', 'cobertura', 'sala comercial', 'casa', 'terreno', 'imovel', 'imóvel',
    'dormitorio', 'dormitório', 'vagas', 'locação', 'locacao', 'condominio', 'condomínio',
    'calça', 'calca', 'camisa', 'camiseta', 'tenis', 'tênis', 'vestido', 'bermuda', 'roupa',
    'relogio', 'relógio', 'adega', 'guarda roupa', 'cama', 'sofa', 'sofá', 'mesa cabeceira',
    'kawasaki', 'moto', 'honda', 'yamaha', 'carro', 'fiat', 'chevrolet', 'volkswagen',
    'compressor', 'filtro polarizador', 'brinquedo', 'hot wheels', 'boneco', 'salão', 'salao'
]

PALAVRAS_CHAVE_HARDWARE = [
    'rtx', 'gtx', 'rx ', 'radeon', 'geforce', 'placa de video', 'placa de vídeo', 'vga',
    'ryzen', 'core i3', 'core i5', 'core i7', 'core i9', 'intel', 'amd', 'xeon',
    'notebook', 'laptop', 'computador', 'pc gamer', 'desktop', 'gabinete', 'processador',
    'ddr3', 'ddr4', 'ddr5', 'placa mae', 'placa mãe', 'motherboard'
]

async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Anuncio))
        todos = res.scalars().all()
        print(f"Total antes da faxina: {len(todos)} anúncios")
        
        ids_deletar = []
        mantidos = 0
        
        for a in todos:
            texto = f"{a.titulo} {a.descricao or ''}".lower()
            
            # Se contém termo banido -> DELETA
            if any(b in texto for b in TERMOS_BANIDOS):
                ids_deletar.append(a.id)
                continue
                
            # Se NÃO contém nenhuma palavra-chave de hardware -> DELETA
            if not any(h in texto for h in PALAVRAS_CHAVE_HARDWARE):
                ids_deletar.append(a.id)
                continue
                
            # Recalcula categoria correta com base no título real
            specs = extrair_specs(a.titulo, a.descricao)
            if 'notebook' in texto or 'laptop' in texto:
                a.categoria = 'notebook'
            elif 'pc gamer' in texto or 'computador' in texto or 'desktop' in texto:
                a.categoria = 'desktop'
            elif any(x in texto for x in ['placa de video', 'placa de vídeo', 'rtx', 'gtx', 'rx ']):
                a.categoria = 'gpu'
            elif any(x in texto for x in ['processador', 'ryzen', 'core i']):
                a.categoria = 'cpu'
            else:
                a.categoria = specs.get('categoria') or 'desktop'
                
            mantidos += 1
            
        print(f"Removendo {len(ids_deletar)} anúncios irrelevantes do banco...")
        for i in range(0, len(ids_deletar), 100):
            lote = ids_deletar[i:i+100]
            await db.execute(delete(Anuncio).where(Anuncio.id.in_(lote)))
        await db.commit()
        
        print(f"✅ Anúncios legítimos de HARDWARE mantidos: {mantidos}")

if __name__ == '__main__':
    asyncio.run(main())
