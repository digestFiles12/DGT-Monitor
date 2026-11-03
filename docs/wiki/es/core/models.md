# dgt_monitor/core/models.py
Declara los modelos de datos tipados compartidos por las aplicaciones de escritorio y web. Los modelos de incidente y cámara se pueden convertir a diccionarios; los filtros y estadísticas son inmutables.
## Dependencias
Importa `asdict`, `dataclass` y `Any`; importa `CAMERA_MATCH_RANGE_KM` de [constants](constants.md). Las demás capas usan estos modelos para representar resultados y criterios.
## Contenido
### `Incident`
- Dataclass mutable para una incidencia; incluye identificadores y tiempos, datos de clasificación, localización, condiciones de vía y cobertura de cámaras.
### `Incident` — campos de identificación y tiempo
- `id`, `record_id`, `version`, `creation_time`, `source`, `start_time` y `end_time` describen la situación, su registro y su vigencia.
### `Incident` — clasificación y localización
- `severity`, `type`, `type_label`, `cause`, `cause_label`, `road`, `destination`, `municipality`, `province`, `community`, `km`, `direction`, `direction_label`, `direction_road`, `latitude` y `longitude` guardan clasificación y ubicación; las coordenadas pueden ser `None`.
### `Incident` — condiciones y cobertura
- `lane_usage`, `management_type`, `maintenance_type`, `information_status`, `probability`, `compliance`, `vehicle_type`, `temp_speed_limit`, `environment_type`, `road_condition_type`, `location_description` y `geographic_descriptor` conservan detalles del registro; `has_camera_coverage`, `camera_coverage_count` y `nearest_camera_km_delta` describen cobertura cercana.
### `Incident.to_dict(self) -> dict[str, Any]`
- Convierte la dataclass y sus campos a un diccionario mediante `asdict`.
### `Camera`
- Dataclass mutable que representa una cámara con identificador, carretera, provincia, punto kilométrico, URL de imagen y coordenadas; `distance_km` y `km_delta` son distancias opcionales de asociación.
### `Camera.to_dict(self) -> dict[str, Any]`
- Devuelve los campos de la cámara como diccionario mediante `asdict`.
### `IncidentStats`
- Dataclass inmutable con contadores `total`, `accidents`, `roadworks`, `stuck`, `obstructions` y `weather`, inicializados a cero.
### `IncidentStats.to_dict(self) -> dict[str, int]`
- Convierte los contadores de estadísticas a un diccionario.
### `IncidentFilters`
- Filtros inmutables opcionales de provincia, municipio, carretera, gravedad, tipo y cámara; `match_mode` predeterminado es `contains` y el último campo opcional, `community`, filtra por comunidad sin distinguir mayúsculas.
### `CameraFilters`
- Filtros inmutables de provincia, carretera, kilómetro y coordenadas, con límite predeterminado 12, rango kilométrico predeterminado compartido, distancia máxima opcional e indicador de cobertura de incidente; `community` es el último campo opcional y filtra la comunidad derivada de la provincia de la cámara.
