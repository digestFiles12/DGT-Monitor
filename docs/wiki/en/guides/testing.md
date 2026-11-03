# Testing strategy
## Status
The suite contains 148 tests (`pytest tests`), all passing, organized by layer:
```text
tests/
  conftest.py            # shared (autouse) fixtures
  fixtures/incidents_sample.xml
  unit/                  # core, regions, statistics, cache, stores, parsers, menu
  integration/           # facade and incident persistence
  api/                   # REST, WebSocket, statistics, and Activity API
  gui/                   # PyQt6 in offscreen mode
```
## Commands
```powershell
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m pytest tests\unit -q
.\.venv\Scripts\python.exe -m pytest tests\integration -q
.\.venv\Scripts\python.exe -m pytest tests\api -q
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests\gui -q
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```
## Fixtures and data
- `isolated_incident_db` (autouse, in `tests/conftest.py`): points `INCIDENT_DB_PATH` at a temporary directory so the incident SQLite file never touches the project.
- `init_activity_store` (autouse): creates an activity store per test and reinitializes it when `ACTIVITY_DB_PATH` changes.
- `tests/fixtures/incidents_sample.xml`: sample DATEX2 XML used by the regions, statistics, statistics API, persistence, and console menu tests.
## Rules
- Never use the real DGT: inject fake repositories or a fake facade.
- Add a contract test for every endpoint or PWA route.
- For the GUI use `QT_QPA_PLATFORM=offscreen`.
- Keep a manual checklist for non-modal windows, images, thread shutdown, and deployment.
## What must be covered
- Cache expiration and invalidation, and concurrent access.
- Invalid XML and optional fields; model serialization.
- API filters and limits, including `match_mode`, invalid regex, and `incident_coverage`.
- `/api/stats` (`level`, extremes) and `/api/stats/grouped`; `/ws/incidents`.
- Activity API: authentication, revocation, SSE, CSV, and pagination.
- Province-to-region mapping and grouped statistics.
- Console menu (`src/dgt_monitor/menu.py`) with injected input and output.
- `QThread` lifecycle, failed image loads, and worker errors.
- Dashboard/PWA contracts (static routes, manifest, and service worker).
See also [the API guide](api.md) and [the GUI guide](gui.md).
