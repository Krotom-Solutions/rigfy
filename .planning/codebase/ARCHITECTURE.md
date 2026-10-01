---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# System Architecture

**Analysis Date:** 2026-10-01

## Architectural Pattern

Rigfy adopts a **Decoupled Monorepo Architecture** separating the data ingestion / intelligence engine (Backend) from the presentation layer (Frontend).

```
[ Marketplace (OLX Brasil) ]
            │ (HTML via ZenRows headless proxy)
            ▼
[ Scraper Pipeline (app/scraper) ]
            │
            ▼
[ Extraction & Normalization (app/scraper/extractor) ]
            │
            ▼
[ PostgreSQL / Supabase (app/models/anuncio) ]
            │
            ├──────────────┐
            ▼              ▼
[ ML Training Pipeline ]   [ Analytics API (app/api/stats) ]
 (app/ml/pipeline)         [ Listings API (app/api/listings) ]
            │              [ Price API (app/api/price) ]
            ▼              │
[ Serialized Model (.joblib) ]
            │
            ▼
[ Prediction Engine ] ◄─── [ React 19 Frontend SPA (src/) ]
```

## System Layers

### 1. Presentation & Client Layer (`frontend/src/`)

- **UI Framework:** React 19 SPA bundled with Vite 6.
- **Styling Architecture:** Tailwind CSS v4 using a High-Contrast Brutalist/Minimalist design language (`frontend/src/index.css`).
- **Component Hierarchy:**
  - `components/layout/`: Global framing (`Navbar.tsx`, `Footer.tsx`).
  - `components/sections/`: Page sections (`Hero.tsx`, `Calculator.tsx`, `ResultCard.tsx`, `HowItWorks.tsx`, `Pricing.tsx`).
  - `components/ui/`: Reusable primitives (`Button.tsx`, `Select.tsx`, `Divider.tsx`, `ProgressBar.tsx`).
- **Client State & Network:** Direct asynchronous fetch handlers in `frontend/src/pages/Home.tsx` interacting with the backend REST endpoints.

### 2. API Routing & Serialization Layer (`backend/app/api/`)

- **Framework:** FastAPI with automatic OpenAPI generation.
- **Routers:**
  - `app/api/price.py`: Machine learning price predictions (`POST /price/predict`, `GET /price/predict`).
  - `app/api/listings.py`: Querying, filtering, and paginating stored ads (`GET /listings`, `GET /listings/opcoes`).
  - `app/api/stats.py`: Market metrics and aggregations for analytics (`GET /stats/mercado`, `GET /stats/resumo`).
- **Request / Response Contracts:** Defined strictly with Pydantic in `app/schemas/api.py` and `app/schemas/anuncio.py`.

### 3. Business Logic & Intelligence Layer

- **Machine Learning Subsystem (`backend/app/ml/`):**
  - Feature engineering pipeline using `ColumnTransformer` with `OneHotEncoder` for categorical hardware specs (brand, cpu line, storage type, gpu memory) and `passthrough` for numerical variables.
  - Regressor: `RandomForestRegressor` with 100 estimators.
  - Distribution prediction: Computes 15th percentile (min), median (estimated), and 85th percentile (max) across tree predictions (`prever_faixa_preco` in `backend/app/ml/pipeline.py`).
- **Scraping Subsystem (`backend/app/scraper/`):**
  - `fetcher.py`: Asynchronous proxy requests via ZenRows API with automatic retries and headless browser rendering.
  - `parser.py`: HTML parsing using Scrapling CSS/XPath selectors.
  - `extractor.py`: Regular expression pattern matching extracting hardware specs (CPU family, generation, RAM amount, storage type, GPU model).
  - `pipeline.py`: Orchestrator driving fetch, deduplication, extraction, and persistence.
- **Scheduling Subsystem (`backend/app/scheduler/`):**
  - APScheduler `AsyncIOScheduler` configured in `backend/app/scheduler/jobs.py` executing daily collection jobs.

### 4. Data Access & Persistence Layer (`backend/app/crud/` & `backend/app/core/`)

- **ORM:** SQLAlchemy 2.0 async mapped classes.
- **Database Model:** `Anuncio` (`backend/app/models/anuncio.py`) indexing `olx_id`, `coletado_em`, `preco`, `ram_gb`, `cpu_linha`.
- **CRUD Operations:** Pure async functions in `backend/app/crud/anuncio.py` executing parameterized SQL via SQLAlchemy `select`.

## Key Entry Points

- **Backend Application Entry Point:** `backend/app/main.py`
  - Defines lifespan managing APScheduler lifecycle and ML model pre-loading (`app.state.modelo_ml`).
- **Frontend Application Entry Point:** `frontend/src/main.tsx` and `frontend/src/App.tsx`
- **Data Collection Script Entry Point:** `backend/scripts/run_coleta.py`
- **ML Training Script Entry Point:** `backend/scripts/treinar_modelo.py`
- **Database Initialization Entry Point:** `backend/scripts/init_db.py`

## Cross-Cutting Concerns

- **Error Handling:** FastAPI exception handling and fallbacks in `backend/app/api/price.py` returning `confianca: "insuficiente"` if the model cannot be loaded.
- **CORS:** Configured in `backend/app/main.py` using settings from `backend/app/core/config.py`.
- **Database Session Lifecycle:** Injected via FastAPI dependency `Depends(get_db)` ensuring transactions close after request completion.

---
*Architecture analysis: 2026-10-01*
