# dgt_monitor/api/factory.py
Ensambla la aplicación FastAPI: registra rutas, estado de servicio, CORS, archivos estáticos y manejo de errores.
## Dependencias
Importa todos los routers, `DgtApplicationService`, `build_application`, `DgtError` y componentes de FastAPI/Starlette. El módulo de entrada web invoca `create_app`.
## Contenido
### `create_app(service=None)`
- Crea la aplicación titulada `DGT Monitor API`, guarda el servicio inyectado o uno construido por `build_application`, configura CORS para cualquier origen/método/cabecera sin credenciales y registra los routers y estáticos. Define también las rutas raíz y el manejador de errores descritos debajo.
### `handle_dgt_error(_request, exc)` (handler interno)
- Convierte cualquier `DgtError` atendido por la aplicación en HTTP 502 con JSON `{"detail": "<mensaje>"}`.
### `dashboard()` (endpoint interno)
- `GET /` devuelve `web/static/index.html` como archivo; no aparece en OpenAPI. Respuesta normal: archivo (200); no declara parámetros de consulta.
### `manifest()` (endpoint interno)
- `GET /manifest.webmanifest` sirve el manifiesto con tipo `application/manifest+json` (200; sin parámetros de consulta; archivo de respuesta).
### `service_worker()` (endpoint interno)
- `GET /sw.js` sirve el service worker con tipo `application/javascript` (200; sin parámetros de consulta; archivo de respuesta).
