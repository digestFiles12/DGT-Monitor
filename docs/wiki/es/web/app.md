# dgt_monitor/web/app.py
Es el punto de entrada ASGI estable que crea la aplicación FastAPI para Render y el desarrollo local.
## Dependencias
Importa `create_app` de la fábrica API y lo invoca al importar el módulo. El servidor ASGI consume la variable global `app`.
## Contenido
### `app`
- Instancia FastAPI creada por `create_app()` al cargar el módulo; no es una función definida aquí y no contiene lógica adicional.
## Ejemplo
Un servidor ASGI puede apuntar a `dgt_monitor.web.app:app`.
