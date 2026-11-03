# dgt_monitor/api/routes/stats.py
**ES:** Expone indicadores agrupados por provincia o región y la estructura completa de agrupaciones de incidentes.
**EN:** Exposes indicators grouped by province or region and the full incident-grouping structure.
## Dependencies / Dependencias
Usa `get_service`, la fachada y tipos de FastAPI. El router se registra en `api.factory.create_app`.
## Contents / Contenido
### `stats(service, level="province", refresh=False)`
- **ES:** `GET /api/stats`; consultas `level` (`province` o `region`, predeterminado `province`) y `refresh` booleano (false). Devuelve `{"level", "total", "groups", "extremes"}` con cuatro indicadores y máximos/mínimos. Respuestas: 200; 422 si `level` no pertenece a los dos valores permitidos; 502 para `DgtError`.
- **EN:** `GET /api/stats`; query parameters are `level` (`province` or `region`, default `province`) and boolean `refresh` (false). Returns `{"level", "total", "groups", "extremes"}` with four indicators and maxima/minima. Responses: 200; 422 if `level` is not one of the two allowed values; 502 for `DgtError`.
### `grouped(service, refresh=False)`
- **ES:** `GET /api/stats/grouped`; consulta `refresh` booleano (false). Devuelve el JSON agrupado con `generated_at`, `total`, indicadores y agrupaciones por provincia, región, tipo y día (también desgloses geográficos por día). Respuestas: 200; 502 para `DgtError`.
- **EN:** `GET /api/stats/grouped`; accepts boolean query parameter `refresh` (false). Returns grouped JSON with `generated_at`, `total`, indicators, and groupings by province, region, type, and weekday (including weekday geographic breakdowns). Responses: 200; 502 for `DgtError`.
