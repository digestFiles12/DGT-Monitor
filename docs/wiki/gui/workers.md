# dgt_monitor/gui/workers.py
**ES:** Define objetos de trabajo Qt para cargar incidencias, cámaras e imágenes fuera del hilo de la interfaz y comunicar resultados mediante señales.
**EN:** Defines Qt worker objects for loading incidents, cameras, and images outside the UI thread, reporting results through signals.
## Dependencies / Dependencias
`QObject`, `pyqtSignal` y `pyqtSlot` de PyQt6; `requests`; `DgtApplicationService`, `IncidentFilters` y `CameraFilters` del proyecto; `Callable` para inyectar una descarga de imagen.
PyQt6 `QObject`, `pyqtSignal`, and `pyqtSlot`; `requests`; project `DgtApplicationService`, `IncidentFilters`, and `CameraFilters`; `Callable` for an injectable image downloader.
## Contents / Contenido
### `IncidentLoadWorker(QObject)`
Señales `loaded(object)`, `error(str)` y `finished()` informan resultado, error y fin del trabajo.
Signals `loaded(object)`, `error(str)`, and `finished()` report the result, error, and completion.
#### `__init__(service: DgtApplicationService, filters: IncidentFilters) -> None`
- **ES:** Guarda el servicio y los filtros que usará el worker.
- **EN:** Stores the service and filters the worker will use.
#### `run() -> None`
- **ES:** Obtiene el payload de incidencias y lo emite; emite el mensaje de cualquier excepción y siempre emite `finished`.
- **EN:** Gets and emits the incident payload; emits any exception message and always emits `finished`.
### `CameraLoadWorker(QObject)`
Señales `loaded(object)`, `error(str)` y `finished()` comunican el resultado, error y finalización.
Signals `loaded(object)`, `error(str)`, and `finished()` communicate the result, error, and completion.
#### `__init__(service: DgtApplicationService, filters: CameraFilters) -> None`
- **ES:** Guarda el servicio y filtros de cámaras para la consulta.
- **EN:** Stores the service and camera filters for the query.
#### `run() -> None`
- **ES:** Solicita cámaras al servicio y emite datos, error si ocurre una excepción y siempre `finished`.
- **EN:** Requests cameras from the service and emits data, an error if an exception occurs, and always `finished`.
### `ImageLoadWorker(QObject)`
Sus señales `loaded(str, object)`, `error(str, str)` y `finished()` incluyen URL/datos o mensaje de error.
Its `loaded(str, object)`, `error(str, str)`, and `finished()` signals carry the URL/data or error message.
#### `__init__(url: str, downloader: Callable[[str], bytes] | None = None) -> None`
- **ES:** Guarda la URL y usa el descargador inyectado o el método `_download` predeterminado.
- **EN:** Stores the URL and uses the injected downloader or the default `_download` method.
#### `run() -> None`
- **ES:** Descarga la imagen y emite URL y bytes; ante excepción emite URL y error, y al final `finished`.
- **EN:** Downloads the image and emits URL and bytes; on exception emits URL and error, then always emits `finished`.
#### `_download(url: str) -> bytes`
- **ES:** Hace un GET con timeout de 8 segundos, exige respuesta HTTP satisfactoria y devuelve el contenido.
- **EN:** Makes a GET with an 8-second timeout, requires a successful HTTP response, and returns its content.
