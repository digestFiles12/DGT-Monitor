# dgt_monitor/gui/theme.py
**ES:** Proporciona tipos y funciones compartidas para normalizar el tema claro/oscuro y generar hojas de estilo de la ventana y el diálogo de cámaras.
**EN:** Provides shared types and functions to normalize light/dark themes and generate stylesheets for the main window and camera dialog.
## Dependencies / Dependencias
Solo importa `Literal` de la biblioteca estándar de Python; sus cadenas de estilo se aplican mediante Qt.
Imports only `Literal` from Python's standard library; its stylesheet strings are applied by Qt.
## Contents / Contenido
### `ThemeName`
- **ES:** Alias de tipo que limita el nombre del tema a `"light"` o `"dark"`.
- **EN:** Type alias restricting the theme name to `"light"` or `"dark"`.
### `normalize_theme(theme: str | None) -> ThemeName`
- **ES:** Devuelve `dark` solo cuando el valor de entrada es exactamente `dark`; en otro caso devuelve `light`.
- **EN:** Returns `dark` only when the input is exactly `dark`; otherwise returns `light`.
### `next_theme(theme: ThemeName) -> ThemeName`
- **ES:** Devuelve el tema opuesto al recibido.
- **EN:** Returns the opposite of the supplied theme.
### `main_window_stylesheet(theme: ThemeName) -> str`
- **ES:** Genera el QSS de la ventana principal usando la paleta del tema para paneles, botones, campos, tabla y texto.
- **EN:** Builds the main-window QSS using the theme palette for panels, buttons, fields, table, and text.
### `camera_dialog_stylesheet(theme: ThemeName) -> str`
- **ES:** Genera el QSS del diálogo de cámaras, incluidas tarjetas, imágenes, títulos y botones.
- **EN:** Builds the camera-dialog QSS, including cards, images, titles, and buttons.
### `_palette(theme: ThemeName) -> dict[str, str]`
- **ES:** Devuelve el mapa de colores claro u oscuro consumido por las funciones de estilos.
- **EN:** Returns the light or dark color map consumed by the stylesheet functions.
