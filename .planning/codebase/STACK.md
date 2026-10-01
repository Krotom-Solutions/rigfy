---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# Technology Stack

**Analysis Date:** 2026-10-01

## Overview

Rigfy is a SaaS platform for intelligent hardware pricing using automated web scraping and Machine Learning. The repository is organized as a decoupled monorepo containing a Python FastAPI backend and a React 19 (TypeScript) frontend.

## Languages & Runtimes

- **Backend Runtime:** Python `3.12+` (specifically Python `3.12.7` pinned in `backend/render.yaml`)
- **Backend Package Management:** Standard pip via `backend/requirements.txt`, local virtual environment in `backend/.venv`
- **Frontend Runtime:** Node.js `20+` / Bun (detected lockfile `frontend/bun.lock`)
- **Frontend Language:** TypeScript `~5.8.2` (`frontend/tsconfig.json`)
- **Frontend Build Tool:** Vite `^6.2.3` (`frontend/vite.config.ts`)

## Frameworks & Core Libraries

### Backend (`backend/`)

- **Web Framework:** FastAPI `0.111.0` (`backend/app/main.py`)
- **ASGI Server:** Uvicorn (standard) `0.29.0`
- **HTTP Client:** HTTPX `0.27.0` (asynchronous HTTP requests for ZenRows proxying)
- **Web Scraping & Parsing:** Scrapling `0.2.9` (`backend/app/scraper/parser.py`)
- **Database ORM:** SQLAlchemy `2.0.30` with `asyncio` extension (`backend/app/core/database.py`)
- **Database Driver:** Asyncpg `0.29.0` (async PostgreSQL driver)
- **Data Validation & Settings:** Pydantic `2.7.1` and Pydantic-Settings `2.2.1` (`backend/app/core/config.py`)
- **Task Scheduling:** APScheduler `3.10.4` (`backend/app/scheduler/jobs.py`)
- **Machine Learning & Data Processing:**
  - Scikit-Learn `1.5.0` (`RandomForestRegressor`, `OneHotEncoder`, `ColumnTransformer` in `backend/app/ml/pipeline.py`)
  - Pandas `2.2.2` (data transformations and feature extraction)
  - Joblib `1.4.2` (model serialization to `backend/app/ml/modelo_rigfy.joblib`)
  - Matplotlib `3.9.2` (validation charts generation in `backend/validation/`)
- **Migrations:** Alembic `1.13.1` (installed in requirements, pending migration scripts)

### Frontend (`frontend/`)

- **UI Framework:** React `19.0.1` (`frontend/src/App.tsx`)
- **DOM Renderer:** React DOM `19.0.1`
- **Routing:** React Router DOM `^7.18.1` (`frontend/src/App.tsx`)
- **Styling Engine:** Tailwind CSS `^4.1.14` with `@tailwindcss/vite` `^4.1.14` (`frontend/src/index.css`)
- **Animation:** Motion `^12.23.24` (Framer Motion v12)
- **Iconography:** Lucide React `^0.546.0`
- **Typography:** `@fontsource/inter` `^5.2.8` and `@fontsource/jetbrains-mono` `^5.2.8`
- **BaaS Client:** `@supabase/supabase-js` `^2.110.6` (`frontend/src/lib/supabase.ts`)
- **AI Integration (Client SDK):** `@google/genai` `^2.4.0`

## Configuration & Environment Variables

### Backend Configuration

- Handled by Pydantic `BaseSettings` in `backend/app/core/config.py` loading `.env`
- Pydantic model: `Settings` with `extra="ignore"`
- Required environment variables (specified in `backend/.env.example`):
  - `DATABASE_URL`: PostgreSQL connection string (asyncpg formatted: `postgresql+asyncpg://...`)
  - `ZENROWS_API_KEY`: API key for ZenRows headless proxy scraping
  - `SCRAPER_PAGES_PER_RUN`: Number of pages scraped per run (default: 5)
  - `SCRAPER_DELAY_SECONDS`: Delay between scraping requests (default: 2)
  - `SCRAPER_SCHEDULE_HOUR`: Scheduled run hour (default: 3)
  - `SCRAPER_SCHEDULE_MINUTE`: Scheduled run minute (default: 0)
  - `APP_ENV`: Deployment environment (`development` / `production`)
  - `LOG_LEVEL`: Logging verbosity (default: `INFO`)

### Frontend Configuration

- Managed via Vite `import.meta.env`
- Defined in `frontend/.env.example`:
  - `VITE_API_URL`: Backend URL (e.g. `http://localhost:8000`)
  - `VITE_SUPABASE_URL`: Supabase project URL
  - `VITE_SUPABASE_ANON_KEY`: Supabase anonymous public key

### Deployment Manifests

- `backend/render.yaml`: Defines Render Web Service `rigfy-backend` in region `ohio` running Python `3.12.7`, automatic ML model training if missing on build, and health check at `/health`.

---
*Stack analysis: 2026-10-01*
