# dgt_monitor/api/routes/cameras.py
Define la búsqueda HTTP de cámaras con filtros geográficos (provincia y comunidad autónoma), por carretera y cobertura de incidentes.
## Dependencias
Usa `get_service`, la fachada, `CameraFilters` y la distancia predeterminada de coincidencia. El router se registra en `api.factory.create_app`.
## Contenido
### `cameras(service, province=None, road=None, km=None, lat=None, lon=None, limit=12, all=False, max_km_delta=CAMERA_MATCH_RANGE_KM, max_distance_km=None, incident_coverage=False, match_mode="contains", community=None)`
- `GET /api/cameras` devuelve el payload de cámaras `{"updated_at": ..., "count": ..., "items": [...]}`. Consultas: `province`, `community` (derivada de la provincia de cada cámara y comparada sin distinguir mayúsculas), `road`, `km`, `lat`, `lon`; `limit` entero 1–50 (12), `all` booleano (false), `max_km_delta` 0.1–20 (constante), `max_distance_km` opcional 1–100, `incident_coverage` booleano (false) y `match_mode` (contains). `all=true` desactiva el límite; `422` para límites fuera de rango o tipos inválidos; `200` al completar; `502` si la aplicación eleva `DgtError`.
