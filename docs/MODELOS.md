# Modelos

Los modelos de dominio viven en `dgt_monitor/core/models.py` y no dependen de FastAPI, PyQt6 ni `requests`.

## Incident

Representa un registro DATEX2 de situacion. Incluye identificacion, temporalidad, ubicacion, causa, severidad, trafico, coordenadas y cobertura de camaras. Conserva los campos utilizados por la GUI de referencia y anade etiquetas traducidas para las presentaciones.

Los campos técnicos se nombran en inglés y conservan el valor original de DGT. Las salidas de aplicación/API añaden equivalentes `*_label` localizados, por ejemplo `severity_label`, `type_label`, `cause_label`, `direction_label`, `lane_usage_label` o `information_status_label`.

## Camera

Representa una camara DGT con carretera, provincia, punto kilometrico, coordenadas y URL de imagen. `distance_km` y `km_delta` son resultados calculados por un caso de uso y no forman parte de la fuente remota.

## Filtros y estadísticas

`IncidentFilters` y `CameraFilters` son valores inmutables que transportan criterios hacia los servicios. `IncidentStats` contiene los seis contadores compartidos por GUI y dashboard.

`IncidentFilters` incluye `province`, `municipality`, `road`, `severity`, `kind`, `camera` y `match_mode`. `camera` acepta `with`/`without` para filtrar por cobertura visual y `match_mode` controla las busquedas textuales con `contains`, `exact` o `regex`.

`CameraFilters` incluye `province`, `road`, `kilometer`, `latitude`, `longitude`, `limit`, `max_km_delta`, `max_distance_km`, `incident_coverage` y `match_mode`. `max_km_delta` usa por defecto `CAMERA_MATCH_RANGE_KM = 2.0`; `incident_coverage` activa el filtro inverso de camaras que cubren incidencias activas.

Los filtros son el contrato comun entre FastAPI, dashboard web y GUI PyQt6: las capas de presentacion solo construyen estos valores y la fachada aplica las reglas de filtrado.

La funcion `matches_text(value, needle, mode)` centraliza la semantica textual. Un regex invalido devuelve `False` para el campo evaluado y no propaga una excepcion a API/dashboard.

## Serialización

Los modelos de salida implementan `to_dict()`. Este método es el contrato explícito con FastAPI y evita que el dominio dependa de Pydantic o de detalles de la interfaz.