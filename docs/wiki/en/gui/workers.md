# dgt_monitor/gui/workers.py
Defines Qt worker objects for loading incidents, cameras, and images outside the UI thread, reporting results through signals.
## Dependencies
PyQt6 `QObject`, `pyqtSignal`, and `pyqtSlot`; `requests`; project `DgtApplicationService`, `IncidentFilters`, and `CameraFilters`; `Callable` for an injectable image downloader.
## Contents
### `IncidentLoadWorker(QObject)`
Señales `loaded(object)`, `error(str)` y `finished()` informan resultado, error y fin del trabajo.
Signals `loaded(object)`, `error(str)`, and `finished()` report the result, error, and completion.
#### `__init__(service: DgtApplicationService, filters: IncidentFilters) -> None`
- Stores the service and filters the worker will use.
#### `run() -> None`
- Gets and emits the incident payload; emits any exception message and always emits `finished`.
### `CameraLoadWorker(QObject)`
Señales `loaded(object)`, `error(str)` y `finished()` comunican el resultado, error y finalización.
Signals `loaded(object)`, `error(str)`, and `finished()` communicate the result, error, and completion.
#### `__init__(service: DgtApplicationService, filters: CameraFilters) -> None`
- Stores the service and camera filters for the query.
#### `run() -> None`
- Requests cameras from the service and emits data, an error if an exception occurs, and always `finished`.
### `ImageLoadWorker(QObject)`
Sus señales `loaded(str, object)`, `error(str, str)` y `finished()` incluyen URL/datos o mensaje de error.
Its `loaded(str, object)`, `error(str, str)`, and `finished()` signals carry the URL/data or error message.
#### `__init__(url: str, downloader: Callable[[str], bytes] | None = None) -> None`
- Stores the URL and uses the injected downloader or the default `_download` method.
#### `run() -> None`
- Downloads the image and emits URL and bytes; on exception emits URL and error, then always emits `finished`.
#### `_download(url: str) -> bytes`
- Makes a GET with an 8-second timeout, requires a successful HTTP response, and returns its content.
