# Rigfy Scraper

Backend de coleta de dados do Rigfy — precificação inteligente de hardware usado.

## Setup

### 1. Clonar e instalar dependências
```bash
git clone <repo>
cd rigfy-scraper
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Editar .env com sua ZENROWS_API_KEY e DATABASE_URL
```

### 3. Iniciar o PostgreSQL
```bash
# Com Docker:
docker run -d \
  --name rigfy-db \
  -e POSTGRES_USER=rigfy \
  -e POSTGRES_PASSWORD=rigfy123 \
  -e POSTGRES_DB=rigfy \
  -p 5432:5432 \
  postgres:15
```

### 4. Criar as tabelas
```bash
python scripts/init_db.py
```

### 5. Testar o scraper
```bash
python scripts/run_once.py
```

### 6. Iniciar o servidor
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Status do serviço |
| GET | `/status` | Estatísticas do banco + próximo job |
| POST | `/collect/trigger` | Dispara coleta manualmente |

## ZenRows

Crie sua conta em [zenrows.com](https://www.zenrows.com) e copie a API key para o `.env`.
O plano gratuito oferece 1.000 créditos — suficiente para testar.
Cada página com `js_render=true` + `premium_proxy=true` consome 25 créditos.
1.000 créditos = 40 páginas = ~800 anúncios no teste inicial.

## Arquitetura

```
ZenRows (fetch + JS render)
    ↓
Scrapling Adaptor (parse HTML)
    ↓
Extractor (regex → specs estruturadas)
    ↓
PostgreSQL (armazenamento)
    ↓
FastAPI /status (monitoramento)
```
