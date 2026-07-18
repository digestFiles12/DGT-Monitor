# Continuidad para un nuevo chat

**Este documento es un QUICK-START para reanudación rápida. Para contexto completo, ver `docs/PHASE_7_COMPLETED.md`.**

---

## Status: Phase 7 ✅ COMPLETE

- ✅ 34 tests passing
- ✅ Activity system (API + SQLite + auth) implemented
- ✅ Render deployment configured
- ✅ GitHub Actions CI/CD operational
- ✅ All documentation updated
- ✅ Ready for code review, staging, production

**See `docs/PHASE_7_COMPLETED.md` for complete phase closure documentation.**

---

## Quick Start

### Paths & Environment

```powershell
# Navigate to project root
cd <project-root>

# Activate venv
.\.venv\Scripts\Activate.ps1

# Python 3.12
python --version
```

### Validate State (Always First)

```powershell
# 34 tests should pass
python -m pytest test -q

# No compilation errors
python -m compileall -q dgt_monitor dashboard

# Git clean
git status
git log --oneline -5
```

### Architecture Quick Reference

```
API (FastAPI) → Application (Services) → Infrastructure (Cache/Parsers/HTTP)
                                      ↓
                              Core (Domain Models)
```

**Key Files:**
- `dgt_monitor/core/` - Domain models, ports, exceptions
- `dgt_monitor/infrastructure/` - HTTP, parsers, cache, activity store
- `dgt_monitor/application/` - Services, facade
- `dgt_monitor/api/` - FastAPI routes and app factory
- `test/` - Unit, integration, API, GUI tests

### Environment Variables

```powershell
# Activity store backend
$env:ACTIVITY_DB_PATH = "activity.db"     # If omitted: in-memory

# API authentication
$env:ACCEPTED_KEYS = "key1,key2"          # Accepted API keys
$env:REVOKED_KEYS = "revoked1"            # Revoked API keys
```

---

## Documentation Reference

| Document | Purpose |
|----------|---------|
| `docs/INDEX.md` | Navigation hub |
| `docs/PLAN_REFACTORIZACION.md` | Refactoring phases (1-7) |
| `docs/ARQUITECTURA.md` | Layered architecture diagram |
| `docs/PHASE_7_COMPLETED.md` | **← MAIN HANDOFF DOC: Exact Phase 7 status** |
| `docs/PRUEBAS.md` | Test suite (34 tests, execution) |
| `docs/SMOKE_TEST.md` | Manual validation checklist |
| `docs/DESPLIEGUE.md` | Render configuration, env vars |
| `docs/DECISIONES.md` | Architectural constraints & decisions |

---

## Git History

All commits preserve semantic history:
- Latest: Stabilize test suite (Phase 7 completion)
- Previous: Document project handoff and migration state
- Earlier: Add modular FastAPI and WebSocket adapters
- Earlier: Build shared DGT domain and application services
- Earlier: Add initial OOP architecture & PyQt GUI

---

## Onboarding Instructions for New Chat/Developer

1. **Read Documentation** (in order):
   - `docs/INDEX.md` → navigation
   - `docs/PHASE_7_COMPLETED.md` → current status
   - `docs/PLAN_REFACTORIZACION.md` → context
   - `docs/ARQUITECTURA.md` → design

2. **Verify Setup**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   python -m pytest test -q          # expect 34 passed
   python -m compileall -q dgt_monitor dashboard
   git status                         # should be clean
   ```

3. **Check Render Dashboard**:
   - Verify current branch deployment
   - Test `/api/health` endpoint

4. **Next Phase**:
   - Code review (if not yet done)
   - Merge to `main`
   - Smoke test on staging
   - Production deployment

---

## Environment Setup

- **Workspace Structure:** Root directory contains `pyproject.toml`, `dgt_monitor/`, `dashboard/`, `test/`
- **Virtual Environment:** `.\.venv` (relative to project root)
- **Python:** 3.12.x
- **Repository:** Managed via git with feature branches

---

**For detailed Phase 7 completion status, test results, and handoff checklist, see `docs/PHASE_7_COMPLETED.md`.**