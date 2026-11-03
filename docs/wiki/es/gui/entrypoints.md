# dgt_monitor/gui/entrypoints.py
Configura y ejecuta la aplicación de escritorio PyQt6, construyendo el servicio y mostrando la ventana principal.
## Dependencias
`sys`, `QApplication` de PyQt6, `build_application` de `dgt_monitor.bootstrap` y `MainWindow` de `dgt_monitor.gui.main_window`.
## Contenido
### `run() -> int`
- Reutiliza o crea `QApplication`, establece el nombre “DGT Monitor”, construye y muestra `MainWindow` y devuelve el resultado de `app.exec()`.
