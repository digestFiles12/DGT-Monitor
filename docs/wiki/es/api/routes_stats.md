# dgt_monitor/api/routes/stats.py
Expone indicadores agrupados por provincia o región y la estructura completa de agrupaciones de incidentes.
## Dependencias
Usa `get_service`, la fachada y tipos de FastAPI. El router se registra en `api.factory.create_app`.
## Contenido
### `stats(service, level="province", refresh=False)`
- `GET /api/stats`; consultas `level` (`province` o `region`, predeterminado `province`) y `refresh` booleano (false). Devuelve `{"level", "total", "groups", "extremes"}` con los seis indicadores `total`, `accidents`, `roadworks`, `breakdowns`, `obstructions` y `weather`, además de máximos/mínimos. Respuestas: 200; 422 si `level` no pertenece a los dos valores permitidos; 502 para `DgtError`.
### `grouped(service, refresh=False)`
- `GET /api/stats/grouped`; consulta `refresh` booleano (false). Devuelve el JSON agrupado con `generated_at`, `total`, indicadores y agrupaciones por provincia, región, tipo y día (también desgloses geográficos por día). Respuestas: 200; 502 para `DgtError`.
