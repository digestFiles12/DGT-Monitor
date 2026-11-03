# dgt_monitor/gui/workers.py
Define objetos de trabajo Qt para cargar incidencias, cámaras e imágenes fuera del hilo de la interfaz y comunicar resultados mediante señales.
## Dependencias
`QObject`, `pyqtSignal` y `pyqtSlot` de PyQt6; `requests`; `DgtApplicationService`, `IncidentFilters` y `CameraFilters` del proyecto; `Callable` para inyectar una descarga de imagen.
## Contenido
### `IncidentLoadWorker(QObject)`
Señales `loaded(object)`, `error(str)` y `finished()` informan resultado, error y fin del trabajo.
Signals `loaded(object)`, `error(str)`, and `finished()` report the result, error, and completion.
#### `__init__(service: DgtApplicationService, filters: IncidentFilters) -> None`
- Guarda el servicio y los filtros que usará el worker.
#### `run() -> None`
- Obtiene el payload de incidencias y lo emite; emite el mensaje de cualquier excepción y siempre emite `finished`.
### `CameraLoadWorker(QObject)`
Señales `loaded(object)`, `error(str)` y `finished()` comunican el resultado, error y finalización.
Signals `loaded(object)`, `error(str)`, and `finished()` communicate the result, error, and completion.
#### `__init__(service: DgtApplicationService, filters: CameraFilters) -> None`
- Guarda el servicio y filtros de cámaras para la consulta.
#### `run() -> None`
- Solicita cámaras al servicio y emite datos, error si ocurre una excepción y siempre `finished`.
### `ImageLoadWorker(QObject)`
Sus señales `loaded(str, object)`, `error(str, str)` y `finished()` incluyen URL/datos o mensaje de error.
Its `loaded(str, object)`, `error(str, str)`, and `finished()` signals carry the URL/data or error message.
#### `__init__(url: str, downloader: Callable[[str], bytes] | None = None) -> None`
- Guarda la URL y usa el descargador inyectado o el método `_download` predeterminado.
#### `run() -> None`
- Descarga la imagen y emite URL y bytes; ante excepción emite URL y error, y al final `finished`.
#### `_download(url: str) -> bytes`
- Hace un GET con timeout de 8 segundos, exige respuesta HTTP satisfactoria y devuelve el contenido.
