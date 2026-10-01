---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# Coding Conventions

**Analysis Date:** 2026-10-01

## Code Style & Formatting

### Backend (Python)

- **Standard:** Follows PEP 8 conventions for Python 3.12.
- **Type Annotations:** Full modern type hinting throughout the application:
  - SQLAlchemy 2.0 `Mapped[...]` and `mapped_column(...)` for ORM models.
  - Python 3.10+ union syntax `str | None` instead of `Optional[str]`.
  - Pydantic v2 type annotations for request and response models.
- **Async First:** All route handlers, database queries, and network fetchers use `async` / `await`.

### Frontend (TypeScript / React)

- **Standard:** TypeScript with strict mode enabled (`frontend/tsconfig.json`).
- **Styling:** Tailwind CSS v4 utility classes. Custom color tokens (`bg`, `bg-subtle`, `text-primary`, `border-strong`) defined via theme CSS in `frontend/src/index.css`.
- **UI Architecture:** Brutalist / Minimalist aesthetic (sharp corners `rounded-none`, high contrast black-and-white borders and accents, monospace accents for metadata).

## Naming Conventions

### Python Backend

- **Modules and packages:** lowercase with underscores (`anuncio.py`, `pipeline.py`).
- **Classes:** `PascalCase` (`Anuncio`, `PriceRequest`, `MercadoStatsResponse`).
- **Functions:** lowercase with underscores (`prever_faixa_preco`, `carregar_modelo`, `executar_coleta`).
- **Constants:** `UPPER_SNAKE_CASE` (`MODELO_PATH`, `FEATURES_CATEGORICAS`, `FEATURES_NUMERICAS`, `OLX_URLS`).

### TypeScript / React Frontend

- **Components:** `PascalCase` matching the file name (`Calculator.tsx`, `Navbar.tsx`).
- **Hooks and Functions:** `camelCase` (`handleCalculate`, `handleReset`).
- **Props Interfaces:** Inline or typed with interface/type declaration.

## Import Organization

### Backend Imports

1. Standard library modules (`os`, `sys`, `logging`, `asyncio`, `datetime`).
2. Third-party packages (`fastapi`, `sqlalchemy`, `pydantic`, `pandas`, `sklearn`).
3. Internal application modules (`from app.core...`, `from app.models...`, `from app.crud...`).

### Frontend Imports

1. React core libraries (`react`, `react-router-dom`).
2. UI and animation libraries (`motion`, `lucide-react`).
3. Internal components (`../components/layout/...`, `../components/sections/...`).
4. Internal utilities and libraries (`../lib/supabase`).

## Error Handling Patterns

### Backend

- **API Error Responses:** FastAPI HTTPException for client errors.
- **External Network Errors:** `httpx.HTTPStatusError` and `httpx.RequestError` caught inside `backend/app/scraper/fetcher.py`, logged with `logger.error`, returning `None` to prevent crashing the collection loop.
- **Fallback Predictions:** In `backend/app/api/price.py`, if the ML model is not available or input fails, returns a default `PriceResponse` with `confianca="insuficiente"` and `preco_estimado=None` instead of throwing an unhandled 500 error.

### Frontend

- Asynchronous actions wrapped in `try/catch/finally` blocks with local loading state flags (`setLoading(true)` / `setLoading(false)`).

## Logging Practices

- **Backend Framework:** Python standard `logging` configured in `backend/app/main.py`:
  ```python
  logging.basicConfig(
      level=getattr(logging, settings.log_level),
      format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
  )
  ```
- **Logger Instances:** Instantiated per module with `logger = logging.getLogger(__name__)`.
- **Log Levels Used:**
  - `logger.info()`: Application startup, scheduler events, completed scraping batch summaries.
  - `logger.warning()`: Missing ML model files, empty pages received from proxies, missing specs.
  - `logger.error()`: Network timeouts, parsing failures, database connection errors.

---
*Convention analysis: 2026-10-01*
