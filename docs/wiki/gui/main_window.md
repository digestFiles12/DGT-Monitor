# dgt_monitor/gui/main_window.py
**ES:** Define la ventana principal del adaptador PyQt6: aplica filtros, presenta estadísticas e incidencias, muestra detalles y abre el diálogo de cámaras.
**EN:** Defines the PyQt6 adapter's main window: it applies filters, presents statistics and incidents, shows details, and opens the camera dialog.
## Dependencies / Dependencias
PyQt6 Core/Gui/Widgets (`QThread`, señales, widgets, tabla y colores), `datetime`, `Any`, `DgtApplicationService`, `IncidentFilters`, `CamerasDialog`, utilidades de tema y `IncidentLoadWorker`.
PyQt6 Core/Gui/Widgets (`QThread`, signals, widgets, table, and colors), `datetime`, `Any`, `DgtApplicationService`, `IncidentFilters`, `CamerasDialog`, theme utilities, and `IncidentLoadWorker`.
## Contents / Contenido
### `MainWindow(QMainWindow)`
- **ES:** Ventana de escritorio con filtros, tarjetas métricas, tabla de incidencias, panel de detalle y selector de tema; emite `load_completed` al terminar la carga.
- **EN:** Desktop window with filters, metric cards, incident table, detail panel, and theme toggle; emits `load_completed` when loading finishes.
#### `__init__(service: DgtApplicationService, autoload: bool = True) -> None`
- **ES:** Guarda servicio y estado, configura tamaño/ventana, construye y estiliza la interfaz y opcionalmente inicia la carga.
- **EN:** Stores the service and state, configures the window, builds and styles the UI, and optionally starts loading.
#### `_build_ui() -> None`
- **ES:** Construye cabecera, filtros, métricas, tabla seleccionable y detalle; conecta botones y selección a sus manejadores.
- **EN:** Builds the header, filters, metrics, selectable table, and details; connects buttons and selection to handlers.
#### `reload() -> None`
- **ES:** Evita cargas simultáneas, crea `IncidentFilters` desde controles y ejecuta `IncidentLoadWorker` en un `QThread`.
- **EN:** Prevents concurrent loads, builds `IncidentFilters` from controls, and runs `IncidentLoadWorker` in a `QThread`.
#### `_apply_payload(payload: object) -> None`
- **ES:** Valida el payload, guarda incidencias, actualiza métricas y rellena la tabla con los campos seleccionados.
- **EN:** Validates the payload, stores incidents, updates metrics, and fills the table with selected fields.
#### `clear_filters() -> None`
- **ES:** Limpia entradas y selectores, quita el filtro de tipo y vuelve a cargar.
- **EN:** Clears inputs and selectors, removes the kind filter, and reloads.
#### `_set_kind_filter(kind: str, reload: bool = True) -> None`
- **ES:** Guarda el filtro de tipo, actualiza la tarjeta activa y opcionalmente vuelve a cargar.
- **EN:** Stores the kind filter, updates the active card, and optionally reloads.
#### `_sync_stat_buttons() -> None`
- **ES:** Actualiza la propiedad `active` de cada tarjeta métrica y repoliza el estilo Qt.
- **EN:** Updates each metric card's `active` property and repolishes its Qt style.
#### `_kind_for_stat(key: str) -> str`
- **ES:** Traduce la clave de una tarjeta (`total`, `accidents`, etc.) al valor de filtro `kind`.
- **EN:** Maps a metric key (`total`, `accidents`, etc.) to its `kind` filter value.
#### `_show_selection() -> None`
- **ES:** Toma la incidencia de la fila seleccionada, activa el botón de cámaras y muestra campos de detalle; sin fila, limpia la selección y desactiva el botón.
- **EN:** Reads the selected row's incident, enables the camera button, and shows detail fields; with no row, clears selection and disables the button.
#### `open_cameras_dialog() -> CamerasDialog | None`
- **ES:** Si hay incidencia seleccionada, crea, registra, muestra y devuelve un diálogo no modal de cámaras; si no, devuelve `None`.
- **EN:** If an incident is selected, creates, tracks, shows, and returns a non-modal camera dialog; otherwise returns `None`.
#### `_forget_camera_dialog(dialog: CamerasDialog) -> None`
- **ES:** Retira el diálogo de la lista de ventanas abiertas cuando se destruye.
- **EN:** Removes the dialog from the list of open windows when it is destroyed.
#### `_show_error(message: str) -> None`
- **ES:** Marca la conexión como caída y muestra un aviso con el error recibido.
- **EN:** Marks the connection as unavailable and displays a warning with the supplied error.
#### `_load_finished() -> None`
- **ES:** Reactiva el botón, programa la eliminación de worker/hilo, limpia sus referencias y emite `load_completed`.
- **EN:** Re-enables the button, schedules worker/thread deletion, clears references, and emits `load_completed`.
#### `toggle_theme() -> None`
- **ES:** Alterna al tema opuesto mediante `set_theme`.
- **EN:** Switches to the opposite theme through `set_theme`.
#### `set_theme(theme: str) -> None`
- **ES:** Normaliza y aplica el tema de ventana y lo sincroniza con los diálogos de cámaras abiertos.
- **EN:** Normalizes and applies the window theme and synchronizes it with open camera dialogs.
#### `closeEvent(event) -> None`
- **ES:** Cierra diálogos, solicita que el hilo de carga termine y espera hasta un segundo antes del cierre normal.
- **EN:** Closes dialogs, asks the load thread to stop, and waits up to one second before normal close handling.
#### `_severity_label(value: str) -> str`
- **ES:** Traduce severidades conocidas al español o devuelve el valor recibido/dato faltante.
- **EN:** Translates known severity values into Spanish or returns the supplied value/missing-data label.
#### `_severity_color(value: str) -> QColor`
- **ES:** Devuelve el color configurado para la severidad o un color neutro para valores desconocidos.
- **EN:** Returns the configured severity color or a neutral color for unknown values.
#### `_format_datetime(value: object) -> str`
- **ES:** Devuelve vacío para valores falsos, formatea fechas ISO como `dd/mm/aaaa hh:mm` o conserva texto no interpretable.
- **EN:** Returns empty text for false values, formats ISO dates as `dd/mm/yyyy hh:mm`, or preserves unparseable text.
#### `_apply_style() -> None`
- **ES:** Aplica la hoja de estilo de ventana para el tema actual.
- **EN:** Applies the main-window stylesheet for the current theme.

