# dgt_monitor/gui/entrypoints.py
**ES:** Configura y ejecuta la aplicación de escritorio PyQt6, construyendo el servicio y mostrando la ventana principal.
**EN:** Configures and runs the PyQt6 desktop application, building its service and showing the main window.
## Dependencies / Dependencias
`sys`, `QApplication` de PyQt6, `build_application` de `dgt_monitor.bootstrap` y `MainWindow` de `dgt_monitor.gui.main_window`.
`sys`, PyQt6 `QApplication`, `build_application` from `dgt_monitor.bootstrap`, and `MainWindow` from `dgt_monitor.gui.main_window`.
## Contents / Contenido
### `run() -> int`
- **ES:** Reutiliza o crea `QApplication`, establece el nombre “DGT Monitor”, construye y muestra `MainWindow` y devuelve el resultado de `app.exec()`.
- **EN:** Reuses or creates `QApplication`, sets its name to “DGT Monitor”, builds and shows `MainWindow`, and returns `app.exec()`'s result.
