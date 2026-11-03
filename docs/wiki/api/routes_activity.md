# dgt_monitor/api/routes/activity.py
**ES:** Expone operaciones protegidas para consultar, exportar, transmitir y borrar el registro de actividad.
**EN:** Exposes protected operations to query, export, stream, and clear the activity log.
## Dependencies / Dependencias
Usa el módulo de registro `core.activity`, autenticación por encabezado y utilidades estándar para asyncio, JSON, entorno y CSV manual. El router se registra en `api.factory.create_app`.
## Contents / Contenido
### `_split_env(env_var)`
- **ES:** Divide una variable de entorno separada por comas, quita espacios y descarta entradas vacías.
- **EN:** Splits a comma-separated environment variable, trims whitespace, and drops empty entries.
### `_require_api_key(x_api_key=None)`
- **ES:** Exige `X-API-Key`; rechaza primero claves revocadas y luego compara en tiempo constante con la clave heredada o la lista permitida. Los fallos producen 401.
- **EN:** Requires `X-API-Key`; rejects revoked keys first, then constant-time compares against the legacy key or allow-list. Failures produce 401.
### `list_activity(_, level=None, source=None, event_type=None, user=None, start_ts=None, end_ts=None, offset=0, limit=100)`
- **ES:** `GET /api/activity/` requiere `X-API-Key`. Acepta `level`, `source`, `event_type`, `user`, `start_ts`, `end_ts`, `offset` (0) y `limit` (100); filtra exactamente por los cuatro primeros, pero `start_ts` y `end_ts` están declarados y no se aplican. Devuelve `{"total": int, "offset": int, "limit": int, "entries": [...]}`; si `limit` está fuera de 1–1000 se reemplaza por 100. Respuestas: 200; 401 si falta o no es válida la clave; 422 si un parámetro no se puede convertir a su tipo declarado.
- **EN:** `GET /api/activity/` requires `X-API-Key`. Accepts `level`, `source`, `event_type`, `user`, `start_ts`, `end_ts`, `offset` (0), and `limit` (100); exact-filters by the first four, but `start_ts` and `end_ts` are declared and not applied. Returns `{"total": int, "offset": int, "limit": int, "entries": [...]}`; a limit outside 1–1000 is replaced with 100. Responses: 200; 401 for a missing or invalid key; 422 if a parameter cannot be converted to its declared type.
### `export_csv(_)`
- **ES:** `GET /api/activity/csv` requiere `X-API-Key` y entrega el registro completo como CSV (`timestamp,level,source,event_type,user,message`) con descarga `activity.csv` y tipo `text/csv; charset=utf-8`. Respuestas: 200; 401 por autenticación fallida.
- **EN:** `GET /api/activity/csv` requires `X-API-Key` and returns the full log as CSV (`timestamp,level,source,event_type,user,message`) with download name `activity.csv` and media type `text/csv; charset=utf-8`. Responses: 200; 401 for failed authentication.
### `stream_activity(_, replay=0, once=False)`
- **ES:** `GET /api/activity/stream` requiere `X-API-Key`; consulta `replay` (entero, predeterminado 0) y `once` (booleano, predeterminado `false`). Responde con `text/event-stream`: cada evento contiene `id`, tipo `activity` y JSON en `data`; `replay` solicita eventos previos y `once=true` termina después de ellos, si no sigue sondeando cada 0,5 s. Respuestas: 200; 401 por autenticación fallida.
- **EN:** `GET /api/activity/stream` requires `X-API-Key`; accepts `replay` (integer, default 0) and `once` (boolean, default `false`). Returns `text/event-stream`: each event has an `id`, type `activity`, and JSON `data`; `replay` requests prior events and `once=true` ends after them, otherwise it polls every 0.5 seconds. Responses: 200; 401 for failed authentication.
### `event_generator()` (generador interno de `stream_activity`)
- **ES:** Emite las entradas iniciales solicitadas y luego detecta entradas nuevas; si el registro se acorta por debajo del cursor, reinicia el cursor a cero.
- **EN:** Emits the requested initial entries and then detects new entries; if the log shrinks below the cursor, resets the cursor to zero.
### `clear_activity(_)`
- **ES:** `POST /api/activity/clear`; requiere `X-API-Key`, vacía el registro y devuelve `{"status":"cleared"}`. Respuestas: 200; 401 por autenticación fallida.
- **EN:** `POST /api/activity/clear` requires `X-API-Key`, clears the log, and returns `{"status":"cleared"}`. Responses: 200; 401 for failed authentication.
