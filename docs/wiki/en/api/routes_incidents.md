# dgt_monitor/api/routes/incidents.py
Publishes an HTTP incident query and a WebSocket stream that periodically sends the incident payload.
## Dependencies
Uses `get_service`, the facade, `IncidentFilters`, `DgtError`, and asyncio. The router is registered in `api.factory.create_app`.
## Contents
### `incidents(service, province=None, municipality=None, road=None, severity=None, kind=None, camera=None, match_mode="contains", lang="es")`
- `GET /api/incidents` accepts query parameters `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode` (contains), and `lang` (es). Builds filters and returns the facade payload with `updated_at`, `count`, `stats`, `language`, and `items`. Responses: 200; 502 for a `DgtError` handled by the factory.
### `incidents_websocket(websocket)`
- `WS /ws/incidents` accepts the connection; reads `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode`, `lang`, and `interval` (seconds, default 120, clamped to 5–300). Periodically sends the same payload augmented with `transport="websocket"` and `refresh_interval_seconds`; a `DgtError` produces `{"error":"..."}`. It has no HTTP response body; a successful handshake is 101 and client disconnect ends the loop.
