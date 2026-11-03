# dgt_monitor/infrastructure/parsers/camera.py
Parses DGT `DevicePublication` documents and extracts cameras with an image URL. It skips nodes that do not match the expected device type or lack a URL.
## Dependencies
Uses `xml.etree.ElementTree`, `DgtParseError`, the `Camera` model, `TextCleaner`, and the `Datex2Parser` base class. `DgtCameraRepository` calls this parser.
## Contents
### `CameraParser`
- Camera parser inheriting common XML searches from `Datex2Parser`.
### `CameraParser.__init__(self, cleaner: TextCleaner | None = None) -> None`
- Uses the supplied cleaner or creates a default `TextCleaner`.
### `CameraParser.parse(self, xml_content: str) -> list[Camera]`
- Parses XML elements and translates syntax errors into `DgtParseError`. It selects nodes containing `device` with an XSI type ending in `ExtendedDevice` and device type `camera`; it adds only cameras with `deviceUrl`, cleaning road and province and parsing optional coordinates.
