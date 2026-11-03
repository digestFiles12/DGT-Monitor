# dgt_monitor/gui/dialogs/cameras.py
Implements a non-modal dialog for cameras near an incident, asynchronous image loading, and a fullscreen image viewer.
## Dependencies
PyQt6 Core/Gui/Widgets, `Callable`, `Any`, `DgtApplicationService`, `CAMERA_MATCH_RANGE_KM`, `CameraFilters`, theme utilities, and `CameraLoadWorker`/`ImageLoadWorker`.
## Contents
### `CamerasDialog(QDialog)`
- Non-modal dialog listing nearby cameras and their images. `load_completed`, `image_loaded(str)`, and `image_fullscreen_opened()` signals report loading and image-viewer events.
#### `__init__(self, service: DgtApplicationService, incident: dict[str, Any], parent: QWidget | None = None, autoload: bool = True, image_downloader: Callable[[str], bytes] | None = None, theme: str = "light") -> None`
- Stores the service/incident and job state, configures the window, builds/applies the theme, and optionally loads cameras.
#### `items(self) -> list[dict[str, Any]]`
- Property returning a shallow copy of the loaded camera list.
#### `reload() -> None`
- Avoids concurrent loads, clears cards, creates a `CameraLoadWorker` in a Qt thread, and connects its signals.
#### `_build_ui() -> None`
- Builds a header with title/location, refresh/theme buttons, and a scrollable card area.
#### `_filters() -> CameraFilters`
- Builds filters from the incident's province, road, kilometer point, and coordinates, with limit 12 and `CAMERA_MATCH_RANGE_KM` range.
#### `_apply_payload(payload: object) -> None`
- Extracts cameras from the payload, replaces cards, and updates the status with the number found.
#### `_camera_card(camera: dict[str, Any]) -> QFrame`
- Builds a road/PK/metadata and image card; starts a download when `image_url` exists.
#### `_empty_card(message: str) -> QFrame`
- Creates a simple card with a word-wrapped message.
#### `_show_error(message: str) -> None`
- Clears results, shows the error in a card, and updates the status.
#### `_load_finished() -> None`
- Re-enables refresh, schedules worker/thread deletion, clears references, and emits `load_completed`.
#### `toggle_theme() -> None`
- Switches to the opposite theme.
#### `set_theme(theme: str) -> None`
- Normalizes the theme name, updates the button, and applies the stylesheet.
#### `_sync_theme_button() -> None`
- Sets the button text to offer the alternate theme.
#### `_load_image(url: str, label: QLabel) -> None`
- Runs `ImageLoadWorker` in a thread, connects success/error to the label, and tracks the job for cleanup.
#### `_apply_image(url: str, payload: object, label: QLabel) -> None`
- Decodes bytes into `QPixmap`, displays a scaled image and enables click-to-enlarge; emits `image_loaded`.
#### `_fullscreen_click_handler(pixmap: QPixmap)`
- Returns a click handler that opens the `pixmap` fullscreen.
#### `open_fullscreen(_event) -> None` (función interna)
- Calls `_open_fullscreen_image` with the image captured by the handler.
#### `_open_fullscreen_image(pixmap: QPixmap) -> QDialog`
- Creates and tracks the image dialog, shows it, and emits `image_fullscreen_opened`.
#### `_show_fullscreen_dialog(dialog: QDialog) -> None`
- Shows the dialog with `showFullScreen()`.
#### `_forget_fullscreen_dialog(dialog: QDialog) -> None`
- Removes the destroyed dialog from the list of open dialogs.
#### `_forget_image_job(item: tuple[QThread, ImageLoadWorker]) -> None`
- Removes a completed job and schedules deletion of its worker and thread.
#### `_clear_cards() -> None`
- Stops and briefly waits for image threads, clears job references, and removes existing cards.
#### `closeEvent(event) -> None`
- Closes open viewers, asks camera/image threads to stop, and continues Qt close handling.
#### `_title_for_incident() -> str`
- Builds the title from the incident road and, when present, kilometer point.
#### `_subtitle_for_incident() -> str`
- Returns municipality/province or text describing the search criteria.
#### `_camera_meta(camera: dict[str, Any]) -> str`
- Joins the available province and kilometer/distance differences into one line.
#### `_clean(value: object) -> str | None`
- Converts non-null values to trimmed text and returns `None` when empty.
#### `_apply_style() -> None`
- Applies the dialog stylesheet for the current theme.

### `_FullscreenImageDialog(QDialog)`
- Fullscreen dialog displaying a `QPixmap` scaled to its dimensions.
#### `__init__(pixmap: QPixmap, parent: QWidget | None = None) -> None`
- Stores the image, creates a centered label, and synchronizes its initial size.
#### `resizeEvent(event) -> None`
- Delegates the resize event and rescales the image.
#### `keyPressEvent(event) -> None`
- Closes on Escape; delegates other keys to the base behavior.
#### `mousePressEvent(event) -> None`
- Closes on a mouse press and then calls the base handler.
#### `_sync_pixmap() -> None`
- If the window has positive dimensions, scales the pixmap with aspect ratio and smooth transformation preserved.
