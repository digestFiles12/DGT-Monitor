# dgt_monitor/api/routes/incidents.py
Publica una consulta HTTP de incidentes y un flujo WebSocket que envía periódicamente el payload de incidentes.
## Dependencias
Usa `get_service`, la fachada, `IncidentFilters`, `DgtError` y asyncio. El router se registra en `api.factory.create_app`.
## Contenido
### `incidents(service, province=None, municipality=None, road=None, severity=None, kind=None, camera=None, match_mode="contains", lang="es", community=None)`
- `GET /api/incidents` admite consultas `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `community`, `match_mode` (contains) y `lang` (es). `community` compara el nombre de la comunidad sin distinguir mayúsculas. Construye filtros y devuelve el payload `updated_at`, `count`, `stats`, `language` e `items` de la fachada. Respuestas: 200; 502 para `DgtError` manejado por la fábrica.
### `incidents_websocket(websocket)`
- `WS /ws/incidents` acepta la conexión; lee `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `community`, `match_mode`, `lang` y `interval` (segundos, predeterminado 120, limitado a 5–300). `community` compara el nombre sin distinguir mayúsculas. Envía periódicamente el mismo payload, ampliado con `transport="websocket"` y `refresh_interval_seconds`; un `DgtError` produce `{"error":"..."}`. No tiene cuerpo HTTP de respuesta; la negociación correcta es 101 y la desconexión del cliente termina el bucle.
