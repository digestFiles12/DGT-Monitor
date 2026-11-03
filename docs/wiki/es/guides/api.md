# API HTTP y WebSocket
Referencia de los endpoints expuestos por FastAPI. La aplicación se construye con `dgt_monitor.api.factory.create_app()` y el punto ASGI de producción es `dgt_monitor.web.app:app`.
## Principios
- Las rutas (`src/dgt_monitor/api/routes/`) no descargan ni parsean XML: obtienen `DgtApplicationService` desde `app.state.dgt_service` mediante `dependencies.get_service`, lo que permite sustituirlo por un doble en las pruebas.
- Un `DgtError` se traduce a HTTP 502 con `{"detail": "<mensaje>"}`.
- CORS abierto (`allow_origins=["*"]`, sin credenciales).
- Los campos técnicos conservan los valores DATEX2 en inglés; la fachada añade campos `*_label` localizados según `lang`.
## Resumen de endpoints
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Dashboard web (`index.html`). |
| GET | `/manifest.webmanifest` | Manifiesto PWA. |
| GET | `/sw.js` | Service worker. |
| GET | `/static/*` | Recursos estáticos del dashboard. |
| GET | `/api/health` | Estado y hora UTC. |
| GET | `/api/incidents` | Incidencias filtradas y localizadas. |
| WS | `/ws/incidents` | Incidencias con refresco periódico. |
| GET | `/api/stats` | Indicadores por provincia o comunidad. |
| GET | `/api/stats/grouped` | Agrupación completa de incidencias. |
| GET | `/api/cameras` | Cámaras filtradas. |
| GET | `/api/activity/` | Registro de actividad paginado (requiere clave). |
| GET | `/api/activity/csv` | Exportación CSV (requiere clave). |
| GET | `/api/activity/stream` | Flujo SSE (requiere clave). |
| POST | `/api/activity/clear` | Vacía el registro (requiere clave). |
## `GET /api/health`
Respuesta:
```json
{"status": "ok", "time": "2026-11-03T10:14:18.633+00:00"}
```
## `GET /api/incidents`
Parámetros de consulta (todos opcionales):
- `province`, `municipality`, `road`: filtros de texto, sujetos a `match_mode`.
- `severity`: igualdad sin distinguir mayúsculas (`highest`, `high`, `medium`, `low`).
- `kind`: `accident`, `roadworks`, `stuck`, `obstruction` o `weather`.
- `camera`: `with` (con cobertura de cámara) o `without`.
- `match_mode`: `contains` (por defecto), `exact` o `regex`.
- `lang`: `es` (por defecto) o `en`.

Forma de la respuesta:
```json
{
  "updated_at": "2026-11-03T10:14:18+00:00",
  "count": 1,
  "stats": {"total": 10, "accidents": 2, "roadworks": 3, "stuck": 1, "obstructions": 1, "weather": 0},
  "language": "es",
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
- `stats` se calcula sobre el conjunto filtrado **sin** el filtro `kind`, de modo que las tarjetas siguen mostrando todos los tipos.
- Además de `type_label`, `cause_label` y `direction_label`, cada elemento incluye `*_label` para `severity`, `lane_usage`, `management_type`, `maintenance_type`, `information_status`, `probability`, `compliance`, `vehicle_type`, `environment_type` y `road_condition_type`.
## `WS /ws/incidents`
Envía el primer mensaje al conectar y repite cada `interval` segundos.

Parámetros de consulta: `province`, `municipality`, `road`, `severity`, `kind`, `camera`, `match_mode`, `lang` (igual que REST) e `interval` (segundos; por defecto 120, limitado al rango 5–300).

Cada mensaje es el payload de `/api/incidents` más `"transport": "websocket"` y `"refresh_interval_seconds": <interval>`. Ante un `DgtError` transitorio envía `{"error": "<mensaje>"}` y mantiene la conexión abierta.
## `GET /api/stats`
Parámetros:
- `level`: `province` (por defecto) o `region`; cualquier otro valor produce 422.
- `refresh`: `true` fuerza una nueva consulta a la DGT.

```json
{
  "level": "province",
  "total": 120,
  "groups": {"Madrid": {"total": 10, "accidents": 1, "roadworks": 4, "breakdowns": 2, "obstructions": 1, "weather": 0}},
  "extremes": {
    "total": {"max": {"name": "Madrid", "value": 10}, "min": {"name": "Soria", "value": 1}},
    "accidents": {"max": {"name": "Madrid", "value": 1}, "min": null},
    "roadworks": {"max": {"name": "Madrid", "value": 4}, "min": {"name": "Soria", "value": 1}},
    "breakdowns": {"max": {"name": "Madrid", "value": 2}, "min": {"name": "Madrid", "value": 2}},
    "obstructions": {"max": {"name": "Madrid", "value": 1}, "min": {"name": "Madrid", "value": 1}},
    "weather": {"max": {"name": "Madrid", "value": 0}, "min": null}
  }
}
```
Los seis indicadores son `total`, `accidents`, `roadworks`, `breakdowns`, `obstructions` y `weather`; sus reglas compartidas están en [core.indicators](../core/indicators.md). `max` desempata alfabéticamente y `min` ignora grupos con valor 0; si `weather` vale 0 en todos los grupos, su mínimo es `null`.
## `GET /api/stats/grouped`
Parámetro: `refresh` (booleano).
```json
{
  "generated_at": "2026-11-03T11:14:18+01:00",
  "total": 120,
  "indicators": ["total", "accidents", "roadworks", "breakdowns", "obstructions", "weather"],
  "by_province": {"Madrid": {"total": 10, "accidents": 1, "roadworks": 4, "breakdowns": 2, "obstructions": 1, "weather": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 10, "accidents": 1, "roadworks": 4, "breakdowns": 2, "obstructions": 1, "weather": 0}},
  "by_type": {"<tipo>": {"total": 3, "accidents": 0, "roadworks": 0, "breakdowns": 0, "obstructions": 0, "weather": 0}},
  "labels": {"by_type": {"es": {"<tipo>": "<etiqueta en español>"}, "en": {"<tipo>": "<label in English>"}}},
  "by_weekday": {"monday": {"total": 5, "accidents": 0, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}},
  "by_weekday_province": {"monday": {"Madrid": {"total": 2, "accidents": 0, "roadworks": 0, "breakdowns": 0, "obstructions": 0, "weather": 0}}},
  "by_weekday_region": {"monday": {"<comunidad>": {"total": 2, "accidents": 0, "roadworks": 0, "breakdowns": 0, "obstructions": 0, "weather": 0}}},
  "by_province_type": {"<type>": {"Madrid": {"total": 1, "accidents": 0, "roadworks": 0, "breakdowns": 0, "obstructions": 0, "weather": 0}}},
  "by_region_type": {"<type>": {"<region>": {"total": 1, "accidents": 0, "roadworks": 0, "breakdowns": 0, "obstructions": 0, "weather": 0}}}
}
```
`by_weekday` siempre contiene los siete días (`monday`…`sunday`); aparece `unknown` solo si alguna incidencia no tiene fecha válida. El día se calcula a partir de `start_time` y, en su defecto, de `creation_time`. Las provincias no reconocidas se agrupan como `Unknown`.
## `GET /api/regions`
Lista las comunidades autónomas con sus provincias: `{"regions": [{"name": "Andalucía", "provinces": ["Almería", ...]}]}`. Se usa para rellenar el filtro de comunidad.

Los endpoints `/api/incidents`, `/api/cameras` y `/ws/incidents` aceptan además `community` (nombre exacto de la comunidad, sin distinguir mayúsculas).
## `GET /api/cameras`
Parámetros:
- `province`, `road`: filtros de texto sujetos a `match_mode`.
- `km`: punto kilométrico de referencia.
- `lat`, `lon`: coordenadas de referencia.
- `limit`: entero 1–50 (por defecto 12); `all=true` lo ignora.
- `max_km_delta`: 0,1–20 (por defecto `CAMERA_MATCH_RANGE_KM`, 2.0 km).
- `max_distance_km`: 1–100, opcional.
- `incident_coverage`: `true` devuelve solo cámaras que cubren alguna incidencia activa.
- `match_mode`: `contains` (por defecto), `exact` o `regex`.

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
La cobertura se calcula por carretera normalizada, provincia compatible y diferencia de punto kilométrico menor o igual a `max_km_delta`. Con `incident_coverage=true` y `limit`, el límite se aplica después de calcular la cobertura para no perder coincidencias.
## Modos de búsqueda
- `contains`: coincidencia parcial sin distinguir mayúsculas.
- `exact`: igualdad completa tras `casefold()`.
- `regex`: `re.search()` insensible a mayúsculas; una expresión inválida no rompe la API, solo no produce coincidencias.

```http
GET /api/incidents?road=A-52&match_mode=exact
GET /api/incidents?province=^Za&match_mode=regex
GET /api/cameras?road=^A-\d+$&match_mode=regex&incident_coverage=true
```
## Activity API
Todos los endpoints requieren la cabecera `X-API-Key`. Las claves válidas se leen de `ACTIVITY_API_KEYS` (separadas por comas) o de `ACTIVITY_API_KEY`; las de `ACTIVITY_REVOKED_API_KEYS` se rechazan primero. La comparación usa `secrets.compare_digest()`. Sin cabecera, con clave inválida o revocada se responde 401.

Cada entrada tiene los campos `timestamp`, `level`, `source`, `event_type`, `user` y `message`.
### `GET /api/activity/`
Parámetros: `level`, `source`, `event_type`, `user` (igualdad exacta), `offset` (0 por defecto) y `limit` (1–1000; fuera de rango vuelve a 100). Los parámetros `start_ts` y `end_ts` se aceptan, pero actualmente no filtran.
```json
{"total": 42, "offset": 0, "limit": 100, "entries": [{"timestamp": "...", "level": "info", "source": "...", "event_type": "...", "user": "...", "message": "..."}]}
```
### `GET /api/activity/csv`
Descarga `activity.csv` (`text/csv`) con la cabecera `timestamp,level,source,event_type,user,message`.
### `GET /api/activity/stream`
Flujo `text/event-stream`; cada evento es `event: activity` con `id` e `data` en JSON. `replay=N` reenvía las últimas N entradas antes de las nuevas y `once=true` termina tras ese envío.
### `POST /api/activity/clear`
Vacía el registro y responde `{"status": "cleared"}`.
## Dashboard web
Se sirve desde `src/dgt_monitor/web/static/` y consume estos endpoints desde el mismo origen, sin lógica DATEX2 propia.
- Pestañas: Incidencias, Cámaras, Favoritas (guardadas en `localStorage`), Gráficas y Mapa.
- La pestaña **Gráficas** usa `/api/stats?level=province|region` y permite agrupar por provincia/comunidad, día de la semana o tipo, en barras, líneas o queso (los ocho mayores y «Otros»), con máximos y mínimos. Chart.js se sirve localmente (`static/chart.umd.min.js`).
- Selector de idioma ES/EN, modo claro/oscuro y filtros con modo de búsqueda.
- PWA: el service worker (caché `dgt-monitor-v59`) guarda el shell estático y nunca cachea `/api/`.
## Ejecución en desarrollo
```powershell
.\.venv\Scripts\python.exe -m uvicorn dgt_monitor.web.app:app --reload
```
Véase también [la guía de pruebas](testing.md) y [la guía de la GUI](gui.md).
