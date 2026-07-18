# Despliegue

## Estado

El wrapper ASGI `dashboard.app:app` está implementado con frontend PWA, manifest y service worker incluidos.

## Render

```yaml
services:
  - type: web
    name: dgt-monitor
    runtime: python
    plan: free
    buildCommand: pip install -e ".[web]"
    startCommand: python -m uvicorn dashboard.app:app --host 0.0.0.0 --port $PORT
```

Antes de publicar se debe verificar `/` (HTML), `/api/health`, REST, WebSocket seguro `wss`, `/manifest.webmanifest`, `/sw.js` e iconos en `/static/icons/`. El intervalo WebSocket predeterminado es 120 segundos para reducir carga en Render.

## Desarrollo local

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --host 127.0.0.1 --port 8000
```