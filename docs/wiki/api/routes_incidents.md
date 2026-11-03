# dgt_monitor/api/routes/incidents.py
**ES:** Publica una consulta HTTP de incidentes y un flujo WebSocket que envía periódicamente el payload de incidentes.
**EN:** Publishes an HTTP incident query and a WebSocket stream that periodically sends the incident payload.
## Dependencies / Dependencias
Usa `get_service`, la fachada, `IncidentFilters`, `DgtError` y asyncio. El router se registra en `api.factory.create_app`.
## Contents / Contenido
### `incidents(service, province=None, municipality=None, road=None, severity=None, kind=None, camera=None, match_mode="contains", lang="es")`
- **ES:** `GET /api/incidents` admite consultas `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode` (contains) y `lang` (es). Construye filtros y devuelve el payload `updated_at`, `count`, `stats`, `language` e `items` de la fachada. Respuestas: 200; 502 para `DgtError` manejado por la fábrica.
- **EN:** `GET /api/incidents` accepts query parameters `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode` (contains), and `lang` (es). Builds filters and returns the facade payload with `updated_at`, `count`, `stats`, `language`, and `items`. Responses: 200; 502 for a `DgtError` handled by the factory.
### `incidents_websocket(websocket)`
- **ES:** `WS /ws/incidents` acepta la conexión; lee `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode`, `lang` y `interval` (segundos, predeterminado 120, limitado a 5–300). Envía periódicamente el mismo payload, ampliado con `transport="websocket"` y `refresh_interval_seconds`; un `DgtError` produce `{"error":"..."}`. No tiene cuerpo HTTP de respuesta; la negociación correcta es 101 y la desconexión del cliente termina el bucle.
- **EN:** `WS /ws/incidents` accepts the connection; reads `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode`, `lang`, and `interval` (seconds, default 120, clamped to 5–300). Periodically sends the same payload augmented with `transport="websocket"` and `refresh_interval_seconds`; a `DgtError` produces `{"error":"..."}`. It has no HTTP response body; a successful handshake is 101 and client disconnect ends the loop.
