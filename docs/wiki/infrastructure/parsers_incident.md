# dgt_monitor/infrastructure/parsers/incident.py
**ES:** Analiza documentos DGT `SituationPublication` y convierte situaciones con registros en modelos `Incident`. Completa etiquetas traducidas y la comunidad autónoma cuando se puede determinar.
**EN:** Parses DGT `SituationPublication` documents and converts situations containing records into `Incident` models. It fills translated labels and the autonomous community when determinable.
## Dependencies / Dependencias
Usa `ElementTree`, `DgtParseError`, `Translator`, `Incident`, funciones de regiones, `TextCleaner` y `Datex2Parser`. `DgtIncidentRepository` consume el parser.
## Contents / Contenido
### `IncidentParser`
- **ES:** Parser de situaciones DGT con traductor y limpiador inyectables.
- **EN:** DGT situation parser with injectable translator and cleaner.
### `IncidentParser.__init__(self, translator: Translator | None = None, cleaner: TextCleaner | None = None) -> None`
- **ES:** Conserva las dependencias suministradas o crea instancias predeterminadas de `Translator` y `TextCleaner`.
- **EN:** Stores the supplied dependencies or creates default `Translator` and `TextCleaner` instances.
### `IncidentParser.parse(self, xml_content: str) -> list[Incident]`
- **ES:** Analiza el XML y convierte errores sintácticos en `DgtParseError`; recorre elementos `situation` y conserva los resultados no nulos de `_parse_one`.
- **EN:** Parses the XML and converts syntax errors into `DgtParseError`; traverses `situation` elements and keeps non-null results from `_parse_one`.
### `IncidentParser._parse_one(self, situation: ET.Element) -> Incident | None`
- **ES:** Busca un `situationRecord`; si falta devuelve `None`. Extrae sus campos, obtiene tipo del atributo XSI (o `Unknown`), combina causa y detalle disponibles, convierte coordenadas opcionales, resuelve comunidad por provincia y usa el campo `autonomousCommunity` si la provincia no se reconoce. Luego crea el modelo con etiquetas traducidas y campos de la situación/registro.
- **EN:** Looks for a `situationRecord`; returns `None` if absent. Extracts its fields, gets the type from the XSI attribute (or `Unknown`), combines available cause and detail, parses optional coordinates, resolves community by province, and uses `autonomousCommunity` when the province is unknown. It then builds the model with translated labels and situation/record fields.
