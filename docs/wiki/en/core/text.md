# dgt_monitor/core/text.py
Collects utilities for correcting selected encoding glitches, matching text, normalizing road names, and extracting kilometer points. These helpers are shared by parsers and services.
## Dependencies
Imports `re` from the standard library. Parsers use `TextCleaner`; other components can use the matching and normalization functions.
## Contents
### `TextCleaner`
- Text cleaner with an internal replacement table for selected mis-decoded sequences.
### `TextCleaner._replacements`
- Private table of nine malformed sequences and their intended accented characters.
### `TextCleaner.clean(self, value: str | None) -> str`
- Replaces known sequences; if given `None`, operates on an empty string.
### `matches_text(value: str | None, needle: str | None, mode: str = "contains") -> bool`
- Returns `True` when there is no search term; `exact` compares case-insensitively, `regex` evaluates a regular expression and returns `False` if invalid, and other modes perform a case-insensitive substring search.
### `normalize_road(value: str | None) -> str`
- Converts to uppercase and removes every character that is not an ASCII letter or digit.
### `parse_kilometer_point(value: str | None) -> float | None`
- Parses numeric values with comma or dot decimals and `km+meters` notation (adding meters as thousandths); returns `None` when no number is found.
