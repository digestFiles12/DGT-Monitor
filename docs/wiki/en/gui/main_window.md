# dgt_monitor/gui/main_window.py
Defines the PyQt6 adapter's main window: it applies filters, presents statistics and incidents, shows details, and opens the camera dialog.
## Dependencies
PyQt6 Core/Gui/Widgets (`QThread`, signals, widgets, table, and colors), `datetime`, `Any`, `DgtApplicationService`, `IncidentFilters`, `CamerasDialog`, theme utilities, and `IncidentLoadWorker`.
## Contents
### `MainWindow(QMainWindow)`
- Desktop window with filters, metric cards, incident table, detail panel, and theme toggle; emits `load_completed` when loading finishes.
#### `__init__(service: DgtApplicationService, autoload: bool = True) -> None`
- Stores the service and state, configures the window, builds and styles the UI, and optionally starts loading.
#### `_build_ui() -> None`
- Builds the header, filters, metrics, selectable table, and details; connects buttons and selection to handlers.
#### `reload() -> None`
- Prevents concurrent loads, builds `IncidentFilters` from controls, and runs `IncidentLoadWorker` in a `QThread`.
#### `_apply_payload(payload: object) -> None`
- Validates the payload, stores incidents, updates metrics, and fills the table with selected fields.
#### `clear_filters() -> None`
- Clears inputs and selectors, removes the kind filter, and reloads.
#### `_set_kind_filter(kind: str, reload: bool = True) -> None`
- Stores the kind filter, updates the active card, and optionally reloads.
#### `_sync_stat_buttons() -> None`
- Updates each metric card's `active` property and repolishes its Qt style.
#### `_kind_for_stat(key: str) -> str`
- Maps a metric key (`total`, `accidents`, etc.) to its `kind` filter value.
#### `_show_selection() -> None`
- Reads the selected row's incident, enables the camera button, and shows detail fields; with no row, clears selection and disables the button.
#### `open_cameras_dialog() -> CamerasDialog | None`
- If an incident is selected, creates, tracks, shows, and returns a non-modal camera dialog; otherwise returns `None`.
#### `_forget_camera_dialog(dialog: CamerasDialog) -> None`
- Removes the dialog from the list of open windows when it is destroyed.
#### `_show_error(message: str) -> None`
- Marks the connection as unavailable and displays a warning with the supplied error.
#### `_load_finished() -> None`
- Re-enables the button, schedules worker/thread deletion, clears references, and emits `load_completed`.
#### `toggle_theme() -> None`
- Switches to the opposite theme through `set_theme`.
#### `set_theme(theme: str) -> None`
- Normalizes and applies the window theme and synchronizes it with open camera dialogs.
#### `closeEvent(event) -> None`
- Closes dialogs, asks the load thread to stop, and waits up to one second before normal close handling.
#### `_severity_label(value: str) -> str`
- Translates known severity values into Spanish or returns the supplied value/missing-data label.
#### `_severity_color(value: str) -> QColor`
- Returns the configured severity color or a neutral color for unknown values.
#### `_format_datetime(value: object) -> str`
- Returns empty text for false values, formats ISO dates as `dd/mm/yyyy hh:mm`, or preserves unparseable text.
#### `_apply_style() -> None`
- Applies the main-window stylesheet for the current theme.
