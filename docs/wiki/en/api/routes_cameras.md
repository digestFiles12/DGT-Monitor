# dgt_monitor/api/routes/cameras.py
Defines HTTP camera search with geographic, road, and incident-coverage filters.
## Dependencies
Uses `get_service`, the facade, `CameraFilters`, and the default match distance. The router is registered in `api.factory.create_app`.
## Contents
### `cameras(service, province=None, road=None, km=None, lat=None, lon=None, limit=12, all=False, max_km_delta=CAMERA_MATCH_RANGE_KM, max_distance_km=None, incident_coverage=False, match_mode="contains")`
- `GET /api/cameras` returns camera payload `{"updated_at": ..., "count": ..., "items": [...]}`. Query parameters: `province`, `road`, `km`, `lat`, `lon`; integer `limit` 1–50 (12), boolean `all` (false), `max_km_delta` 0.1–20 (constant default), optional `max_distance_km` 1–100, boolean `incident_coverage` (false), and `match_mode` (contains). `all=true` disables the limit; `422` for out-of-range limits or invalid types; `200` on success; `502` if the application raises `DgtError`.
