---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# External Integrations

**Analysis Date:** 2026-10-01

## Overview

Rigfy interacts with external data sources, proxy infrastructures, cloud databases, and authentication services to harvest marketplace listings and deliver price estimates.

## External Services & APIs

### 1. ZenRows Proxy & Scraping Service

- **Purpose:** Anti-bot bypass, residential IP rotation, and headless browser rendering for marketplace scraping.
- **Implementation:** `backend/app/scraper/fetcher.py`
- **Protocol:** REST API over HTTPS (`https://api.zenrows.com/v1/`)
- **Authentication:** Query parameter `apikey=${ZENROWS_API_KEY}`
- **Parameters Used:**
  - `url`: Target URL on OLX Brasil
  - `js_render`: `true` (enables headless browser for JavaScript execution)
  - `premium_proxy`: `true` (uses residential proxies to prevent 403 IP bans)
- **Error Handling:** Returns empty HTML or `None` on network timeouts/errors (`httpx.HTTPStatusError`, `httpx.RequestError`), caught and logged in `backend/app/scraper/fetcher.py`.

### 2. Supabase (Database & Authentication)

- **Purpose:** Cloud PostgreSQL data persistence for scraped ads, extracted hardware specifications, and user authentication.
- **Backend Database Connection:**
  - Managed in `backend/app/core/database.py`
  - Engine: SQLAlchemy `create_async_engine` with `asyncpg` driver
  - Connection Pool: `AsyncSessionLocal` with `expire_on_commit=False`
  - Target Schema: `public` (table `anuncios`)
- **Frontend Client Connection:**
  - Managed in `frontend/src/lib/supabase.ts`
  - Client: `createClient` from `@supabase/supabase-js`
  - Configuration: `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`
  - Intended for user session management and protected pricing calculator features.

### 3. Marketplace Target: OLX Brasil

- **Purpose:** Primary data source for real-world used computer hardware prices and listings.
- **Implementation:**
  - Target URLs defined in `backend/app/scraper/fetcher.py` (`OLX_URLS` mapping `notebook`, `desktop`, `pc_gamer`)
  - HTML parsing handled in `backend/app/scraper/parser.py` using Scrapling CSS/XPath selectors
  - Hardware specification extraction handled in `backend/app/scraper/extractor.py` using regular expressions.

### 4. Google Gemini API (GenAI)

- **Purpose:** Future-ready GenAI capabilities and automated hardware inspection assistance.
- **Implementation:** Referenced in `frontend/package.json` (`@google/genai`) and `frontend/.env.example` (`GEMINI_API_KEY`).

### 5. Render Hosting Platform

- **Purpose:** Cloud deployment platform for the FastAPI backend service and cron background tasks.
- **Configuration:** `backend/render.yaml`
- **Health Check:** `GET /health` (`backend/app/main.py`)

## Webhooks & Background Queues

- **APScheduler:** In-memory async background scheduler (`backend/app/scheduler/jobs.py`).
  - Job ID: `coleta_diaria`
  - Trigger: Cron trigger configured by `SCRAPER_SCHEDULE_HOUR` and `SCRAPER_SCHEDULE_MINUTE`.
- **Manual Trigger Webhook:** `POST /collect/trigger` in `backend/app/main.py` allowing on-demand triggering via FastAPI `BackgroundTasks`.

---
*Integrations analysis: 2026-10-01*
