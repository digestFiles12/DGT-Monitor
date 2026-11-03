# Arquitectura

DGT-Monitor separa el dominio, los adaptadores de datos y los casos de uso. La estructura de ejecución está en `src/dgt_monitor/`: `core`, `infrastructure`, `application`, `api`, `web` y `gui`; el menú de consola está en `menu.py`.

## Componentes

- `core/` contiene modelos, puertos, utilidades de dominio, localización y la relación provincia-comunidad autónoma.
- `infrastructure/` implementa el acceso HTTP, los repositorios y parsers DATEX II, la caché en memoria y los almacenes SQLite.
- `application/` coordina los servicios de incidencias y cámaras, la fachada común y los cálculos estadísticos.
- `api/` adapta los casos de uso a FastAPI. `web/` contiene la aplicación ASGI y los recursos estáticos del dashboard.
- `gui/` ofrece la interfaz de escritorio PyQt6; `menu.py` implementa el menú de consola para generar y explorar estadísticas.

El punto de entrada ASGI es `dgt_monitor.web.app:app`. `bootstrap.build_application()` conecta repositorios, parsers, cachés y almacén. La fábrica `create_app(service=...)` permite proporcionar una fachada ya construida, por ejemplo durante las pruebas.

## Flujo de datos

Los repositorios obtienen XML de la DGT y los parsers lo convierten en modelos del dominio. `IncidentService` aplica la caché y persiste las incidencias cuando el almacén está disponible. La fachada entrega datos a la API y a la GUI; `application.statistics` produce agrupaciones y estadísticas que también consume la pestaña de gráficas del dashboard.

La cobertura de cámaras se calcula en la aplicación: se compara carretera normalizada, provincia compatible y distancia por punto kilométrico. No es una relación proporcionada por el XML.

## Diagrama

El [diagrama de arquitectura y flujo](../diagrams.md) documenta las capas, los recorridos de datos y el despliegue; se reutiliza aquí para evitar duplicar su contenido.

Véase también [Modelos](models.md) y [Servicios](services.md).
