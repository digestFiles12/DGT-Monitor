# Continuidad para un nuevo chat

**Este documento es un QUICK-START para reanudación rápida. Para contexto completo, ver `docs/PHASE_7_COMPLETED.md`.**

---

## Status: proyecto operativo

- ✅ API FastAPI, WebSocket, SSE y Activity API operativas
- ✅ Dashboard web/PWA servido desde `/`, con filtros completos, celdas estadísticas clicables, modo claro/oscuro, visor fullscreen de cámaras y desplegable en Render
- ✅ GUI PyQt6 modular con filtros completos, celdas estadísticas clicables, incidencias, dialogo de camaras, imagenes asincronas, visor fullscreen y modo claro/oscuro
- ✅ Activity system con backend en memoria o SQLite
- ✅ Render y GitHub Actions configurados
- ✅ 48 tests pasando

**See `docs/PHASE_7_COMPLETED.md` for complete project status and handoff documentation.**

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
# 48 tests should pass
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

# Activity API authentication
$env:ACTIVITY_API_KEYS = "key1,key2"          # Accepted API keys
$env:ACTIVITY_REVOKED_API_KEYS = "revoked1"  # Revoked API keys
```

---

## Documentation Reference

| Document | Purpose |
|----------|---------|
| `docs/INDEX.md` | Navigation hub |
| `docs/PLAN_REFACTORIZACION.md` | Refactoring phases (1-7) |
| `docs/ARQUITECTURA.md` | Layered architecture diagram |
| `docs/PHASE_7_COMPLETED.md` | **← MAIN HANDOFF DOC: Exact current status** |
| `docs/PRUEBAS.md` | Test suite (48 tests, execution) |
| `docs/DESPLIEGUE.md` | Render configuration, env vars |
| `docs/DECISIONES.md` | Architectural constraints & decisions |

---

## Recent history

La rama conserva commits separados por incremento: dashboard web para Render, GUI PyQt6 modular, dialogo no modal de camaras y carga asincrona de imagenes.

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
   python -m pytest test -q          # expect 43 passed
   python -m compileall -q dgt_monitor dashboard
   git status                         # should be clean
   ```

3. **Check Render Dashboard**:
   - Verify current branch deployment
   - Test `/` and `/api/health`

4. **Next Phase**:
   - Wrappers de compatibilidad de escritorio (`DGT.py`, `DGT_V2.py`)
   - Temporizador configurable y registro visible en GUI
   - Smoke test manual en Render

---

## Environment Setup

- **Workspace Structure:** Root directory contains `pyproject.toml`, `dgt_monitor/`, `dashboard/`, `test/`
- **Virtual Environment:** `.\.venv` (relative to project root)
- **Python:** 3.12.x
- **Repository:** Managed via git with feature branches

---

**For detailed Phase 7 completion status, test results, and handoff checklist, see `docs/PHASE_7_COMPLETED.md`.**