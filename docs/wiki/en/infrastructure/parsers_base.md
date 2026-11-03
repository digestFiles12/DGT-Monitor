# dgt_monitor/infrastructure/parsers/base.py
Provides namespace-independent XML utilities for DATEX2 parsers. Searches traverse the supplied element and its descendants.
## Dependencies
Imports `Element` from `xml.etree.ElementTree` and has no dependencies on other project modules. `CameraParser` and `IncidentParser` inherit from this class.
## Contents
### `Datex2Parser`
- Base class of static helpers for traversing XML nodes.
### `Datex2Parser.text(parent: Element, tag_name: str) -> str`
- Returns the text of the first descendant whose tag name ends with `tag_name`; returns `""` if none is found or its text is null.
### `Datex2Parser.element(parent: Element, tag_name: str) -> Element | None`
- Returns the first descendant element whose tag ends with the supplied name; returns `None` if there is no match.
### `Datex2Parser.optional_float(value: str) -> float | None`
- Converts a non-empty string to `float`; returns `None` for an empty or non-numeric value.
