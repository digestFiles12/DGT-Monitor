# dgt_monitor/core/indicators.py
Defines the shared incident-classification rules used to calculate dashboard indicators.
## Dependencies
Uses `Incident` from `core.models` and `Callable` from the standard library. `IncidentService` and `application.statistics` reuse these functions.
## Contents
### `WEATHER_WORDS`
- Keywords (`weather`, `fog`, `snow`, `flooding`, `ice`, `rain`) that identify weather events.
### `is_accident(incident: Incident) -> bool`
- Returns `True` if the cause contains `accident`, case-insensitively.
### `is_roadworks(incident: Incident) -> bool`
- Returns `True` if the cause contains `roadworks` or `maintenance`, case-insensitively.
### `is_breakdown(incident: Incident) -> bool`
- Returns `True` if the cause contains `stuck` or `breakdown`, case-insensitively.
### `is_obstruction(incident: Incident) -> bool`
- Returns `True` if the cause contains `obstruction`, case-insensitively.
### `is_weather(incident: Incident) -> bool`
- Returns `True` if the cause contains any word in `WEATHER_WORDS`, case-insensitively.
### `INDICATOR_RULES`
- Ordered mapping from indicator keys to predicates for `accidents`, `roadworks`, `breakdowns`, `obstructions`, and `weather`. `total` is counted separately because it includes every incident.
## Shared use
`IncidentService.stats()` and `_matches()` apply these rules to their counters and cause filters. `application.statistics` builds `INDICATORS` by prepending `total` to the `INDICATOR_RULES` keys, then uses them for counting and grouping. Therefore, grouped indicator keys are `total`, `accidents`, `roadworks`, `breakdowns`, `obstructions`, and `weather`.
