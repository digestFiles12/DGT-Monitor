# dgt_monitor/api/routes/activity.py
Expone operaciones protegidas para consultar, exportar, transmitir y borrar el registro de actividad.
## Dependencias
Usa el módulo de registro `core.activity`, autenticación por encabezado y utilidades estándar para asyncio, JSON, entorno y CSV manual. El router se registra en `api.factory.create_app`.
## Contenido
### `_split_env(env_var)`
- Divide una variable de entorno separada por comas, quita espacios y descarta entradas vacías.
### `_require_api_key(x_api_key=None)`
- Exige `X-API-Key`; rechaza primero claves revocadas y luego compara en tiempo constante con la clave heredada o la lista permitida. Los fallos producen 401.
### `list_activity(_, level=None, source=None, event_type=None, user=None, start_ts=None, end_ts=None, offset=0, limit=100)`
- `GET /api/activity/` requiere `X-API-Key`. Acepta `level`, `source`, `event_type`, `user`, `start_ts`, `end_ts`, `offset` (0) y `limit` (100); filtra exactamente por los cuatro primeros, pero `start_ts` y `end_ts` están declarados y no se aplican. Devuelve `{"total": int, "offset": int, "limit": int, "entries": [...]}`; si `limit` está fuera de 1–1000 se reemplaza por 100. Respuestas: 200; 401 si falta o no es válida la clave; 422 si un parámetro no se puede convertir a su tipo declarado.
### `export_csv(_)`
- `GET /api/activity/csv` requiere `X-API-Key` y entrega el registro completo como CSV (`timestamp,level,source,event_type,user,message`) con descarga `activity.csv` y tipo `text/csv; charset=utf-8`. Respuestas: 200; 401 por autenticación fallida.
### `stream_activity(_, replay=0, once=False)`
- `GET /api/activity/stream` requiere `X-API-Key`; consulta `replay` (entero, predeterminado 0) y `once` (booleano, predeterminado `false`). Responde con `text/event-stream`: cada evento contiene `id`, tipo `activity` y JSON en `data`; `replay` solicita eventos previos y `once=true` termina después de ellos, si no sigue sondeando cada 0,5 s. Respuestas: 200; 401 por autenticación fallida.
### `event_generator()` (generador interno de `stream_activity`)
- Emite las entradas iniciales solicitadas y luego detecta entradas nuevas; si el registro se acorta por debajo del cursor, reinicia el cursor a cero.
### `clear_activity(_)`
- `POST /api/activity/clear`; requiere `X-API-Key`, vacía el registro y devuelve `{"status":"cleared"}`. Respuestas: 200; 401 por autenticación fallida.
