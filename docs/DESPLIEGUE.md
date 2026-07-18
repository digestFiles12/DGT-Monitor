# Despliegue

## Estado

El wrapper ASGI `dashboard.app:app`, el dashboard web/PWA, `render.yaml` y GitHub Actions están implementados. Render ejecuta la instalación editable, la suite de tests y `compileall` durante el build.

## Render

```yaml
services:
  - type: web
    name: dgt-monitor
    runtime: python
    plan: free
    buildCommand: pip install -e ".[dev]" && python -m pytest test -q --tb=no && python -m compileall -q dgt_monitor dashboard
    startCommand: python -m uvicorn dashboard.app:app --host 0.0.0.0 --port $PORT
```

Variables de entorno principales: `PYTHON_VERSION=3.12.0`, `PYTHONUNBUFFERED=1`, `ACTIVITY_API_KEYS`, `ACTIVITY_REVOKED_API_KEYS` y `ACTIVITY_DB_PATH`. Las claves de API se configuran en Render como secretos, no en el repositorio.

Antes de publicar se debe verificar `/`, `/api/health`, REST, WebSocket seguro `wss`, manifest y service worker. El intervalo WebSocket predeterminado es 120 segundos para reducir carga en Render.

## Desarrollo local

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --host 127.0.0.1 --port 8000
```