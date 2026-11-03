# dgt_monitor/gui/theme.py
Provides shared types and functions to normalize light/dark themes and generate stylesheets for the main window and camera dialog.
## Dependencies
Imports only `Literal` from Python's standard library; its stylesheet strings are applied by Qt.
## Contents
### `ThemeName`
- Type alias restricting the theme name to `"light"` or `"dark"`.
### `normalize_theme(theme: str | None) -> ThemeName`
- Returns `dark` only when the input is exactly `dark`; otherwise returns `light`.
### `next_theme(theme: ThemeName) -> ThemeName`
- Returns the opposite of the supplied theme.
### `main_window_stylesheet(theme: ThemeName) -> str`
- Builds the main-window QSS using the theme palette for panels, buttons, fields, table, and text.
### `camera_dialog_stylesheet(theme: ThemeName) -> str`
- Builds the camera-dialog QSS, including cards, images, titles, and buttons.
### `_palette(theme: ThemeName) -> dict[str, str]`
- Returns the light or dark color map consumed by the stylesheet functions.
