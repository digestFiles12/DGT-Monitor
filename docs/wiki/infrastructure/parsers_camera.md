# dgt_monitor/infrastructure/parsers/camera.py
**ES:** Analiza documentos DGT `DevicePublication` y extrae cámaras con URL de imagen. Omite nodos que no coinciden con el tipo de dispositivo esperado o no tienen URL.
**EN:** Parses DGT `DevicePublication` documents and extracts cameras with an image URL. It skips nodes that do not match the expected device type or lack a URL.
## Dependencies / Dependencias
Usa `xml.etree.ElementTree`, `DgtParseError`, el modelo `Camera`, `TextCleaner` y la base `Datex2Parser`. `DgtCameraRepository` invoca este parser.
## Contents / Contenido
### `CameraParser`
- **ES:** Parser de cámaras que hereda las búsquedas XML comunes de `Datex2Parser`.
- **EN:** Camera parser inheriting common XML searches from `Datex2Parser`.
### `CameraParser.__init__(self, cleaner: TextCleaner | None = None) -> None`
- **ES:** Usa el limpiador recibido o crea un `TextCleaner` predeterminado.
- **EN:** Uses the supplied cleaner or creates a default `TextCleaner`.
### `CameraParser.parse(self, xml_content: str) -> list[Camera]`
- **ES:** Convierte XML a elementos; traduce errores de sintaxis a `DgtParseError`. Recorre nodos que contienen `device`, tienen tipo XSI terminado en `ExtendedDevice` y tipo `camera`; solo agrega cámaras con `deviceUrl`, limpiando carretera y provincia y convirtiendo coordenadas opcionales.
- **EN:** Parses XML elements and translates syntax errors into `DgtParseError`. It selects nodes containing `device` with an XSI type ending in `ExtendedDevice` and device type `camera`; it adds only cameras with `deviceUrl`, cleaning road and province and parsing optional coordinates.
