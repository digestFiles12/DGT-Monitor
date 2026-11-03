# dgt_monitor/gui/dialogs/cameras.py
Implementa el diálogo no modal de cámaras cercanas a una incidencia, la carga asíncrona de imágenes y un visor de imagen a pantalla completa.
## Dependencias
PyQt6 Core/Gui/Widgets, `Callable`, `Any`, `DgtApplicationService`, `CAMERA_MATCH_RANGE_KM`, `CameraFilters`, utilidades de tema y `CameraLoadWorker`/`ImageLoadWorker`.
## Contenido
### `CamerasDialog(QDialog)`
- Diálogo no modal que lista cámaras cercanas y sus imágenes. Señales `load_completed`, `image_loaded(str)` e `image_fullscreen_opened()` informan de cargas y aperturas de imagen.
#### `__init__(self, service: DgtApplicationService, incident: dict[str, Any], parent: QWidget | None = None, autoload: bool = True, image_downloader: Callable[[str], bytes] | None = None, theme: str = "light") -> None`
- Guarda servicio/incidencia y estado de tareas, configura la ventana, construye/aplica tema y opcionalmente carga cámaras.
#### `items(self) -> list[dict[str, Any]]`
- Propiedad que devuelve una copia superficial de la lista de cámaras cargada.
#### `reload() -> None`
- Evita cargas concurrentes, limpia tarjetas, crea un `CameraLoadWorker` en un hilo Qt y conecta sus señales.
#### `_build_ui() -> None`
- Construye cabecera con título/ubicación, botones de actualizar/tema y un área desplazable de tarjetas.
#### `_filters() -> CameraFilters`
- Construye filtros desde provincia, carretera, PK y coordenadas de la incidencia, con límite 12 y rango `CAMERA_MATCH_RANGE_KM`.
#### `_apply_payload(payload: object) -> None`
- Extrae cámaras del payload, reemplaza tarjetas y actualiza el mensaje con el número encontrado.
#### `_camera_card(camera: dict[str, Any]) -> QFrame`
- Construye tarjeta de carretera/PK/metadatos e imagen; inicia descarga si hay `image_url`.
#### `_empty_card(message: str) -> QFrame`
- Crea una tarjeta sencilla con un mensaje multilínea.
#### `_show_error(message: str) -> None`
- Limpia el resultado, muestra el mensaje de error en una tarjeta y actualiza el estado.
#### `_load_finished() -> None`
- Reactiva actualizar, programa la eliminación de worker/hilo, limpia referencias y emite `load_completed`.
#### `toggle_theme() -> None`
- Alterna al tema opuesto.
#### `set_theme(theme: str) -> None`
- Normaliza el nombre del tema, actualiza el botón y aplica el estilo.
#### `_sync_theme_button() -> None`
- Cambia el texto del botón para ofrecer el tema alternativo.
#### `_load_image(url: str, label: QLabel) -> None`
- Ejecuta `ImageLoadWorker` en un hilo, conecta éxito/error con la etiqueta y registra la tarea para limpiarla.
#### `_apply_image(url: str, payload: object, label: QLabel) -> None`
- Decodifica bytes en `QPixmap`, muestra imagen escalada y habilita clic para ampliarla; emite `image_loaded`.
#### `_fullscreen_click_handler(pixmap: QPixmap)`
- Devuelve el manejador de clic que abre el `pixmap` en pantalla completa.
#### `open_fullscreen(_event) -> None` (función interna)
- Llama a `_open_fullscreen_image` con la imagen capturada por el manejador.
#### `_open_fullscreen_image(pixmap: QPixmap) -> QDialog`
- Crea y registra el diálogo de imagen, lo muestra y emite `image_fullscreen_opened`.
#### `_show_fullscreen_dialog(dialog: QDialog) -> None`
- Muestra el diálogo con `showFullScreen()`.
#### `_forget_fullscreen_dialog(dialog: QDialog) -> None`
- Retira el diálogo destruido de la lista de diálogos abiertos.
#### `_forget_image_job(item: tuple[QThread, ImageLoadWorker]) -> None`
- Retira una tarea terminada y programa la eliminación de su worker y su hilo.
#### `_clear_cards() -> None`
- Detiene y espera brevemente los hilos de imagen, elimina referencias a tareas y retira tarjetas existentes.
#### `closeEvent(event) -> None`
- Cierra visores abiertos, solicita terminar los hilos de cámaras/imágenes y continúa el cierre Qt.
#### `_title_for_incident() -> str`
- Forma el título usando carretera y, si existe, punto kilométrico de la incidencia.
#### `_subtitle_for_incident() -> str`
- Devuelve municipio/provincia o un texto que describe los criterios de búsqueda.
#### `_camera_meta(camera: dict[str, Any]) -> str`
- Une provincia y diferencias de PK/distancia disponibles en una línea.
#### `_clean(value: object) -> str | None`
- Convierte valores no nulos a texto recortado y devuelve `None` si queda vacío.
#### `_apply_style() -> None`
- Aplica la hoja de estilo de diálogo para el tema actual.

### `_FullscreenImageDialog(QDialog)`
- Diálogo de pantalla completa que muestra un `QPixmap` ajustado a sus dimensiones.
#### `__init__(pixmap: QPixmap, parent: QWidget | None = None) -> None`
- Guarda la imagen, crea una etiqueta centrada y sincroniza su tamaño inicial.
#### `resizeEvent(event) -> None`
- Delega el evento de redimensionado y vuelve a escalar la imagen.
#### `keyPressEvent(event) -> None`
- Cierra con Escape; para otras teclas usa el comportamiento base.
#### `mousePressEvent(event) -> None`
- Cierra al recibir un clic y después llama al manejador base.
#### `_sync_pixmap() -> None`
- Si la ventana tiene dimensiones positivas, escala el pixmap manteniendo proporción y suavizado.
