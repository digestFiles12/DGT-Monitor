# Modelos

Los modelos de dominio viven en `dgt_monitor/core/models.py` y no dependen de FastAPI, PyQt6 ni `requests`.

## Incident

Representa un registro DATEX2 de situación. Incluye identificación, temporalidad, ubicación, causa, severidad, tráfico, coordenadas y cobertura de cámaras. Conserva los campos utilizados por la GUI de referencia y añade etiquetas traducidas para las presentaciones.

Los campos técnicos se nombran en inglés y conservan el valor original de DGT. Las salidas de aplicación/API añaden equivalentes `*_label` localizados, por ejemplo `severity_label`, `type_label`, `cause_label`, `direction_label`, `lane_usage_label` o `information_status_label`.

## Camera

Representa una cámara DGT con carretera, provincia, punto kilométrico, coordenadas y URL de imagen. `distance_km` y `km_delta` son resultados calculados por un caso de uso y no forman parte de la fuente remota.

## Filtros y estadísticas

`IncidentFilters` y `CameraFilters` son valores inmutables que transportan criterios hacia los servicios. `IncidentStats` contiene los seis contadores compartidos por GUI y dashboard.

Los filtros son el contrato comun entre FastAPI, dashboard web y GUI PyQt6: las capas de presentacion solo construyen estos valores y la fachada aplica las reglas de filtrado.

## Serialización

Los modelos de salida implementan `to_dict()`. Este método es el contrato explícito con FastAPI y evita que el dominio dependa de Pydantic o de detalles de la interfaz.