# Migración desde DGT30_GUI

## Referencia

El comportamiento se consulta en una copia local del proyecto legado, especialmente:

- `DGT_V2.py`: GUI completa, cámaras y diálogos no modales.
- `dashboard/app.py`: API anterior, caché y cobertura.
- `dashboard/static/`: dashboard/PWA que debe preservarse visualmente.
- `test/test_dashboard_app.py`: contratos anteriores de API y WebSocket.
- `render.yaml`: configuración de despliegue anterior.

## Mapeo actual

| Legacy | Nuevo |
|---|---|
| `traducir` | `core.localization.Translator.translate` |
| `limpiar_texto` | `core.text.TextCleaner.clean` |
| `DataFetchThread.parse_all` | `infrastructure.parsers.IncidentParser.parse` |
| `CameraFetchThread.parse_cameras` | `infrastructure.parsers.CameraParser.parse` |
| filtros y estadísticas | `application.IncidentService` |
| Haversine y cámaras cercanas | `application.CameraService` |
| cachés globales | `infrastructure.TtlCache` |
| `dashboard/app.py` monolítico | `api.factory` + rutas + wrapper |

## Compatibilidad pendiente

- Crear wrappers `DGT.py` y `DGT_V2.py` sobre `gui.entrypoints`.
- Preservar filtros, estadísticas, selección, detalles y log de la GUI.
- Preservar búsqueda, orden, visualización de cámaras y mapas.
- Mantener diálogos no modales con referencias vivas.
- Preservar rutas PWA y frontend responsive.

No debe copiarse lógica de red, parsing, filtros, distancia o caché a GUI/API.