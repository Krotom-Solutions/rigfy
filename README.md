# 💻 Rigfy SaaS - Precificação Inteligente de Hardware

O **Rigfy** é uma plataforma SaaS (Software as a Service) desenvolvida para precificação inteligente de hardware usado. Ele utiliza uma arquitetura de **Monorepo** moderna, separando de forma clara o Frontend (Interface do Usuário) e o Backend (Coleta de Dados, API e Machine Learning).

---

## 🏗 Arquitetura do Projeto (Workflow)

O projeto é dividido em duas partes principais que se comunicam através de uma API REST:

### 1. Backend (Python + FastAPI)
Localizado na pasta `/backend`. Responsável pela lógica pesada do sistema:
- **Scraper Automático:** Utiliza `APScheduler` e `Scrapling` para raspar dados de anúncios de hardware diariamente (via ZenRows para contornar bloqueios).
- **Processamento e ML:** Estrutura e limpa os dados usando `pandas` e utiliza modelos do `Scikit-Learn` (Random Forest) para prever o preço ideal de revenda.
- **Banco de Dados:** Utiliza PostgreSQL (Hospedado no Supabase) para armazenar os milhares de anúncios coletados.
- **Servidor:** API de alta performance utilizando o framework `FastAPI`.

### 2. Frontend (React 19 + Vite + Tailwind CSS v4)
Localizado na pasta `/frontend`. Interface responsiva e moderna:
- **Design:** Segue um estilo Brutalista/Minimalista, focado em alta conversão e experiência de usuário limpa.
- **Autenticação:** Integração direta com **Supabase Auth** (Login Social com Google e Email/Senha).
- **Componentização:** Utiliza React Router para SPA (Single Page Application) e componentes modulares.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.12+
- Node.js 20+
- Banco de Dados PostgreSQL (Local ou Nuvem)

### Configurando o Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```
> Crie um arquivo `.env` baseado no `.env.example` com sua `DATABASE_URL` e `ZENROWS_API_KEY`.
```bash
# Iniciar o servidor
uvicorn app.main:app --reload --port 8000
```

### Configurando o Frontend
```bash
cd frontend
npm install
```
> Crie um arquivo `.env` na pasta frontend com suas variáveis do Supabase (`VITE_SUPABASE_URL` e `VITE_SUPABASE_ANON_KEY`) e a URL do backend (`VITE_API_URL=http://localhost:8000`).
```bash
# Iniciar o ambiente de desenvolvimento
npm run dev
```

---

## ☁️ Deploy (Produção)

O ambiente de produção foi desenhado para ser **Serverless e Contínuo**:
- **Banco de Dados & Auth:** [Supabase](https://supabase.com)
- **Backend API:** [Render](https://render.com) (Hospedagem nativa de Python lendo o arquivo `render.yaml`)
- **Frontend SPA:** [Netlify](https://netlify.com) ou Vercel.

---

## 📚 Endpoints Principais da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/stats/resumo` | Retorna o volume total de anúncios coletados e hardware monitorado. |
| GET | `/price/predict` | Recebe parâmetros de hardware e retorna a faixa de preço ideal usando ML. |
| POST | `/collect/trigger` | Dispara manualmente o robô de coleta no background. |
