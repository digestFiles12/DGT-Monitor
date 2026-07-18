# API HTTP y WebSocket

La aplicación se construye con `dgt_monitor.api.factory.create_app()`. En producción, `dashboard/app.py` mantiene el punto ASGI `dashboard.app:app`.

## Endpoints

- `GET /`: dashboard web responsive.
- `GET /manifest.webmanifest`: manifiesto PWA.
- `GET /sw.js`: service worker del dashboard.
- `GET /static/*`: assets web versionados por el service worker.
- `GET /api/health`: estado y hora UTC.
- `GET /api/incidents`: filtros `province`, `municipality`, `road`, `severity` y `kind`.
- `GET /api/cameras`: filtros de provincia, carretera, km, coordenadas, límite y distancia kilométrica máxima.
- `GET /api/activity/`: log de actividad paginado; requiere `X-API-Key`.
- `GET /api/activity/stream`: stream SSE de actividad; soporta `replay` y `once=true`.
- `GET /api/activity/export`: export CSV de actividad; requiere `X-API-Key`.
- `POST /api/activity/clear`: limpia el log de actividad; requiere `X-API-Key`.
- `WS /ws/incidents`: entrega inmediata y refresco periódico; intervalo predeterminado de 120 segundos.

Las rutas no descargan ni parsean XML. Obtienen `DgtApplicationService` desde `app.state`, lo que permite sustituir toda la aplicación por un doble en pruebas.

Los errores `DgtError` se traducen a HTTP 502. El WebSocket envía un objeto con `error` sin cerrar la conexión por un fallo transitorio de DGT.

## Autenticacion de Activity API

Los endpoints de actividad usan cabecera `X-API-Key`. Las claves aceptadas se configuran con `ACTIVITY_API_KEYS`; las revocadas con `ACTIVITY_REVOKED_API_KEYS`. La comparación de claves aceptadas usa `secrets.compare_digest()`.

## Dashboard web

El dashboard consume los endpoints REST desde el mismo origen y no contiene lógica de dominio. Incluye vistas de incidencias y cámaras, filtros por ubicación y carretera, estados de carga/error, actualización automática cada 120 segundos y carga progresiva de incidencias. Puede instalarse como PWA y conserva el shell estático en caché; las respuestas de `/api/` nunca se cachean.

## Desarrollo

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --reload
```