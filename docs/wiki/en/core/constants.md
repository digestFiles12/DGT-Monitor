# dgt_monitor/core/constants.py
Centralizes DGT URLs and default values used by HTTP requests, caching, and camera matching. This lets modules share the same settings.
## Dependencies
It imports no project or third-party modules. HTTP adapters, repositories, and bootstrap use these constants.
## Contents
### `DGT_INCIDENTS_URL`, `DGT_CAMERAS_URL`
- URLs for the DGT DATEX2 incident and camera documents, respectively.
### `HTTP_TIMEOUT_SECONDS`, `HTTP_HEADERS`
- Default HTTP timeout (15 seconds) and headers sent by the client, including `User-Agent` and `Accept`.
### `INCIDENT_CACHE_SECONDS`, `CAMERA_CACHE_SECONDS`
- Default cache durations: 120 seconds for incidents and 300 for cameras.
### `CAMERA_MATCH_RANGE_KM`
- Default kilometer-distance range for matching cameras: 2.0 km.
