# dgt_monitor/application/incidents.py
Implements cached loading, filtering, and cause-based incident counts; it can optionally persist loaded incidents.
## Dependencies
Uses core models and ports, the shared rules in [core.indicators](../core/indicators.md), text matching, and the infrastructure `TtlCache`; the application facade uses `IncidentService`.
## Contents
### `IncidentService`
- Application service for loading and filtering incidents, calculating cause-based counts, and optionally persisting results.
### `IncidentService.__init__(repository, cache, store=None)`
- Stores the repository, cache, and optional store.
### `IncidentService.get_all(refresh=False)`
- Gets incidents through the cache; refresh invalidates `incidents`. Loading calls the repository and, if a store exists, attempts to save the result; save errors are logged without preventing the result from being returned.
### `load_incidents()` (internal function of `IncidentService.get_all`)
- Loads incidents from the repository and, if a store is configured, attempts to persist them; catches and logs save exceptions so the loaded data is retained.
### `IncidentService.filter(incidents, filters)`
- Returns only incidents that pass every criterion according to `_matches`.
### `IncidentService.stats(incidents)`
- Counts total, accidents, roadworks/maintenance, stuck or broken-down vehicles, obstructions, and weather events through the shared predicates in `core.indicators`; its counters are `total`, `accidents`, `roadworks`, `stuck`, `obstructions`, and `weather`.
### `IncidentService._matches(item, filters)`
- Applies text matching to province, municipality, and road; compares community (`community`) and severity case-insensitively and filters cause (`kind`) through the same predicates in `core.indicators` and coverage (`camera`). An unrecognized `kind` or `camera` value does not exclude the incident.
