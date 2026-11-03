# dgt_monitor/web/static/styles.css
**ES:** Establece el diseño visual de la interfaz y adapta paneles, tablas y controles a los temas y tamaños de pantalla.
**EN:** Defines the interface's visual design and adapts panels, tables, and controls to themes and screen sizes.
## Dependencies / Dependencias
CSS estándar; usa clases/atributos de `index.html` y variables CSS propias. El modo oscuro depende de `data-theme="dark"` en el elemento raíz, aplicado por `app.js`.
Standard CSS; uses classes/attributes from `index.html` and its own CSS variables. Dark mode depends on `data-theme="dark"` on the root element, set by `app.js`.
## Contents / Contenido
### Variables and themes
- **ES:** `:root` define `--ink`, `--muted`, `--line`, `--paper`, `--white`, `--panel`, `--subtle`, `--field`, `--field-border`, `--row-hover`, `--media-bg`, `--footer-bg`, `--footer-ink`, `--red`, `--red-dark`, `--amber`, `--green`, `--blue` y `--shadow` para el tema claro. `:root[data-theme="dark"]` redefine esos valores y `color-scheme`; las reglas de componentes usan las variables compartidas para cambiar de tema.
- **EN:** `:root` defines `--ink`, `--muted`, `--line`, `--paper`, `--white`, `--panel`, `--subtle`, `--field`, `--field-border`, `--row-hover`, `--media-bg`, `--footer-bg`, `--footer-ink`, `--red`, `--red-dark`, `--amber`, `--green`, `--blue`, and `--shadow` for light mode. `:root[data-theme="dark"]` overrides those values and `color-scheme`; component rules use the shared variables to switch themes.
### Global layout and navigation
- **ES:** Las reglas globales normalizan el modelo de caja y controles. `.topbar`, `.brand`, `.topbar-actions` y `.connection` componen la cabecera; `main`, `.overview`, `.summary-grid`, `.metric`, `.view-tabs` y `.tab` organizan métricas y navegación.
- **EN:** Global rules normalize box sizing and controls. `.topbar`, `.brand`, `.topbar-actions`, and `.connection` form the header; `main`, `.overview`, `.summary-grid`, `.metric`, `.view-tabs`, and `.tab` organize metrics and navigation.
### Filters, results, and incidents
- **ES:** `.workspace`, `.filters` y sus controles crean el panel de filtros. `.results`, `.table-wrap`, filas, detalles expandibles, insignias, menús de cobertura y paneles de estado organizan los resultados.
- **EN:** `.workspace`, `.filters`, and their controls form the filter panel. `.results`, `.table-wrap`, rows, expandable details, badges, coverage menus, and state panels organize results.
### Charts, cameras, and map
- **ES:** `.charts-view`, `.chart-menu`, `.chart-panel` y `.chart-canvas-wrap` disponen gráficas. `.camera-grid`, `.camera-card`, `.camera-media`, `.camera-favorite` y `.image-viewer` definen tarjetas/visor; `.map-results`, `.map-shell`, `.map-detail` y `.map-marker` disponen el mapa.
- **EN:** `.charts-view`, `.chart-menu`, `.chart-panel`, and `.chart-canvas-wrap` lay out charts. `.camera-grid`, `.camera-card`, `.camera-media`, `.camera-favorite`, and `.image-viewer` style camera cards/viewer; `.map-results`, `.map-shell`, `.map-detail`, and `.map-marker` lay out the map.
### Footer and responsive layout
- **ES:** `footer` sigue los colores del tema. `@keyframes spin` anima indicadores de carga; media queries para anchos de 1050 px, 760 px y orientación móvil reorganizan rejillas, filtros, tabla, mapa y pie.
- **EN:** `footer` follows theme colors. `@keyframes spin` animates loading indicators; media queries at 1050 px, 760 px, and mobile orientations rearrange grids, filters, table, map, and footer.

