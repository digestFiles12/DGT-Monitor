# dgt_monitor/web/static/app.js
Controla la interfaz web: estado, idioma y tema, vistas, carga de datos, incidencias, cámaras, favoritos, mapa y gráficas. Solo se describe el código activo anterior al bloque comentado `Legacy dashboard implementation retained for reference`.
## Dependencias
JavaScript del navegador (DOM, `fetch`, `URLSearchParams`, `localStorage`, timers y canvas); endpoints JSON `/api/incidents`, `/api/cameras`, `/api/stats` y `/api/stats/grouped`; globals `Chart`, `L` (Leaflet) y `lucide` cuando están disponibles.
## Contenido
### Estado, inicio, idioma y tema
El listener `DOMContentLoaded` resuelve elementos por ID, carga favoritos, aplica idioma y tema, conecta controles, registra `/sw.js`, hace la carga inicial y programa actualizaciones. `state` guarda vista/opciones, datos, mapa, tema, filtros, contador de solicitudes y `chartSelection` (un `Set` de geografías seleccionadas); `uiCopy`/`detailLabels` contienen traducciones, incluidos `communityLabel` y los textos `selector*`.
#### `resolveInitialTheme()`
- Devuelve el tema guardado (`dark`/`light`) o el preferido por el sistema.
#### `toggleTheme()`
- Alterna entre claro y oscuro llamando a `applyTheme`.
#### `resolveInitialLanguage()`
- Recupera `es` o `en` de `localStorage`; usa español si no hay valor válido.
#### `applyLanguage(language, reload = true)`
- Normaliza y guarda el idioma, actualiza `lang` y textos, y opcionalmente recarga la vista.
#### `applyStaticLanguage()`
- Traduce textos, etiquetas, opciones, cabeceras y atributos accesibles de la interfaz.
#### `setMetricLabel(kind, label)`
- Cambia el texto de la métrica identificada por `data-kind`.
#### `setTabLabel(view, label)`
- Cambia el texto de la pestaña correspondiente a `view`.
#### `setLabelText(control, label)`
- Sustituye el nodo de texto directo de la etiqueta que contiene `control`.
#### `setSubmitButtonText()`
- Actualiza el texto del botón principal del formulario de filtros.
#### `setSelectOptions(select, values, labels)`
- Asigna las etiquetas a las opciones existentes del `<select>` mediante sus valores; `loadCommunities()` obtiene `/api/regions` para poblar el selector de comunidades y, si falla, conserva «Todas».
#### `setTableHeaders()`
- Traduce las seis cabeceras de la tabla de incidencias.
#### `switchViewLabelOnly()`
- Actualiza los títulos y subtítulos de resultados y gráficas para la vista actual.
#### `applyTheme(theme)`
- Guarda y aplica el tema al documento, botón y color del navegador; redibuja gráficas visibles.

### Cambio de vistas y carga de datos
#### `switchView(view)`
- Actualiza pestaña, filtros y clases de diseño para `view`, y solicita sus datos.
#### `toggleFilters()`
- Muestra u oculta los filtros y recalcula el tamaño del mapa si está inicializado.
#### `updateFilterToggle()`
- Sincroniza estado expandido, título, etiqueta accesible e icono del botón de filtros.
#### `loadCurrentView()`
- Carga incidencias o cámaras según la vista, procesa respuestas/errores e ignora solicitudes obsoletas.
#### `buildParams()`
- Construye los parámetros desde los filtros, siempre envía `community` si está seleccionada, y añade los específicos de la vista; ese filtro también limita las cámaras de los ámbitos del mapa.
#### `addParam(params, key, value)`
- Recorta `value` y la añade a `URLSearchParams` si no queda vacía.

### Pestaña de gráficas
#### `loadChartsData(requestId)`
- Solicita `/api/stats?level=…&refresh=true` y `/api/stats/grouped`, guarda ambas respuestas y renderiza si la petición sigue vigente.
#### `applyChartsLanguage()`
- Traduce controles y estados de Gráficas y vuelve a dibujar si hay datos cargados.
#### `renderChart()`
- `chartSource()` selecciona los datos de nivel, día o tipo; `selectedExtremes()` recalcula máximo y mínimo de la selección; `renderChartSelector()`/`selectorToggle()` implementan búsqueda, selección múltiple, botones seleccionar todo/limpiar, chips removibles y grupos regionales con estado parcial. `renderChart()` restringe los gráficos de nivel/día/tipo y sus extremos a la selección y dibuja con Chart.js.
#### `formatChartExtremes(extremes)`
- Formatea máximo y mínimo de estadísticas como texto localizado o indica que faltan.

### Visualización y detalles de incidencias
#### `renderIncidents(payload)`
- Guarda incidencias/estadísticas, actualiza métricas y contadores, dibuja filas y muestra estado vacío si procede.
#### `updateRelatedTabCounts(payload, requestId)`
- Obtiene cámaras cercanas para los contadores de cámaras y mapa; ignora respuestas obsoletas o fuera de Incidencias.
#### `renderIncidentRows()`
- Dibuja hasta `incidentLimit` incidencias y actualiza el control para mostrar más.
#### `showMoreIncidents()`
- Aumenta en 100 el límite visible y vuelve a dibujar las filas.
#### `createIncidentRows(incident)`
- Crea la fila accesible de una incidencia y la fila de detalle expandible; devuelve ambas.
#### `createIncidentDetailRow(incident)`
- Construye una fila inicialmente oculta con los campos de detalle de la incidencia.
#### `formatDetailValue(key, value)`
- Formatea valores vacíos, booleanos, fechas, direcciones y distancias según la clave.
#### `detailEntries(item, preferredKeys = [])`
- Devuelve pares de etiqueta y valor formateado, poniendo primero las claves preferidas.
#### `directionContent(incident)`
- Crea una abreviatura de dirección cuyo texto original queda como ayuda emergente.
#### `formatDirectionValue(value)`
- Normaliza direcciones conocidas a abreviaturas y deja valores desconocidos como texto.
#### `formatHumanDateTime(value)`
- Formatea una fecha válida según el idioma actual o devuelve el valor original.
#### `detailLabel(key)`
- Busca una etiqueta localizada y, si falta, humaniza el nombre de la clave.
#### `uiText(key)`
- Devuelve el texto del idioma actual y evalúa las entradas función con argumentos adicionales.

### Cámaras y favoritas
#### `renderCameras(payload)`
- Guarda cámaras, actualiza contadores y tarjetas y muestra la vista de cámaras o vacía.
#### `renderFavoriteCameras()`
- Lee favoritos locales, actualiza el contador y muestra sus tarjetas o el estado vacío.
#### `createCameraCard(camera)`
- Crea una tarjeta con ubicación e imagen, alternativa si no está disponible y acceso al visor.
#### `createFavoriteButton(camera, className = "")`
- Crea el botón accesible de favorito para `camera`, con una clase opcional.
#### `updateFavoriteButton(button, camera)`
- Actualiza el botón para indicar si la cámara está guardada como favorita.
#### `toggleCameraFavorite(camera)`
- Añade o elimina la cámara de `localStorage` y actualiza lista, contador y botones visibles.
#### `refreshFavoriteButtons(key, active)`
- Actualiza estado y etiquetas de los botones con el identificador `key`.
#### `loadFavoriteCameras()`
- Lee y valida el JSON de favoritos; devuelve una lista vacía si es inválido.
#### `saveFavoriteCameras(cameras)`
- Normaliza cámaras y guarda la lista JSON en `localStorage`.
#### `normalizeFavoriteCamera(camera)`
- Conserva los campos usados por favoritos y proporciona valores vacíos o nulos por defecto.
#### `cameraFavoriteId(camera)`
- Usa el ID de cámara o forma una clave con provincia, carretera, PK e imagen.
#### `isFavoriteCamera(camera)`
- Comprueba si hay un favorito guardado con el mismo identificador.
#### `updateFavoriteTabCount()`
- Muestra en la pestaña el número de favoritos que contiene el estado.
#### `locationContent(incident)`
- Crea la ubicación con municipio, provincia y PK cuando existe.
#### `coverageContent(incident)`
- Muestra falta de cobertura o un botón que consulta cámaras cercanas a la incidencia.
#### `openIncidentCameras(incident, wrapper, button)`
- Deshabilita temporalmente el botón, consulta cámaras y abre el resultado único o el menú de opciones.
#### `fetchIncidentCameras(incident)`
- Consulta `/api/cameras` con provincia, carretera, PK/coordenadas, límite de hasta 12 y rango de 1 km.
#### `showCameraMenu(wrapper, cameras, message = "")`
- Inserta un menú con previsualizaciones, datos y favoritos, o un mensaje si no hay cámaras.
#### `closeCameraMenus(except = null)`
- Cierra menús salvo los contenidos en `except`, si se proporciona.
#### `openCameraTarget(camera)`
- Abre el visor si hay URL de imagen; si no, configura filtros y cambia a Cámaras.
#### `imageFallback()`
- Crea un elemento que indica que la imagen de cámara no está disponible.
#### `showCameraMediaFallback(media)`
- Sustituye el medio fallido por el mensaje de indisponibilidad y conserva el botón favorito.
#### `openCameraViewer(src, alt, camera = null)`
- Crea un visor modal con cierre y pantalla completa; añade favorito si recibe una cámara.
#### `disconnectedFallback()`
- Crea el mensaje de estado para una imagen ampliada que no responde.
#### `isUnavailableCameraImage(image)`
- Comprueba dimensiones y muestrea un lienzo para detectar imágenes predominantemente grises de indisponibilidad.

### Mapa
#### `renderMap(incidentPayload, requestId)`
- Combina incidencias con cámaras para el mapa, actualiza contadores y dibuja marcadores si la solicitud sigue vigente.
#### `fetchMapCameras(incidents)`
- Obtiene cámaras para los ámbitos derivados de filtros/incidencias y elimina duplicados.
#### `mapCameraScopes(incidents)`
- Decide filtros de cámara según carretera, municipio, provincia y cobertura.
#### `mapMunicipalityCameraScopes(incidents)`
- Crea ámbitos únicos a partir de coordenadas de incidencias, con distancia máxima de 25 km.
#### `fetchMapCameraScope(scope)`
- Consulta `/api/cameras` para un ámbito, pide todos los resultados y añade coordenadas/distancia cuando aplica.
#### `renderStats(stats, fallbackTotal = 0)`
- Actualiza las seis métricas y usa `fallbackTotal` si no viene el total.
#### `hasCoordinates(item)`
- Comprueba que latitud y longitud no sean `null` ni `undefined`.
#### `initMap()`
- Inicializa Leaflet una vez, con mapa base OpenStreetMap y capas de incidencias y cámaras.
#### `mapIcon(kind, label)`
- Crea un `divIcon` Leaflet para un marcador y escapa la etiqueta.
#### `renderMapMarkers()`
- Limpia y redibuja marcadores con coordenadas, ventanas emergentes, contadores y encuadre.
#### `renderMapDetail(kind, item)`
- Muestra datos del punto seleccionado; para cámaras añade imagen y favorito si están disponibles.

### Ayudantes del DOM, estado y actualización
#### `badge(value, className)`
- Crea un `<span>` con texto y clases de etiqueta.
#### `text(tag, value, className = "")`
- Crea un elemento DOM con texto plano y clase opcional.
#### `cell(content)`
- Crea una celda `<td>` y añade el nodo recibido.
#### `escapeHtml(value)`
- Escapa ampersand, signos angulares, comillas y apóstrofos antes de insertar texto en HTML.
#### `safeClass(value)`
- Pasa a minúsculas y quita caracteres no permitidos en las clases usadas aquí.
#### `formatSeverity(value)`
- Traduce severidades conocidas y usa el valor o texto de dato desconocido como alternativa.
#### `showState(active)`
- Muestra el estado de carga, error, vacío, tabla, cámaras o mapa y actualiza `aria-busy`.
#### `setEmptyStateText(message)`
- Actualiza título y mensaje del estado sin resultados.
#### `setConnection(online)`
- Cambia clases y texto del indicador de conexión.
#### `updateTimestamp(value)`
- Actualiza la fecha ISO y muestra la hora localizada; usa la hora actual si no recibe valor.
#### `clearFilters()`
- Restablece el formulario, fija límite de cámaras en 12, limpia el filtro de tipo y recarga.
#### `applyKindFilter(kind, reload = true)`
- Guarda el filtro de tipo, actualiza la métrica activa y opcionalmente recarga datos.
#### `scheduleRefresh()`
- Reinicia el temporizador y, si está marcada la casilla, programa cargas cada 120 segundos.
