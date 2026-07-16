# 💻 Rigfy SaaS - Precificação Inteligente de Hardware

O **Rigfy** é uma plataforma SaaS (Software as a Service) desenvolvida para resolver o problema de assimetria de informações no mercado de hardware usado. Através de coleta automatizada de dados e Inteligência Artificial, o Rigfy entrega precificações precisas e justas em tempo real, eliminando a dependência do "achismo" na compra e venda de peças de computador.

O projeto foi estruturado utilizando uma arquitetura moderna de **Monorepo**, garantindo isolamento total entre o serviço de coleta/inteligência (Backend) e a interface do usuário (Frontend).

---

## 🎯 O Problema e a Solução

- **Problema:** O mercado de hardware usado é volátil. Vendedores e compradores dependem de pesquisas manuais e cálculos subjetivos para definir o valor de peças como Placas de Vídeo (GPUs) e Processadores (CPUs).
- **Solução (Rigfy):** Um algoritmo varre diariamente os maiores marketplaces, armazena o histórico de milhares de anúncios reais, e aplica modelos de *Machine Learning* para determinar o valor estatístico exato de um equipamento baseado nas flutuações do mercado.

---

## 🏗 Arquitetura do Projeto

O sistema opera em uma estrutura de microsserviços desacoplada:

### 1. Backend (Motor de Dados e Inteligência) - `/backend`
Desenvolvido em **Python**, focado em performance e processamento assíncrono.
- **Framework REST:** `FastAPI` (alta performance, documentação automática via Swagger/OpenAPI).
- **Web Scraping:** `Scrapling` para manipulação de DOM e `APScheduler` para orquestrar as rotinas de coleta (Cron Jobs) que rodam no background 24/7.
- **Machine Learning (IA):** Utiliza `Scikit-Learn` (modelos de *Random Forest Regressor*) e `pandas` para limpeza, tratamento de outliers e predição estatística da faixa de preço de um hardware.

### 2. Frontend (Interface SPA) - `/frontend`
Desenvolvido em **React 19** e orquestrado pelo `Vite`.
- **Design System:** Construído com `Tailwind CSS v4` e `Framer Motion`, adotando uma estética Brutalista/Minimalista. O foco é UI de alto impacto e baixa fricção cognitiva.
- **Roteamento & Estado:** Roteamento client-side focado em performance e consumo dinâmico da API do Backend.
- **Autenticação Segura:** Sistema de Login Social (OAuth) e Email/Senha provido pelo pacote oficial `@supabase/supabase-js`.

### 3. Banco de Dados e Auth
Hospedado na nuvem usando **Supabase** (PostgreSQL).
- **`public` schema:** Armazena o histórico cru e metadados dos milhares de anúncios coletados, atualizados dinamicamente pelo scraper.
- **`auth` schema:** Isola a tabela de usuários, garantindo que o acesso à calculadora de precificação seja exclusivo para usuários registrados na plataforma, mantendo padrões de segurança modernos.

---

## 🤖 Coleta de Dados e Anti-Bot (ZenRows)

Um dos maiores desafios de projetos de inteligência de mercado é a extração de dados em larga escala sem sofrer bloqueios (IP Bans ou Captchas). 

O Rigfy resolve isso delegando a camada de requisição ao **ZenRows**:
- A requisição é enviada pelo nosso `FastAPI` para a rede do ZenRows.
- O ZenRows utiliza um cluster distribuído de **proxies premium residenciais** e renderização de JavaScript em instâncias de navegadores *headless*.
- Retornamos o HTML cru e estruturado para o nosso interpretador local (Scrapling) fazer a extração limpa via Regex e XPath.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.12+
- Node.js 20+

### Passo 1: Configurando o Backend (API)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Crie um arquivo `.env` baseado no `.env.example`:
```env
DATABASE_URL=postgresql://postgres... (URL do seu banco Supabase)
ZENROWS_API_KEY=sua_chave_aqui
```
Inicie o servidor (ele cuidará das coletas no plano de fundo automaticamente):
```bash
uvicorn app.main:app --reload --port 8000
```

### Passo 2: Configurando o Frontend (React)
Em um novo terminal:
```bash
cd frontend
npm install
```
Crie um arquivo `.env` na raiz do frontend:
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://...
VITE_SUPABASE_ANON_KEY=eyJhbGciOi...
```
Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

---

## ☁️ Topologia de Deploy (Produção)

A aplicação foi planejada para operar de forma elástica, descentralizada e com baixíssimo custo de manutenção de infraestrutura (*Serverless-first*):

1. **Banco de Dados (PostgreSQL) + Auth:** [Supabase](https://supabase.com)
2. **Motor de Coleta e API (Python):** [Render](https://render.com) (Lendo o `render.yaml` nativo).
3. **Distribuição do Frontend (React):** [Netlify](https://netlify.com) / Vercel (distribuição via CDN global Edge).

---

## 📚 Documentação dos Endpoints REST

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/stats/resumo` | Varre o Banco de Dados e retorna insights de volume: total de peças rastreadas e contagem histórica. |
| `GET` | `/price/predict` | Recebe a categoria, série e modelo do hardware, cruza com a base histórica via modelo ML e retorna as estimativas de revenda e custo. |
| `POST` | `/collect/trigger` | Dispara um job manual (síncrono) para varrer os marketplaces imediatamente e alimentar o banco de dados. |
