# dgt_monitor/web/static/styles.css
Defines the interface's visual design and adapts panels, tables, and controls to themes and screen sizes.
## Dependencies
Standard CSS; uses classes/attributes from `index.html` and its own CSS variables. Dark mode depends on `data-theme="dark"` on the root element, set by `app.js`.
## Contents
### Variables and themes
- `:root` defines `--ink`, `--muted`, `--line`, `--paper`, `--white`, `--panel`, `--subtle`, `--field`, `--field-border`, `--row-hover`, `--media-bg`, `--footer-bg`, `--footer-ink`, `--red`, `--red-dark`, `--amber`, `--green`, `--blue`, and `--shadow` for light mode. `:root[data-theme="dark"]` overrides those values and `color-scheme`; component rules use the shared variables to switch themes.
### Global layout and navigation
- Global rules normalize box sizing and controls. `.topbar`, `.brand`, `.topbar-actions`, and `.connection` form the header; `main`, `.overview`, `.summary-grid`, `.metric`, `.view-tabs`, and `.tab` organize metrics and navigation.
### Filters, results, and incidents
- `.workspace`, `.filters`, and their controls form the filter panel. `.results`, `.table-wrap`, rows, expandable details, badges, coverage menus, and state panels organize results.
### Charts, cameras, and map
- `.charts-view`, `.chart-menu`, `.chart-panel`, and `.chart-canvas-wrap` lay out charts. `.camera-grid`, `.camera-card`, `.camera-media`, `.camera-favorite`, and `.image-viewer` style camera cards/viewer; `.map-results`, `.map-shell`, `.map-detail`, and `.map-marker` lay out the map.
### Footer and responsive layout
- `footer` follows theme colors. `@keyframes spin` animates loading indicators; media queries at 1050 px, 760 px, and mobile orientations rearrange grids, filters, table, map, and footer.
