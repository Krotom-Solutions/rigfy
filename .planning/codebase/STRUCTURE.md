---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# Codebase Structure

**Analysis Date:** 2026-10-01

## Directory Layout

```
rigfy/
├── .planning/                  # Project planning, codebase maps, and GSD specs
│   └── codebase/               # High-fidelity architectural and codebase maps
├── backend/                    # Python FastAPI backend service
│   ├── app/                    # Core backend application code
│   │   ├── api/                # FastAPI endpoints and route handlers
│   │   ├── core/               # Configuration, database session, settings
│   │   ├── crud/               # Database access functions (CRUD)
│   │   ├── ml/                 # Machine learning pipeline, feature engineering, trained model
│   │   ├── models/             # SQLAlchemy ORM database models
│   │   ├── scheduler/          # APScheduler cron jobs setup
│   │   ├── schemas/            # Pydantic schemas for request/response serialization
│   │   └── scraper/            # Web scraping fetchers, parsers, and regex extractors
│   ├── scripts/                # Operational scripts (training, scraping, db init, validation)
│   ├── validation/             # Validation datasets, human evaluation forms, and metric plots
│   ├── render.yaml             # Render cloud deployment configuration
│   └── requirements.txt        # Python dependency manifest
├── frontend/                   # React 19 + TypeScript frontend application
│   ├── src/                    # Frontend source code
│   │   ├── components/         # Reusable React UI components
│   │   │   ├── layout/         # Frame components (Navbar, Footer)
│   │   │   ├── sections/       # Landing page sections (Calculator, Hero, Pricing, etc.)
│   │   │   └── ui/             # Reusable design primitives (Button, Select, Divider)
│   │   ├── lib/                # Client libraries (Supabase client)
│   │   ├── pages/              # Top-level page views (Home.tsx)
│   │   ├── App.tsx             # Root React application router component
│   │   ├── main.tsx            # React client DOM mount
│   │   └── index.css           # Global stylesheet and Tailwind CSS v4 setup
│   ├── package.json            # Frontend package manifest
│   ├── tsconfig.json           # TypeScript compiler configuration
│   └── vite.config.ts          # Vite build and development configuration
└── README.md                   # Project documentation and architectural overview
```

## Directory Purposes

- **`backend/app/api/`**: Contains route controllers for API versioning. Each file maps to a specific domain (`price.py`, `listings.py`, `stats.py`).
- **`backend/app/core/`**: Central infrastructure modules like `config.py` (Pydantic settings) and `database.py` (SQLAlchemy async engine).
- **`backend/app/crud/`**: Pure async database queries isolating SQL logic from API routers.
- **`backend/app/ml/`**: Machine learning logic, feature encoders, model loading/dumping, and tree variance prediction.
- **`backend/app/scraper/`**: Modular scraping layers separating network transport (`fetcher.py`), DOM parsing (`parser.py`), regex spec extraction (`extractor.py`), and orchestration (`pipeline.py`).
- **`backend/scripts/`**: One-off CLI utilities for training (`treinar_modelo.py`), manual scraping runs (`run_coleta.py`), and database setup (`init_db.py`).
- **`backend/validation/`**: Offline evaluation artifacts including ground truth comparison metrics (`metricas.md`, `resultados.csv`).
- **`frontend/src/components/sections/`**: Main functional sections for the single-page application.
- **`frontend/src/components/ui/`**: Base UI elements following the brutalist theme.

## Key File Locations

**Entry Points:**
- `backend/app/main.py`: FastAPI server entry point and lifespan hooks.
- `frontend/src/main.tsx`: React DOM mount.
- `frontend/src/App.tsx`: Top-level application layout and routing.

**Configuration:**
- `backend/app/core/config.py`: Environment configuration via Pydantic.
- `backend/render.yaml`: Cloud deployment definition.
- `frontend/vite.config.ts`: Vite plugins and dev server settings.
- `frontend/tsconfig.json`: TypeScript compiler options.

**Core Business Logic:**
- `backend/app/ml/pipeline.py`: Feature engineering pipeline and model inference.
- `backend/app/scraper/extractor.py`: Hardware specification parsing regexes.
- `backend/app/scraper/fetcher.py`: ZenRows client and request rate limiting.

## Naming Conventions

- **Python Backend:**
  - Files and directories: `snake_case.py` (e.g. `anuncio.py`, `run_coleta.py`).
  - Classes: `PascalCase` (e.g. `Anuncio`, `Settings`, `PriceRequest`).
  - Functions and variables: `snake_case` (e.g. `prever_faixa_preco`, `obter_modelo`).
- **Frontend:**
  - Component files: `PascalCase.tsx` (e.g. `Calculator.tsx`, `ResultCard.tsx`).
  - Utility and entry files: `camelCase.ts` or `kebab-case` (e.g. `supabase.ts`, `main.tsx`).
  - CSS variables and utility classes: Tailwind utility classes with custom theme aliases in `frontend/src/index.css`.

## Where to Add New Code

**Adding a New Hardware Category / Marketplace Source:**
- Add target URLs: `backend/app/scraper/fetcher.py`
- Add DOM selectors: `backend/app/scraper/parser.py`
- Add regex extraction rules: `backend/app/scraper/extractor.py`
- Add category filter options: `frontend/src/components/sections/Calculator.tsx`

**Adding a New API Endpoint:**
- Define Pydantic request/response schema in `backend/app/schemas/`
- Implement DB access logic in `backend/app/crud/`
- Create or update router in `backend/app/api/`
- Register router in `backend/app/main.py`

**Adding a New Frontend Component or Page:**
- Reusable UI element: `frontend/src/components/ui/`
- Landing page block: `frontend/src/components/sections/`
- Full view / page: `frontend/src/pages/`
- Register new route in `frontend/src/App.tsx`

---
*Structure analysis: 2026-10-01*
