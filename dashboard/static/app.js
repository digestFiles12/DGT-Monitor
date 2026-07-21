const state = {
  view: "incidents",
  incidents: [],
  cameras: [],
  favoriteCameras: [],
  incidentLimit: 100,
  timer: null,
  theme: "light",
  language: "es",
  kind: "",
  map: null,
  incidentLayer: null,
  cameraLayer: null,
  requestId: 0,
};

const cameraFavoritesKey = "dgt-monitor-camera-favorites";

const incidentDetailFields = [
  "id", "record_id", "version", "source", "creation_time", "start_time", "end_time",
  "severity_label", "type_label", "cause_label", "road", "destination", "municipality", "province",
  "community", "km", "direction_label", "direction_road_label", "latitude", "longitude",
  "lane_usage_label", "management_type_label", "maintenance_type_label", "information_status_label",
  "probability_label", "compliance_label", "vehicle_type_label", "temp_speed_limit",
  "environment_type_label", "road_condition_type_label", "location_description", "geographic_descriptor",
  "has_camera_coverage", "camera_coverage_count", "nearest_camera_km_delta"
];
const timeDetailFields = new Set(["creation_time", "start_time", "end_time"]);

const detailLabels = {
  es: {
    id: "ID", record_id: "Registro", version: "Versión", source: "Fuente", creation_time: "Creación",
    start_time: "Inicio", end_time: "Fin", severity_label: "Gravedad", type_label: "Tipo", cause_label: "Causa",
    road: "Carretera", destination: "Destino", municipality: "Municipio", province: "Provincia", community: "Comunidad",
    km: "Punto kilométrico", direction: "Dirección original", direction_label: "Dirección", direction_road: "Carretera de dirección", direction_road_label: "Carretera de dirección",
    latitude: "Latitud", longitude: "Longitud", lane_usage_label: "Uso de carril", management_type_label: "Gestión",
    maintenance_type_label: "Mantenimiento", information_status_label: "Estado de información", probability_label: "Probabilidad",
    compliance_label: "Cumplimiento", vehicle_type_label: "Vehículo", temp_speed_limit: "Límite temporal",
    environment_type_label: "Entorno", road_condition_type_label: "Estado de vía", location_description: "Descripción de ubicación",
    geographic_descriptor: "Descriptor geográfico", has_camera_coverage: "Cobertura de cámaras", camera_coverage_count: "Cámaras cercanas",
    nearest_camera_km_delta: "Distancia a la cámara", image_url: "URL de imagen", distance_km: "Distancia", km_delta: "Diferencia de PK",
  },
  en: {
    id: "ID", record_id: "Record", version: "Version", source: "Source", creation_time: "Created",
    start_time: "Start", end_time: "End", severity_label: "Severity", type_label: "Type", cause_label: "Cause",
    road: "Road", destination: "Destination", municipality: "Municipality", province: "Province", community: "Region",
    km: "Kilometer point", direction: "Original direction", direction_label: "Direction", direction_road: "Road direction", direction_road_label: "Road direction",
    latitude: "Latitude", longitude: "Longitude", lane_usage_label: "Lane usage", management_type_label: "Management",
    maintenance_type_label: "Maintenance", information_status_label: "Information status", probability_label: "Probability",
    compliance_label: "Compliance", vehicle_type_label: "Vehicle", temp_speed_limit: "Temporary speed limit",
    environment_type_label: "Environment", road_condition_type_label: "Road condition", location_description: "Location description",
    geographic_descriptor: "Geographic descriptor", has_camera_coverage: "Camera coverage", camera_coverage_count: "Nearby cameras",
    nearest_camera_km_delta: "Camera distance", image_url: "Image URL", distance_km: "Distance", km_delta: "KP difference",
  },
};

const uiCopy = {
  es: {
    brandSubtitle: "Estado de la red viaria", connecting: "Conectando", online: "En línea", offline: "Sin conexión", notUpdated: "Sin actualizar",
    provincePlaceholder: "Ej. Madrid", roadPlaceholder: "Ej. A-6", municipalityPlaceholder: "Todos", kmPlaceholder: "Ej. 24.5",
    darkOn: "Activar modo oscuro", darkOff: "Activar modo claro", refresh: "Actualizar datos", operations: "Panel operativo",
    title: "Tráfico en tiempo real", intro: "Consulta incidencias activas y cámaras de la red estatal desde una única vista.",
    total: "Total", accidents: "Accidentes", roadworks: "Obras", stuck: "Averías", obstructions: "Obstrucciones", weather: "Meteorología",
    incidents: "Incidencias", cameras: "Cámaras", favorites: "Favoritas", map: "Mapa", query: "Consulta", filters: "Filtros", hideFilters: "Ocultar filtros", showFilters: "Mostrar filtros", clear: "Limpiar", province: "Provincia",
    road: "Carretera", location: "Ubicación", type: "Tipo", direction: "Dirección", municipality: "Municipio", severity: "Gravedad", camera: "Cámara", searchMode: "Modo de búsqueda", searchContains: "Contiene", searchExact: "Exacta", searchRegex: "Regex", kilometerPoint: "Punto kilométrico",
    cameraLimit: "Máximo de cámaras", cameraIncidentCoverage: "Incidencia con cámara", all: "Todas", withCamera: "Con cámara", withoutCamera: "Sin cámara", severityHighest: "Muy alta", severityHigh: "Alta", severityMedium: "Media", severityLow: "Baja", applyFilters: "Aplicar filtros", autoRefresh: "Actualizar cada 2 minutos", roadNetwork: "Red viaria",
    visualObservation: "Observación visual", activeIncidents: "Incidencias activas", trafficCameras: "Cámaras de tráfico", loadingTitle: "Consultando datos de tráfico",
    loadingText: "La primera carga puede tardar unos segundos.", errorTitle: "No se pudieron cargar los datos", retry: "Reintentar", emptyTitle: "Sin resultados",
    emptyText: "Prueba a ampliar o limpiar los filtros.", api: "API", serviceStatus: "Estado del servicio", unknownSeverity: "Sin dato",
    unclassified: "Sin clasificar", incidentDetail: "Detalle de incidencia", dgtData: "Datos de DGT", unavailableLocation: "Ubicación no disponible", noCoverage: "Sin cobertura",
    noCameraRange: "Sin cámara en rango por PK", cameraUnavailable: "Imagen no disponible", cameraUnavailableLong: "La cámara no está respondiendo ahora mismo.", unavailableProvince: "Provincia no disponible",
    unidentifiedRoad: "Carretera sin identificar", dgtCamera: "Cámara DGT", cameraImage: "Imagen de cámara", favoriteCameras: "Cámaras favoritas", favoriteCamera: "Marcar cámara favorita", unfavoriteCamera: "Quitar cámara favorita", unavailableFavorites: "No hay cámaras favoritas.", unavailableCameras: "No hay cámaras disponibles.", cameraLoadError: "No se pudieron cargar las cámaras cercanas.", serverUnavailable: "La fuente de datos DGT no está disponible temporalmente.",
    connectionRetry: "Revisa la conexión y vuelve a intentarlo.", imageOpenFullscreen: "Abrir imagen a pantalla completa", closeImage: "Cerrar imagen",
    cameraImageFullscreen: "Abrir imagen de cámara a pantalla completa", serverStatus: (status) => `El servidor respondió con código ${status}.`, results: (count) => `${count} resultados`, loadMore: (count) => `Mostrar ${count} más`,
    nearbyCameras: (count) => `${count} cámaras cercanas`, cameraAlt: (road, km) => `Cámara ${road || "DGT"} PK ${km || "sin dato"}`, updatedAt: (time) => `Actualizado ${time}`,
    mapPointPrompt: "Selecciona un punto", mapPointPromptText: "Elige una incidencia o cámara en el mapa para ver sus detalles.", mapUnavailable: "Mapa no disponible", mapSummary: (incidents, cameras) => `${incidents} incidencias · ${cameras} cámaras`, incidentPoint: "Incidencia", cameraPoint: "Cámara", yes: "Sí", no: "No",
  },
  en: {
    brandSubtitle: "Road network status", connecting: "Connecting", online: "Online", offline: "Offline", notUpdated: "Not updated",
    provincePlaceholder: "E.g. Madrid", roadPlaceholder: "E.g. A-6", municipalityPlaceholder: "All", kmPlaceholder: "E.g. 24.5",
    darkOn: "Enable dark mode", darkOff: "Enable light mode", refresh: "Refresh data", operations: "Operations panel",
    title: "Real-time traffic", intro: "Check active incidents and traffic cameras across the state road network from one view.",
    total: "Total", accidents: "Accidents", roadworks: "Roadworks", stuck: "Breakdowns", obstructions: "Obstructions", weather: "Weather",
    incidents: "Incidents", cameras: "Cameras", favorites: "Favorites", map: "Map", query: "Query", filters: "Filters", hideFilters: "Hide filters", showFilters: "Show filters", clear: "Clear", province: "Province",
    road: "Road", location: "Location", type: "Type", direction: "Direction", municipality: "Municipality", severity: "Severity", camera: "Camera", searchMode: "Search mode", searchContains: "Contains", searchExact: "Exact", searchRegex: "Regex", kilometerPoint: "Kilometer point",
    cameraLimit: "Maximum cameras", cameraIncidentCoverage: "Incident with camera", all: "All", withCamera: "With camera", withoutCamera: "Without camera", severityHighest: "Critical", severityHigh: "High", severityMedium: "Medium", severityLow: "Low", applyFilters: "Apply filters", autoRefresh: "Refresh every 2 minutes", roadNetwork: "Road network",
    visualObservation: "Visual observation", activeIncidents: "Active incidents", trafficCameras: "Traffic cameras", loadingTitle: "Checking traffic data",
    loadingText: "The first load can take a few seconds.", errorTitle: "Could not load data", retry: "Retry", emptyTitle: "No results",
    emptyText: "Try broadening or clearing the filters.", api: "API", serviceStatus: "Service status", unknownSeverity: "N/A",
    unclassified: "Unclassified", incidentDetail: "Incident detail", dgtData: "DGT data", unavailableLocation: "Location unavailable", noCoverage: "No coverage",
    noCameraRange: "No camera in kilometer range", cameraUnavailable: "Image unavailable", cameraUnavailableLong: "The camera is not responding right now.", unavailableProvince: "Province unavailable",
    unidentifiedRoad: "Unidentified road", dgtCamera: "DGT camera", cameraImage: "Camera image", favoriteCameras: "Favorite cameras", favoriteCamera: "Mark favorite camera", unfavoriteCamera: "Remove favorite camera", unavailableFavorites: "No favorite cameras.", unavailableCameras: "No cameras available.", cameraLoadError: "Could not load nearby cameras.", serverUnavailable: "The DGT data source is temporarily unavailable.",
    connectionRetry: "Check the connection and try again.", imageOpenFullscreen: "Open image fullscreen", closeImage: "Close image",
    cameraImageFullscreen: "Open camera image fullscreen", serverStatus: (status) => `The server responded with status ${status}.`, results: (count) => `${count} results`, loadMore: (count) => `Show ${count} more`,
    nearbyCameras: (count) => `${count} nearby cameras`, cameraAlt: (road, km) => `Camera ${road || "DGT"} KP ${km || "unavailable"}`, updatedAt: (time) => `Updated ${time}`,
    mapPointPrompt: "Select a point", mapPointPromptText: "Choose an incident or camera on the map to see its details.", mapUnavailable: "Map unavailable", mapSummary: (incidents, cameras) => `${incidents} incidents · ${cameras} cameras`, incidentPoint: "Incident", cameraPoint: "Camera", yes: "Yes", no: "No",
  },
};

const elements = {};
const ids = [
  "connectionStatus", "lastUpdate", "refreshButton", "filterForm", "clearFilters",
  "matchModeFilter", "provinceFilter", "roadFilter", "municipalityFilter", "severityFilter", "cameraCoverageFilter", "kmFilter",
  "cameraIncidentFilter", "limitFilter", "incidentFilters", "cameraFilters", "autoRefresh", "statTotal",
  "statAccidents", "statRoadworks", "statStuck", "statObstructions", "statWeather", "incidentTabCount",
  "cameraTabCount", "favoriteTabCount", "mapTabCount", "resultsTitle", "resultEyebrow", "resultCount", "loadingState",
  "errorState", "errorMessage", "emptyState", "incidentResults", "incidentRows",
  "cameraResults", "mapResults", "mapStatus", "mapDetail", "trafficMap", "retryButton", "loadMoreWrap", "loadMoreButton", "themeButton", "workspace", "filtersPanel", "filterToggle"
];

document.addEventListener("DOMContentLoaded", () => {
  ids.forEach((id) => { elements[id] = document.getElementById(id); });
  state.favoriteCameras = loadFavoriteCameras();
  applyTheme(resolveInitialTheme());
  applyLanguage(resolveInitialLanguage(), false);
  document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));
  document.querySelectorAll(".metric").forEach((metric) => metric.addEventListener("click", () => applyKindFilter(metric.dataset.kind || "")));
  document.querySelectorAll(".language-button").forEach((button) => button.addEventListener("click", () => applyLanguage(button.dataset.language || "es")));
  elements.filterForm.addEventListener("submit", (event) => { event.preventDefault(); loadCurrentView(); });
  elements.clearFilters.addEventListener("click", clearFilters);
  elements.refreshButton.addEventListener("click", loadCurrentView);
  elements.retryButton.addEventListener("click", loadCurrentView);
  elements.loadMoreButton.addEventListener("click", showMoreIncidents);
  elements.autoRefresh.addEventListener("change", scheduleRefresh);
  elements.themeButton.addEventListener("click", toggleTheme);
  elements.filterToggle.addEventListener("click", toggleFilters);
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".coverage-menu") && !event.target.closest(".coverage-button")) closeCameraMenus();
  });
  window.addEventListener("online", loadCurrentView);
  window.addEventListener("offline", () => setConnection(false));
  window.addEventListener("resize", () => { if (state.map) state.map.invalidateSize(); });
  if (window.lucide) window.lucide.createIcons();
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
  loadCurrentView();
  scheduleRefresh();
});

function resolveInitialTheme() {
  const stored = localStorage.getItem("dgt-monitor-theme");
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function toggleTheme() {
  applyTheme(state.theme === "dark" ? "light" : "dark");
}

function resolveInitialLanguage() {
  const stored = localStorage.getItem("dgt-monitor-language");
  if (stored === "es" || stored === "en") return stored;
  return "es";
}

function applyLanguage(language, reload = true) {
  const nextLanguage = language === "en" ? "en" : "es";
  state.language = nextLanguage;
  localStorage.setItem("dgt-monitor-language", nextLanguage);
  document.documentElement.lang = nextLanguage;
  document.querySelectorAll(".language-button").forEach((button) => {
    const active = button.dataset.language === nextLanguage;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  applyStaticLanguage();
  if (reload) loadCurrentView();
}

function applyStaticLanguage() {
  document.querySelector(".brand small").textContent = uiText("brandSubtitle");
  elements.clearFilters.textContent = uiText("clear");
  if (!elements.connectionStatus.classList.contains("is-online") && !elements.connectionStatus.classList.contains("is-offline")) {
    elements.connectionStatus.lastChild.textContent = uiText("connecting");
  }
  if (!elements.lastUpdate.dateTime) elements.lastUpdate.textContent = uiText("notUpdated");
  elements.refreshButton.title = uiText("refresh");
  elements.refreshButton.setAttribute("aria-label", uiText("refresh"));
  setMetricLabel("", uiText("total"));
  setMetricLabel("accident", uiText("accidents"));
  setMetricLabel("roadworks", uiText("roadworks"));
  setMetricLabel("stuck", uiText("stuck"));
  setMetricLabel("obstruction", uiText("obstructions"));
  setMetricLabel("weather", uiText("weather"));
  setTabLabel("incidents", uiText("incidents"));
  setTabLabel("cameras", uiText("cameras"));
  setTabLabel("favorites", uiText("favorites"));
  setTabLabel("map", uiText("map"));
  updateFavoriteTabCount();
  document.querySelector(".filter-heading .eyebrow").textContent = uiText("query");
  document.getElementById("filterTitle").textContent = uiText("filters");
  updateFilterToggle();
  setLabelText(elements.provinceFilter, uiText("province"));
  setLabelText(elements.matchModeFilter, uiText("searchMode"));
  setLabelText(elements.roadFilter, uiText("road"));
  setLabelText(elements.municipalityFilter, uiText("municipality"));
  setLabelText(elements.severityFilter, uiText("severity"));
  setLabelText(elements.cameraCoverageFilter, uiText("camera"));
  setLabelText(elements.kmFilter, uiText("kilometerPoint"));
  setLabelText(elements.cameraIncidentFilter, uiText("cameraIncidentCoverage"));
  setLabelText(elements.limitFilter, uiText("cameraLimit"));
  elements.provinceFilter.placeholder = uiText("provincePlaceholder");
  elements.roadFilter.placeholder = uiText("roadPlaceholder");
  elements.municipalityFilter.placeholder = uiText("municipalityPlaceholder");
  elements.kmFilter.placeholder = uiText("kmPlaceholder");
  setSelectOptions(elements.severityFilter, ["", "highest", "high", "medium", "low"], [uiText("all"), uiText("severityHighest"), uiText("severityHigh"), uiText("severityMedium"), uiText("severityLow")]);
  setSelectOptions(elements.cameraCoverageFilter, ["", "with", "without"], [uiText("all"), uiText("withCamera"), uiText("withoutCamera")]);
  setSelectOptions(elements.matchModeFilter, ["contains", "exact", "regex"], [uiText("searchContains"), uiText("searchExact"), uiText("searchRegex")]);
  setSubmitButtonText();
  document.querySelector(".auto-refresh span").textContent = uiText("autoRefresh");
  document.querySelector("#loadingState strong").textContent = uiText("loadingTitle");
  document.querySelector("#loadingState p").textContent = uiText("loadingText");
  document.querySelector("#errorState strong").textContent = uiText("errorTitle");
  elements.retryButton.textContent = uiText("retry");
  setEmptyStateText(uiText("emptyText"));
  setTableHeaders();
  document.querySelector("footer a[href='/docs']").textContent = uiText("api");
  document.querySelector("footer a[href='/api/health']").textContent = uiText("serviceStatus");
  switchViewLabelOnly();
  applyTheme(state.theme);
}

function setMetricLabel(kind, label) {
  document.querySelector(`.metric[data-kind="${kind}"] span`).textContent = label;
}

function setTabLabel(view, label) {
  const tab = document.querySelector(`.tab[data-view="${view}"]`);
  tab.querySelector(".tab-label").textContent = label;
}

function setLabelText(control, label) {
  const textNode = Array.from(control.closest("label").childNodes).find((node) => node.nodeType === Node.TEXT_NODE);
  if (textNode) textNode.textContent = label;
}

function setSubmitButtonText() {
  const button = elements.filterForm.querySelector(".primary-button");
  button.lastChild.textContent = ` ${uiText("applyFilters")}`;
}

function setSelectOptions(select, values, labels) {
  values.forEach((value, index) => {
    const option = Array.from(select.options).find((item) => item.value === value);
    if (option) option.textContent = labels[index];
  });
}

function setTableHeaders() {
  const labels = [uiText("severity"), uiText("road"), uiText("location"), uiText("type"), uiText("direction"), uiText("cameras")];
  document.querySelectorAll("#incidentResults th").forEach((header, index) => { header.textContent = labels[index]; });
}

function switchViewLabelOnly() {
  elements.resultsTitle.textContent = state.view === "favorites" ? uiText("favoriteCameras") : state.view === "cameras" ? uiText("trafficCameras") : state.view === "map" ? uiText("map") : uiText("activeIncidents");
  elements.resultEyebrow.textContent = state.view === "cameras" || state.view === "favorites" ? uiText("visualObservation") : uiText("roadNetwork");
}

function applyTheme(theme) {
  state.theme = theme;
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("dgt-monitor-theme", theme);
  const dark = theme === "dark";
  elements.themeButton.setAttribute("aria-pressed", String(dark));
  elements.themeButton.setAttribute("aria-label", dark ? uiText("darkOff") : uiText("darkOn"));
  elements.themeButton.title = dark ? uiText("darkOff") : uiText("darkOn");
  elements.themeButton.innerHTML = `<i data-lucide="${dark ? "sun" : "moon"}" aria-hidden="true"></i>`;
  document.querySelector('meta[name="theme-color"]')?.setAttribute("content", dark ? "#101820" : "#b91c1c");
  if (window.lucide) window.lucide.createIcons();
}

function switchView(view) {
  state.view = view;
  elements.workspace.classList.toggle("is-map-view", view === "map");
  document.body.classList.toggle("is-map-view", view === "map");
  document.querySelectorAll(".tab").forEach((tab) => {
    const active = tab.dataset.view === view;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
  });
  elements.incidentFilters.hidden = view === "cameras" || view === "favorites";
  elements.cameraFilters.hidden = view !== "cameras";
  switchViewLabelOnly();
  loadCurrentView();
}

function toggleFilters() {
  const collapsed = elements.workspace.classList.toggle("is-filters-hidden");
  elements.filtersPanel.hidden = collapsed;
  updateFilterToggle();
  if (state.map) setTimeout(() => state.map.invalidateSize(), 180);
}

function updateFilterToggle() {
  const collapsed = elements.workspace?.classList.contains("is-filters-hidden") || false;
  elements.filterToggle.setAttribute("aria-expanded", String(!collapsed));
  elements.filterToggle.setAttribute("aria-label", collapsed ? uiText("showFilters") : uiText("hideFilters"));
  elements.filterToggle.title = collapsed ? uiText("showFilters") : uiText("hideFilters");
  elements.filterToggle.querySelector("i")?.setAttribute("data-lucide", collapsed ? "panel-left-open" : "panel-left-close");
  if (window.lucide) window.lucide.createIcons();
}

async function loadCurrentView() {
  const requestId = ++state.requestId;
  if (state.view === "favorites") {
    renderFavoriteCameras();
    return;
  }
  setEmptyStateText(uiText("emptyText"));
  showState("loading");
  elements.refreshButton.classList.add("is-loading");
  try {
    const params = buildParams();
    const endpoint = state.view === "cameras" ? "/api/cameras" : "/api/incidents";
    const response = await fetch(`${endpoint}?${params.toString()}`, { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(response.status === 502 ? uiText("serverUnavailable") : uiText("serverStatus", response.status));
    const payload = await response.json();
    if (requestId !== state.requestId) return;
    if (state.view === "cameras") renderCameras(payload);
    else if (state.view === "map") await renderMap(payload, requestId);
    else {
      renderIncidents(payload);
      await updateRelatedTabCounts(payload, requestId);
    }
    if (requestId !== state.requestId) return;
    updateTimestamp(payload.updated_at);
    setConnection(true);
  } catch (error) {
    if (requestId !== state.requestId) return;
    elements.errorMessage.textContent = error.message || uiText("connectionRetry");
    showState("error");
    setConnection(false);
  } finally {
    if (requestId === state.requestId) elements.refreshButton.classList.remove("is-loading");
  }
}

function buildParams() {
  const params = new URLSearchParams();
  addParam(params, "match_mode", elements.matchModeFilter.value === "contains" ? "" : elements.matchModeFilter.value);
  addParam(params, "province", elements.provinceFilter.value);
  addParam(params, "road", elements.roadFilter.value.toUpperCase());
  if (state.view !== "cameras") {
    addParam(params, "lang", state.language);
    addParam(params, "municipality", elements.municipalityFilter.value);
    addParam(params, "severity", elements.severityFilter.value);
    addParam(params, "camera", elements.cameraCoverageFilter.value);
    addParam(params, "kind", state.kind);
  } else {
    addParam(params, "km", elements.kmFilter.value);
    if (elements.cameraIncidentFilter.checked) params.set("incident_coverage", "true");
    addParam(params, "limit", elements.limitFilter.value);
  }
  return params;
}

function addParam(params, key, value) {
  const clean = String(value ?? "").trim();
  if (clean) params.set(key, clean);
}

function renderIncidents(payload) {
  state.incidents = payload.items || [];
  state.incidentLimit = 100;
  const stats = payload.stats || {};
  elements.statTotal.textContent = stats.total ?? payload.count ?? 0;
  elements.statAccidents.textContent = stats.accidents ?? 0;
  elements.statRoadworks.textContent = stats.roadworks ?? 0;
  elements.statStuck.textContent = stats.stuck ?? 0;
  elements.statObstructions.textContent = stats.obstructions ?? 0;
  elements.statWeather.textContent = stats.weather ?? 0;
  elements.incidentTabCount.textContent = payload.count ?? state.incidents.length;
  elements.resultCount.textContent = uiText("results", payload.count ?? state.incidents.length);
  renderIncidentRows();
  showState(state.incidents.length ? "incidents" : "empty");
}

async function updateRelatedTabCounts(payload, requestId) {
  const incidents = payload.items || [];
  if (!incidents.length) {
    elements.cameraTabCount.textContent = 0;
    elements.mapTabCount.textContent = 0;
    return;
  }
  const cameraPayload = await fetchMapCameras(incidents);
  if (requestId !== state.requestId || state.view !== "incidents") return;
  const cameraCount = cameraPayload.count ?? (cameraPayload.items || []).length;
  elements.cameraTabCount.textContent = cameraCount;
  elements.mapTabCount.textContent = (payload.count ?? incidents.length) + cameraCount;
}

function renderIncidentRows() {
  const visible = state.incidents.slice(0, state.incidentLimit);
  elements.incidentRows.replaceChildren(...visible.flatMap(createIncidentRows));
  elements.loadMoreWrap.hidden = visible.length >= state.incidents.length;
  elements.loadMoreButton.textContent = uiText("loadMore", Math.min(100, state.incidents.length - visible.length));
}

function showMoreIncidents() {
  state.incidentLimit += 100;
  renderIncidentRows();
}

function createIncidentRows(incident) {
  const row = document.createElement("tr");
  const detailRow = createIncidentDetailRow(incident);
  const detailId = `incident-detail-${safeClass(incident.id || incident.record_id || `${incident.road}-${incident.km}`)}`;
  const severity = incident.severity || "unknown";
  row.className = "incident-row";
  row.tabIndex = 0;
  row.setAttribute("role", "button");
  row.setAttribute("aria-expanded", "false");
  row.setAttribute("aria-controls", detailId);
  detailRow.id = detailId;
  row.append(
    cell(badge(incident.severity_label || formatSeverity(severity), `severity-${safeClass(severity)}`)),
    cell(text("strong", incident.road || "--", "road")),
    cell(locationContent(incident)),
    cell(text("span", incident.type_label || incident.type || uiText("unclassified"), "badge")),
    cell(directionContent(incident)),
    cell(coverageContent(incident))
  );
  const toggleDetails = () => {
    const expanded = row.getAttribute("aria-expanded") === "true";
    row.setAttribute("aria-expanded", String(!expanded));
    row.classList.toggle("is-expanded", !expanded);
    detailRow.hidden = expanded;
  };
  row.addEventListener("click", toggleDetails);
  row.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      toggleDetails();
    }
  });
  return [row, detailRow];
}

function createIncidentDetailRow(incident) {
  const row = document.createElement("tr");
  row.className = "incident-detail-row";
  row.hidden = true;
  const detailCell = document.createElement("td");
  detailCell.colSpan = 6;
  const panel = document.createElement("div");
  panel.className = "incident-detail-panel";
  const heading = document.createElement("div");
  heading.className = "incident-detail-heading";
  heading.append(text("strong", incident.type_label || uiText("incidentDetail")), text("small", [incident.road, incident.municipality, incident.province].filter(Boolean).join(" · ") || uiText("dgtData")));
  const grid = document.createElement("dl");
  grid.className = "incident-detail-grid";
  const details = detailEntries(incident, incidentDetailFields);
  details.forEach(([label, value]) => {
    const item = document.createElement("div");
    item.append(text("dt", label), text("dd", value));
    grid.append(item);
  });
  panel.append(heading, grid);
  detailCell.append(panel);
  row.append(detailCell);
  return row;
}

function formatDetailValue(key, value) {
  if (value === null || value === undefined || value === "") return "--";
  if (typeof value === "boolean") return value ? uiText("yes") : uiText("no");
  if (timeDetailFields.has(key)) return formatHumanDateTime(value);
  if (key === "direction_label") return formatDirectionValue(value);
  if (key === "nearest_camera_km_delta" && Number.isFinite(Number(value))) return `${Number(value).toFixed(3)} PK`;
  if (["distance_km", "km_delta"].includes(key) && Number.isFinite(Number(value))) return `${Number(value).toFixed(3)} km`;
  return String(value);
}

function detailEntries(item, preferredKeys = []) {
  const keys = [...preferredKeys, ...Object.keys(item || {}).filter((key) => !preferredKeys.includes(key))];
  return keys.map((key) => [detailLabel(key), formatDetailValue(key, item?.[key])]);
}

function directionContent(incident) {
  const full = incident.direction_label || incident.direction || "--";
  const short = formatDirectionValue(full);
  const node = text("abbr", short, "direction-abbr");
  node.title = full;
  return node;
}

function formatDirectionValue(value) {
  const textValue = String(value || "").trim();
  const normalized = textValue.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const compact = normalized.replace(/[^a-z]/g, "");
  if (["unknown", "desconocido", "sindato", "na"].includes(compact)) return "--";
  const matches = [
    ["northeastbound", "NE"], ["northeast", "NE"], ["noreste", "NE"],
    ["northwestbound", "NO"], ["northwest", "NO"], ["noroeste", "NO"],
    ["southeastbound", "SE"], ["southeast", "SE"], ["sureste", "SE"],
    ["southwestbound", "SO"], ["southwest", "SO"], ["suroeste", "SO"],
    ["northbound", "N"], ["direccionnorte", "N"], ["north", "N"], ["norte", "N"],
    ["southbound", "S"], ["direccionsur", "S"], ["south", "S"], ["sur", "S"],
    ["eastbound", "E"], ["direccioneste", "E"], ["east", "E"], ["este", "E"],
    ["westbound", "O"], ["direccionoeste", "O"], ["west", "O"], ["oeste", "O"],
    ["bothdirections", "N/S"], ["ambossentidos", "N/S"],
    ["positivedirection", "+"], ["sentidopositivo", "+"],
    ["negativedirection", "-"], ["sentidonegativo", "-"],
  ];
  const match = matches.find(([needle]) => compact.includes(needle));
  return match ? match[1] : textValue;
}

function formatHumanDateTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  const locale = state.language === "en" ? "en-GB" : "es-ES";
  return new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }).format(date);
}

function detailLabel(key) {
  return (detailLabels[state.language] || detailLabels.es)[key] || key.replace(/_/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function uiText(key) {
  const value = (uiCopy[state.language] || uiCopy.es)[key] || uiCopy.es[key] || key;
  return typeof value === "function" ? value(...Array.from(arguments).slice(1)) : value;
}

function renderCameras(payload) {
  state.cameras = payload.items || [];
  updateFavoriteTabCount();
  elements.cameraTabCount.textContent = payload.count ?? state.cameras.length;
  elements.resultCount.textContent = uiText("results", payload.count ?? state.cameras.length);
  elements.cameraResults.replaceChildren(...state.cameras.map(createCameraCard));
  if (window.lucide) window.lucide.createIcons();
  showState(state.cameras.length ? "cameras" : "empty");
}

function renderFavoriteCameras() {
  state.favoriteCameras = loadFavoriteCameras();
  updateFavoriteTabCount();
  switchViewLabelOnly();
  setEmptyStateText(uiText("unavailableFavorites"));
  elements.resultCount.textContent = uiText("results", state.favoriteCameras.length);
  elements.cameraResults.replaceChildren(...state.favoriteCameras.map(createCameraCard));
  if (window.lucide) window.lucide.createIcons();
  showState(state.favoriteCameras.length ? "cameras" : "empty");
}

async function renderMap(incidentPayload, requestId) {
  const incidents = incidentPayload.items || [];
  const cameraPayload = await fetchMapCameras(incidents);
  if (requestId !== state.requestId) return;
  state.incidents = incidents;
  state.cameras = cameraPayload.items || [];
  elements.incidentTabCount.textContent = incidentPayload.count ?? state.incidents.length;
  elements.cameraTabCount.textContent = cameraPayload.count ?? state.cameras.length;
  elements.mapTabCount.textContent = state.incidents.length + state.cameras.length;
  elements.resultCount.textContent = uiText("mapSummary", state.incidents.length, state.cameras.length);
  renderStats(incidentPayload.stats || {}, incidentPayload.count ?? state.incidents.length);
  renderMapMarkers();
  showState(state.incidents.length || state.cameras.length ? "map" : "empty");
}

async function fetchMapCameras(incidents) {
  const scopes = mapCameraScopes(incidents);
  if (!scopes.length) return { count: 0, items: [] };
  const payloads = await Promise.all(scopes.map(fetchMapCameraScope));
  const cameras = new Map();
  payloads.flatMap((payload) => payload.items || []).forEach((camera) => {
    const key = camera.id || [camera.province, camera.road, camera.km, camera.image_url].join("|");
    if (!cameras.has(key)) cameras.set(key, camera);
  });
  return { updated_at: payloads[0]?.updated_at, count: cameras.size, items: Array.from(cameras.values()) };
}

function mapCameraScopes(incidents) {
  const road = elements.roadFilter.value.trim().toUpperCase();
  const municipality = elements.municipalityFilter.value.trim();
  const province = elements.provinceFilter.value.trim();
  const incidentCoverage = elements.cameraCoverageFilter.value === "with";
  const matchMode = elements.matchModeFilter.value;
  if (incidentCoverage) {
    if (!incidents.length) return [];
    if (road || province) return [{ road, province, incidentCoverage, matchMode }];
    if (municipality) return mapMunicipalityCameraScopes(incidents).map((scope) => ({ ...scope, incidentCoverage, matchMode }));
    return [{ incidentCoverage, matchMode }];
  }
  if (road) return [{ road, matchMode }];
  if (municipality) return mapMunicipalityCameraScopes(incidents);
  if (province) return [{ province, matchMode }];
  return [{ matchMode }];
}

function mapMunicipalityCameraScopes(incidents) {
  const scopes = new Map();
  incidents.forEach((incident) => {
    const latitude = Number(incident.latitude);
    const longitude = Number(incident.longitude);
    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return;
    const key = `${latitude.toFixed(4)}|${longitude.toFixed(4)}`;
    scopes.set(key, { latitude, longitude, maxDistanceKm: 25 });
  });
  return Array.from(scopes.values());
}

async function fetchMapCameraScope(scope) {
  const params = new URLSearchParams();
  addParam(params, "province", scope.province);
  addParam(params, "road", scope.road);
  addParam(params, "match_mode", scope.matchMode === "contains" ? "" : scope.matchMode);
  if (scope.incidentCoverage) params.set("incident_coverage", "true");
  if (Number.isFinite(scope.latitude) && Number.isFinite(scope.longitude)) {
    params.set("lat", String(scope.latitude));
    params.set("lon", String(scope.longitude));
    params.set("max_distance_km", String(scope.maxDistanceKm));
  }
  params.set("all", "true");
  const response = await fetch(`/api/cameras?${params.toString()}`, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(response.status === 502 ? uiText("serverUnavailable") : uiText("serverStatus", response.status));
  return response.json();
}

function renderStats(stats, fallbackTotal = 0) {
  elements.statTotal.textContent = stats.total ?? fallbackTotal;
  elements.statAccidents.textContent = stats.accidents ?? 0;
  elements.statRoadworks.textContent = stats.roadworks ?? 0;
  elements.statStuck.textContent = stats.stuck ?? 0;
  elements.statObstructions.textContent = stats.obstructions ?? 0;
  elements.statWeather.textContent = stats.weather ?? 0;
}

function hasCoordinates(item) {
  return item?.latitude !== null && item?.latitude !== undefined && item?.longitude !== null && item?.longitude !== undefined;
}

function initMap() {
  if (state.map || !elements.trafficMap || !window.L) return;
  state.map = L.map(elements.trafficMap).setView([40.4168, -3.7038], 6);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(state.map);
  state.incidentLayer = L.layerGroup().addTo(state.map);
  state.cameraLayer = L.layerGroup().addTo(state.map);
}

function mapIcon(kind, label) {
  return L.divIcon({ className: `map-marker ${kind}`, html: `<span>${escapeHtml(label)}</span>`, iconSize: [30, 30], iconAnchor: [15, 15], popupAnchor: [0, -16] });
}

function renderMapMarkers() {
  if (!window.L) {
    elements.mapStatus.textContent = uiText("mapUnavailable");
    return;
  }
  initMap();
  if (!state.map) return;
  state.incidentLayer.clearLayers();
  state.cameraLayer.clearLayers();
  const bounds = [];
  state.incidents.filter(hasCoordinates).forEach((incident) => {
    const point = [Number(incident.latitude), Number(incident.longitude)];
    bounds.push(point);
    L.marker(point, { icon: mapIcon("incident", formatDirectionValue(incident.direction_label || "!")) })
      .addTo(state.incidentLayer)
      .bindPopup(`<strong>${escapeHtml(incident.road || uiText("incidentPoint"))}</strong><br>${escapeHtml([incident.municipality, incident.province].filter(Boolean).join(" · ") || uiText("unavailableLocation"))}`)
      .on("click", () => renderMapDetail("incident", incident));
  });
  state.cameras.filter(hasCoordinates).forEach((camera) => {
    const point = [Number(camera.latitude), Number(camera.longitude)];
    bounds.push(point);
    L.marker(point, { icon: mapIcon("camera", "CM") })
      .addTo(state.cameraLayer)
      .bindPopup(`<strong>${escapeHtml(camera.road || uiText("cameraPoint"))}</strong><br>PK ${escapeHtml(camera.km || "--")}`)
      .on("click", () => renderMapDetail("camera", camera));
  });
  elements.mapStatus.textContent = uiText("mapSummary", state.incidents.filter(hasCoordinates).length, state.cameras.filter(hasCoordinates).length);
  if (bounds.length) state.map.fitBounds(bounds, { padding: [28, 28], maxZoom: 13 });
  queueMicrotask(() => state.map.invalidateSize());
}

function renderMapDetail(kind, item) {
  const details = detailEntries(item, kind === "incident" ? incidentDetailFields : []);
  const detailList = `<dl>${details.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`).join("")}</dl>`;
  if (kind === "camera") {
    const image = item.image_url ? `<button class="map-camera-preview" type="button"><img src="${escapeHtml(item.image_url)}" alt="${escapeHtml(uiText("cameraAlt", item.road, item.km))}"></button>` : `<div class="image-fallback"><i data-lucide="wifi-off" aria-hidden="true"></i><strong>${uiText("cameraUnavailable")}</strong></div>`;
    elements.mapDetail.innerHTML = `<section class="map-window map-image-window"><p class="eyebrow">${uiText("cameraImage")}</p><h3>${escapeHtml(item.road || uiText("dgtCamera"))}</h3>${image}</section><section class="map-window map-detail-window"><p class="eyebrow">${uiText("cameraPoint")}</p><h3>${escapeHtml(item.road || uiText("dgtCamera"))}</h3>${detailList}</section>`;
    const imageWindow = elements.mapDetail.querySelector(".map-image-window");
    imageWindow?.append(createFavoriteButton(item, "map-camera-favorite"));
    elements.mapDetail.querySelector(".map-camera-preview")?.addEventListener("click", () => openCameraViewer(item.image_url, uiText("cameraAlt", item.road, item.km), item));
  } else {
    elements.mapDetail.innerHTML = `<section class="map-window map-detail-window"><p class="eyebrow">${uiText("incidentPoint")}</p><h3>${escapeHtml(item.road || uiText("incidentDetail"))}</h3>${detailList}</section>`;
  }
  if (window.lucide) window.lucide.createIcons();
}

function createCameraCard(camera) {
  const card = document.createElement("article");
  card.className = "camera-card";
  card.dataset.favoriteId = cameraFavoriteId(camera);
  const favoriteButton = createFavoriteButton(camera);
  const media = document.createElement("div");
  media.className = "camera-media";
  if (camera.image_url) {
    const image = document.createElement("img");
    image.src = camera.image_url;
    image.alt = uiText("cameraAlt", camera.road, camera.km);
    image.loading = "lazy";
    image.addEventListener("error", () => showCameraMediaFallback(media));
    image.addEventListener("load", () => {
      if (isUnavailableCameraImage(image)) showCameraMediaFallback(media);
    });
    media.classList.add("is-clickable");
    media.tabIndex = 0;
    media.setAttribute("role", "button");
    media.setAttribute("aria-label", uiText("cameraImageFullscreen"));
    media.addEventListener("click", () => openCameraViewer(image.src, image.alt));
    media.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openCameraViewer(image.src, image.alt);
      }
    });
    media.append(image, favoriteButton);
  } else media.append(imageFallback(), favoriteButton);
  const body = document.createElement("div");
  body.className = "camera-body";
  const label = document.createElement("div");
  label.append(text("strong", camera.road || uiText("unidentifiedRoad")), text("small", camera.province || uiText("unavailableProvince")));
  body.append(label, text("span", camera.km ? `PK ${camera.km}` : "PK --", "camera-km"));
  card.append(media, body);
  return card;
}

function createFavoriteButton(camera, className = "") {
  const button = document.createElement("button");
  button.className = ["camera-favorite", className].filter(Boolean).join(" ");
  button.type = "button";
  button.dataset.favoriteId = cameraFavoriteId(camera);
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleCameraFavorite(camera);
  });
  button.addEventListener("keydown", (event) => event.stopPropagation());
  updateFavoriteButton(button, camera);
  return button;
}

function updateFavoriteButton(button, camera) {
  const active = isFavoriteCamera(camera);
  button.classList.toggle("is-active", active);
  button.setAttribute("aria-pressed", String(active));
  button.setAttribute("aria-label", active ? uiText("unfavoriteCamera") : uiText("favoriteCamera"));
  button.title = active ? uiText("unfavoriteCamera") : uiText("favoriteCamera");
  button.innerHTML = `<i data-lucide="star" aria-hidden="true"></i>`;
}

function toggleCameraFavorite(camera) {
  const key = cameraFavoriteId(camera);
  const favorites = loadFavoriteCameras();
  const index = favorites.findIndex((item) => cameraFavoriteId(item) === key);
  const active = index < 0;
  if (active) favorites.unshift(normalizeFavoriteCamera(camera));
  else favorites.splice(index, 1);
  saveFavoriteCameras(favorites);
  state.favoriteCameras = favorites;
  updateFavoriteTabCount();
  if (state.view === "favorites") {
    renderFavoriteCameras();
    return;
  }
  refreshFavoriteButtons(key, active);
  if (window.lucide) window.lucide.createIcons();
}

function refreshFavoriteButtons(key, active) {
  document.querySelectorAll(".camera-favorite").forEach((button) => {
    if (button.dataset.favoriteId !== key) return;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-pressed", String(active));
    button.setAttribute("aria-label", active ? uiText("unfavoriteCamera") : uiText("favoriteCamera"));
    button.title = active ? uiText("unfavoriteCamera") : uiText("favoriteCamera");
  });
}

function loadFavoriteCameras() {
  try {
    const value = JSON.parse(localStorage.getItem(cameraFavoritesKey) || "[]");
    return Array.isArray(value) ? value.filter((camera) => camera && typeof camera === "object") : [];
  } catch (_error) {
    return [];
  }
}

function saveFavoriteCameras(cameras) {
  localStorage.setItem(cameraFavoritesKey, JSON.stringify(cameras.map(normalizeFavoriteCamera)));
}

function normalizeFavoriteCamera(camera) {
  return {
    id: camera.id || "",
    road: camera.road || "",
    province: camera.province || "",
    km: camera.km || "",
    image_url: camera.image_url || "",
    latitude: camera.latitude ?? null,
    longitude: camera.longitude ?? null,
  };
}

function cameraFavoriteId(camera) {
  return camera.id || [camera.province, camera.road, camera.km, camera.image_url].map((value) => String(value || "").trim()).join("|");
}

function isFavoriteCamera(camera) {
  const key = cameraFavoriteId(camera);
  return loadFavoriteCameras().some((item) => cameraFavoriteId(item) === key);
}

function updateFavoriteTabCount() {
  elements.favoriteTabCount.textContent = state.favoriteCameras.length;
}

function locationContent(incident) {
  const wrapper = document.createElement("div");
  wrapper.className = "location";
  wrapper.append(text("strong", incident.municipality || uiText("unavailableLocation")), text("small", [incident.province, incident.km && `PK ${incident.km}`].filter(Boolean).join(" · ")));
  return wrapper;
}

function coverageContent(incident) {
  const wrapper = document.createElement("span");
  wrapper.className = incident.has_camera_coverage ? "coverage-wrap" : "coverage-wrap no-coverage";
  if (!incident.has_camera_coverage) {
    wrapper.innerHTML = `<i data-lucide="camera-off" aria-hidden="true"></i>`;
    wrapper.setAttribute("aria-label", uiText("noCoverage"));
    wrapper.title = uiText("noCoverage");
    if (window.lucide) queueMicrotask(() => window.lucide.createIcons());
    return wrapper;
  }
  const button = document.createElement("button");
  button.className = "coverage-button";
  button.type = "button";
  button.innerHTML = `<i data-lucide="camera"></i>${incident.camera_coverage_count || 1}`;
  button.setAttribute("aria-label", uiText("nearbyCameras", incident.camera_coverage_count || 1));
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    openIncidentCameras(incident, wrapper, button);
  });
  wrapper.append(button);
  if (window.lucide) queueMicrotask(() => window.lucide.createIcons());
  return wrapper;
}

async function openIncidentCameras(incident, wrapper, button) {
  closeCameraMenus(wrapper);
  button.disabled = true;
  button.classList.add("is-loading");
  try {
    const cameras = await fetchIncidentCameras(incident);
    if (cameras.length === 1) {
      openCameraTarget(cameras[0]);
      return;
    }
    showCameraMenu(wrapper, cameras);
  } catch (error) {
    showCameraMenu(wrapper, [], error.message || uiText("cameraLoadError"));
  } finally {
    button.disabled = false;
    button.classList.remove("is-loading");
  }
}

async function fetchIncidentCameras(incident) {
  const params = new URLSearchParams();
  addParam(params, "province", incident.province || "");
  addParam(params, "road", incident.road || "");
  addParam(params, "km", incident.km || "");
  if (incident.latitude != null) params.set("lat", String(incident.latitude));
  if (incident.longitude != null) params.set("lon", String(incident.longitude));
  params.set("limit", String(Math.max(1, Math.min(12, incident.camera_coverage_count || 12))));
  params.set("max_km_delta", "1");
  const response = await fetch(`/api/cameras?${params.toString()}`, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(uiText("cameraLoadError"));
  const payload = await response.json();
  return payload.items || [];
}

function showCameraMenu(wrapper, cameras, message = "") {
  const menu = document.createElement("div");
  menu.className = "coverage-menu";
  menu.setAttribute("role", "menu");
  if (!cameras.length) {
    const empty = document.createElement("span");
    empty.className = "coverage-menu-empty";
    empty.textContent = message || uiText("unavailableCameras");
    menu.append(empty);
  } else {
    cameras.forEach((camera, index) => {
      const item = document.createElement("div");
      item.className = "coverage-menu-item";
      item.setAttribute("role", "menuitem");
      const preview = document.createElement("button");
      preview.className = "coverage-camera-preview";
      preview.type = "button";
      preview.setAttribute("aria-label", uiText("cameraImageFullscreen"));
      if (camera.image_url) {
        const image = document.createElement("img");
        image.src = camera.image_url;
        image.alt = uiText("cameraAlt", camera.road, camera.km);
        image.loading = "lazy";
        preview.append(image);
        preview.addEventListener("click", () => openCameraViewer(camera.image_url, uiText("cameraAlt", camera.road, camera.km), camera));
      } else {
        preview.innerHTML = `<i data-lucide="wifi-off" aria-hidden="true"></i>`;
        preview.disabled = true;
      }
      const target = document.createElement("button");
      target.className = "coverage-camera-target";
      target.type = "button";
      target.innerHTML = `<strong>${camera.road || uiText("dgtCamera")} · PK ${camera.km || "--"}</strong><small>${camera.province || uiText("unavailableProvince")}${camera.km_delta != null ? ` · Δ PK ${Number(camera.km_delta).toFixed(3)}` : ""}</small>`;
      target.addEventListener("click", () => {
        closeCameraMenus();
        openCameraTarget(camera);
      });
      item.append(preview, target, createFavoriteButton(camera, "coverage-camera-favorite"));
      menu.append(item);
      if (index === 0) queueMicrotask(() => target.focus());
    });
  }
  wrapper.append(menu);
}

function closeCameraMenus(except = null) {
  document.querySelectorAll(".coverage-menu").forEach((menu) => {
    if (!except || !except.contains(menu)) menu.remove();
  });
}

function openCameraTarget(camera) {
  if (camera.image_url) {
    openCameraViewer(camera.image_url, uiText("cameraAlt", camera.road, camera.km), camera);
    return;
  }
  state.view = "cameras";
  elements.provinceFilter.value = camera.province || "";
  elements.roadFilter.value = camera.road || "";
  elements.kmFilter.value = camera.km || "";
  switchView("cameras");
}

function imageFallback() {
  const fallback = document.createElement("div");
  fallback.className = "image-fallback";
  fallback.innerHTML = `<i data-lucide="wifi-off" aria-hidden="true"></i><strong>${uiText("cameraUnavailable")}</strong><small>${uiText("cameraUnavailableLong")}</small>`;
  if (window.lucide) queueMicrotask(() => window.lucide.createIcons());
  return fallback;
}

function showCameraMediaFallback(media) {
  const favoriteButton = media.querySelector(".camera-favorite");
  media.classList.remove("is-clickable");
  media.removeAttribute("role");
  media.removeAttribute("aria-label");
  media.removeAttribute("tabindex");
  media.replaceChildren(imageFallback());
  if (favoriteButton) media.append(favoriteButton);
}

function openCameraViewer(src, alt, camera = null) {
  const viewer = document.createElement("div");
  viewer.className = "image-viewer";
  viewer.setAttribute("role", "dialog");
  viewer.setAttribute("aria-modal", "true");
  viewer.setAttribute("aria-label", alt || uiText("cameraImage"));
  const frame = document.createElement("div");
  frame.className = "image-viewer-frame";
  const closeButton = document.createElement("button");
  closeButton.className = "image-viewer-close";
  closeButton.type = "button";
  closeButton.setAttribute("aria-label", uiText("closeImage"));
  closeButton.innerHTML = `<i data-lucide="x" aria-hidden="true"></i>`;
  const favoriteButton = camera ? createFavoriteButton(camera, "image-viewer-favorite") : null;
  const image = document.createElement("img");
  image.src = src;
  image.alt = alt || uiText("cameraImage");
  image.tabIndex = 0;
  image.setAttribute("role", "button");
  image.setAttribute("aria-label", uiText("imageOpenFullscreen"));
  const showViewerFallback = () => {
    if (!frame.contains(image)) return;
    image.remove();
    frame.classList.add("has-error");
    frame.append(disconnectedFallback());
  };
  image.addEventListener("error", showViewerFallback);
  image.addEventListener("load", () => {
    if (isUnavailableCameraImage(image)) showViewerFallback();
  });
  frame.append(closeButton, image);
  if (favoriteButton) frame.append(favoriteButton);
  viewer.append(frame);
  const enterFullscreen = () => {
    if (!frame.contains(image)) return;
    viewer.classList.add("is-fullscreen");
    viewer.requestFullscreen?.().catch(() => {});
  };
  const closeViewer = () => {
    document.removeEventListener("keydown", handleKeydown);
    document.removeEventListener("fullscreenchange", handleFullscreenChange);
    if (document.fullscreenElement === viewer) document.exitFullscreen().catch(() => {});
    viewer.remove();
  };
  const handleKeydown = (event) => {
    if (event.key === "Escape") closeViewer();
  };
  const handleFullscreenChange = () => {
    if (document.fullscreenElement !== viewer) viewer.classList.remove("is-fullscreen");
  };
  viewer.addEventListener("click", (event) => {
    if (event.target === viewer) closeViewer();
  });
  closeButton.addEventListener("click", closeViewer);
  image.addEventListener("click", (event) => {
    event.stopPropagation();
    enterFullscreen();
  });
  image.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      enterFullscreen();
    }
  });
  document.addEventListener("keydown", handleKeydown);
  document.addEventListener("fullscreenchange", handleFullscreenChange);
  document.body.append(viewer);
  if (window.lucide) window.lucide.createIcons();
  closeButton.focus();
}

function disconnectedFallback() {
  const fallback = document.createElement("div");
  fallback.className = "image-viewer-fallback";
  fallback.setAttribute("role", "status");
  fallback.innerHTML = `<i data-lucide="wifi-off" aria-hidden="true"></i><strong>${uiText("cameraUnavailable")}</strong><small>${uiText("cameraUnavailableLong")}</small>`;
  if (window.lucide) queueMicrotask(() => window.lucide.createIcons());
  return fallback;
}

function isUnavailableCameraImage(image) {
  if (!image.naturalWidth || !image.naturalHeight) return true;
  const canvas = document.createElement("canvas");
  canvas.width = 32;
  canvas.height = 18;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  if (!context) return false;
  try {
    context.drawImage(image, 0, 0, canvas.width, canvas.height);
    const pixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
    let grayish = 0;
    let lightGray = 0;
    for (let index = 0; index < pixels.length; index += 4) {
      const red = pixels[index];
      const green = pixels[index + 1];
      const blue = pixels[index + 2];
      const spread = Math.max(red, green, blue) - Math.min(red, green, blue);
      const average = (red + green + blue) / 3;
      if (spread < 16) grayish += 1;
      if (spread < 12 && average > 120 && average < 220) lightGray += 1;
    }
    const total = pixels.length / 4;
    return grayish / total > 0.92 && lightGray / total > 0.58;
  } catch (_error) {
    return false;
  }
}

function badge(value, className) { return text("span", value, `badge ${className}`); }
function text(tag, value, className = "") { const node = document.createElement(tag); node.textContent = value; node.className = className; return node; }
function cell(content) { const td = document.createElement("td"); td.append(content); return td; }
function escapeHtml(value) {
  return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
}
function safeClass(value) { return String(value).toLowerCase().replace(/[^a-z0-9_-]/g, ""); }
function formatSeverity(value) { return ({ highest: uiText("severityHighest"), high: uiText("severityHigh"), medium: uiText("severityMedium"), low: uiText("severityLow") })[String(value).toLowerCase()] || value || uiText("unknownSeverity"); }

function showState(active) {
  elements.loadingState.hidden = active !== "loading";
  elements.errorState.hidden = active !== "error";
  elements.emptyState.hidden = active !== "empty";
  elements.incidentResults.hidden = active !== "incidents";
  elements.cameraResults.hidden = active !== "cameras";
  elements.mapResults.hidden = active !== "map";
  document.querySelector(".results").setAttribute("aria-busy", String(active === "loading"));
}

function setEmptyStateText(message) {
  document.querySelector("#emptyState strong").textContent = uiText("emptyTitle");
  document.querySelector("#emptyState p").textContent = message;
}

function setConnection(online) {
  elements.connectionStatus.classList.toggle("is-online", online);
  elements.connectionStatus.classList.toggle("is-offline", !online);
  elements.connectionStatus.lastChild.textContent = online ? uiText("online") : uiText("offline");
}

function updateTimestamp(value) {
  const date = value ? new Date(value) : new Date();
  elements.lastUpdate.dateTime = date.toISOString();
  const locale = state.language === "en" ? "en-GB" : "es-ES";
  elements.lastUpdate.textContent = uiText("updatedAt", date.toLocaleTimeString(locale, { hour: "2-digit", minute: "2-digit" }));
}

function clearFilters() {
  elements.filterForm.reset();
  elements.limitFilter.value = "12";
  applyKindFilter("", false);
  loadCurrentView();
}

function applyKindFilter(kind, reload = true) {
  state.kind = kind;
  document.querySelectorAll(".metric").forEach((metric) => metric.classList.toggle("is-active", (metric.dataset.kind || "") === kind));
  if (reload) loadCurrentView();
}

function scheduleRefresh() {
  clearInterval(state.timer);
  if (elements.autoRefresh.checked) state.timer = setInterval(loadCurrentView, 120000);
}

/* Legacy dashboard implementation retained for reference.
const LIVE_REFRESH_SECONDS = 120;

const state = {
  incidents: [],
  visibleIncidents: [],
  selectedId: null,
  kind: "",
  sortKey: "",
  sortDirection: "asc",
  cameras: [],
  cameraIndex: 0,
  cameraIncidentId: null,
  map: null,
  incidentLayer: null,
  cameraLayer: null,
  socket: null,
  reconnectTimer: null,
  reconnectAttempts: 0,
};

const elements = {
  province: document.querySelector("#province"),
  municipality: document.querySelector("#municipality"),
  road: document.querySelector("#road"),
  severity: document.querySelector("#severity"),
  cameraFilter: document.querySelector("#camera-filter"),
  refresh: document.querySelector("#refresh"),
  clear: document.querySelector("#clear"),
  body: document.querySelector("#incidents-body"),
  detail: document.querySelector("#detail"),
  updatedAt: document.querySelector("#updated-at"),
  statusDot: document.querySelector("#status-dot"),
  statusText: document.querySelector("#status-text"),
  cameraContext: document.querySelector("#camera-context"),
  cameraImage: document.querySelector("#camera-image"),
  cameraEmpty: document.querySelector("#camera-empty"),
  cameraMeta: document.querySelector("#camera-meta"),
  cameraCounter: document.querySelector("#camera-counter"),
  cameraPrev: document.querySelector("#camera-prev"),
  cameraNext: document.querySelector("#camera-next"),
  cameraExpand: document.querySelector("#camera-expand"),
  cameraLightbox: document.querySelector("#camera-lightbox"),
  cameraLightboxImage: document.querySelector("#camera-lightbox-image"),
  cameraLightboxClose: document.querySelector("#camera-lightbox-close"),
  map: document.querySelector("#traffic-map"),
  mapStatus: document.querySelector("#map-status"),
  stats: {
    total: document.querySelector("#stat-total"),
    accidents: document.querySelector("#stat-accidents"),
    roadworks: document.querySelector("#stat-roadworks"),
    stuck: document.querySelector("#stat-stuck"),
    obstructions: document.querySelector("#stat-obstructions"),
    weather: document.querySelector("#stat-weather"),
  },
};

function setStatus(text, mode) {
  elements.statusText.textContent = text;
  elements.statusDot.className = `dot ${mode}`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function iconForCause(cause) {
  const lower = (cause || "").toLowerCase();
  if (lower.includes("accident")) return "AC";
  if (lower.includes("roadworks") || lower.includes("maintenance")) return "OB";
  if (lower.includes("stuck") || lower.includes("breakdown")) return "AV";
  if (lower.includes("obstruction")) return "BL";
  if (["weather", "fog"].some((word) => lower.includes(word))) return "CL";
  if (["snow", "ice"].some((word) => lower.includes(word))) return "NV";
  if (lower.includes("flooding") || lower.includes("flood")) return "IN";
  return "AL";
}

function cameraCoverageTitle(incident) {
  if (!incident.has_camera_coverage) return "Sin cámara en rango por km";
  const count = incident.camera_coverage_count || 1;
  const distance = incident.nearest_camera_km_delta ?? 0;
  return `${count} cámara${count === 1 ? "" : "s"} en rango · más cercana a ${distance} km`;
}

function hasCoordinates(item) {
  return item?.latitude !== null && item?.latitude !== undefined && item?.longitude !== null && item?.longitude !== undefined;
}

function createMapIcon(kind, label) {
  return L.divIcon({
    className: `map-marker ${kind}`,
    html: `<span>${label}</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -16],
  });
}

function initMap() {
  if (state.map || !elements.map || !window.L) return;

  state.map = L.map(elements.map, {
    zoomControl: true,
    attributionControl: true,
  }).setView([40.4168, -3.7038], 6);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(state.map);

  state.incidentLayer = L.layerGroup().addTo(state.map);
  state.cameraLayer = L.layerGroup().addTo(state.map);
}

function selectCamera(cameraId) {
  const cameraIndex = state.cameras.findIndex((camera) => String(camera.id || camera.image_url) === String(cameraId));
  if (cameraIndex === -1) return;

  state.cameraIndex = cameraIndex;
  renderCamera();
}

function selectIncident(incidentId, options = {}) {
  const incident = state.incidents.find((item) => String(item.id) === String(incidentId));
  if (!incident) return;

  state.selectedId = incident.id;
  renderTable();
  renderDetail(incident);
  loadCamerasForIncident(incident, true);

  if (options.scrollToRow) {
    const row = elements.body.querySelector(`tr[data-id="${CSS.escape(String(incident.id))}"]`);
    row?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }
}

function updateMapMarkers() {
  if (!window.L) {
    elements.mapStatus.textContent = "Mapa no disponible";
    return;
  }

  initMap();
  if (!state.map) return;

  state.incidentLayer.clearLayers();
  state.cameraLayer.clearLayers();

  const bounds = [];
  const incidentsWithCoords = state.visibleIncidents.filter(hasCoordinates);
  const camerasWithCoords = state.cameras.filter(hasCoordinates);

  incidentsWithCoords.forEach((incident) => {
    const marker = L.marker([incident.latitude, incident.longitude], {
      icon: createMapIcon("incident", iconForCause(incident.cause)),
    }).bindPopup(`
      <strong>${escapeHtml(incident.road || "Incidente")}</strong><br>
      ${escapeHtml(incident.cause_label || incident.cause || "N/A")}<br>
      Km ${escapeHtml(incident.km || "N/A")} · ${escapeHtml(incident.province || "")}
    `);
    marker.on("click", () => selectIncident(incident.id, { scrollToRow: true }));
    marker.addTo(state.incidentLayer);
    bounds.push([incident.latitude, incident.longitude]);
  });

  camerasWithCoords.forEach((camera) => {
    const cameraId = String(camera.id || camera.image_url);
    const marker = L.marker([camera.latitude, camera.longitude], {
      icon: createMapIcon("camera", "CM"),
    }).bindPopup(`
      <strong>${escapeHtml(camera.road || "Cámara")}</strong><br>
      Km ${escapeHtml(camera.km || "N/A")} · ${escapeHtml(camera.province || "")}<br>
      <a href="${escapeHtml(camera.image_url)}" target="_blank" rel="noreferrer">Abrir imagen</a>
    `);
    marker.on("click", () => selectCamera(cameraId));
    marker.addTo(state.cameraLayer);
    bounds.push([camera.latitude, camera.longitude]);
  });

  elements.mapStatus.textContent = `${incidentsWithCoords.length} incidentes · ${camerasWithCoords.length} cámaras`;

  if (bounds.length) {
    state.map.fitBounds(bounds, { padding: [24, 24], maxZoom: 13 });
  }

  window.setTimeout(() => state.map.invalidateSize(), 0);
}

function buildQuery() {
  const params = new URLSearchParams();
  const values = {
    province: elements.province.value.trim(),
    municipality: elements.municipality.value.trim(),
    road: elements.road.value.trim(),
    severity: elements.severity.value,
    kind: state.kind,
  };

  Object.entries(values).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });

  return params.toString();
}

function parseNumber(value) {
  const number = Number.parseFloat(String(value ?? "").replace(",", "."));
  return Number.isFinite(number) ? number : Number.POSITIVE_INFINITY;
}

function valueForSort(incident, key) {
  const values = {
    type: iconForCause(incident.cause),
    id: incident.id || "",
    road: incident.road || "",
    municipality: incident.municipality || "",
    province: incident.province || "",
    cause: incident.cause_label || incident.cause || "",
    camera: incident.has_camera_coverage ? 1 : 0,
    severity: incident.severity || "",
    km: parseNumber(incident.km),
  };
  return values[key] ?? "";
}

function includesText(value, needle) {
  return !needle || String(value || "").toLowerCase().includes(needle.toLowerCase());
}

function matchesKind(incident, kind) {
  const cause = String(incident.cause || "").toLowerCase();
  if (!kind) return true;
  if (kind === "accident") return cause.includes("accident");
  if (kind === "roadworks") return cause.includes("roadworks") || cause.includes("maintenance");
  if (kind === "stuck") return cause.includes("stuck") || cause.includes("breakdown");
  if (kind === "obstruction") return cause.includes("obstruction");
  if (kind === "weather") return ["weather", "fog", "snow", "flooding", "ice", "rain"].some((word) => cause.includes(word));
  return true;
}

function buildClientStats(incidents) {
  const hasAny = (incident, words) => {
    const cause = String(incident.cause || "").toLowerCase();
    return words.some((word) => cause.includes(word));
  };

  return {
    total: incidents.length,
    accidents: incidents.filter((incident) => hasAny(incident, ["accident"])).length,
    roadworks: incidents.filter((incident) => hasAny(incident, ["roadworks", "maintenance"])).length,
    stuck: incidents.filter((incident) => hasAny(incident, ["stuck", "breakdown"])).length,
    obstructions: incidents.filter((incident) => hasAny(incident, ["obstruction"])).length,
    weather: incidents.filter((incident) => hasAny(incident, ["weather", "fog", "snow", "flooding", "ice", "rain"])).length,
  };
}

function applyLocalTableState() {
  const cameraFilter = elements.cameraFilter.value;
  const provinceFilter = elements.province.value.trim();
  const municipalityFilter = elements.municipality.value.trim();
  const roadFilter = elements.road.value.trim();
  const severityFilter = elements.severity.value;
  let visible = [...state.incidents];

  visible = visible.filter((incident) => (
    includesText(incident.province, provinceFilter)
    && includesText(incident.municipality, municipalityFilter)
    && includesText(incident.road, roadFilter)
    && (!severityFilter || String(incident.severity || "").toLowerCase() === severityFilter.toLowerCase())
    && matchesKind(incident, state.kind)
  ));

  if (cameraFilter === "with") {
    visible = visible.filter((incident) => incident.has_camera_coverage);
  } else if (cameraFilter === "without") {
    visible = visible.filter((incident) => !incident.has_camera_coverage);
  }

  if (state.sortKey) {
    const direction = state.sortDirection === "asc" ? 1 : -1;
    visible.sort((left, right) => {
      const leftValue = valueForSort(left, state.sortKey);
      const rightValue = valueForSort(right, state.sortKey);
      if (typeof leftValue === "number" && typeof rightValue === "number") {
        return (leftValue - rightValue) * direction;
      }
      return String(leftValue).localeCompare(String(rightValue), "es", { numeric: true, sensitivity: "base" }) * direction;
    });
  }

  state.visibleIncidents = visible;
}

async function loadIncidents() {
  setStatus("Actualizando", "loading");
  const query = buildQuery();
  const response = await fetch(`/api/incidents${query ? `?${query}` : ""}`);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Error desconocido" }));
    throw new Error(error.detail || "No se pudieron cargar los incidentes");
  }

  const payload = await response.json();
  state.incidents = payload.items;
  renderStats(payload.stats);
  renderTable();
  elements.updatedAt.textContent = `Actualizado: ${new Date(payload.updated_at).toLocaleString()}`;
  setStatus(`${payload.count} incidentes`, "ok");
}

function applyPayload(payload) {
  state.incidents = payload.items || [];
  renderStats(payload.stats || {});
  renderTable();
  elements.updatedAt.textContent = `Actualizado: ${new Date(payload.updated_at).toLocaleString()} · WebSocket cada ${payload.refresh_interval_seconds || LIVE_REFRESH_SECONDS}s`;
  setStatus(`${payload.count ?? state.incidents.length} incidentes · en directo`, "ok");

  if (state.selectedId) {
    const selected = state.incidents.find((item) => item.id === state.selectedId);
    if (selected) renderDetail(selected);
  }

  const cameraIncident = state.incidents.find((item) => item.id === state.selectedId) || state.incidents[0];
  if (cameraIncident) {
    loadCamerasForIncident(cameraIncident);
  } else {
    clearCameraViewer("No hay incidentes para buscar cámaras cercanas.");
  }
}

function websocketUrl() {
  const params = new URLSearchParams(buildQuery());
  params.set("interval", String(LIVE_REFRESH_SECONDS));
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://${window.location.host}/ws/incidents?${params.toString()}`;
}

function scheduleReconnect() {
  window.clearTimeout(state.reconnectTimer);
  const delay = Math.min(1000 * 2 ** state.reconnectAttempts, 15000);
  state.reconnectAttempts += 1;
  state.reconnectTimer = window.setTimeout(connectLiveUpdates, delay);
}

function connectLiveUpdates() {
  window.clearTimeout(state.reconnectTimer);
  if (state.socket) {
    state.socket.onclose = null;
    state.socket.close();
  }

  setStatus("Conectando en directo", "loading");
  const socket = new WebSocket(websocketUrl());
  state.socket = socket;

  socket.addEventListener("open", () => {
    state.reconnectAttempts = 0;
    setStatus("Sincronizado", "ok");
  });

  socket.addEventListener("message", (event) => {
    const payload = JSON.parse(event.data);
    if (payload.error) {
      setStatus("Error DGT", "error");
      elements.body.innerHTML = `<tr><td colspan="9">${escapeHtml(payload.error)}</td></tr>`;
      return;
    }
    applyPayload(payload);
  });

  socket.addEventListener("close", () => {
    if (state.socket === socket) {
      setStatus("Reconectando", "loading");
      scheduleReconnect();
    }
  });

  socket.addEventListener("error", () => {
    setStatus("Error de conexión", "error");
    socket.close();
  });
}

function renderStats(stats) {
  Object.entries(elements.stats).forEach(([key, element]) => {
    element.textContent = stats[key] ?? 0;
  });
}

function renderTable() {
  applyLocalTableState();
  updateSortHeaders();
  renderStats(buildClientStats(state.visibleIncidents));
  updateMapMarkers();

  if (!state.visibleIncidents.length) {
    elements.body.innerHTML = `<tr><td colspan="9">No hay resultados con estos filtros.</td></tr>`;
    elements.detail.className = "empty";
    elements.detail.textContent = "Selecciona un incidente para ver la información completa.";
    return;
  }

  elements.body.innerHTML = state.visibleIncidents.map((incident) => `
    <tr data-id="${escapeHtml(incident.id)}" class="${incident.id === state.selectedId ? "selected" : ""}">
      <td class="type-cell" data-label="Tipo">
        <span class="badge">${iconForCause(incident.cause)}</span>
      </td>
      <td data-label="ID" title="${escapeHtml(incident.id || "N/A")}">${escapeHtml(incident.id || "N/A")}</td>
      <td data-label="Carretera">${escapeHtml(incident.road || "N/A")}</td>
      <td data-label="Municipio">${escapeHtml(incident.municipality || "N/A")}</td>
      <td data-label="Provincia">${escapeHtml(incident.province || "N/A")}</td>
      <td data-label="Causa">${escapeHtml(incident.cause_label || incident.cause || "N/A")}</td>
      <td class="camera-cell" data-label="Cámara">${incident.has_camera_coverage ? `<span class="camera-check" title="${escapeHtml(cameraCoverageTitle(incident))}">✓</span>` : `<span class="camera-missing" title="Sin cámara en rango por km">—</span>`}</td>
      <td data-label="Severidad"><span class="badge ${escapeHtml(incident.severity || "")}">${escapeHtml(incident.severity_label || "N/A")}</span></td>
      <td data-label="Km">${escapeHtml(incident.km || "N/A")}</td>
    </tr>
  `).join("");
}

function updateSortHeaders() {
  document.querySelectorAll(".sort-header").forEach((button) => {
    const active = button.dataset.sort === state.sortKey;
    button.classList.toggle("active", active);
    button.dataset.direction = active ? state.sortDirection : "";
  });
}

function formatDistance(camera) {
  if (camera.distance_km === null || camera.distance_km === undefined) return "distancia no disponible";
  return camera.distance_km < 1
    ? `${Math.round(camera.distance_km * 1000)} m`
    : `${camera.distance_km.toFixed(1)} km`;
}

function clearCameraViewer(message) {
  state.cameras = [];
  state.cameraIndex = 0;
  state.cameraIncidentId = null;
  elements.cameraImage.removeAttribute("src");
  elements.cameraImage.hidden = true;
  elements.cameraEmpty.hidden = false;
  elements.cameraEmpty.textContent = message;
  elements.cameraContext.textContent = "Sin cámaras disponibles";
  elements.cameraMeta.textContent = "";
  elements.cameraCounter.textContent = "0 / 0";
  elements.cameraPrev.disabled = true;
  elements.cameraNext.disabled = true;
  elements.cameraExpand.disabled = true;
}

function renderCamera() {
  const camera = state.cameras[state.cameraIndex];
  if (!camera) {
    clearCameraViewer("No se encontraron cámaras cercanas para este incidente.");
    return;
  }

  elements.cameraImage.hidden = false;
  elements.cameraEmpty.hidden = true;
  elements.cameraImage.src = camera.image_url;
  elements.cameraContext.textContent = `${camera.road || "Carretera N/A"} · ${camera.province || "Provincia N/A"}`;
  elements.cameraMeta.textContent = `Km ${camera.km || "N/A"} · ${formatDistance(camera)}`;
  elements.cameraCounter.textContent = `${state.cameraIndex + 1} / ${state.cameras.length}`;
  elements.cameraPrev.disabled = state.cameras.length <= 1;
  elements.cameraNext.disabled = state.cameras.length <= 1;
  elements.cameraExpand.disabled = false;
}

async function loadCamerasForIncident(incident, force = false) {
  if (!incident || (!force && state.cameraIncidentId === incident.id)) return;
  state.cameraIncidentId = incident.id;
  elements.cameraContext.textContent = `Buscando cámaras: ${incident.road || "N/A"} · ${incident.province || "N/A"}`;
  elements.cameraMeta.textContent = "Cargando imágenes de DGT...";
  elements.cameraImage.hidden = true;
  elements.cameraEmpty.hidden = false;
  elements.cameraEmpty.textContent = "Cargando cámaras cercanas...";

  const params = new URLSearchParams();
  if (incident.province) params.set("province", incident.province);
  if (incident.road) params.set("road", incident.road);
  if (incident.km) params.set("km", incident.km);
  params.set("max_km_delta", "1");
  if (incident.latitude !== null && incident.latitude !== undefined && incident.longitude !== null && incident.longitude !== undefined) {
    params.set("lat", incident.latitude);
    params.set("lon", incident.longitude);
  }
  params.set("limit", "12");

  try {
    const response = await fetch(`/api/cameras?${params.toString()}`);
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Error desconocido" }));
      throw new Error(error.detail || "No se pudieron cargar las cámaras");
    }
    const payload = await response.json();
    state.cameras = payload.items || [];
    state.cameraIndex = 0;
    renderCamera();
    updateMapMarkers();
  } catch (error) {
    clearCameraViewer(error.message);
    updateMapMarkers();
  }
}

function renderDetail(incident) {
  const mapsLink = incident.latitude && incident.longitude
    ? `<a href="https://maps.google.com/?q=${incident.latitude},${incident.longitude}" target="_blank" rel="noreferrer">Ver en Google Maps</a>`
    : "Sin coordenadas";

  elements.detail.className = "detail-grid";
  elements.detail.innerHTML = `
    <div class="detail-row"><span>ID</span>${escapeHtml(incident.id || "N/A")}</div>
    <div class="detail-row"><span>Ubicación</span>${escapeHtml(incident.road || "N/A")} · Km ${escapeHtml(incident.km || "N/A")} · ${escapeHtml(incident.municipality || "N/A")} · ${escapeHtml(incident.province || "N/A")}</div>
    <div class="detail-row"><span>Causa</span>${escapeHtml(incident.cause_label || incident.cause || "N/A")}</div>
    <div class="detail-row"><span>Severidad</span>${escapeHtml(incident.severity_label || "N/A")}</div>
    <div class="detail-row"><span>Dirección</span>${escapeHtml(formatDirectionValue(incident.direction_label || incident.direction || "N/A"))}</div>
    <div class="detail-row"><span>Inicio</span>${escapeHtml(formatDetailValue("start_time", incident.start_time) || "N/A")}</div>
    <div class="detail-row"><span>Fin previsto</span>${escapeHtml(formatDetailValue("end_time", incident.end_time) || "N/A")}</div>
    <div class="detail-row"><span>Mapa</span>${mapsLink}</div>
    <div class="detail-row"><span>Fuente</span>${escapeHtml(incident.source || "DGT")}</div>
  `;
}

function debounce(callback, wait = 350) {
  let timer;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => callback(...args), wait);
  };
}

async function refreshSafely() {
  try {
    connectLiveUpdates();
  } catch (error) {
    setStatus("Error", "error");
    elements.body.innerHTML = `<tr><td colspan="7">${escapeHtml(error.message)}</td></tr>`;
  }
}

document.querySelectorAll(".stat").forEach((button) => {
  button.addEventListener("click", () => {
    state.kind = button.dataset.kind || "";
    document.querySelectorAll(".stat").forEach((item) => item.classList.toggle("active", item === button));
    renderTable();
    refreshSafely();
  });
});

elements.body.addEventListener("click", (event) => {
  const row = event.target.closest("tr[data-id]");
  if (!row) return;
  selectIncident(row.dataset.id);
});

document.querySelectorAll(".sort-header").forEach((button) => {
  button.addEventListener("click", () => {
    if (state.sortKey === button.dataset.sort) {
      state.sortDirection = state.sortDirection === "asc" ? "desc" : "asc";
    } else {
      state.sortKey = button.dataset.sort;
      state.sortDirection = "asc";
    }
    renderTable();
  });
});

elements.cameraPrev.addEventListener("click", () => {
  if (!state.cameras.length) return;
  state.cameraIndex = (state.cameraIndex - 1 + state.cameras.length) % state.cameras.length;
  renderCamera();
});

elements.cameraNext.addEventListener("click", () => {
  if (!state.cameras.length) return;
  state.cameraIndex = (state.cameraIndex + 1) % state.cameras.length;
  renderCamera();
});

elements.cameraExpand.addEventListener("click", () => {
  const camera = state.cameras[state.cameraIndex];
  if (!camera) return;
  elements.cameraLightboxImage.src = camera.image_url;
  elements.cameraLightbox.hidden = false;
});

elements.cameraLightboxClose.addEventListener("click", () => {
  elements.cameraLightbox.hidden = true;
  elements.cameraLightboxImage.removeAttribute("src");
});

elements.cameraLightbox.addEventListener("click", (event) => {
  if (event.target === elements.cameraLightbox) {
    elements.cameraLightbox.hidden = true;
    elements.cameraLightboxImage.removeAttribute("src");
  }
});

elements.cameraImage.addEventListener("error", () => {
  elements.cameraImage.hidden = true;
  elements.cameraEmpty.hidden = false;
  elements.cameraEmpty.textContent = "No se pudo cargar esta imagen. Usa los controles para probar otra cámara.";
});

elements.cameraImage.addEventListener("load", () => {
  if (elements.cameraImage.naturalWidth && elements.cameraImage.naturalHeight) {
    elements.cameraImage.parentElement?.style.setProperty(
      "--camera-aspect",
      `${elements.cameraImage.naturalWidth} / ${elements.cameraImage.naturalHeight}`
    );
  }
});

elements.refresh.addEventListener("click", refreshSafely);
elements.clear.addEventListener("click", () => {
  elements.province.value = "";
  elements.municipality.value = "";
  elements.road.value = "";
  elements.severity.value = "";
  elements.cameraFilter.value = "";
  state.sortKey = "";
  state.sortDirection = "asc";
  state.kind = "";
  document.querySelectorAll(".stat").forEach((item) => item.classList.toggle("active", item.dataset.kind === ""));
  refreshSafely();
});

const debouncedRefresh = debounce(refreshSafely);
[elements.province, elements.municipality, elements.road].forEach((input) => {
  input.addEventListener("input", () => {
    renderTable();
    debouncedRefresh();
  });
});
elements.severity.addEventListener("change", () => {
  renderTable();
  refreshSafely();
});
elements.cameraFilter.addEventListener("change", renderTable);

initMap();
connectLiveUpdates();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // El dashboard funciona igualmente si el navegador bloquea el service worker.
    });
  });
}
*/