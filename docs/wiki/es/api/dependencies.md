# dgt_monitor/api/dependencies.py
Proporciona la dependencia FastAPI que obtiene el servicio de aplicación almacenado en el estado de la petición.
## Dependencias
Importa `Request` y `DgtApplicationService`. Las rutas de API que necesitan lógica de aplicación lo usan con `Depends`.
## Contenido
### `get_service(request)`
- Devuelve `request.app.state.dgt_service`, configurado normalmente por `create_app`; si esa propiedad no existe, el acceso falla en tiempo de ejecución.
