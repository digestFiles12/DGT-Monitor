# Modelos

Los modelos de dominio viven en `dgt_monitor/core/models.py` y no dependen de FastAPI, PyQt6 ni `requests`.

## Incident

Representa un registro DATEX2 de situación. Incluye identificación, temporalidad, ubicación, causa, severidad, tráfico, coordenadas y cobertura de cámaras. Conserva los campos utilizados por la GUI de referencia y añade etiquetas traducidas para las presentaciones.

## Camera

Representa una cámara DGT con carretera, provincia, punto kilométrico, coordenadas y URL de imagen. `distance_km` y `km_delta` son resultados calculados por un caso de uso y no forman parte de la fuente remota.

## Filtros y estadísticas

`IncidentFilters` y `CameraFilters` son valores inmutables que transportan criterios hacia los servicios. `IncidentStats` contiene los seis contadores compartidos por GUI y dashboard.

Los filtros son el contrato comun entre FastAPI, dashboard web y GUI PyQt6: las capas de presentacion solo construyen estos valores y la fachada aplica las reglas de filtrado.

## Serialización

Los modelos de salida implementan `to_dict()`. Este método es el contrato explícito con FastAPI y evita que el dominio dependa de Pydantic o de detalles de la interfaz.