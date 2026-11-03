# dgt_monitor/gui/main_window.py
Define la ventana principal del adaptador PyQt6: aplica filtros, presenta estadísticas e incidencias, muestra detalles y abre el diálogo de cámaras.
## Dependencias
PyQt6 Core/Gui/Widgets (`QThread`, señales, widgets, tabla y colores), `datetime`, `Any`, `DgtApplicationService`, `IncidentFilters`, `CamerasDialog`, utilidades de tema y `IncidentLoadWorker`.
## Contenido
### `MainWindow(QMainWindow)`
- Ventana de escritorio con filtros, tarjetas métricas, tabla de incidencias, panel de detalle y selector de tema; emite `load_completed` al terminar la carga.
#### `__init__(service: DgtApplicationService, autoload: bool = True) -> None`
- Guarda servicio y estado, configura tamaño/ventana, construye y estiliza la interfaz y opcionalmente inicia la carga.
#### `_build_ui() -> None`
- Construye cabecera, filtros, métricas, tabla seleccionable y detalle; conecta botones y selección a sus manejadores.
#### `reload() -> None`
- Evita cargas simultáneas, crea `IncidentFilters` desde controles y ejecuta `IncidentLoadWorker` en un `QThread`.
#### `_apply_payload(payload: object) -> None`
- Valida el payload, guarda incidencias, actualiza métricas y rellena la tabla con los campos seleccionados.
#### `clear_filters() -> None`
- Limpia entradas y selectores, quita el filtro de tipo y vuelve a cargar.
#### `_set_kind_filter(kind: str, reload: bool = True) -> None`
- Guarda el filtro de tipo, actualiza la tarjeta activa y opcionalmente vuelve a cargar.
#### `_sync_stat_buttons() -> None`
- Actualiza la propiedad `active` de cada tarjeta métrica y repoliza el estilo Qt.
#### `_kind_for_stat(key: str) -> str`
- Traduce la clave de una tarjeta (`total`, `accidents`, etc.) al valor de filtro `kind`.
#### `_show_selection() -> None`
- Toma la incidencia de la fila seleccionada, activa el botón de cámaras y muestra campos de detalle; sin fila, limpia la selección y desactiva el botón.
#### `open_cameras_dialog() -> CamerasDialog | None`
- Si hay incidencia seleccionada, crea, registra, muestra y devuelve un diálogo no modal de cámaras; si no, devuelve `None`.
#### `_forget_camera_dialog(dialog: CamerasDialog) -> None`
- Retira el diálogo de la lista de ventanas abiertas cuando se destruye.
#### `_show_error(message: str) -> None`
- Marca la conexión como caída y muestra un aviso con el error recibido.
#### `_load_finished() -> None`
- Reactiva el botón, programa la eliminación de worker/hilo, limpia sus referencias y emite `load_completed`.
#### `toggle_theme() -> None`
- Alterna al tema opuesto mediante `set_theme`.
#### `set_theme(theme: str) -> None`
- Normaliza y aplica el tema de ventana y lo sincroniza con los diálogos de cámaras abiertos.
#### `closeEvent(event) -> None`
- Cierra diálogos, solicita que el hilo de carga termine y espera hasta un segundo antes del cierre normal.
#### `_severity_label(value: str) -> str`
- Traduce severidades conocidas al español o devuelve el valor recibido/dato faltante.
#### `_severity_color(value: str) -> QColor`
- Devuelve el color configurado para la severidad o un color neutro para valores desconocidos.
#### `_format_datetime(value: object) -> str`
- Devuelve vacío para valores falsos, formatea fechas ISO como `dd/mm/aaaa hh:mm` o conserva texto no interpretable.
#### `_apply_style() -> None`
- Aplica la hoja de estilo de ventana para el tema actual.
