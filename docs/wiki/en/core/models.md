# dgt_monitor/core/models.py
Declares typed data models shared by the desktop and web applications. Incident and camera models can be converted to dictionaries; filters and statistics are immutable.
## Dependencies
Imports `asdict`, `dataclass`, and `Any`; imports `CAMERA_MATCH_RANGE_KM` from [constants](constants.md). Other layers use these models to represent results and criteria.
## Contents
### `Incident`
- Mutable dataclass for an incident; includes identifiers and times, classification data, location, road conditions, and camera coverage.
### `Incident` — identification and time fields
- `id`, `record_id`, `version`, `creation_time`, `source`, `start_time`, and `end_time` describe the situation, its record, and its timing.
### `Incident` — classification and location
- `severity`, `type`, `type_label`, `cause`, `cause_label`, `road`, `destination`, `municipality`, `province`, `community`, `km`, `direction`, `direction_label`, `direction_road`, `latitude`, and `longitude` hold classification and location; coordinates may be `None`.
### `Incident` — conditions and coverage
- `lane_usage`, `management_type`, `maintenance_type`, `information_status`, `probability`, `compliance`, `vehicle_type`, `temp_speed_limit`, `environment_type`, `road_condition_type`, `location_description`, and `geographic_descriptor` retain record details; `has_camera_coverage`, `camera_coverage_count`, and `nearest_camera_km_delta` describe nearby coverage.
### `Incident.to_dict(self) -> dict[str, Any]`
- Converts the dataclass and its fields to a dictionary using `asdict`.
### `Camera`
- Mutable dataclass representing a camera with identifier, road, province, kilometer point, image URL, and coordinates; `distance_km` and `km_delta` are optional matching distances.
### `Camera.to_dict(self) -> dict[str, Any]`
- Returns camera fields as a dictionary using `asdict`.
### `IncidentStats`
- Immutable dataclass of `total`, `accidents`, `roadworks`, `stuck`, `obstructions`, and `weather` counters, initialized to zero.
### `IncidentStats.to_dict(self) -> dict[str, int]`
- Converts the statistics counters to a dictionary.
### `IncidentFilters`
- Immutable optional filters for province, municipality, road, severity, kind, and camera; `match_mode` defaults to `contains`.
### `CameraFilters`
- Immutable filters for province, road, kilometer, and coordinates, with a default limit of 12, shared default kilometer range, optional maximum distance, incident-coverage flag, and `contains` matching mode.
