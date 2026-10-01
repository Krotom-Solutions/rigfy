---
last_mapped_commit: 233af598b802a4676c1a05ba0efcc8b9961cccfa
last_mapped_at: 2026-10-01
---
# Testing Patterns & Verification

**Analysis Date:** 2026-10-01

## Current Testing State

The codebase currently relies on **standalone verification scripts**, offline regression fixtures, and statistical model evaluation scripts rather than an automated CI test suite (such as Pytest or Vitest).

## Verification Scripts (`backend/scripts/`)

### 1. Offline Parser Verification

- **Script:** `backend/scripts/test_parser.py`
- **Purpose:** Validates DOM parsing and regex extraction against cached HTML (`backend/debug_olx.html`) without consuming ZenRows proxy credits or triggering remote rate limits.
- **Execution:**
  ```bash
  cd backend
  python scripts/test_parser.py
  ```

### 2. Database Connectivity Test

- **Script:** `backend/scripts/test_db_conn.py`
- **Purpose:** Verifies PostgreSQL credentials, network reachability, and async session handling.
- **Execution:**
  ```bash
  cd backend
  python scripts/test_db_conn.py
  ```

### 3. Data Quality Audit

- **Script:** `backend/scripts/relatorio_qualidade.py`
- **Purpose:** Analyzes the proportion of stored ads with successful hardware specification extraction (CPU line, generation, RAM, storage, price).
- **Execution:**
  ```bash
  cd backend
  python scripts/relatorio_qualidade.py
  ```

### 4. Machine Learning Model Validation

- **Script:** `backend/scripts/executar_validacao.py`
- **Purpose:** Generates a stratified hold-out validation report comparing model predictions against baseline statistical models and generating visual evaluation plots:
  - `backend/validation/barras_mae.png` (MAE comparison)
  - `backend/validation/boxplot_erros.png` (Residual distribution)
  - `backend/validation/previsto_vs_real.png` (Predicted vs Actual price regression)
  - `backend/validation/metricas.md` (Summary table of MAE, RMSE, MAPE, R²)
- **Execution:**
  ```bash
  cd backend
  python scripts/executar_validacao.py
  ```

## Frontend Verification & Type Checking

- **Type Checking:** Runs TypeScript compiler in no-emit mode to catch type regressions.
  ```bash
  cd frontend
  npm run lint
  ```
- **Build Verification:** Validates production bundle assembly via Vite.
  ```bash
  cd frontend
  npm run build
  ```

## Recommended Testing Architecture (Target State)

To support robust Spec-Driven Development, the following automated testing setup is recommended for future phases:
1. **Backend Integration & Unit Tests:**
   - Add `pytest` and `pytest-asyncio` to `backend/requirements.txt`.
   - Implement unit tests for regex extraction in `tests/test_extractor.py`.
   - Implement FastAPI endpoint tests using `httpx.AsyncClient` in `tests/test_api.py`.
2. **Frontend Component & Integration Tests:**
   - Add `vitest` and `@testing-library/react` to `frontend/package.json`.
   - Add unit tests for form validation in `Calculator.test.tsx`.

---
*Testing analysis: 2026-10-01*
