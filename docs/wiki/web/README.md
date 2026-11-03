# Web frontend wiki
**ES:** Índice de las páginas que explican, archivo por archivo, la interfaz web del monitor.
**EN:** Index of the pages documenting the monitor's web interface, one source file per page.
## Dependencies / Dependencias
Las páginas describen archivos bajo `src/dgt_monitor/web/static/`; la lógica de datos también depende de la API de la aplicación.
The pages cover files under `src/dgt_monitor/web/static/`; data logic also depends on the application API.
## Contents / Contenido
| Page | Description / Descripción |
|---|---|
| [app.js](app_js.md) | **ES:** Estado, interacciones, carga y renderizado activos. **EN:** Active state, interactions, loading, and rendering. |
| [index.html](index_html.md) | **ES:** Estructura y regiones principales. **EN:** Structure and main regions. |
| [styles.css](styles_css.md) | **ES:** Estilos, variables, temas y diseño adaptable. **EN:** Styles, variables, themes, and responsive layout. |
| [sw.js](sw_js.md) | **ES:** Caché del shell y modo sin conexión. **EN:** App-shell cache and offline behavior. |
| [manifest.webmanifest](manifest.md) | **ES:** Metadatos de instalación PWA. **EN:** PWA installation metadata. |

### How the Charts tab gets its data / Cómo obtiene datos la pestaña Gráficas
- **ES:** `loadChartsData` pide `/api/stats?level=<nivel>&refresh=true` (Provincia o CCAA) y después `/api/stats/grouped`. Guarda ambas respuestas: el primer endpoint aporta estadísticas y grupos por nivel; el segundo, `by_weekday` y `by_type`. `renderChart` elige agrupación, indicador y modo de gráfica.
- **EN:** `loadChartsData` requests `/api/stats?level=<level>&refresh=true` (Province or Region), then `/api/stats/grouped`. It stores both responses: the first endpoint provides statistics and level groups; the second provides `by_weekday` and `by_type`. `renderChart` selects the grouping, indicator, and chart mode.
