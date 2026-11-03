# dgt_monitor/web/static/index.html
Defines the web application's structure: header, metrics, filters, tabs, and incident, camera, map, and chart panels.
## Dependencies
Local `/static/styles.css?v=54`, `/static/app.js?v=54`, and `/manifest.webmanifest`; Lucide and Leaflet, including Leaflet styles, load from CDNs. Chart.js 4.4.7 is bundled locally as `chart.umd.min.js`, with no CDN.
## Contents
### Document head
- Declares Spanish, encoding, viewport, theme color, and description; links fonts, manifest, Leaflet, and CSS. Lucide, Leaflet, Chart.js, and `app.js` scripts use `defer`.
### Header and summary metrics
- The header groups branding, connection (`connectionStatus`), update time (`lastUpdate`), language, theme (`themeButton`), and refresh (`refreshButton`). `data-kind` metrics and IDs `statTotal`, `statAccidents`, `statRoadworks`, `statStuck`, `statObstructions`, and `statWeather` display values and provide filters.
### Tabs and filters
- `data-view` tabs open Incidents, Cameras, Favorites, Charts, or Map; `filterToggle` collapses filters. `filtersPanel` contains `filterForm` and fields `provinceFilter`, `roadFilter`, `municipalityFilter`, `severityFilter`, `cameraCoverageFilter`, `kmFilter`, `cameraIncidentFilter`, and `limitFilter`; `incidentFilters` and `cameraFilters` group view-specific controls.
### Results, map, and charts
- `.results` contains loading/error/empty states, the `incidentResults` table with `incidentRows`, `loadMoreButton`, `cameraResults` cards, and `mapResults` (`trafficMap`, `mapDetail`). `chartsView` includes `chartLevel`, `chartGrouping`, indicator/mode menus, states, `chartCanvas`, and `chartExtremes`.
### Footer
- Links to API documentation (`/docs`) and service health (`/api/health`).
