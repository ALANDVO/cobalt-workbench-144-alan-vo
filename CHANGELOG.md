# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

### Added
- Enhanced health check endpoint (`/api/v1/health`) with uptime and environment fields
- Readiness probe endpoint (`/api/v1/ready`) for Kubernetes liveness/readiness checks
- Frontend displays uptime, environment, and readiness status
- Updated backend and frontend tests for new endpoints

### Verified
- Backend: pytest (4 tests) pass
- Frontend: vitest (5 tests) pass

## 1.1.0 — work-in-progress checkpoint

### Fixed
- Backend mypy type errors: `SettingsConfigDict` for pydantic-settings v2, return type annotations for `health_check()` and `lifespan()`
- Frontend ESLint configuration with TypeScript, React, and React Hooks support

### Verified
- Backend: pytest, ruff, mypy all pass
- Frontend: vitest, eslint, tsc, vite build all pass

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- FastAPI backend with health check endpoint (`/api/v1/health`)
- React + TypeScript + Vite frontend displaying backend health
- Docker Compose with backend, frontend, and Keycloak services
- Backend tests (pytest) and frontend tests (vitest)
- Configuration via `.env.example`
- README with architecture diagram and setup instructions
- MIT License
- portfolio.json with product metadata

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
