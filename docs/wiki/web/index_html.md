# dgt_monitor/web/static/index.html
**ES:** Define la estructura de la aplicación web: cabecera, métricas, filtros, pestañas y paneles de incidencias, cámaras, mapa y gráficas.
**EN:** Defines the web application's structure: header, metrics, filters, tabs, and incident, camera, map, and chart panels.
## Dependencies / Dependencias
Hoja local `/static/styles.css?v=54`, lógica `/static/app.js?v=54`, manifiesto `/manifest.webmanifest`; Lucide y Leaflet y los estilos de Leaflet se cargan desde CDN. Chart.js 4.4.7 está incluido localmente como `chart.umd.min.js`, sin CDN.
Local `/static/styles.css?v=54`, `/static/app.js?v=54`, and `/manifest.webmanifest`; Lucide and Leaflet, including Leaflet styles, load from CDNs. Chart.js 4.4.7 is bundled locally as `chart.umd.min.js`, with no CDN.
## Contents / Contenido
### Document head
- **ES:** Declara español, codificación, viewport, color de tema y descripción; vincula fuentes, manifiesto, Leaflet y CSS. Los scripts de Lucide, Leaflet, Chart.js y `app.js` usan `defer`.
- **EN:** Declares Spanish, encoding, viewport, theme color, and description; links fonts, manifest, Leaflet, and CSS. Lucide, Leaflet, Chart.js, and `app.js` scripts use `defer`.
### Header and summary metrics
- **ES:** La cabecera reúne marca, conexión (`connectionStatus`), hora (`lastUpdate`), idioma, tema (`themeButton`) y recarga (`refreshButton`). Las métricas `data-kind` y los IDs `statTotal`, `statAccidents`, `statRoadworks`, `statStuck`, `statObstructions`, `statWeather` muestran valores y permiten filtrar.
- **EN:** The header groups branding, connection (`connectionStatus`), update time (`lastUpdate`), language, theme (`themeButton`), and refresh (`refreshButton`). `data-kind` metrics and IDs `statTotal`, `statAccidents`, `statRoadworks`, `statStuck`, `statObstructions`, and `statWeather` display values and provide filters.
### Tabs and filters
- **ES:** Las pestañas `data-view` abren Incidencias, Cámaras, Favoritas, Gráficas o Mapa; `filterToggle` contrae filtros. `filtersPanel` contiene `filterForm` y los campos `provinceFilter`, `roadFilter`, `municipalityFilter`, `severityFilter`, `cameraCoverageFilter`, `kmFilter`, `cameraIncidentFilter` y `limitFilter`; `incidentFilters` y `cameraFilters` agrupan controles específicos.
- **EN:** `data-view` tabs open Incidents, Cameras, Favorites, Charts, or Map; `filterToggle` collapses filters. `filtersPanel` contains `filterForm` and fields `provinceFilter`, `roadFilter`, `municipalityFilter`, `severityFilter`, `cameraCoverageFilter`, `kmFilter`, `cameraIncidentFilter`, and `limitFilter`; `incidentFilters` and `cameraFilters` group view-specific controls.
### Results, map, and charts
- **ES:** `.results` contiene estados de carga/error/vacío, tabla `incidentResults` con `incidentRows`, `loadMoreButton`, tarjetas `cameraResults` y mapa `mapResults` (`trafficMap`, `mapDetail`). `chartsView` incluye `chartLevel`, `chartGrouping`, menús de indicador/modo, estados, `chartCanvas` y `chartExtremes`.
- **EN:** `.results` contains loading/error/empty states, the `incidentResults` table with `incidentRows`, `loadMoreButton`, `cameraResults` cards, and `mapResults` (`trafficMap`, `mapDetail`). `chartsView` includes `chartLevel`, `chartGrouping`, indicator/mode menus, states, `chartCanvas`, and `chartExtremes`.
### Footer
- **ES:** Enlaces a la documentación de API (`/docs`) y al estado del servicio (`/api/health`).
- **EN:** Links to API documentation (`/docs`) and service health (`/api/health`).
