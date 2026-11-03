# dgt_monitor/web/static/app.js
**ES:** Controla la interfaz web: estado, idioma y tema, vistas, carga de datos, incidencias, cámaras, favoritos, mapa y gráficas. Solo se describe el código activo anterior al bloque comentado `Legacy dashboard implementation retained for reference`.
**EN:** Controls the web interface: state, language and theme, views, data loading, incidents, cameras, favorites, map, and charts. Only the active code before the commented `Legacy dashboard implementation retained for reference` block is documented.
## Dependencies / Dependencias
JavaScript del navegador (DOM, `fetch`, `URLSearchParams`, `localStorage`, timers y canvas); endpoints JSON `/api/incidents`, `/api/cameras`, `/api/stats` y `/api/stats/grouped`; globals `Chart`, `L` (Leaflet) y `lucide` cuando están disponibles.
Browser JavaScript (DOM, `fetch`, `URLSearchParams`, `localStorage`, timers, and canvas); JSON endpoints `/api/incidents`, `/api/cameras`, `/api/stats`, and `/api/stats/grouped`; `Chart`, `L` (Leaflet), and `lucide` globals when available.
## Contents / Contenido
### State, startup, language, and theme
El listener `DOMContentLoaded` resuelve elementos por ID, carga favoritos, aplica idioma y tema, conecta controles, registra `/sw.js`, hace la carga inicial y programa actualizaciones. `state` guarda vista/opciones, datos, mapa, tema, filtros y contador de solicitudes; `uiCopy` y `detailLabels` contienen traducciones.
The `DOMContentLoaded` listener resolves elements by ID, loads favorites, applies language and theme, wires controls, registers `/sw.js`, performs the initial load, and schedules refreshes. `state` stores view/options, data, map, theme, filters, and request counter; `uiCopy` and `detailLabels` hold translations.
#### `resolveInitialTheme()`
- **ES:** Devuelve el tema guardado (`dark`/`light`) o el preferido por el sistema.
- **EN:** Returns the saved (`dark`/`light`) theme or the system preference.
#### `toggleTheme()`
- **ES:** Alterna entre claro y oscuro llamando a `applyTheme`.
- **EN:** Toggles between light and dark by calling `applyTheme`.
#### `resolveInitialLanguage()`
- **ES:** Recupera `es` o `en` de `localStorage`; usa español si no hay valor válido.
- **EN:** Reads `es` or `en` from `localStorage`; defaults to Spanish if the value is invalid.
#### `applyLanguage(language, reload = true)`
- **ES:** Normaliza y guarda el idioma, actualiza `lang` y textos, y opcionalmente recarga la vista.
- **EN:** Normalizes and saves the language, updates `lang` and text, and optionally reloads the view.
#### `applyStaticLanguage()`
- **ES:** Traduce textos, etiquetas, opciones, cabeceras y atributos accesibles de la interfaz.
- **EN:** Translates interface text, labels, options, headings, and accessibility attributes.
#### `setMetricLabel(kind, label)`
- **ES:** Cambia el texto de la métrica identificada por `data-kind`.
- **EN:** Changes the label of the metric identified by `data-kind`.
#### `setTabLabel(view, label)`
- **ES:** Cambia el texto de la pestaña correspondiente a `view`.
- **EN:** Changes the text of the tab corresponding to `view`.
#### `setLabelText(control, label)`
- **ES:** Sustituye el nodo de texto directo de la etiqueta que contiene `control`.
- **EN:** Replaces the direct text node in the label containing `control`.
#### `setSubmitButtonText()`
- **ES:** Actualiza el texto del botón principal del formulario de filtros.
- **EN:** Updates the filter form's primary button text.
#### `setSelectOptions(select, values, labels)`
- **ES:** Asigna las etiquetas a las opciones existentes del `<select>` mediante sus valores.
- **EN:** Assigns labels to existing `<select>` options by their values.
#### `setTableHeaders()`
- **ES:** Traduce las seis cabeceras de la tabla de incidencias.
- **EN:** Translates the six incident-table headings.
#### `switchViewLabelOnly()`
- **ES:** Actualiza los títulos y subtítulos de resultados y gráficas para la vista actual.
- **EN:** Updates the results and chart titles and subtitles for the current view.
#### `applyTheme(theme)`
- **ES:** Guarda y aplica el tema al documento, botón y color del navegador; redibuja gráficas visibles.
- **EN:** Saves and applies the theme to the document, button, and browser theme color; redraws a visible chart.

### View switching and data loading
#### `switchView(view)`
- **ES:** Actualiza pestaña, filtros y clases de diseño para `view`, y solicita sus datos.
- **EN:** Updates the tab, filters, and layout classes for `view`, then requests its data.
#### `toggleFilters()`
- **ES:** Muestra u oculta los filtros y recalcula el tamaño del mapa si está inicializado.
- **EN:** Shows or hides filters and resizes an initialized map.
#### `updateFilterToggle()`
- **ES:** Sincroniza estado expandido, título, etiqueta accesible e icono del botón de filtros.
- **EN:** Synchronizes the filter button's expanded state, title, accessible label, and icon.
#### `loadCurrentView()`
- **ES:** Carga incidencias o cámaras según la vista, procesa respuestas/errores e ignora solicitudes obsoletas.
- **EN:** Loads incidents or cameras for the current view, handles responses/errors, and ignores stale requests.
#### `buildParams()`
- **ES:** Construye los parámetros de consulta desde los filtros e incorpora los propios de cada vista.
- **EN:** Builds query parameters from the filters, including those specific to each view.
#### `addParam(params, key, value)`
- **ES:** Recorta `value` y la añade a `URLSearchParams` si no queda vacía.
- **EN:** Trims `value` and adds it to `URLSearchParams` when non-empty.

### Charts tab
#### `loadChartsData(requestId)`
- **ES:** Solicita `/api/stats?level=…&refresh=true` y `/api/stats/grouped`, guarda ambas respuestas y renderiza si la petición sigue vigente.
- **EN:** Fetches `/api/stats?level=…&refresh=true` and `/api/stats/grouped`, stores both responses, and renders if the request is current.
#### `applyChartsLanguage()`
- **ES:** Traduce controles y estados de Gráficas y vuelve a dibujar si hay datos cargados.
- **EN:** Translates Charts controls and states, and redraws when data is loaded.
#### `renderChart()`
- **ES:** Elige grupo e indicador, ordena y limita filas, y dibuja barras, líneas o sectores con Chart.js.
- **EN:** Selects group and indicator, sorts and limits rows, and draws a bar, line, or pie chart with Chart.js.
#### `formatChartExtremes(extremes)`
- **ES:** Formatea máximo y mínimo de estadísticas como texto localizado o indica que faltan.
- **EN:** Formats statistics' maximum and minimum as localized text or indicates missing values.

### Incident rendering and details
#### `renderIncidents(payload)`
- **ES:** Guarda incidencias/estadísticas, actualiza métricas y contadores, dibuja filas y muestra estado vacío si procede.
- **EN:** Stores incidents/statistics, updates metrics and counts, renders rows, and shows the empty state when needed.
#### `updateRelatedTabCounts(payload, requestId)`
- **ES:** Obtiene cámaras cercanas para los contadores de cámaras y mapa; ignora respuestas obsoletas o fuera de Incidencias.
- **EN:** Fetches nearby cameras for camera/map counts; ignores stale responses or responses outside Incidents.
#### `renderIncidentRows()`
- **ES:** Dibuja hasta `incidentLimit` incidencias y actualiza el control para mostrar más.
- **EN:** Renders up to `incidentLimit` incidents and updates the show-more control.
#### `showMoreIncidents()`
- **ES:** Aumenta en 100 el límite visible y vuelve a dibujar las filas.
- **EN:** Increases the visible limit by 100 and redraws the rows.
#### `createIncidentRows(incident)`
- **ES:** Crea la fila accesible de una incidencia y la fila de detalle expandible; devuelve ambas.
- **EN:** Creates an accessible incident row and its expandable detail row; returns both.
#### `createIncidentDetailRow(incident)`
- **ES:** Construye una fila inicialmente oculta con los campos de detalle de la incidencia.
- **EN:** Builds an initially hidden row with the incident's detail fields.
#### `formatDetailValue(key, value)`
- **ES:** Formatea valores vacíos, booleanos, fechas, direcciones y distancias según la clave.
- **EN:** Formats empty values, booleans, dates, directions, and distances according to the key.
#### `detailEntries(item, preferredKeys = [])`
- **ES:** Devuelve pares de etiqueta y valor formateado, poniendo primero las claves preferidas.
- **EN:** Returns label/value pairs with formatted values, placing preferred keys first.
#### `directionContent(incident)`
- **ES:** Crea una abreviatura de dirección cuyo texto original queda como ayuda emergente.
- **EN:** Creates a direction abbreviation with the original text as its tooltip.
#### `formatDirectionValue(value)`
- **ES:** Normaliza direcciones conocidas a abreviaturas y deja valores desconocidos como texto.
- **EN:** Normalizes recognized directions to abbreviations and leaves unknown values as text.
#### `formatHumanDateTime(value)`
- **ES:** Formatea una fecha válida según el idioma actual o devuelve el valor original.
- **EN:** Formats a valid date for the current language or returns the original value.
#### `detailLabel(key)`
- **ES:** Busca una etiqueta localizada y, si falta, humaniza el nombre de la clave.
- **EN:** Looks up a localized label and, if absent, humanizes the key name.
#### `uiText(key)`
- **ES:** Devuelve el texto del idioma actual y evalúa las entradas función con argumentos adicionales.
- **EN:** Returns current-language text and evaluates function entries with extra arguments.

### Cameras and favorites
#### `renderCameras(payload)`
- **ES:** Guarda cámaras, actualiza contadores y tarjetas y muestra la vista de cámaras o vacía.
- **EN:** Stores cameras, updates counts and cards, and shows the camera or empty state.
#### `renderFavoriteCameras()`
- **ES:** Lee favoritos locales, actualiza el contador y muestra sus tarjetas o el estado vacío.
- **EN:** Reads local favorites, updates the count, and renders their cards or the empty state.
#### `createCameraCard(camera)`
- **ES:** Crea una tarjeta con ubicación e imagen, alternativa si no está disponible y acceso al visor.
- **EN:** Creates a card with location and image, an unavailable-image fallback, and viewer access.
#### `createFavoriteButton(camera, className = "")`
- **ES:** Crea el botón accesible de favorito para `camera`, con una clase opcional.
- **EN:** Creates an accessible favorite button for `camera`, with an optional class.
#### `updateFavoriteButton(button, camera)`
- **ES:** Actualiza el botón para indicar si la cámara está guardada como favorita.
- **EN:** Updates the button to show whether the camera is saved as a favorite.
#### `toggleCameraFavorite(camera)`
- **ES:** Añade o elimina la cámara de `localStorage` y actualiza lista, contador y botones visibles.
- **EN:** Adds or removes the camera in `localStorage` and updates the list, count, and visible buttons.
#### `refreshFavoriteButtons(key, active)`
- **ES:** Actualiza estado y etiquetas de los botones con el identificador `key`.
- **EN:** Updates the state and labels of buttons matching identifier `key`.
#### `loadFavoriteCameras()`
- **ES:** Lee y valida el JSON de favoritos; devuelve una lista vacía si es inválido.
- **EN:** Reads and validates favorites JSON; returns an empty list if invalid.
#### `saveFavoriteCameras(cameras)`
- **ES:** Normaliza cámaras y guarda la lista JSON en `localStorage`.
- **EN:** Normalizes cameras and stores the JSON list in `localStorage`.
#### `normalizeFavoriteCamera(camera)`
- **ES:** Conserva los campos usados por favoritos y proporciona valores vacíos o nulos por defecto.
- **EN:** Keeps the fields used by favorites and supplies empty or null defaults.
#### `cameraFavoriteId(camera)`
- **ES:** Usa el ID de cámara o forma una clave con provincia, carretera, PK e imagen.
- **EN:** Uses the camera ID or builds a key from province, road, kilometer point, and image URL.
#### `isFavoriteCamera(camera)`
- **ES:** Comprueba si hay un favorito guardado con el mismo identificador.
- **EN:** Checks whether a saved favorite has the same identifier.
#### `updateFavoriteTabCount()`
- **ES:** Muestra en la pestaña el número de favoritos que contiene el estado.
- **EN:** Displays the number of favorites held in state in the tab.
#### `locationContent(incident)`
- **ES:** Crea la ubicación con municipio, provincia y PK cuando existe.
- **EN:** Creates the location block with municipality, province, and kilometer point when present.
#### `coverageContent(incident)`
- **ES:** Muestra falta de cobertura o un botón que consulta cámaras cercanas a la incidencia.
- **EN:** Shows no-coverage status or a button that fetches cameras near the incident.
#### `openIncidentCameras(incident, wrapper, button)`
- **ES:** Deshabilita temporalmente el botón, consulta cámaras y abre el resultado único o el menú de opciones.
- **EN:** Temporarily disables the button, fetches cameras, and opens the only result or a choice menu.
#### `fetchIncidentCameras(incident)`
- **ES:** Consulta `/api/cameras` con provincia, carretera, PK/coordenadas, límite de hasta 12 y rango de 1 km.
- **EN:** Requests `/api/cameras` with province, road, kilometer point/coordinates, a limit up to 12, and a 1 km range.
#### `showCameraMenu(wrapper, cameras, message = "")`
- **ES:** Inserta un menú con previsualizaciones, datos y favoritos, o un mensaje si no hay cámaras.
- **EN:** Inserts a menu with previews, details, and favorite controls, or a message when no cameras exist.
#### `closeCameraMenus(except = null)`
- **ES:** Cierra menús salvo los contenidos en `except`, si se proporciona.
- **EN:** Closes menus except those contained by `except`, when supplied.
#### `openCameraTarget(camera)`
- **ES:** Abre el visor si hay URL de imagen; si no, configura filtros y cambia a Cámaras.
- **EN:** Opens the viewer when an image URL exists; otherwise sets filters and switches to Cameras.
#### `imageFallback()`
- **ES:** Crea un elemento que indica que la imagen de cámara no está disponible.
- **EN:** Creates an element indicating that the camera image is unavailable.
#### `showCameraMediaFallback(media)`
- **ES:** Sustituye el medio fallido por el mensaje de indisponibilidad y conserva el botón favorito.
- **EN:** Replaces failed media with the unavailable message and preserves the favorite button.
#### `openCameraViewer(src, alt, camera = null)`
- **ES:** Crea un visor modal con cierre y pantalla completa; añade favorito si recibe una cámara.
- **EN:** Creates a modal viewer with close and fullscreen controls; adds a favorite button when given a camera.
#### `disconnectedFallback()`
- **ES:** Crea el mensaje de estado para una imagen ampliada que no responde.
- **EN:** Creates the status message for an unresponsive enlarged image.
#### `isUnavailableCameraImage(image)`
- **ES:** Comprueba dimensiones y muestrea un lienzo para detectar imágenes predominantemente grises de indisponibilidad.
- **EN:** Checks dimensions and samples a canvas to detect predominantly gray unavailable-camera images.

### Map
#### `renderMap(incidentPayload, requestId)`
- **ES:** Combina incidencias con cámaras para el mapa, actualiza contadores y dibuja marcadores si la solicitud sigue vigente.
- **EN:** Combines incidents with map cameras, updates counts, and draws markers if the request is current.
#### `fetchMapCameras(incidents)`
- **ES:** Obtiene cámaras para los ámbitos derivados de filtros/incidencias y elimina duplicados.
- **EN:** Fetches cameras for scopes derived from filters/incidents and removes duplicates.
#### `mapCameraScopes(incidents)`
- **ES:** Decide filtros de cámara según carretera, municipio, provincia y cobertura.
- **EN:** Chooses camera filters based on road, municipality, province, and coverage.
#### `mapMunicipalityCameraScopes(incidents)`
- **ES:** Crea ámbitos únicos a partir de coordenadas de incidencias, con distancia máxima de 25 km.
- **EN:** Creates unique scopes from incident coordinates, with a 25 km maximum distance.
#### `fetchMapCameraScope(scope)`
- **ES:** Consulta `/api/cameras` para un ámbito, pide todos los resultados y añade coordenadas/distancia cuando aplica.
- **EN:** Requests `/api/cameras` for a scope, asks for all results, and adds coordinates/distance when applicable.
#### `renderStats(stats, fallbackTotal = 0)`
- **ES:** Actualiza las seis métricas y usa `fallbackTotal` si no viene el total.
- **EN:** Updates the six metrics and uses `fallbackTotal` if total is absent.
#### `hasCoordinates(item)`
- **ES:** Comprueba que latitud y longitud no sean `null` ni `undefined`.
- **EN:** Checks that latitude and longitude are neither `null` nor `undefined`.
#### `initMap()`
- **ES:** Inicializa Leaflet una vez, con mapa base OpenStreetMap y capas de incidencias y cámaras.
- **EN:** Initializes Leaflet once with an OpenStreetMap base layer and incident and camera layers.
#### `mapIcon(kind, label)`
- **ES:** Crea un `divIcon` Leaflet para un marcador y escapa la etiqueta.
- **EN:** Creates a Leaflet `divIcon` for a marker and escapes its label.
#### `renderMapMarkers()`
- **ES:** Limpia y redibuja marcadores con coordenadas, ventanas emergentes, contadores y encuadre.
- **EN:** Clears and redraws markers with coordinates, popups, counts, and map bounds.
#### `renderMapDetail(kind, item)`
- **ES:** Muestra datos del punto seleccionado; para cámaras añade imagen y favorito si están disponibles.
- **EN:** Displays the selected point's details; for cameras, adds the image and favorite control when available.

### DOM, status, and refresh helpers
#### `badge(value, className)`
- **ES:** Crea un `<span>` con texto y clases de etiqueta.
- **EN:** Creates a `<span>` containing text and badge classes.
#### `text(tag, value, className = "")`
- **ES:** Crea un elemento DOM con texto plano y clase opcional.
- **EN:** Creates a DOM element with plain text and an optional class.
#### `cell(content)`
- **ES:** Crea una celda `<td>` y añade el nodo recibido.
- **EN:** Creates a `<td>` cell and appends the supplied node.
#### `escapeHtml(value)`
- **ES:** Escapa ampersand, signos angulares, comillas y apóstrofos antes de insertar texto en HTML.
- **EN:** Escapes ampersands, angle brackets, quotes, and apostrophes before inserting text into HTML.
#### `safeClass(value)`
- **ES:** Pasa a minúsculas y quita caracteres no permitidos en las clases usadas aquí.
- **EN:** Lowercases a string and removes characters not allowed in the class names used here.
#### `formatSeverity(value)`
- **ES:** Traduce severidades conocidas y usa el valor o texto de dato desconocido como alternativa.
- **EN:** Translates known severity values and falls back to the original or unknown label.
#### `showState(active)`
- **ES:** Muestra el estado de carga, error, vacío, tabla, cámaras o mapa y actualiza `aria-busy`.
- **EN:** Shows the loading, error, empty, table, camera, or map state and updates `aria-busy`.
#### `setEmptyStateText(message)`
- **ES:** Actualiza título y mensaje del estado sin resultados.
- **EN:** Updates the no-results title and message.
#### `setConnection(online)`
- **ES:** Cambia clases y texto del indicador de conexión.
- **EN:** Changes the connection indicator's classes and text.
#### `updateTimestamp(value)`
- **ES:** Actualiza la fecha ISO y muestra la hora localizada; usa la hora actual si no recibe valor.
- **EN:** Updates the ISO date and displays localized time; uses the current time if no value is supplied.
#### `clearFilters()`
- **ES:** Restablece el formulario, fija límite de cámaras en 12, limpia el filtro de tipo y recarga.
- **EN:** Resets the form, sets camera limit to 12, clears the kind filter, and reloads.
#### `applyKindFilter(kind, reload = true)`
- **ES:** Guarda el filtro de tipo, actualiza la métrica activa y opcionalmente recarga datos.
- **EN:** Saves the kind filter, updates the active metric, and optionally reloads data.
#### `scheduleRefresh()`
- **ES:** Reinicia el temporizador y, si está marcada la casilla, programa cargas cada 120 segundos.
- **EN:** Resets the timer and, if the checkbox is enabled, schedules loads every 120 seconds.

> El bloque comentado desde `Legacy dashboard implementation retained for reference` hasta el final se conserva como referencia; no es código activo.
>
> The commented block from `Legacy dashboard implementation retained for reference` to the end is retained for reference; it is not active code.
