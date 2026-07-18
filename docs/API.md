# API HTTP y WebSocket

La aplicación se construye con `dgt_monitor.api.factory.create_app()`. En producción, `dashboard/app.py` mantiene el punto ASGI `dashboard.app:app`.

## Endpoints

- `GET /`: dashboard PWA (HTML).
- `GET /manifest.webmanifest`: manifiesto PWA.
- `GET /sw.js`: service worker.
- `GET /static/*`: assets estáticos del dashboard (CSS, JS, iconos).
- `GET /api/health`: estado y hora UTC.
- `GET /api/incidents`: filtros `province`, `municipality`, `road`, `severity` y `kind`.
- `GET /api/cameras`: filtros de provincia, carretera, km, coordenadas, límite y distancia kilométrica máxima.
- `WS /ws/incidents`: entrega inmediata y refresco periódico; intervalo predeterminado de 120 segundos.

Las rutas no descargan ni parsean XML. Obtienen `DgtApplicationService` desde `app.state`, lo que permite sustituir toda la aplicación por un doble en pruebas.

Los errores `DgtError` se traducen a HTTP 502. El WebSocket envía un objeto con `error` sin cerrar la conexión por un fallo transitorio de DGT.

## Desarrollo

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --reload
```