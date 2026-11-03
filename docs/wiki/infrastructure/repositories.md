# dgt_monitor/infrastructure/repositories.py
**ES:** Implementa los repositorios que conectan el cliente XML con los parsers específicos de incidencias y cámaras. Cada lectura descarga el documento configurado y lo analiza.
**EN:** Implements repositories connecting the XML client to the incident and camera parsers. Each fetch downloads the configured document and parses it.
## Dependencies / Dependencias
Importa las URLs y modelos del núcleo, el puerto `XmlClient` y `CameraParser`/`IncidentParser`. Bootstrap compone estas clases con el cliente HTTP real.
## Contents / Contenido
### `DgtIncidentRepository`
- **ES:** Adaptador del repositorio de incidencias DGT; conserva cliente, parser y URL.
- **EN:** DGT incident repository adapter; stores a client, parser, and URL.
### `DgtIncidentRepository.__init__(self, client: XmlClient, parser: IncidentParser, url: str = DGT_INCIDENTS_URL) -> None`
- **ES:** Guarda las tres dependencias, usando por defecto la URL de incidencias.
- **EN:** Stores the three dependencies, defaulting to the incident URL.
### `DgtIncidentRepository.fetch(self) -> list[Incident]`
- **ES:** Obtiene el XML mediante el cliente y devuelve el resultado de `IncidentParser.parse`.
- **EN:** Retrieves XML through the client and returns the result of `IncidentParser.parse`.
### `DgtCameraRepository`
- **ES:** Adaptador del repositorio de cámaras DGT.
- **EN:** DGT camera repository adapter.
### `DgtCameraRepository.__init__(self, client: XmlClient, parser: CameraParser, url: str = DGT_CAMERAS_URL) -> None`
- **ES:** Guarda cliente, parser y URL, que por defecto es la de cámaras.
- **EN:** Stores the client, parser, and URL, which defaults to the camera URL.
### `DgtCameraRepository.fetch(self) -> list[Camera]`
- **ES:** Descarga el XML mediante el cliente y devuelve las cámaras producidas por `CameraParser.parse`.
- **EN:** Downloads XML through the client and returns the cameras produced by `CameraParser.parse`.
