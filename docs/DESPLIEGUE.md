# Despliegue

## Estado

El wrapper ASGI `dashboard.app:app` está implementado. Aún faltan frontend/PWA, `render.yaml` y archivos de requisitos de despliegue.

## Render previsto

```yaml
services:
  - type: web
    name: dgt-monitor
    runtime: python
    plan: free
    buildCommand: pip install -e ".[web]"
    startCommand: python -m uvicorn dashboard.app:app --host 0.0.0.0 --port $PORT
```

Antes de publicar se debe verificar `/api/health`, REST, WebSocket seguro `wss`, manifest, service worker e iconos. El intervalo WebSocket predeterminado es 120 segundos para reducir carga en Render.

## Desarrollo local

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --host 127.0.0.1 --port 8000
```