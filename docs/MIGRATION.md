# Migración desde DGT30_GUI

## Referencia funcional

La migración conserva comportamientos esperados de la aplicación anterior: GUI de escritorio, cámaras cercanas, diálogos no modales, dashboard/PWA, API, WebSocket y despliegue Render. No se conserva ninguna dependencia directa con rutas privadas ni con código monolítico.

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
| `src/dgt_monitor/web/app.py` monolítico | `api.factory` + rutas + wrapper |

## Compatibilidad pendiente

- Crear wrappers `DGT.py` y `DGT_V2.py` sobre `gui.entrypoints`.
- Añadir temporizador configurable y log visible de actividad en la GUI.
- Completar paridad final de búsqueda/orden avanzado si se requiere.

## Compatibilidad ya implementada

- Filtros, estadisticas, seleccion y detalle de incidencias en GUI.
- Diálogo no modal de cámaras cercanas con referencias vivas.
- Carga asincrona de miniaturas de cámaras.
- Rutas PWA y frontend responsive servidos desde `/`.
- Dashboard con busqueda contiene/exacta/regex, filtro de camaras con incidencia, mapa sincronizado y scroll general/interno.
- Cobertura incidencia-camara centralizada en servicios con rango de 2.0 km por punto kilometrico.

No debe copiarse lógica de red, parsing, filtros, distancia o caché a GUI/API.