# dgt_monitor/infrastructure/parsers/incident.py
Parses DGT `SituationPublication` documents and converts situations containing records into `Incident` models. It fills translated labels and the autonomous community when determinable.
## Dependencies
Uses `ElementTree`, `DgtParseError`, `Translator`, `Incident`, region functions, `TextCleaner`, and `Datex2Parser`. `DgtIncidentRepository` uses this parser.
## Contents
### `IncidentParser`
- DGT situation parser with injectable translator and cleaner.
### `IncidentParser.__init__(self, translator: Translator | None = None, cleaner: TextCleaner | None = None) -> None`
- Stores the supplied dependencies or creates default `Translator` and `TextCleaner` instances.
### `IncidentParser.parse(self, xml_content: str) -> list[Incident]`
- Parses the XML and converts syntax errors into `DgtParseError`; traverses `situation` elements and keeps non-null results from `_parse_one`.
### `IncidentParser._parse_one(self, situation: ET.Element) -> Incident | None`
- Looks for a `situationRecord`; returns `None` if absent. Extracts its fields, gets the type from the XSI attribute (or `Unknown`), combines available cause and detail, parses optional coordinates, resolves community by province, and uses `autonomousCommunity` when the province is unknown. It then builds the model with translated labels and situation/record fields.
