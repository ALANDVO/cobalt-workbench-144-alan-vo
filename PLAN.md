# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

skeleton-fastapi-react

## Roadmap

### skeleton-fastapi-react — FastAPI + React skeleton with health check and basic UI

Status: done

Acceptance:
- FastAPI backend starts and serves /health endpoint
- React + Vite frontend builds and loads
- Frontend displays backend health status
- Docker compose brings up both services
- Backend tests pass (pytest)
- Frontend tests pass (vitest)

Implementation: `backend/app/main.py`, `backend/app/api/health.py`, `backend/requirements.txt`, `backend/tests/test_health.py`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/api/client.ts`, `frontend/tests/App.test.tsx`, `compose.yaml`, `Dockerfile.backend`, `Dockerfile.frontend`, `.env.example`, `README.md`, `pyproject.toml`

Tests: `backend/tests/test_health.py`, `frontend/tests/App.test.tsx`

### sandbox-orchestration — Cross-OS sandbox orchestration (lume + Docker drivers)

Status: planned

Acceptance:
- API to create/start/stop/destroy sandboxes
- Driver abstraction for lume VMs and Docker containers
- ARM64 (Apple Silicon) compatible Docker image handling
- Sandbox state persistence (SQLite)

### benchmark-runner — Benchmark runner for computer-use evaluation

Status: planned

Acceptance:
- Define benchmark tasks (JSON/YAML)
- Execute tasks in sandboxes with timing/metrics
- Collect screenshots, action traces, outcomes
- Export results (JSON/CSV)

### auth-oidc-keycloak — OIDC authentication with Keycloak (SAML broker ready)

Status: planned

Acceptance:
- Keycloak realm import
- Backend session auth with HttpOnly cookies + CSRF
- Frontend login/logout flow
- Role-based access (viewer/operator/admin)

### llm-adapters — LLM provider adapters (OpenAI-compatible, Anthropic, Gemini, Ollama)

Status: planned

Acceptance:
- Unified adapter interface
- Configurable provider/model/endpoint
- Server-side keys only
- Bounded timeouts, redacted errors

### data-generation — Training data generation workflow

Status: planned

Acceptance:
- Record action sequences with screenshots
- Export labeled trajectories
- Filter/validate dataset quality

