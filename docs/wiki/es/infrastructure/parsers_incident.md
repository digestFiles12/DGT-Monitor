# dgt_monitor/infrastructure/parsers/incident.py
Analiza documentos DGT `SituationPublication` y convierte situaciones con registros en modelos `Incident`. Completa etiquetas traducidas y la comunidad autónoma cuando se puede determinar.
## Dependencias
Usa `ElementTree`, `DgtParseError`, `Translator`, `Incident`, funciones de regiones, `TextCleaner` y `Datex2Parser`. `DgtIncidentRepository` consume el parser.
## Contenido
### `IncidentParser`
- Parser de situaciones DGT con traductor y limpiador inyectables.
### `IncidentParser.__init__(self, translator: Translator | None = None, cleaner: TextCleaner | None = None) -> None`
- Conserva las dependencias suministradas o crea instancias predeterminadas de `Translator` y `TextCleaner`.
### `IncidentParser.parse(self, xml_content: str) -> list[Incident]`
- Analiza el XML y convierte errores sintácticos en `DgtParseError`; recorre elementos `situation` y conserva los resultados no nulos de `_parse_one`.
### `IncidentParser._parse_one(self, situation: ET.Element) -> Incident | None`
- Busca un `situationRecord`; si falta devuelve `None`. Extrae sus campos, obtiene tipo del atributo XSI (o `Unknown`), combina causa y detalle disponibles, convierte coordenadas opcionales, resuelve comunidad por provincia y usa el campo `autonomousCommunity` si la provincia no se reconoce. Luego crea el modelo con etiquetas traducidas y campos de la situación/registro.
