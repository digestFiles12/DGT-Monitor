# dgt_monitor/web/static/styles.css
Establece el diseño visual de la interfaz y adapta paneles, tablas y controles a los temas y tamaños de pantalla.
## Dependencias
CSS estándar; usa clases/atributos de `index.html` y variables CSS propias. El modo oscuro depende de `data-theme="dark"` en el elemento raíz, aplicado por `app.js`.
## Contenido
### Variables y temas
- `:root` define `--ink`, `--muted`, `--line`, `--paper`, `--white`, `--panel`, `--subtle`, `--field`, `--field-border`, `--row-hover`, `--media-bg`, `--footer-bg`, `--footer-ink`, `--red`, `--red-dark`, `--amber`, `--green`, `--blue` y `--shadow` para el tema claro. `:root[data-theme="dark"]` redefine esos valores y `color-scheme`; las reglas de componentes usan las variables compartidas para cambiar de tema.
### Diseño global y navegación
- Las reglas globales normalizan el modelo de caja y controles. `.topbar`, `.brand`, `.topbar-actions` y `.connection` componen la cabecera; `main`, `.overview`, `.summary-grid`, `.metric`, `.view-tabs` y `.tab` organizan métricas y navegación.
### Filtros, resultados e incidencias
- `.workspace`, `.filters` y sus controles crean el panel de filtros. `.results`, `.table-wrap`, filas, detalles expandibles, insignias, menús de cobertura y paneles de estado organizan los resultados.
### Gráficas, cámaras y mapa
- `.charts-view`, `.chart-menu`, `.chart-panel` y `.chart-canvas-wrap` disponen gráficas; `.chart-selector` estructura el selector múltiple, `.selector-group` agrupa regiones/provincias, `.selector-items` organiza opciones, `.selector-pill` muestra contadores y estados seleccionado/parcial, y `.selector-chip` presenta selecciones removibles. `.camera-grid`, `.camera-card`, `.camera-media`, `.camera-favorite` y `.image-viewer` definen tarjetas/visor; `.map-results`, `.map-shell`, `.map-detail` y `.map-marker` disponen el mapa.
### Pie y diseño adaptable
- `footer` sigue los colores del tema. `@keyframes spin` anima indicadores de carga; media queries para anchos de 1050 px, 760 px y orientación móvil reorganizan rejillas, filtros, tabla, mapa y pie.
