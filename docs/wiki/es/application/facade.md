# dgt_monitor/application/facade.py
Expone una fachada única para que los adaptadores (API y GUI) soliciten incidentes localizados, estadísticas, agrupaciones y cámaras sin conocer los servicios internos.
## Dependencias
Compone `IncidentService` y `CameraService`, usa modelos de filtros y utilidades de localización, y delega cálculos de estadísticas al módulo `application.statistics`. La fábrica API construye/consume esta fachada y las rutas la consultan a través de ella.
## Contenido
### `DgtApplicationService`
- Fachada que combina los servicios de incidentes y cámaras y prepara respuestas para los adaptadores.
### `DgtApplicationService.__init__(incidents, cameras)`
- Guarda los servicios de incidentes y cámaras que atenderán las operaciones de la fachada.
### `DgtApplicationService.get_incident_payload(filters=None, refresh=False, language="es")`
- Carga incidentes y cámaras, anota cobertura, devuelve los incidentes filtrados y estadísticas calculadas con los filtros excepto `kind`. Incluye hora UTC, cantidad, idioma normalizado y etiquetas traducidas.
### `DgtApplicationService._localized_incident(item, translator)`
- Copia un diccionario de incidente y añade etiquetas traducidas para los campos enumerados; `cause` usa traducción compuesta y los demás usan traducción simple.
### `DgtApplicationService._filters_without_kind(filters)`
- Construye un nuevo filtro conservando provincia, municipio, carretera, severidad, cámara y modo de coincidencia, pero omite `kind`; así el recuento estadístico no depende de la categoría seleccionada.
### `DgtApplicationService.get_statistics(level="province", refresh=False)`
- Devuelve los cuatro indicadores agrupados por provincia o región, incluidos máximos y mínimos; rechaza niveles distintos mediante la función delegada.
### `DgtApplicationService.get_grouped_incidents(refresh=False)`
- Devuelve la estructura completa de agrupación de incidentes por geografía, tipo y día de semana, más `labels.by_type` con la etiqueta de cada tipo en español e inglés (las claves del JSON siguen siendo los códigos DATEX II).
### `DgtApplicationService.get_cameras(filters=None, refresh=False)`
- Filtra cámaras y devuelve hora UTC, cantidad y elementos. Si se pide cobertura de incidentes, difiere el límite hasta después de esa selección y luego lo aplica.
