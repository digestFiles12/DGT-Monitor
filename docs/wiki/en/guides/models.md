# Models

The typed domain models are in `src/dgt_monitor/core/models.py`. They are dataclasses and provide a shared representation for application services and adapters.

## `Incident`

Represents an incident normalized from a DATEX II situation. It groups identifiers and timestamps, severity, type and cause, location (road, municipality, province, community, and kilometer point), direction, coordinates, and other traffic attributes. It also contains camera-coverage fields calculated by the application: `has_camera_coverage`, `camera_coverage_count`, and `nearest_camera_km_delta`.

The model includes labels for type, cause, and direction. When building an incident response, the facade adds localized labels for other translatable fields; those additional labels belong to the payload and are not fields declared on the dataclass.

## `Camera`

Represents a camera with an identifier, road, province, kilometer point, image URL, and coordinates. `distance_km` and `km_delta` hold distances calculated during a search; they are not required to identify a camera in the source.

## Statistics and filters

`IncidentStats` is an immutable value with six counters: total, accidents, roadworks, stuck vehicles, obstructions, and weather conditions.

`IncidentFilters` carries province, municipality, road, severity, kind, camera coverage, and match mode. `CameraFilters` carries province, road, kilometer point, coordinates, result limit, distance thresholds, incident coverage, and match mode. Both are immutable dataclasses; the services apply their criteria.

## Dictionary conversion

`Incident.to_dict()`, `Camera.to_dict()`, and `IncidentStats.to_dict()` use `dataclasses.asdict()` to create serializable structures without coupling the models to FastAPI or Pydantic.

See [Services](services.md) for how these models are used and [Architecture](architecture.md) for their place in the layers.
