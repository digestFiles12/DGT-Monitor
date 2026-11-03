# Índice de la interfaz web
Índice de las páginas que explican, archivo por archivo, la interfaz web del monitor.
## Dependencias
Las páginas describen archivos bajo `src/dgt_monitor/web/static/`; la lógica de datos también depende de la API de la aplicación.
## Contenido
| Página | Descripción |
|---|---|
| [app.js](app_js.md) | Estado, interacciones, carga y renderizado activos. |
| [index.html](index_html.md) | Estructura y regiones principales. |
| [styles.css](styles_css.md) | Estilos, variables, temas y diseño adaptable. |
| [sw.js](sw_js.md) | Caché del shell y modo sin conexión. |
| [manifest.webmanifest](manifest.md) | Metadatos de instalación PWA. |

### Cómo obtiene datos la pestaña Gráficas
`loadChartsData` pide `/api/stats?level=<nivel>&refresh=true` (Provincia o CCAA) y después `/api/stats/grouped`. Guarda ambas respuestas: el primer endpoint aporta estadísticas y grupos por nivel; el segundo, `by_weekday` y `by_type`. `renderChart` elige agrupación, indicador y modo de gráfica.
