# Web frontend index
Index of the pages documenting the monitor's web interface, one source file per page.
## Dependencies
The pages cover files under `src/dgt_monitor/web/static/`; data logic also depends on the application API.
## Contents
| Page | Description |
|---|---|
| [app.js](app_js.md) | Active state, interactions, loading, and rendering. |
| [index.html](index_html.md) | Page structure and main regions. |
| [styles.css](styles_css.md) | Styles, variables, themes, and responsive layout. |
| [sw.js](sw_js.md) | App-shell cache and offline behavior. |
| [manifest.webmanifest](manifest.md) | PWA installation metadata. |

### How the Charts tab gets its data
`loadChartsData` requests `/api/stats?level=<level>&refresh=true` (Province or Region), then `/api/stats/grouped`. It stores both responses: the first endpoint provides statistics and level groups; the second provides `by_weekday` and `by_type`. `renderChart` selects the grouping, indicator, and chart mode.
