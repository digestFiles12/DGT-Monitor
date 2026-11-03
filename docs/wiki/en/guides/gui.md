# Desktop GUI (PyQt6)
The GUI lives in `src/dgt_monitor/gui/` and consumes `DgtApplicationService` through `QThread` workers; widgets contain no parsing, repositories, or cache.
## Structure
```text
src/dgt_monitor/gui/
  __main__.py          # python -m dgt_monitor.gui
  entrypoints.py       # run(): creates QApplication and MainWindow(build_application())
  main_window.py       # MainWindow
  workers.py           # IncidentLoadWorker, CameraLoadWorker, ImageLoadWorker
  theme.py             # light/dark themes and stylesheets
  dialogs/cameras.py   # CamerasDialog and the fullscreen viewer
```
The `widgets/` and `workers/` subpackages exist but contain no modules.
## Running
```powershell
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```
## `MainWindow`
- Filters: province, municipality, road, search mode (`contains`, `exact`, `regex`), severity (`highest`, `high`, `medium`, `low`), and camera (`with`, `without`), with "Apply filters" and "Clear" buttons.
- Statistic cards clickable by type, a seven-column table with row selection, and a detail panel with human-readable dates.
- A "View cameras" button that opens `CamerasDialog` for the selected incident.
- A refresh button that starts a new load; light/dark mode through `toggle_theme`/`set_theme`.
- There is no automatic refresh timer and no visible activity log.
## `CamerasDialog`
- Non-modal dialog that builds `CameraFilters` from the incident's road, province, kilometer point, and coordinates, and uses `CAMERA_MATCH_RANGE_KM` so it matches the API and dashboard.
- `CameraLoadWorker` loads the cameras and `ImageLoadWorker` downloads images in the background.
- Thumbnails are scaled preserving aspect ratio; when an image fails, a readable status is shown.
- Clicking a thumbnail opens a fullscreen viewer closed with Escape or a click.
## Theme
`dgt_monitor.gui.theme` centralizes `normalize_theme`, `next_theme`, `main_window_stylesheet`, and `camera_dialog_stylesheet`, applied to the main window and the cameras dialog.
## Rules
- Workers call `DgtApplicationService`; they never download or parse XML.
- Widgets know nothing about repositories or caches.
- `MainWindow` coordinates state, selection, filters, the statistic filter, and workers.
- Camera dialogs are non-modal and independent.
- Keep references to dialogs and workers until they finish, and stop threads in `closeEvent`.
## Relationship with the web dashboard
The dashboard (see [the API guide](api.md)) shares the same facade. The extra web controls (charts, map, and favorites tabs) do not exist on the desktop; if they are replicated, the logic must live in the services rather than in the interface. Console charts are available with `python -m dgt_monitor.menu` (see [the console menu](../menu.md)).
## Tests
GUI tests are in `tests/gui/` and run with `QT_QPA_PLATFORM=offscreen`; see [the testing guide](testing.md).
