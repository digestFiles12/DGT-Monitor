# dgt_monitor/application/statistics.py
Computes the six incident indicators, geographic/temporal and type+geography groupings, per-group extremes, and JSON export.
## Dependencies
Uses the shared rules from [core.indicators](../core/indicators.md), `Incident`, and the province-to-region mapping from `core`; `DgtApplicationService` and `menu.py` consume these calculations. It also uses the standard library for dates, JSON, and paths.
## Contents
### `INDICATORS`, `WEEKDAYS`, `DEFAULT_GROUPED_JSON`
- Constants for the indicator order (`total`, `accidents`, `roadworks`, `breakdowns`, `obstructions`, `weather`), the seven English weekday names, and the default filename (`grouped_incidents.json`).
### `count_indicators(incidents)`
- Iterates over an iterable and returns six counts. `total` counts every incident; the other five use the predicates in `core.indicators.INDICATOR_RULES`.
### `weekday_of(incident)`
- Tries the ISO start time; if missing or invalid, tries the creation time. Returns a lowercase English weekday or `None` if neither can be parsed.
### `_empty_leaf()`
- Creates a dictionary with all six indicators initialized to zero.
### `_count(leaf, incident)`
- Increments `total` and adds each shared `INDICATOR_RULES` predicate result to its corresponding indicator.
### `_add_incident(groups, key, incident)`
- Creates the group leaf if absent and updates all six indicators through `_count`.
### `_sorted_groups(groups)`
- Returns a new dictionary with group keys in alphabetical order.
### `group_incidents(incidents, generated_at=None)`
- Builds grouped JSON by province, region, type, and weekday, plus weekday+province, weekday+region, type+province (`by_province_type`), and type+region (`by_region_type`). Unparseable dates go into `unknown`, which is omitted if empty; unknown geographic values use `UNKNOWN_REGION`. The facade adds `region_provinces` with feed provinces by region.
### `find_extremes(groups)`
- For each indicator returns `{max, min}` with name and value. Ties are alphabetical; the minimum ignores zero values and is `None` if no group has a positive value.
### `build_statistics(incidents, level="province", generated_at=None)`
- Accepts only `province` or `region`; groups data and returns level, total, groups, and extremes. An invalid level raises `ValueError`.
### `write_grouped_json(data, path)`
- Creates parent directories, writes UTF-8 JSON with Unicode preserved and two-space indentation, and returns the output path.
## Example
Each group leaf contains all six indicators; this example has no weather events, so the weather minimum is null.
```json
{
  "by_province": {"Madrid": {"total": 2, "accidents": 1, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 2, "accidents": 1, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}},
  "by_weekday": {"monday": {"total": 2, "accidents": 1, "roadworks": 1, "breakdowns": 0, "obstructions": 0, "weather": 0}}
}
```
Classification rules are in [core.indicators](../core/indicators.md). `total` counts every incident; each other indicator applies its predicate to the cause. The maximum can be zero when groups exist and all have zero for that indicator; the minimum ignores those zeroes and is `null` when there are no positive values.
