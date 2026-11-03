# dgt_monitor/gui/theme.py
Proporciona tipos y funciones compartidas para normalizar el tema claro/oscuro y generar hojas de estilo de la ventana y el diálogo de cámaras.
## Dependencias
Solo importa `Literal` de la biblioteca estándar de Python; sus cadenas de estilo se aplican mediante Qt.
## Contenido
### `ThemeName`
- Alias de tipo que limita el nombre del tema a `"light"` o `"dark"`.
### `normalize_theme(theme: str | None) -> ThemeName`
- Devuelve `dark` solo cuando el valor de entrada es exactamente `dark`; en otro caso devuelve `light`.
### `next_theme(theme: ThemeName) -> ThemeName`
- Devuelve el tema opuesto al recibido.
### `main_window_stylesheet(theme: ThemeName) -> str`
- Genera el QSS de la ventana principal usando la paleta del tema para paneles, botones, campos, tabla y texto.
### `camera_dialog_stylesheet(theme: ThemeName) -> str`
- Genera el QSS del diálogo de cámaras, incluidas tarjetas, imágenes, títulos y botones.
### `_palette(theme: ThemeName) -> dict[str, str]`
- Devuelve el mapa de colores claro u oscuro consumido por las funciones de estilos.
