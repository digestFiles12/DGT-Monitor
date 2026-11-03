# dgt_monitor/api/factory.py
**ES:** Ensambla la aplicación FastAPI: registra rutas, estado de servicio, CORS, archivos estáticos y manejo de errores.
**EN:** Assembles the FastAPI application: registers routes, service state, CORS, static files, and error handling.
## Dependencies / Dependencias
Importa todos los routers, `DgtApplicationService`, `build_application`, `DgtError` y componentes de FastAPI/Starlette. El módulo de entrada web invoca `create_app`.
## Contents / Contenido
### `create_app(service=None)`
- **ES:** Crea la aplicación titulada `DGT Monitor API`, guarda el servicio inyectado o uno construido por `build_application`, configura CORS para cualquier origen/método/cabecera sin credenciales y registra los routers y estáticos. Define también las rutas raíz y el manejador de errores descritos debajo.
- **EN:** Creates the `DGT Monitor API` application, stores the injected service or one built by `build_application`, configures CORS for any origin/method/header without credentials, and registers routers and static files. It also defines the root routes and error handler below.
### `handle_dgt_error(_request, exc)` (handler interno)
- **ES:** Convierte cualquier `DgtError` atendido por la aplicación en HTTP 502 con JSON `{"detail": "<mensaje>"}`.
- **EN:** Converts any `DgtError` handled by the application into HTTP 502 with JSON `{"detail": "<message>"}`.
### `dashboard()` (endpoint interno)
- **ES:** `GET /` devuelve `web/static/index.html` como archivo; no aparece en OpenAPI. Respuesta normal: archivo (200); no declara parámetros de consulta.
- **EN:** `GET /` returns `web/static/index.html` as a file; it is omitted from OpenAPI. Normal response: file (200); it declares no query parameters.
### `manifest()` (endpoint interno)
- **ES:** `GET /manifest.webmanifest` sirve el manifiesto con tipo `application/manifest+json` (200; sin parámetros de consulta; archivo de respuesta).
- **EN:** `GET /manifest.webmanifest` serves the manifest as `application/manifest+json` (200; no query parameters; file response).
### `service_worker()` (endpoint interno)
- **ES:** `GET /sw.js` sirve el service worker con tipo `application/javascript` (200; sin parámetros de consulta; archivo de respuesta).
- **EN:** `GET /sw.js` serves the service worker as `application/javascript` (200; no query parameters; file response).
