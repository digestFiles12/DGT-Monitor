# dgt_monitor/application/cameras.py
Implements use cases for loading, filtering, and sorting cameras, and relating them to incidents by road, province, and kilometer point.
## Dependencies
Imports core models and ports, normalization and text-matching functions, distance geometry, the match-range constant, and a TTL cache. The application facade uses `CameraService`.
## Contents
### `CameraService`
- Application service coordinating the repository, cache, and spatial calculation for camera search and coverage.
### `CameraService.__init__(repository, cache, distance=None)`
- Stores the repository and cache; uses the supplied distance calculator or creates a default one.
### `CameraService.get_all(refresh=False)`
- Returns cached cameras, loading them from the repository when needed; `refresh=True` first invalidates the `cameras` cache key.
### `CameraService.filter(cameras, filters)`
- Filters by province, community (derived from `camera.province` with `region_for_province`, case-insensitively), road, and kilometer and/or coordinate distance; adds `km_delta` and `distance_km`, sorts by distance (uncomputed values last), and applies `limit`. An unparseable kilometer point cannot satisfy an active kilometer filter.
### `CameraService.with_incident_coverage(cameras, incidents, range_km=CAMERA_MATCH_RANGE_KM)`
- Returns cameras with at least one incident on the same normalized road and within range; when both provinces exist, they must also match. Incidents or cameras without a parseable kilometer are ignored.
### `CameraService.annotate_coverage(incidents, cameras, range_km=CAMERA_MATCH_RANGE_KM)`
- Copies each incident with coverage fields: boolean, number of matching cameras, and minimum kilometer difference rounded to three decimals. Incidents without coverage are retained.
