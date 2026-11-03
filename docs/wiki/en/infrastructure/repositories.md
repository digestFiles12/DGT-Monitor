# dgt_monitor/infrastructure/repositories.py
Implements repositories connecting the XML client to the incident and camera parsers. Each fetch downloads the configured document and parses it.
## Dependencies
Imports core URLs and models, the `XmlClient` port, and `CameraParser`/`IncidentParser`. Bootstrap composes these classes with the real HTTP client.
## Contents
### `DgtIncidentRepository`
- DGT incident repository adapter; stores a client, parser, and URL.
### `DgtIncidentRepository.__init__(self, client: XmlClient, parser: IncidentParser, url: str = DGT_INCIDENTS_URL) -> None`
- Stores the three dependencies, defaulting to the incident URL.
### `DgtIncidentRepository.fetch(self) -> list[Incident]`
- Retrieves XML through the client and returns the result of `IncidentParser.parse`.
### `DgtCameraRepository`
- DGT camera repository adapter.
### `DgtCameraRepository.__init__(self, client: XmlClient, parser: CameraParser, url: str = DGT_CAMERAS_URL) -> None`
- Stores the client, parser, and URL, which defaults to the camera URL.
### `DgtCameraRepository.fetch(self) -> list[Camera]`
- Downloads XML through the client and returns the cameras produced by `CameraParser.parse`.
