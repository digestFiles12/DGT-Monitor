# dgt_monitor/core/regions.py
Maps Spanish province names to autonomous communities while tolerating accents, bilingual variants, and aliases found in the data. Unrecognized names produce a one-time warning and the value `Unknown`.
## Dependencies
Uses `logging`, `re`, and `unicodedata` from the standard library. `IncidentParser` uses `region_for_province` to fill in the community.
## Contents
### `UNKNOWN_REGION`
- Sentinel value (`"Unknown"`) for unrecognized provinces.
### `PROVINCE_TO_REGION`, `EXTRA_ALIASES`
- Static tables: the first maps canonical provinces to communities, and the second maps spelling variants to a canonical province.
### `_warned_names`
- Private set used to avoid repeating warnings for the same unknown name.
### `normalize_province_name(name: str) -> str`
- Produces a lookup key in lowercase, without accent marks or punctuation, and with normalized spaces.
### `_build_lookup() -> dict[str, str]`
- Builds the normalized index for canonical provinces, individual sides of slash-separated names, and aliases.
### `_LOOKUP`
- Private index built at module import time by `_build_lookup`.
### `region_for_province(name: str) -> str`
- Returns the community for the normalized province; returns `Unknown` when there is no match and warns only once per non-empty unknown name.
