# dgt_monitor/infrastructure/parsers/camera.py
Analiza documentos DGT `DevicePublication` y extrae cámaras con URL de imagen. Omite nodos que no coinciden con el tipo de dispositivo esperado o no tienen URL.
## Dependencias
Usa `xml.etree.ElementTree`, `DgtParseError`, el modelo `Camera`, `TextCleaner` y la base `Datex2Parser`. `DgtCameraRepository` invoca este parser.
## Contenido
### `CameraParser`
- Parser de cámaras que hereda las búsquedas XML comunes de `Datex2Parser`.
### `CameraParser.__init__(self, cleaner: TextCleaner | None = None) -> None`
- Usa el limpiador recibido o crea un `TextCleaner` predeterminado.
### `CameraParser.parse(self, xml_content: str) -> list[Camera]`
- Convierte XML a elementos; traduce errores de sintaxis a `DgtParseError`. Recorre nodos que contienen `device`, tienen tipo XSI terminado en `ExtendedDevice` y tipo `camera`; solo agrega cámaras con `deviceUrl`, limpiando carretera y provincia y convirtiendo coordenadas opcionales.
