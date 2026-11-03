# dgt_monitor/gui/dialogs/cameras.py
**ES:** Implementa el diálogo no modal de cámaras cercanas a una incidencia, la carga asíncrona de imágenes y un visor de imagen a pantalla completa.
**EN:** Implements a non-modal dialog for cameras near an incident, asynchronous image loading, and a fullscreen image viewer.
## Dependencies / Dependencias
PyQt6 Core/Gui/Widgets, `Callable`, `Any`, `DgtApplicationService`, `CAMERA_MATCH_RANGE_KM`, `CameraFilters`, utilidades de tema y `CameraLoadWorker`/`ImageLoadWorker`.
PyQt6 Core/Gui/Widgets, `Callable`, `Any`, `DgtApplicationService`, `CAMERA_MATCH_RANGE_KM`, `CameraFilters`, theme utilities, and `CameraLoadWorker`/`ImageLoadWorker`.
## Contents / Contenido
### `CamerasDialog(QDialog)`
- **ES:** Diálogo no modal que lista cámaras cercanas y sus imágenes. Señales `load_completed`, `image_loaded(str)` e `image_fullscreen_opened()` informan de cargas y aperturas de imagen.
- **EN:** Non-modal dialog listing nearby cameras and their images. `load_completed`, `image_loaded(str)`, and `image_fullscreen_opened()` signals report loading and image-viewer events.
#### `__init__(self, service: DgtApplicationService, incident: dict[str, Any], parent: QWidget | None = None, autoload: bool = True, image_downloader: Callable[[str], bytes] | None = None, theme: str = "light") -> None`
- **ES:** Guarda servicio/incidencia y estado de tareas, configura la ventana, construye/aplica tema y opcionalmente carga cámaras.
- **EN:** Stores the service/incident and job state, configures the window, builds/applies the theme, and optionally loads cameras.
#### `items(self) -> list[dict[str, Any]]`
- **ES:** Propiedad que devuelve una copia superficial de la lista de cámaras cargada.
- **EN:** Property returning a shallow copy of the loaded camera list.
#### `reload() -> None`
- **ES:** Evita cargas concurrentes, limpia tarjetas, crea un `CameraLoadWorker` en un hilo Qt y conecta sus señales.
- **EN:** Avoids concurrent loads, clears cards, creates a `CameraLoadWorker` in a Qt thread, and connects its signals.
#### `_build_ui() -> None`
- **ES:** Construye cabecera con título/ubicación, botones de actualizar/tema y un área desplazable de tarjetas.
- **EN:** Builds a header with title/location, refresh/theme buttons, and a scrollable card area.
#### `_filters() -> CameraFilters`
- **ES:** Construye filtros desde provincia, carretera, PK y coordenadas de la incidencia, con límite 12 y rango `CAMERA_MATCH_RANGE_KM`.
- **EN:** Builds filters from the incident's province, road, kilometer point, and coordinates, with limit 12 and `CAMERA_MATCH_RANGE_KM` range.
#### `_apply_payload(payload: object) -> None`
- **ES:** Extrae cámaras del payload, reemplaza tarjetas y actualiza el mensaje con el número encontrado.
- **EN:** Extracts cameras from the payload, replaces cards, and updates the status with the number found.
#### `_camera_card(camera: dict[str, Any]) -> QFrame`
- **ES:** Construye tarjeta de carretera/PK/metadatos e imagen; inicia descarga si hay `image_url`.
- **EN:** Builds a road/PK/metadata and image card; starts a download when `image_url` exists.
#### `_empty_card(message: str) -> QFrame`
- **ES:** Crea una tarjeta sencilla con un mensaje multilínea.
- **EN:** Creates a simple card with a word-wrapped message.
#### `_show_error(message: str) -> None`
- **ES:** Limpia el resultado, muestra el mensaje de error en una tarjeta y actualiza el estado.
- **EN:** Clears results, shows the error in a card, and updates the status.
#### `_load_finished() -> None`
- **ES:** Reactiva actualizar, programa la eliminación de worker/hilo, limpia referencias y emite `load_completed`.
- **EN:** Re-enables refresh, schedules worker/thread deletion, clears references, and emits `load_completed`.
#### `toggle_theme() -> None`
- **ES:** Alterna al tema opuesto.
- **EN:** Switches to the opposite theme.
#### `set_theme(theme: str) -> None`
- **ES:** Normaliza el nombre del tema, actualiza el botón y aplica el estilo.
- **EN:** Normalizes the theme name, updates the button, and applies the stylesheet.
#### `_sync_theme_button() -> None`
- **ES:** Cambia el texto del botón para ofrecer el tema alternativo.
- **EN:** Sets the button text to offer the alternate theme.
#### `_load_image(url: str, label: QLabel) -> None`
- **ES:** Ejecuta `ImageLoadWorker` en un hilo, conecta éxito/error con la etiqueta y registra la tarea para limpiarla.
- **EN:** Runs `ImageLoadWorker` in a thread, connects success/error to the label, and tracks the job for cleanup.
#### `_apply_image(url: str, payload: object, label: QLabel) -> None`
- **ES:** Decodifica bytes en `QPixmap`, muestra imagen escalada y habilita clic para ampliarla; emite `image_loaded`.
- **EN:** Decodes bytes into `QPixmap`, displays a scaled image and enables click-to-enlarge; emits `image_loaded`.
#### `_fullscreen_click_handler(pixmap: QPixmap)`
- **ES:** Devuelve el manejador de clic que abre el `pixmap` en pantalla completa.
- **EN:** Returns a click handler that opens the `pixmap` fullscreen.
#### `open_fullscreen(_event) -> None` (función interna)
- **ES:** Llama a `_open_fullscreen_image` con la imagen capturada por el manejador.
- **EN:** Calls `_open_fullscreen_image` with the image captured by the handler.
#### `_open_fullscreen_image(pixmap: QPixmap) -> QDialog`
- **ES:** Crea y registra el diálogo de imagen, lo muestra y emite `image_fullscreen_opened`.
- **EN:** Creates and tracks the image dialog, shows it, and emits `image_fullscreen_opened`.
#### `_show_fullscreen_dialog(dialog: QDialog) -> None`
- **ES:** Muestra el diálogo con `showFullScreen()`.
- **EN:** Shows the dialog with `showFullScreen()`.
#### `_forget_fullscreen_dialog(dialog: QDialog) -> None`
- **ES:** Retira el diálogo destruido de la lista de diálogos abiertos.
- **EN:** Removes the destroyed dialog from the list of open dialogs.
#### `_forget_image_job(item: tuple[QThread, ImageLoadWorker]) -> None`
- **ES:** Retira una tarea terminada y programa la eliminación de su worker y su hilo.
- **EN:** Removes a completed job and schedules deletion of its worker and thread.
#### `_clear_cards() -> None`
- **ES:** Detiene y espera brevemente los hilos de imagen, elimina referencias a tareas y retira tarjetas existentes.
- **EN:** Stops and briefly waits for image threads, clears job references, and removes existing cards.
#### `closeEvent(event) -> None`
- **ES:** Cierra visores abiertos, solicita terminar los hilos de cámaras/imágenes y continúa el cierre Qt.
- **EN:** Closes open viewers, asks camera/image threads to stop, and continues Qt close handling.
#### `_title_for_incident() -> str`
- **ES:** Forma el título usando carretera y, si existe, punto kilométrico de la incidencia.
- **EN:** Builds the title from the incident road and, when present, kilometer point.
#### `_subtitle_for_incident() -> str`
- **ES:** Devuelve municipio/provincia o un texto que describe los criterios de búsqueda.
- **EN:** Returns municipality/province or text describing the search criteria.
#### `_camera_meta(camera: dict[str, Any]) -> str`
- **ES:** Une provincia y diferencias de PK/distancia disponibles en una línea.
- **EN:** Joins the available province and kilometer/distance differences into one line.
#### `_clean(value: object) -> str | None`
- **ES:** Convierte valores no nulos a texto recortado y devuelve `None` si queda vacío.
- **EN:** Converts non-null values to trimmed text and returns `None` when empty.
#### `_apply_style() -> None`
- **ES:** Aplica la hoja de estilo de diálogo para el tema actual.
- **EN:** Applies the dialog stylesheet for the current theme.

### `_FullscreenImageDialog(QDialog)`
- **ES:** Diálogo de pantalla completa que muestra un `QPixmap` ajustado a sus dimensiones.
- **EN:** Fullscreen dialog displaying a `QPixmap` scaled to its dimensions.
#### `__init__(pixmap: QPixmap, parent: QWidget | None = None) -> None`
- **ES:** Guarda la imagen, crea una etiqueta centrada y sincroniza su tamaño inicial.
- **EN:** Stores the image, creates a centered label, and synchronizes its initial size.
#### `resizeEvent(event) -> None`
- **ES:** Delega el evento de redimensionado y vuelve a escalar la imagen.
- **EN:** Delegates the resize event and rescales the image.
#### `keyPressEvent(event) -> None`
- **ES:** Cierra con Escape; para otras teclas usa el comportamiento base.
- **EN:** Closes on Escape; delegates other keys to the base behavior.
#### `mousePressEvent(event) -> None`
- **ES:** Cierra al recibir un clic y después llama al manejador base.
- **EN:** Closes on a mouse press and then calls the base handler.
#### `_sync_pixmap() -> None`
- **ES:** Si la ventana tiene dimensiones positivas, escala el pixmap manteniendo proporción y suavizado.
- **EN:** If the window has positive dimensions, scales the pixmap with aspect ratio and smooth transformation preserved.


