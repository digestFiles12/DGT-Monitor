# dgt_monitor/application/statistics.py
Computes incident indicators, geographic/temporal groupings, per-group extremes, and JSON export.
## Dependencies
Uses `Incident` and the province-to-region mapping from `core`; `DgtApplicationService` and `menu.py` consume its calculations. It also uses the standard library for dates, JSON, and paths.
## Contents
### `INDICATORS`, `WEEKDAYS`, `DEFAULT_GROUPED_JSON`
- Constants for the ordered four indicator names, the seven English weekday names, and the default JSON filename (`grouped_incidents.json`).
### `is_severe(incident)`
- Returns `True` only when severity, case-insensitively, is `highest`.
### `is_roadworks(incident)`
- Returns `True` if the cause contains `roadworks` or `maintenance`, case-insensitively.
### `is_road_closure(incident)`
- Returns `True` when `management_type` is exactly `roadClosed` or `carriagewayClosures`.
### `count_indicators(incidents)`
- Iterates over an iterable and returns four counts: all incidents, severe incidents, roadworks, and road closures; the latter three use their predicate functions.
### `weekday_of(incident)`
- Tries the ISO start time; if missing or invalid, tries the creation time. Returns a lowercase English weekday or `None` if neither can be parsed.
### `_empty_leaf()`
- Creates an indicator dictionary initialized to zero.
### `_add_incident(groups, key, incident)`
- Creates the group leaf if absent and increments total, severe, roadworks, and closures according to the indicator rules.
### `_sorted_groups(groups)`
- Returns a new dictionary with group keys in alphabetical order.
### `group_incidents(incidents, generated_at=None)`
- Builds grouped JSON by province, region, type, and weekday, plus weekday+province and weekday+region. Unparseable dates go into `unknown`, which is omitted if empty; unknown geographic values use `UNKNOWN_REGION`.
### `find_extremes(groups)`
- For each indicator returns `{max, min}` with name and value. Ties are alphabetical; the minimum ignores zero values and is `None` if no positive group exists.
### `build_statistics(incidents, level="province", generated_at=None)`
- Accepts only `province` or `region`; groups data and returns level, total, groups, and extremes. An invalid level raises `ValueError`.
### `write_grouped_json(data, path)`
- Creates parent directories, writes UTF-8 JSON with Unicode preserved and two-space indentation, and returns the output path.
## Example
Each group leaf contains all four indicators; this example shows leaves by province, region, and weekday.
```json
{
  "by_province": {"Madrid": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}},
  "by_region": {"Comunidad de Madrid": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}},
  "by_weekday": {"monday": {"total": 2, "severe": 1, "roadworks": 1, "road_closures": 0}}
}
```
Indicator rules: `total` counts every incident; `severe` requires `highest` severity; `roadworks` looks for `roadworks` or `maintenance` in the cause; `road_closures` requires `management_type` to be exactly `roadClosed` or `carriagewayClosures`. The maximum is the largest value and the minimum is the smallest positive value (zero-valued groups are ignored); ties are resolved alphabetically.
