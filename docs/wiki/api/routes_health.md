# dgt_monitor/api/routes/health.py
**ES:** Ofrece una comprobación sencilla de disponibilidad con la hora UTC actual.
**EN:** Provides a simple availability check with the current UTC time.
## Dependencies / Dependencias
Usa `datetime`/`timezone` de la biblioteca estándar y `APIRouter` de FastAPI; el router se registra en `api.factory.create_app`.
## Contents / Contenido
### `health()`
- **ES:** `GET /api/health`, sin parámetros de consulta, devuelve `{"status":"ok","time":"<ISO-8601 UTC>"}`. Respuesta normal: 200.
- **EN:** `GET /api/health`, with no query parameters, returns `{"status":"ok","time":"<ISO-8601 UTC>"}`. Normal response: 200.
