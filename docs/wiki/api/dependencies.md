# dgt_monitor/api/dependencies.py
**ES:** Proporciona la dependencia FastAPI que obtiene el servicio de aplicación almacenado en el estado de la petición.
**EN:** Provides the FastAPI dependency that retrieves the application service stored on the request state.
## Dependencies / Dependencias
Importa `Request` y `DgtApplicationService`. Las rutas de API que necesitan lógica de aplicación lo usan con `Depends`.
## Contents / Contenido
### `get_service(request)`
- **ES:** Devuelve `request.app.state.dgt_service`, configurado normalmente por `create_app`; si esa propiedad no existe, el acceso falla en tiempo de ejecución.
- **EN:** Returns `request.app.state.dgt_service`, normally set by `create_app`; if the attribute is absent, access fails at runtime.
