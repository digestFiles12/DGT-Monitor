# API HTTP y WebSocket

La aplicación se construye con `dgt_monitor.api.factory.create_app()`. En producción, `dashboard/app.py` mantiene el punto ASGI `dashboard.app:app`.

## Endpoints

- `GET /`: dashboard web responsive.
- `GET /manifest.webmanifest`: manifiesto PWA.
- `GET /sw.js`: service worker del dashboard.
- `GET /static/*`: assets web versionados por el service worker.
- `GET /api/health`: estado y hora UTC.
- `GET /api/incidents`: filtros `province`, `municipality`, `road`, `severity`, `kind`, `camera` (`with`/`without`) y `lang` (`es`/`en`).
- `GET /api/cameras`: filtros de provincia, carretera, km, coordenadas, límite y distancia kilométrica máxima.
- `GET /api/activity/`: log de actividad paginado; requiere `X-API-Key`.
- `GET /api/activity/stream`: stream SSE de actividad; soporta `replay` y `once=true`.
- `GET /api/activity/export`: export CSV de actividad; requiere `X-API-Key`.
- `POST /api/activity/clear`: limpia el log de actividad; requiere `X-API-Key`.
- `WS /ws/incidents`: entrega inmediata y refresco periódico; intervalo predeterminado de 120 segundos. Acepta los mismos filtros y `lang` que REST.

Las rutas no descargan ni parsean XML. Obtienen `DgtApplicationService` desde `app.state`, lo que permite sustituir toda la aplicación por un doble en pruebas.

Los errores `DgtError` se traducen a HTTP 502. El WebSocket envía un objeto con `error` sin cerrar la conexión por un fallo transitorio de DGT.

## Localizacion

Los valores DATEX2 se conservan en campos técnicos en inglés (`type`, `cause`, `severity`, etc.) y la fachada añade campos de presentación `*_label` según `lang`. El idioma por defecto es español (`es`) y también se soporta inglés (`en`). Si DGT introduce un código nuevo sin traducción explícita, el traductor lo humaniza para evitar mostrar camelCase o códigos internos en las interfaces.

## Autenticacion de Activity API

Los endpoints de actividad usan cabecera `X-API-Key`. Las claves aceptadas se configuran con `ACTIVITY_API_KEYS`; las revocadas con `ACTIVITY_REVOKED_API_KEYS`. La comparación de claves aceptadas usa `secrets.compare_digest()`.

## Dashboard web

El dashboard consume los endpoints REST desde el mismo origen y no contiene lógica de dominio. Incluye vistas de incidencias y cámaras, selector superior de idioma ES/EN, filtros por provincia, municipio, carretera, severidad y cobertura de cámara, celdas estadísticas clicables por tipo, filas de incidencia desplegables con todos sus detalles disponibles, estados de carga/error, actualización automática cada 120 segundos, carga progresiva de incidencias, modo claro/oscuro persistente en `localStorage` y visor modal de imágenes de cámaras. Los textos de incidencias usan campos `*_label` localizados, no códigos DATEX2. En la tabla de incidencias, el botón de cámaras cercanas consulta `/api/cameras`; si solo hay una cámara abre directamente su imagen en tamaño contenido y, si hay varias, muestra un desplegable para elegir destino. Al pulsar la imagen del visor, se expande a pantalla completa. Puede instalarse como PWA y conserva el shell estático en caché; las respuestas de `/api/` nunca se cachean.

## Desarrollo

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --reload
```