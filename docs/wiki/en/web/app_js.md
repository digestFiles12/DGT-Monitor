# dgt_monitor/web/static/app.js
Controls the web interface: state, language and theme, views, data loading, incidents, cameras, favorites, map, and charts. Only the active code before the commented `Legacy dashboard implementation retained for reference` block is documented.
## Dependencies
Browser JavaScript (DOM, `fetch`, `URLSearchParams`, `localStorage`, timers, and canvas); JSON endpoints `/api/incidents`, `/api/cameras`, `/api/stats`, and `/api/stats/grouped`; `Chart`, `L` (Leaflet), and `lucide` globals when available.
## Contents
### State, startup, language, and theme
The `DOMContentLoaded` listener resolves elements by ID, loads favorites, applies language and theme, wires controls, registers `/sw.js`, performs the initial load, and schedules refreshes. `state` stores view/options, data, map, theme, filters, and request counter; `uiCopy` and `detailLabels` hold translations.
#### `resolveInitialTheme()`
- Returns the saved (`dark`/`light`) theme or the system preference.
#### `toggleTheme()`
- Toggles between light and dark by calling `applyTheme`.
#### `resolveInitialLanguage()`
- Reads `es` or `en` from `localStorage`; defaults to Spanish if the value is invalid.
#### `applyLanguage(language, reload = true)`
- Normalizes and saves the language, updates `lang` and text, and optionally reloads the view.
#### `applyStaticLanguage()`
- Translates interface text, labels, options, headings, and accessibility attributes.
#### `setMetricLabel(kind, label)`
- Changes the label of the metric identified by `data-kind`.
#### `setTabLabel(view, label)`
- Changes the text of the tab corresponding to `view`.
#### `setLabelText(control, label)`
- Replaces the direct text node in the label containing `control`.
#### `setSubmitButtonText()`
- Updates the filter form's primary button text.
#### `setSelectOptions(select, values, labels)`
- Assigns labels to existing `<select>` options by their values.
#### `setTableHeaders()`
- Translates the six incident-table headings.
#### `switchViewLabelOnly()`
- Updates the results and chart titles and subtitles for the current view.
#### `applyTheme(theme)`
- Saves and applies the theme to the document, button, and browser theme color; redraws a visible chart.

### View switching and data loading
#### `switchView(view)`
- Updates the tab, filters, and layout classes for `view`, then requests its data.
#### `toggleFilters()`
- Shows or hides filters and resizes an initialized map.
#### `updateFilterToggle()`
- Synchronizes the filter button's expanded state, title, accessible label, and icon.
#### `loadCurrentView()`
- Loads incidents or cameras for the current view, handles responses/errors, and ignores stale requests.
#### `buildParams()`
- Builds query parameters from the filters, including those specific to each view.
#### `addParam(params, key, value)`
- Trims `value` and adds it to `URLSearchParams` when non-empty.

### Charts tab
#### `loadChartsData(requestId)`
- Fetches `/api/stats?level=…&refresh=true` and `/api/stats/grouped`, stores both responses, and renders if the request is current.
#### `applyChartsLanguage()`
- Translates Charts controls and states, and redraws when data is loaded.
#### `renderChart()`
- Selects group and indicator, sorts and limits rows, and draws a bar, line, or pie chart with Chart.js.
#### `formatChartExtremes(extremes)`
- Formats statistics' maximum and minimum as localized text or indicates missing values.

### Incident rendering and details
#### `renderIncidents(payload)`
- Stores incidents/statistics, updates metrics and counts, renders rows, and shows the empty state when needed.
#### `updateRelatedTabCounts(payload, requestId)`
- Fetches nearby cameras for camera/map counts; ignores stale responses or responses outside Incidents.
#### `renderIncidentRows()`
- Renders up to `incidentLimit` incidents and updates the show-more control.
#### `showMoreIncidents()`
- Increases the visible limit by 100 and redraws the rows.
#### `createIncidentRows(incident)`
- Creates an accessible incident row and its expandable detail row; returns both.
#### `createIncidentDetailRow(incident)`
- Builds an initially hidden row with the incident's detail fields.
#### `formatDetailValue(key, value)`
- Formats empty values, booleans, dates, directions, and distances according to the key.
#### `detailEntries(item, preferredKeys = [])`
- Returns label/value pairs with formatted values, placing preferred keys first.
#### `directionContent(incident)`
- Creates a direction abbreviation with the original text as its tooltip.
#### `formatDirectionValue(value)`
- Normalizes recognized directions to abbreviations and leaves unknown values as text.
#### `formatHumanDateTime(value)`
- Formats a valid date for the current language or returns the original value.
#### `detailLabel(key)`
- Looks up a localized label and, if absent, humanizes the key name.
#### `uiText(key)`
- Returns current-language text and evaluates function entries with extra arguments.

### Cameras and favorites
#### `renderCameras(payload)`
- Stores cameras, updates counts and cards, and shows the camera or empty state.
#### `renderFavoriteCameras()`
- Reads local favorites, updates the count, and renders their cards or the empty state.
#### `createCameraCard(camera)`
- Creates a card with location and image, an unavailable-image fallback, and viewer access.
#### `createFavoriteButton(camera, className = "")`
- Creates an accessible favorite button for `camera`, with an optional class.
#### `updateFavoriteButton(button, camera)`
- Updates the button to show whether the camera is saved as a favorite.
#### `toggleCameraFavorite(camera)`
- Adds or removes the camera in `localStorage` and updates the list, count, and visible buttons.
#### `refreshFavoriteButtons(key, active)`
- Updates the state and labels of buttons matching identifier `key`.
#### `loadFavoriteCameras()`
- Reads and validates favorites JSON; returns an empty list if invalid.
#### `saveFavoriteCameras(cameras)`
- Normalizes cameras and stores the JSON list in `localStorage`.
#### `normalizeFavoriteCamera(camera)`
- Keeps the fields used by favorites and supplies empty or null defaults.
#### `cameraFavoriteId(camera)`
- Uses the camera ID or builds a key from province, road, kilometer point, and image URL.
#### `isFavoriteCamera(camera)`
- Checks whether a saved favorite has the same identifier.
#### `updateFavoriteTabCount()`
- Displays the number of favorites held in state in the tab.
#### `locationContent(incident)`
- Creates the location block with municipality, province, and kilometer point when present.
#### `coverageContent(incident)`
- Shows no-coverage status or a button that fetches cameras near the incident.
#### `openIncidentCameras(incident, wrapper, button)`
- Temporarily disables the button, fetches cameras, and opens the only result or a choice menu.
#### `fetchIncidentCameras(incident)`
- Requests `/api/cameras` with province, road, kilometer point/coordinates, a limit up to 12, and a 1 km range.
#### `showCameraMenu(wrapper, cameras, message = "")`
- Inserts a menu with previews, details, and favorite controls, or a message when no cameras exist.
#### `closeCameraMenus(except = null)`
- Closes menus except those contained by `except`, when supplied.
#### `openCameraTarget(camera)`
- Opens the viewer when an image URL exists; otherwise sets filters and switches to Cameras.
#### `imageFallback()`
- Creates an element indicating that the camera image is unavailable.
#### `showCameraMediaFallback(media)`
- Replaces failed media with the unavailable message and preserves the favorite button.
#### `openCameraViewer(src, alt, camera = null)`
- Creates a modal viewer with close and fullscreen controls; adds a favorite button when given a camera.
#### `disconnectedFallback()`
- Creates the status message for an unresponsive enlarged image.
#### `isUnavailableCameraImage(image)`
- Checks dimensions and samples a canvas to detect predominantly gray unavailable-camera images.

### Map
#### `renderMap(incidentPayload, requestId)`
- Combines incidents with map cameras, updates counts, and draws markers if the request is current.
#### `fetchMapCameras(incidents)`
- Fetches cameras for scopes derived from filters/incidents and removes duplicates.
#### `mapCameraScopes(incidents)`
- Chooses camera filters based on road, municipality, province, and coverage.
#### `mapMunicipalityCameraScopes(incidents)`
- Creates unique scopes from incident coordinates, with a 25 km maximum distance.
#### `fetchMapCameraScope(scope)`
- Requests `/api/cameras` for a scope, asks for all results, and adds coordinates/distance when applicable.
#### `renderStats(stats, fallbackTotal = 0)`
- Updates the six metrics and uses `fallbackTotal` if total is absent.
#### `hasCoordinates(item)`
- Checks that latitude and longitude are neither `null` nor `undefined`.
#### `initMap()`
- Initializes Leaflet once with an OpenStreetMap base layer and incident and camera layers.
#### `mapIcon(kind, label)`
- Creates a Leaflet `divIcon` for a marker and escapes its label.
#### `renderMapMarkers()`
- Clears and redraws markers with coordinates, popups, counts, and map bounds.
#### `renderMapDetail(kind, item)`
- Displays the selected point's details; for cameras, adds the image and favorite control when available.

### DOM, status, and refresh helpers
#### `badge(value, className)`
- Creates a `<span>` containing text and badge classes.
#### `text(tag, value, className = "")`
- Creates a DOM element with plain text and an optional class.
#### `cell(content)`
- Creates a `<td>` cell and appends the supplied node.
#### `escapeHtml(value)`
- Escapes ampersands, angle brackets, quotes, and apostrophes before inserting text into HTML.
#### `safeClass(value)`
- Lowercases a string and removes characters not allowed in the class names used here.
#### `formatSeverity(value)`
- Translates known severity values and falls back to the original or unknown label.
#### `showState(active)`
- Shows the loading, error, empty, table, camera, or map state and updates `aria-busy`.
#### `setEmptyStateText(message)`
- Updates the no-results title and message.
#### `setConnection(online)`
- Changes the connection indicator's classes and text.
#### `updateTimestamp(value)`
- Updates the ISO date and displays localized time; uses the current time if no value is supplied.
#### `clearFilters()`
- Resets the form, sets camera limit to 12, clears the kind filter, and reloads.
#### `applyKindFilter(kind, reload = true)`
- Saves the kind filter, updates the active metric, and optionally reloads data.
#### `scheduleRefresh()`
- Resets the timer and, if the checkbox is enabled, schedules loads every 120 seconds.
