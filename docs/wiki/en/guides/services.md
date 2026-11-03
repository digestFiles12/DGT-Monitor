# Services

Application use cases coordinate repositories, caches, persistence, and models. The `DgtApplicationService` facade is the shared entry point for the API and GUI.

## Incidents

`IncidentService.get_all()` obtains incidents from the repository through `TtlCache`. An explicit refresh invalidates the key before reloading. If a store is configured, each load is saved; persistence errors are logged and do not prevent returning the fetched data. `filter()` applies `IncidentFilters`, and `stats()` calculates the six `IncidentStats` counters.

## Cameras

`CameraService` loads and filters cameras by province, road, kilometer point, and, when coordinates are supplied, geographic distance. Road and province matching use the filter's text mode. `annotate_coverage()` associates cameras and incidents using normalized roads, compatible provinces, and a difference no greater than `CAMERA_MATCH_RANGE_KM` (2 km by default). `with_incident_coverage()` uses the same criteria to select cameras covering active incidents.

## Facade and statistics

`DgtApplicationService.get_incident_payload()` calculates coverage, filters incidents, and prepares localized labels. `get_cameras()` returns filtered cameras; when incident coverage is requested, it applies the result limit after selecting coverage. `get_statistics()` returns four indicators by province or autonomous community, with maximum and minimum values. `get_grouped_incidents()` builds groupings by province, autonomous community, type, and weekday.

The `GET /api/stats` and `GET /api/stats/grouped` routes expose those results. `application.statistics` defines total incidents, severe incidents, roadworks, and road closures; it derives the weekday from the start time (or creation time when the start time is absent) and writes grouped JSON as UTF-8. See [DATEX II](datex2.md) for the data source and parsing process.

## Cache and persistence

`TtlCache` is a thread-safe in-memory cache that returns deep copies. Production composition sets a 120-second TTL for incidents and 300 seconds for cameras. `SqliteIncidentStore` stores incidents by `id` using insert-or-update behavior; its path is configured with `INCIDENT_DB_PATH` and defaults to `data/incidents.db`.

## Console menu

`dgt_monitor.menu` can build grouped JSON from a local or downloaded XML file, or reuse an existing JSON file. It then lets users explore indicators with bar or pie charts and displays their maxima and minima. The web dashboard presents its charts on the charts tab.
