# Servicios

Los casos de uso de aplicación coordinan repositorios, cachés, persistencia y modelos. La fachada `DgtApplicationService` es el punto común de entrada para API y GUI.

## Incidencias

`IncidentService.get_all()` obtiene incidencias del repositorio a través de `TtlCache`. Una actualización explícita invalida la clave antes de volver a cargar. Si hay un almacén configurado, intenta guardar cada carga; un error de persistencia se registra y no impide devolver los datos obtenidos. `filter()` aplica `IncidentFilters`, y `stats()` calcula los seis contadores de `IncidentStats`.

## Cámaras

`CameraService` carga y filtra cámaras por provincia, carretera, punto kilométrico y, si se proporcionan coordenadas, distancia geográfica. Las coincidencias de carretera y provincia usan el modo textual del filtro. `annotate_coverage()` vincula cámaras e incidencias mediante carretera normalizada, provincia compatible y una diferencia de hasta `CAMERA_MATCH_RANGE_KM` (2 km por defecto). `with_incident_coverage()` aplica el mismo criterio para seleccionar cámaras que cubren incidencias activas.

## Fachada y estadísticas

`DgtApplicationService.get_incident_payload()` calcula cobertura, filtra incidencias y prepara etiquetas localizadas. `get_cameras()` devuelve cámaras filtradas; cuando se solicita cobertura de incidencias, aplica el límite de resultados después de seleccionar la cobertura. `get_statistics()` devuelve cuatro indicadores por provincia o comunidad autónoma, con máximo y mínimo. `get_grouped_incidents()` genera agrupaciones por provincia, comunidad autónoma, tipo y día de la semana.

Las rutas `GET /api/stats` y `GET /api/stats/grouped` exponen esos resultados. El módulo `application.statistics` define total, incidencias graves, obras y cierres de carretera; determina el día desde la hora de inicio (o, si falta, la hora de creación) y escribe JSON agrupado en UTF-8. Consulta [DATEX II](datex2.md) para el origen y análisis de los datos.

## Caché y persistencia

`TtlCache` es una caché en memoria segura para uso concurrente que devuelve copias profundas. La composición de producción establece TTL de 120 segundos para incidencias y 300 para cámaras. `SqliteIncidentStore` guarda las incidencias por `id` con inserción o actualización; su ruta se configura con `INCIDENT_DB_PATH` y, si no está definida, usa `data/incidents.db`.

## Menú de consola

`dgt_monitor.menu` puede generar un JSON agrupado desde un XML local o descargado, o reutilizar un JSON existente. Después permite explorar indicadores con gráficas de barras o circulares y muestra sus máximos y mínimos. El dashboard web presenta sus gráficas en la pestaña correspondiente.
