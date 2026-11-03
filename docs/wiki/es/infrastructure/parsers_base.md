# dgt_monitor/infrastructure/parsers/base.py
Proporciona utilidades XML independientes del espacio de nombres para los parsers DATEX2. Las búsquedas recorren el elemento proporcionado y sus descendientes.
## Dependencias
Importa `Element` de `xml.etree.ElementTree` y no depende de otros módulos del proyecto. `CameraParser` e `IncidentParser` heredan de esta clase.
## Contenido
### `Datex2Parser`
- Clase base de utilidades estáticas para recorrer nodos XML.
### `Datex2Parser.text(parent: Element, tag_name: str) -> str`
- Devuelve el texto del primer descendiente cuyo nombre de etiqueta termina con `tag_name`; si no lo encuentra o el texto es nulo, devuelve `""`.
### `Datex2Parser.element(parent: Element, tag_name: str) -> Element | None`
- Devuelve el primer elemento descendiente cuya etiqueta termina con el nombre indicado; si no hay coincidencia devuelve `None`.
### `Datex2Parser.optional_float(value: str) -> float | None`
- Convierte una cadena no vacía a `float`; devuelve `None` para cadena vacía o valor no numérico.
