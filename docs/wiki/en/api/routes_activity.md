# dgt_monitor/api/routes/activity.py
Exposes protected operations to query, export, stream, and clear the activity log.
## Dependencies
Uses the `core.activity` log module, header authentication, and standard utilities for asyncio, JSON, environment variables, and manual CSV generation. The router is registered in `api.factory.create_app`.
## Contents
### `_split_env(env_var)`
- Splits a comma-separated environment variable, trims whitespace, and drops empty entries.
### `_require_api_key(x_api_key=None)`
- Requires `X-API-Key`; rejects revoked keys first, then constant-time compares against the legacy key or allow-list. Failures produce 401.
### `list_activity(_, level=None, source=None, event_type=None, user=None, start_ts=None, end_ts=None, offset=0, limit=100)`
- `GET /api/activity/` requires `X-API-Key`. Accepts `level`, `source`, `event_type`, `user`, `start_ts`, `end_ts`, `offset` (0), and `limit` (100); exact-filters by the first four, but `start_ts` and `end_ts` are declared and not applied. Returns `{"total": int, "offset": int, "limit": int, "entries": [...]}`; a limit outside 1–1000 is replaced with 100. Responses: 200; 401 for a missing or invalid key; 422 if a parameter cannot be converted to its declared type.
### `export_csv(_)`
- `GET /api/activity/csv` requires `X-API-Key` and returns the full log as CSV (`timestamp,level,source,event_type,user,message`) with download name `activity.csv` and media type `text/csv; charset=utf-8`. Responses: 200; 401 for failed authentication.
### `stream_activity(_, replay=0, once=False)`
- `GET /api/activity/stream` requires `X-API-Key`; accepts `replay` (integer, default 0) and `once` (boolean, default `false`). Returns `text/event-stream`: each event has an `id`, type `activity`, and JSON `data`; `replay` requests prior events and `once=true` ends after them, otherwise it polls every 0.5 seconds. Responses: 200; 401 for failed authentication.
### `event_generator()` (nested generator in `stream_activity`)
- Emits the requested initial entries and then detects new entries; if the log shrinks below the cursor, resets the cursor to zero.
### `clear_activity(_)`
- `POST /api/activity/clear` requires `X-API-Key`, clears the log, and returns `{"status":"cleared"}`. Responses: 200; 401 for failed authentication.
