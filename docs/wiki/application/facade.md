# dgt_monitor/application/facade.py
**ES:** Expone una fachada única para que los adaptadores (API y GUI) soliciten incidentes localizados, estadísticas, agrupaciones y cámaras sin conocer los servicios internos.
**EN:** Provides a single facade for adapters (API and GUI) to request localized incidents, statistics, groupings, and cameras without knowing the internal services.
## Dependencies / Dependencias
Compone `IncidentService` y `CameraService`, usa modelos de filtros y utilidades de localización, y delega cálculos de estadísticas al módulo `application.statistics`. La fábrica API construye/consume esta fachada y las rutas la consultan a través de ella.
## Contents / Contenido
### `DgtApplicationService`
- **ES:** Fachada que combina los servicios de incidentes y cámaras y prepara respuestas para los adaptadores.
- **EN:** Facade that combines incident and camera services and prepares responses for adapters.
### `DgtApplicationService.__init__(incidents, cameras)`
- **ES:** Guarda los servicios de incidentes y cámaras que atenderán las operaciones de la fachada.
- **EN:** Stores the incident and camera services that handle facade operations.
### `DgtApplicationService.get_incident_payload(filters=None, refresh=False, language="es")`
- **ES:** Carga incidentes y cámaras, anota cobertura, devuelve los incidentes filtrados y estadísticas calculadas con los filtros excepto `kind`. Incluye hora UTC, cantidad, idioma normalizado y etiquetas traducidas.
- **EN:** Loads incidents and cameras, annotates coverage, returns filtered incidents and statistics computed with all filters except `kind`. Includes UTC time, count, normalized language, and translated labels.
### `DgtApplicationService._localized_incident(item, translator)`
- **ES:** Copia un diccionario de incidente y añade etiquetas traducidas para los campos enumerados; `cause` usa traducción compuesta y los demás usan traducción simple.
- **EN:** Copies an incident dictionary and adds translated labels for the listed fields; `cause` uses compound translation and the others use simple translation.
### `DgtApplicationService._filters_without_kind(filters)`
- **ES:** Construye un nuevo filtro conservando provincia, municipio, carretera, severidad, cámara y modo de coincidencia, pero omite `kind`; así el recuento estadístico no depende de la categoría seleccionada.
- **EN:** Builds a new filter preserving province, municipality, road, severity, camera, and match mode while omitting `kind`; therefore the statistics count does not depend on the selected category.
### `DgtApplicationService.get_statistics(level="province", refresh=False)`
- **ES:** Devuelve los cuatro indicadores agrupados por provincia o región, incluidos máximos y mínimos; rechaza niveles distintos mediante la función delegada.
- **EN:** Returns the four indicators grouped by province or region, including maxima and minima; other levels are rejected by the delegated function.
### `DgtApplicationService.get_grouped_incidents(refresh=False)`
- **ES:** Devuelve la estructura completa de agrupación de incidentes por geografía, tipo y día de semana.
- **EN:** Returns the full incident grouping structure by geography, type, and weekday.
### `DgtApplicationService.get_cameras(filters=None, refresh=False)`
- **ES:** Filtra cámaras y devuelve hora UTC, cantidad y elementos. Si se pide cobertura de incidentes, difiere el límite hasta después de esa selección y luego lo aplica.
- **EN:** Filters cameras and returns UTC time, count, and items. When incident coverage is requested, it postpones the limit until after coverage selection and then applies it.
