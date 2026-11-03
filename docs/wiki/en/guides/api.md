# HTTP and WebSocket API
Reference for the endpoints exposed by FastAPI. The application is built with `dgt_monitor.api.factory.create_app()` and the production ASGI entry point is `dgt_monitor.web.app:app`.
## Principles
- Routes (`src/dgt_monitor/api/routes/`) never download or parse XML: they obtain `DgtApplicationService` from `app.state.dgt_service` through `dependencies.get_service`, so tests can replace it with a double.
- A `DgtError` is translated into HTTP 502 with `{"detail": "<message>"}`.
- CORS is open (`allow_origins=["*"]`, no credentials).
- Technical fields keep the English DATEX2 values; the facade adds localized `*_label` fields according to `lang`.
## Endpoint summary
| Method | Path | Description |
|---|---|---|
| GET | `/` | Web dashboard (`index.html`). |
| GET | `/manifest.webmanifest` | PWA manifest. |
| GET | `/sw.js` | Service worker. |
| GET | `/static/*` | Dashboard static assets. |
| GET | `/api/health` | Status and UTC time. |
| GET | `/api/incidents` | Filtered, localized incidents. |
| WS | `/ws/incidents` | Incidents with periodic refresh. |
| GET | `/api/stats` | Indicators per province or region. |
| GET | `/api/stats/grouped` | Full incident grouping. |
| GET | `/api/cameras` | Filtered cameras. |
| GET | `/api/activity/` | Paginated activity log (key required). |
| GET | `/api/activity/csv` | CSV export (key required). |
| GET | `/api/activity/stream` | SSE stream (key required). |
| POST | `/api/activity/clear` | Clears the log (key required). |
## `GET /api/health`
Response:
```json
{"status": "ok", "time": "2026-11-03T10:14:18.633+00:00"}
```
## `GET /api/incidents`
Query parameters (all optional):
- `province`, `municipality`, `road`: text filters, subject to `match_mode`.
- `severity`: case-insensitive equality (`highest`, `high`, `medium`, `low`).
- `kind`: `accident`, `roadworks`, `stuck`, `obstruction`, or `weather`.
- `camera`: `with` (camera coverage) or `without`.
- `match_mode`: `contains` (default), `exact`, or `regex`.
- `lang`: `es` (default) or `en`.

Response shape:
```json
{
  "updated_at": "2026-11-03T10:14:18+00:00",
  "count": 1,
  "stats": {"total": 10, "accidents": 2, "roadworks": 3, "stuck": 1, "obstructions": 1, "weather": 0},
  "language": "en",
  "items": [{
    "id": "...", "record_id": "...", "version": "...", "creation_time": "...", "source": "DGT",
    "start_time": "...", "end_time": "...", "severity": "highest",
    "type": "...", "type_label": "...", "cause": "...", "cause_label": "...",
    "road": "A-52", "destination": "", "municipality": "...", "province": "Zamora", "community": "...",
    "km": "...", "direction": "...", "direction_label": "...", "direction_road": "", "direction_road_label": "...",
    "latitude": 41.5, "longitude": -5.7,
    "lane_usage": "", "management_type": "", "maintenance_type": "", "information_status": "",
    "probability": "", "compliance": "", "vehicle_type": "", "temp_speed_limit": "",
    "environment_type": "", "road_condition_type": "", "location_description": "", "geographic_descriptor": "",
    "has_camera_coverage": true, "camera_coverage_count": 1, "nearest_camera_km_delta": 0.4
  }]
}
```
- `stats` is computed over the filtered set **without** the `kind` filter, so the cards keep showing every type.
- Besides `type_label`, `cause_label`, and `direction_label`, each item includes `*_label` for `severity`, `lane_usage`, `management_type`, `maintenance_type`, `information_status`, `probability`, `compliance`, `vehicle_type`, `environment_type`, and `road_condition_type`.
## `WS /ws/incidents`
Sends the first message on connect and repeats every `interval` seconds.

Query parameters: `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode`, `lang` (same as REST), and `interval` (seconds; default 120, clamped to 5–300).

Each message is the `/api/incidents` payload plus `"transport": "websocket"` and `"refresh_interval_seconds": <interval>`. On a transient `DgtError` it sends `{"error": "<message>"}` and keeps the connection open.
## `GET /api/stats`
Parameters:
- `level`: `province` (default) or `region`; any other value yields 422.
- `refresh`: `true` forces a new request to the DGT.

```json
{
  "level": "province",
  "total": 120,
  "groups": {"Madrid": {"total": 10, "severe": 1, "roadworks": 4, "road_closures": 0}},
  "extremes": {
    "total": {"max": {"name": "Madrid", "value": 10}, "min": {"name": "Soria", "value": 1}},
    "severe": {"max": {"name": "Madrid", "value": 1}, "min": null},
    "roadworks": {"max": {"name": "Madrid", "value": 4}, "min": {"name": "Soria", "value": 1}},
    "road_closures": {"max": null, "min": null}
  }
}
```
The indicators are `total`, `severe` (`highest` severity), `roadworks` (roadworks or maintenance), and `road_closures` (`roadClosed` or `carriagewayClosures`). `max` breaks ties alphabetically and `min` ignores groups with value 0; both are `null` when there is no data.
## `GET /api/stats/grouped`
Parameter: `refresh` (boolean).
```json
{
  "generated_at": "2026-11-03T11:14:18+01:00",
  "total": 120,
  "indicators": ["total", "severe", "roadworks", "road_closures"],
  "by_province": {"Madrid": {"total": 10, "severe": 1, "roadworks": 4, "road_closures": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 10, "severe": 1, "roadworks": 4, "road_closures": 0}},
  "by_type": {"<type>": {"total": 3, "severe": 0, "roadworks": 0, "road_closures": 0}},
  "by_weekday": {"monday": {"total": 5, "severe": 0, "roadworks": 1, "road_closures": 0}},
  "by_weekday_province": {"monday": {"Madrid": {"total": 2, "severe": 0, "roadworks": 0, "road_closures": 0}}},
  "by_weekday_region": {"monday": {"<region>": {"total": 2, "severe": 0, "roadworks": 0, "road_closures": 0}}}
}
```
`by_weekday` always contains the seven days (`monday`…`sunday`); `unknown` appears only when some incident has no valid date. The day is derived from `start_time`, falling back to `creation_time`. Unrecognized provinces are grouped as `Unknown`.
## `GET /api/cameras`
Parameters:
- `province`, `road`: text filters subject to `match_mode`.
- `km`: reference kilometer point.
- `lat`, `lon`: reference coordinates.
- `limit`: integer 1–50 (default 12); `all=true` ignores it.
- `max_km_delta`: 0.1–20 (default `CAMERA_MATCH_RANGE_KM`, 2.0 km).
- `max_distance_km`: 1–100, optional.
- `incident_coverage`: `true` returns only cameras covering an active incident.
- `match_mode`: `contains` (default), `exact`, or `regex`.

```json
{
  "updated_at": "2026-11-03T10:14:18+00:00",
  "count": 1,
  "items": [{
    "id": "...", "road": "A-52", "province": "Zamora", "km": "...", "image_url": "https://...",
    "latitude": 41.5, "longitude": -5.7, "distance_km": 1.2, "km_delta": 0.4
  }]
}
```
Coverage is computed from the normalized road, a compatible province, and a kilometer-point difference less than or equal to `max_km_delta`. With `incident_coverage=true` and `limit`, the limit is applied after coverage is computed so valid matches are not lost.
## Search modes
- `contains`: case-insensitive partial match.
- `exact`: full equality after `casefold()`.
- `regex`: case-insensitive `re.search()`; an invalid expression does not break the API, it just matches nothing.

```http
GET /api/incidents?road=A-52&match_mode=exact
GET /api/incidents?province=^Za&match_mode=regex
GET /api/cameras?road=^A-\d+$&match_mode=regex&incident_coverage=true
```
## Activity API
Every endpoint requires the `X-API-Key` header. Valid keys come from `ACTIVITY_API_KEYS` (comma-separated) or `ACTIVITY_API_KEY`; keys in `ACTIVITY_REVOKED_API_KEYS` are rejected first. Comparison uses `secrets.compare_digest()`. A missing, invalid, or revoked key returns 401.

Each entry has the fields `timestamp`, `level`, `source`, `event_type`, `user`, and `message`.
### `GET /api/activity/`
Parameters: `level`, `source`, `event_type`, `user` (exact equality), `offset` (default 0), and `limit` (1–1000; out-of-range values fall back to 100). `start_ts` and `end_ts` are accepted but currently do not filter.
```json
{"total": 42, "offset": 0, "limit": 100, "entries": [{"timestamp": "...", "level": "info", "source": "...", "event_type": "...", "user": "...", "message": "..."}]}
```
### `GET /api/activity/csv`
Downloads `activity.csv` (`text/csv`) with the header `timestamp,level,source,event_type,user,message`.
### `GET /api/activity/stream`
`text/event-stream` flow; each event is `event: activity` with an `id` and JSON `data`. `replay=N` resends the last N entries before the new ones, and `once=true` ends after that.
### `POST /api/activity/clear`
Clears the log and responds `{"status": "cleared"}`.
## Web dashboard
Served from `src/dgt_monitor/web/static/`; it consumes these endpoints from the same origin and has no DATEX2 logic of its own.
- Tabs: Incidents, Cameras, Favorites (stored in `localStorage`), Charts, and Map.
- The **Charts** tab uses `/api/stats?level=province|region` and can group by province/region, weekday, or type, as bars, lines, or pie (top eight plus "Others"), with maxima and minima. Chart.js is served locally (`static/chart.umd.min.js`).
- ES/EN language selector, light/dark mode, and filters with search mode.
- PWA: the service worker (cache `dgt-monitor-v54`) stores the static shell and never caches `/api/`.
## Development run
```powershell
.\.venv\Scripts\python.exe -m uvicorn dgt_monitor.web.app:app --reload
```
See also [the testing guide](testing.md) and [the GUI guide](gui.md).
