# dgt_monitor/infrastructure/repositories.py
Implementa los repositorios que conectan el cliente XML con los parsers específicos de incidencias y cámaras. Cada lectura descarga el documento configurado y lo analiza.
## Dependencias
Importa las URLs y modelos del núcleo, el puerto `XmlClient` y `CameraParser`/`IncidentParser`. Bootstrap compone estas clases con el cliente HTTP real.
## Contenido
### `DgtIncidentRepository`
- Adaptador del repositorio de incidencias DGT; conserva cliente, parser y URL.
### `DgtIncidentRepository.__init__(self, client: XmlClient, parser: IncidentParser, url: str = DGT_INCIDENTS_URL) -> None`
- Guarda las tres dependencias, usando por defecto la URL de incidencias.
### `DgtIncidentRepository.fetch(self) -> list[Incident]`
- Obtiene el XML mediante el cliente y devuelve el resultado de `IncidentParser.parse`.
### `DgtCameraRepository`
- Adaptador del repositorio de cámaras DGT.
### `DgtCameraRepository.__init__(self, client: XmlClient, parser: CameraParser, url: str = DGT_CAMERAS_URL) -> None`
- Guarda cliente, parser y URL, que por defecto es la de cámaras.
### `DgtCameraRepository.fetch(self) -> list[Camera]`
- Descarga el XML mediante el cliente y devuelve las cámaras producidas por `CameraParser.parse`.
