# dgt_monitor/api/routes/stats.py
Exposes indicators grouped by province or region, the full incident-grouping structure, and the autonomous-community catalog.
## Dependencies
Uses `get_service`, the facade, and FastAPI types. The router is registered in `api.factory.create_app`.
## Contents
### `stats(service, level="province", refresh=False)`
- `GET /api/stats`; query parameters are `level` (`province` or `region`, default `province`) and boolean `refresh` (false). Returns `{"level", "total", "groups", "extremes"}` with the six indicators `total`, `accidents`, `roadworks`, `breakdowns`, `obstructions`, and `weather`, plus maxima/minima. Responses: 200; 422 if `level` is not one of the two allowed values; 502 for `DgtError`.
### `grouped(service, refresh=False)`
- `GET /api/stats/grouped`; accepts boolean query parameter `refresh` (false). Returns `generated_at`, `total`, indicators, and groupings by province, region, type, weekday, and type+geography (`by_province_type`, `by_region_type`); `region_provinces` lists feed provinces by community. Responses: 200; 502 for `DgtError`.
### `regions()`
- `GET /api/regions` returns `{"regions":[{"name":"...","provinces":[...]}]}`, built from `PROVINCE_TO_REGION` to populate filters.
