# dgt_monitor/core/models.py
**ES:** Declara los modelos de datos tipados compartidos por las aplicaciones de escritorio y web. Los modelos de incidente y cámara se pueden convertir a diccionarios; los filtros y estadísticas son inmutables.
**EN:** Declares typed data models shared by the desktop and web applications. Incident and camera models can be converted to dictionaries; filters and statistics are immutable.
## Dependencies / Dependencias
Importa `asdict`, `dataclass` y `Any`; importa `CAMERA_MATCH_RANGE_KM` de [constants](constants.md). Las demás capas usan estos modelos para representar resultados y criterios.
## Contents / Contenido
### `Incident`
- **ES:** Dataclass mutable para una incidencia; incluye identificadores y tiempos, datos de clasificación, localización, condiciones de vía y cobertura de cámaras.
- **EN:** Mutable dataclass for an incident; includes identifiers and times, classification data, location, road conditions, and camera coverage.
### `Incident` — campos de identificación y tiempo
- **ES:** `id`, `record_id`, `version`, `creation_time`, `source`, `start_time` y `end_time` describen la situación, su registro y su vigencia.
- **EN:** `id`, `record_id`, `version`, `creation_time`, `source`, `start_time`, and `end_time` describe the situation, its record, and its timing.
### `Incident` — clasificación y localización
- **ES:** `severity`, `type`, `type_label`, `cause`, `cause_label`, `road`, `destination`, `municipality`, `province`, `community`, `km`, `direction`, `direction_label`, `direction_road`, `latitude` y `longitude` guardan clasificación y ubicación; las coordenadas pueden ser `None`.
- **EN:** `severity`, `type`, `type_label`, `cause`, `cause_label`, `road`, `destination`, `municipality`, `province`, `community`, `km`, `direction`, `direction_label`, `direction_road`, `latitude`, and `longitude` hold classification and location; coordinates may be `None`.
### `Incident` — condiciones y cobertura
- **ES:** `lane_usage`, `management_type`, `maintenance_type`, `information_status`, `probability`, `compliance`, `vehicle_type`, `temp_speed_limit`, `environment_type`, `road_condition_type`, `location_description` y `geographic_descriptor` conservan detalles del registro; `has_camera_coverage`, `camera_coverage_count` y `nearest_camera_km_delta` describen cobertura cercana.
- **EN:** `lane_usage`, `management_type`, `maintenance_type`, `information_status`, `probability`, `compliance`, `vehicle_type`, `temp_speed_limit`, `environment_type`, `road_condition_type`, `location_description`, and `geographic_descriptor` retain record details; `has_camera_coverage`, `camera_coverage_count`, and `nearest_camera_km_delta` describe nearby coverage.
### `Incident.to_dict(self) -> dict[str, Any]`
- **ES:** Convierte la dataclass y sus campos a un diccionario mediante `asdict`.
- **EN:** Converts the dataclass and its fields to a dictionary using `asdict`.
### `Camera`
- **ES:** Dataclass mutable que representa una cámara con identificador, carretera, provincia, punto kilométrico, URL de imagen y coordenadas; `distance_km` y `km_delta` son distancias opcionales de asociación.
- **EN:** Mutable dataclass representing a camera with identifier, road, province, kilometer point, image URL, and coordinates; `distance_km` and `km_delta` are optional matching distances.
### `Camera.to_dict(self) -> dict[str, Any]`
- **ES:** Devuelve los campos de la cámara como diccionario mediante `asdict`.
- **EN:** Returns camera fields as a dictionary using `asdict`.
### `IncidentStats`
- **ES:** Dataclass inmutable con contadores `total`, `accidents`, `roadworks`, `stuck`, `obstructions` y `weather`, inicializados a cero.
- **EN:** Immutable dataclass of `total`, `accidents`, `roadworks`, `stuck`, `obstructions`, and `weather` counters, initialized to zero.
### `IncidentStats.to_dict(self) -> dict[str, int]`
- **ES:** Convierte los contadores de estadísticas a un diccionario.
- **EN:** Converts the statistics counters to a dictionary.
### `IncidentFilters`
- **ES:** Filtros inmutables opcionales de provincia, municipio, carretera, gravedad, tipo y cámara; `match_mode` predeterminado es `contains`.
- **EN:** Immutable optional filters for province, municipality, road, severity, kind, and camera; `match_mode` defaults to `contains`.
### `CameraFilters`
- **ES:** Filtros inmutables de provincia, carretera, kilómetro y coordenadas, con límite predeterminado 12, rango kilométrico predeterminado compartido, distancia máxima opcional, indicador de cobertura de incidente y modo `contains`.
- **EN:** Immutable filters for province, road, kilometer, and coordinates, with a default limit of 12, shared default kilometer range, optional maximum distance, incident-coverage flag, and `contains` matching mode.
