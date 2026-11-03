# dgt_monitor/web/static/index.html
Define la estructura de la aplicación web: cabecera, métricas, filtros, pestañas y paneles de incidencias, cámaras, mapa y gráficas.
## Dependencias
Hoja local `/static/styles.css?v=59`, lógica `/static/app.js?v=59`, manifiesto `/manifest.webmanifest`; Lucide y Leaflet y los estilos de Leaflet se cargan desde CDN. Chart.js 4.4.7 está incluido localmente como `chart.umd.min.js`, sin CDN.
## Contenido
### Cabecera del documento
- Declara español, codificación, viewport, color de tema y descripción; vincula fuentes, manifiesto, Leaflet y CSS. Los scripts de Lucide, Leaflet, Chart.js y `app.js` usan `defer`.
### Cabecera y métricas de resumen
- La cabecera reúne marca, conexión (`connectionStatus`), hora (`lastUpdate`), idioma, tema (`themeButton`) y recarga (`refreshButton`). Las métricas `data-kind` y los IDs `statTotal`, `statAccidents`, `statRoadworks`, `statStuck`, `statObstructions`, `statWeather` muestran valores y permiten filtrar.
### Pestañas y filtros
- Las pestañas `data-view` abren Incidencias, Cámaras, Favoritas, Gráficas o Mapa; `filterToggle` contrae filtros. `filtersPanel` contiene `filterForm` y los campos `provinceFilter`, `roadFilter`, `municipalityFilter`, `severityFilter`, `cameraCoverageFilter`, `kmFilter`, `cameraIncidentFilter` y `limitFilter`; `incidentFilters` y `cameraFilters` agrupan controles específicos.
### Resultados, mapa y gráficas
- `.results` contiene estados de carga/error/vacío, tabla `incidentResults` con `incidentRows`, `loadMoreButton`, tarjetas `cameraResults` y mapa `mapResults` (`trafficMap`, `mapDetail`). `chartsView` incluye `chartLevel`, `chartGrouping`, menús de indicador/modo, estados, `chartCanvas` y `chartExtremes`.
### Pie de página
- Enlaces a la documentación de API (`/docs`) y al estado del servicio (`/api/health`).
