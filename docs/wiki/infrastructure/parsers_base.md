# dgt_monitor/infrastructure/parsers/base.py
**ES:** Proporciona utilidades XML independientes del espacio de nombres para los parsers DATEX2. Las búsquedas recorren el elemento proporcionado y sus descendientes.
**EN:** Provides namespace-independent XML utilities for DATEX2 parsers. Searches traverse the supplied element and its descendants.
## Dependencies / Dependencias
Importa `Element` de `xml.etree.ElementTree` y no depende de otros módulos del proyecto. `CameraParser` e `IncidentParser` heredan de esta clase.
## Contents / Contenido
### `Datex2Parser`
- **ES:** Clase base de utilidades estáticas para recorrer nodos XML.
- **EN:** Base class of static helpers for traversing XML nodes.
### `Datex2Parser.text(parent: Element, tag_name: str) -> str`
- **ES:** Devuelve el texto del primer descendiente cuyo nombre de etiqueta termina con `tag_name`; si no lo encuentra o el texto es nulo, devuelve `""`.
- **EN:** Returns the text of the first descendant whose tag name ends with `tag_name`; returns `""` if none is found or its text is null.
### `Datex2Parser.element(parent: Element, tag_name: str) -> Element | None`
- **ES:** Devuelve el primer elemento descendiente cuya etiqueta termina con el nombre indicado; si no hay coincidencia devuelve `None`.
- **EN:** Returns the first descendant element whose tag ends with the supplied name; returns `None` if there is no match.
### `Datex2Parser.optional_float(value: str) -> float | None`
- **ES:** Convierte una cadena no vacía a `float`; devuelve `None` para cadena vacía o valor no numérico.
- **EN:** Converts a non-empty string to `float`; returns `None` for an empty or non-numeric value.
