# dgt_monitor/api/factory.py
Assembles the FastAPI application: registers routes, service state, CORS, static files, and error handling.
## Dependencies
Imports all routers, `DgtApplicationService`, `build_application`, `DgtError`, and FastAPI/Starlette components. The web entry module calls `create_app`.
## Contents
### `create_app(service=None)`
- Creates the `DGT Monitor API` application, stores the injected service or one built by `build_application`, configures CORS for any origin/method/header without credentials, and registers routers and static files. It also defines the root routes and error handler below.
### `handle_dgt_error(_request, exc)` (internal handler)
- Converts any `DgtError` handled by the application into HTTP 502 with JSON `{"detail": "<message>"}`.
### `dashboard()` (internal endpoint)
- `GET /` returns `web/static/index.html` as a file; it is omitted from OpenAPI. Normal response: file (200); it declares no query parameters.
### `manifest()` (internal endpoint)
- `GET /manifest.webmanifest` serves the manifest as `application/manifest+json` (200; no query parameters; file response).
### `service_worker()` (internal endpoint)
- `GET /sw.js` serves the service worker as `application/javascript` (200; no query parameters; file response).
