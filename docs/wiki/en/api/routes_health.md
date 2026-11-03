# dgt_monitor/api/routes/health.py
Provides a simple availability check with the current UTC time.
## Dependencies
Uses the standard-library `datetime`/`timezone` and FastAPI `APIRouter`; the router is registered in `api.factory.create_app`.
## Contents
### `health()`
- `GET /api/health`, with no query parameters, returns `{"status":"ok","time":"<ISO-8601 UTC>"}`. Normal response: 200.
