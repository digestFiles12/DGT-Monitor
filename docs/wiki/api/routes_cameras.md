# dgt_monitor/api/routes/cameras.py
**ES:** Define la búsqueda HTTP de cámaras con filtros geográficos, por carretera y cobertura de incidentes.
**EN:** Defines HTTP camera search with geographic, road, and incident-coverage filters.
## Dependencies / Dependencias
Usa `get_service`, la fachada, `CameraFilters` y la distancia predeterminada de coincidencia. El router se registra en `api.factory.create_app`.
## Contents / Contenido
### `cameras(service, province=None, road=None, km=None, lat=None, lon=None, limit=12, all=False, max_km_delta=CAMERA_MATCH_RANGE_KM, max_distance_km=None, incident_coverage=False, match_mode="contains")`
- **ES:** `GET /api/cameras` devuelve el payload de cámaras `{"updated_at": ..., "count": ..., "items": [...]}`. Consultas: `province`, `road`, `km`, `lat`, `lon`; `limit` entero 1–50 (12), `all` booleano (false), `max_km_delta` 0.1–20 (constante), `max_distance_km` opcional 1–100, `incident_coverage` booleano (false) y `match_mode` (contains). `all=true` desactiva el límite; `422` para límites fuera de rango o tipos inválidos; `200` al completar; `502` si la aplicación eleva `DgtError`.
- **EN:** `GET /api/cameras` returns camera payload `{"updated_at": ..., "count": ..., "items": [...]}`. Query parameters: `province`, `road`, `km`, `lat`, `lon`; integer `limit` 1–50 (12), boolean `all` (false), `max_km_delta` 0.1–20 (constant default), optional `max_distance_km` 1–100, boolean `incident_coverage` (false), and `match_mode` (contains). `all=true` disables the limit; `422` for out-of-range limits or invalid types; `200` on success; `502` if the application raises `DgtError`.
