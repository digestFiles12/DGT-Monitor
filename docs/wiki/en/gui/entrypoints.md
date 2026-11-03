# dgt_monitor/gui/entrypoints.py
Configures and runs the PyQt6 desktop application, building its service and showing the main window.
## Dependencies
`sys`, PyQt6 `QApplication`, `build_application` from `dgt_monitor.bootstrap`, and `MainWindow` from `dgt_monitor.gui.main_window`.
## Contents
### `run() -> int`
- Reuses or creates `QApplication`, sets its name to “DGT Monitor”, builds and shows `MainWindow`, and returns `app.exec()`'s result.
