---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# Codebase Concerns & Technical Debt

**Analysis Date:** 2026-10-01

## Critical Issues & Tech Debt

### 1. Hardcoded API Endpoint in Frontend

- **Issue:** `frontend/src/pages/Home.tsx` directly calls `http://localhost:8000/price/predict` instead of referencing the configured environment variable `import.meta.env.VITE_API_URL`.
- **Files:** `frontend/src/pages/Home.tsx`
- **Impact:** Any deployment outside local development (e.g. Vercel, Netlify) will fail to connect to the backend API.
- **Fix approach:** Update `frontend/src/pages/Home.tsx` to use `const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'; fetch(`${apiUrl}/price/predict`, ...)`.

### 2. Hardcoded Supabase Fallback Credentials

- **Issue:** `frontend/src/lib/supabase.ts` contains hardcoded project URL and JWT anon token fallbacks in the source code.
- **Files:** `frontend/src/lib/supabase.ts`
- **Impact:** Hardcoded credentials committed to source control create credential rotation friction and hygiene risks.
- **Fix approach:** Remove hardcoded fallback strings and throw a descriptive error if `VITE_SUPABASE_URL` or `VITE_SUPABASE_ANON_KEY` is missing in the environment.

### 3. Limited Training Dataset & Low ML Accuracy

- **Issue:** As documented in `backend/validation/metricas.md`, the Random Forest model was trained on an initial dataset of only 118 listings.
- **Files:** `backend/app/ml/pipeline.py`, `backend/validation/metricas.md`
- **Impact:** High prediction error (MAPE: 138.45%, R²: 0.027) with only 13.3% of predictions falling within ±20% of the true price.
- **Fix approach:** Scale daily scraping runs to accumulate 1,000+ listings, filter outliers in price/year, and introduce gradient boosted decision trees (e.g., LightGBM / XGBoost) or hyperparameter tuning.

## Architecture & Infrastructure Fragility

### 4. Database Schema Migrations Not Tracked via Alembic

- **Issue:** Although `alembic` is included in `backend/requirements.txt`, no `alembic.ini` or migration version files exist in `backend/`. Schema changes rely on `scripts/init_db.py`.
- **Files:** `backend/requirements.txt`, `backend/scripts/init_db.py`
- **Impact:** High risk of schema drift and destructive updates in production PostgreSQL databases.
- **Fix approach:** Initialize Alembic (`alembic init alembic`) and generate baseline migrations corresponding to `backend/app/models/anuncio.py`.

### 5. In-Process Scheduler Concurrency Risk

- **Issue:** APScheduler is initialized inside the FastAPI lifespan context (`backend/app/main.py`) running in-memory.
- **Files:** `backend/app/main.py`, `backend/app/scheduler/jobs.py`
- **Impact:** If Uvicorn runs with multiple workers (`--workers > 1`), multiple instances of the scraping cron job will fire simultaneously, exhausting ZenRows proxy credits and creating lock contention.
- **Fix approach:** Run the scheduler in a dedicated single-instance background worker process on Render or use a distributed task queue (e.g. Celery / Redis or pg_cron).

## Test Coverage & Quality Gaps

### 6. Absence of Automated Test Suite

- **Issue:** Neither backend nor frontend possesses an automated test harness (no `pytest` or `vitest`).
- **Files:** `backend/`, `frontend/`
- **Impact:** Regressions in regex parsing, endpoint routing, or data serialization cannot be automatically caught during PR or CI runs.
- **Priority:** High.

### 7. Scraper Selector Fragility

- **Issue:** Web scraping depends on specific DOM elements and class patterns on OLX Brasil.
- **Files:** `backend/app/scraper/parser.py`, `backend/app/scraper/extractor.py`
- **Impact:** Any redesign by OLX will break data extraction silently without alerting.
- **Fix approach:** Add monitoring/alerting on scraping success rates and maintain backup selector fallbacks.

---
*Concerns audit: 2026-10-01*
