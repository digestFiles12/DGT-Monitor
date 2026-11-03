# dgt_monitor/core/indicators.py
Define las reglas compartidas para clasificar incidencias y calcular los indicadores del dashboard.
## Dependencias
Usa `Incident` de `core.models` y `Callable` de la biblioteca estándar. `IncidentService` y `application.statistics` reutilizan estas funciones.
## Contenido
### `WEATHER_WORDS`
- Palabras clave (`weather`, `fog`, `snow`, `flooding`, `ice`, `rain`) que identifican eventos meteorológicos.
### `is_accident(incident: Incident) -> bool`
- Devuelve `True` si la causa contiene `accident`, sin distinguir mayúsculas.
### `is_roadworks(incident: Incident) -> bool`
- Devuelve `True` si la causa contiene `roadworks` o `maintenance`, sin distinguir mayúsculas.
### `is_breakdown(incident: Incident) -> bool`
- Devuelve `True` si la causa contiene `stuck` o `breakdown`, sin distinguir mayúsculas.
### `is_obstruction(incident: Incident) -> bool`
- Devuelve `True` si la causa contiene `obstruction`, sin distinguir mayúsculas.
### `is_weather(incident: Incident) -> bool`
- Devuelve `True` si la causa contiene cualquiera de las palabras de `WEATHER_WORDS`, sin distinguir mayúsculas.
### `INDICATOR_RULES`
- Mapa ordenado de clave a predicado para `accidents`, `roadworks`, `breakdowns`, `obstructions` y `weather`. `total` se cuenta aparte porque incluye cada incidencia.
## Uso compartido
`IncidentService.stats()` y `_matches()` aplican estas reglas a sus contadores y filtros por causa. `application.statistics` construye `INDICATORS` anteponiendo `total` a las claves de `INDICATOR_RULES`, y las usa para contar y agrupar. Por ello, las claves agrupadas son `total`, `accidents`, `roadworks`, `breakdowns`, `obstructions` y `weather`.
