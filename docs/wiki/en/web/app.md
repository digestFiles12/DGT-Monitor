# dgt_monitor/web/app.py
This is the stable ASGI entry point that creates the FastAPI application for Render and local development.
## Dependencies
Imports `create_app` from the API factory and calls it when the module is imported. The ASGI server uses the global `app` variable.
## Contents
### `app`
- FastAPI instance created by `create_app()` when the module loads; it is not a function defined here and contains no additional logic.
## Example
An ASGI server can target `dgt_monitor.web.app:app`.
