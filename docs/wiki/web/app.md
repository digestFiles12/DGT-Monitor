# dgt_monitor/web/app.py
**ES:** Es el punto de entrada ASGI estable que crea la aplicación FastAPI para Render y el desarrollo local.
**EN:** This is the stable ASGI entry point that creates the FastAPI application for Render and local development.
## Dependencies / Dependencias
Importa `create_app` de la fábrica API y lo invoca al importar el módulo. El servidor ASGI consume la variable global `app`.
## Contents / Contenido
### `app`
- **ES:** Instancia FastAPI creada por `create_app()` al cargar el módulo; no es una función definida aquí y no contiene lógica adicional.
- **EN:** FastAPI instance created by `create_app()` when the module loads; it is not a function defined here and contains no additional logic.
## Example / Ejemplo
Un servidor ASGI puede apuntar a `dgt_monitor.web.app:app`.
