# dgt_monitor/api/routes/health.py
Ofrece una comprobación sencilla de disponibilidad con la hora UTC actual.
## Dependencias
Usa `datetime`/`timezone` de la biblioteca estándar y `APIRouter` de FastAPI; el router se registra en `api.factory.create_app`.
## Contenido
### `health()`
- `GET /api/health`, sin parámetros de consulta, devuelve `{"status":"ok","time":"<ISO-8601 UTC>"}`. Respuesta normal: 200.
