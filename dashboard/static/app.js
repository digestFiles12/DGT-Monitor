const state = {
  view: "incidents",
  incidents: [],
  cameras: [],
  incidentLimit: 100,
  timer: null,
};

const elements = {};
const ids = [
  "connectionStatus", "lastUpdate", "refreshButton", "filterForm", "clearFilters",
  "provinceFilter", "roadFilter", "municipalityFilter", "severityFilter", "kmFilter",
  "limitFilter", "incidentFilters", "cameraFilters", "autoRefresh", "statTotal",
  "statAccidents", "statRoadworks", "statObstructions", "incidentTabCount",
  "cameraTabCount", "resultsTitle", "resultEyebrow", "resultCount", "loadingState",
  "errorState", "errorMessage", "emptyState", "incidentResults", "incidentRows",
  "cameraResults", "retryButton", "loadMoreWrap", "loadMoreButton"
];

document.addEventListener("DOMContentLoaded", () => {
  ids.forEach((id) => { elements[id] = document.getElementById(id); });
  document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));
  elements.filterForm.addEventListener("submit", (event) => { event.preventDefault(); loadCurrentView(); });
  elements.clearFilters.addEventListener("click", clearFilters);
  elements.refreshButton.addEventListener("click", loadCurrentView);
  elements.retryButton.addEventListener("click", loadCurrentView);
  elements.loadMoreButton.addEventListener("click", showMoreIncidents);
  elements.autoRefresh.addEventListener("change", scheduleRefresh);
  window.addEventListener("online", loadCurrentView);
  window.addEventListener("offline", () => setConnection(false));
  if (window.lucide) window.lucide.createIcons();
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
  loadCurrentView();
  scheduleRefresh();
});

function switchView(view) {
  state.view = view;
  document.querySelectorAll(".tab").forEach((tab) => {
    const active = tab.dataset.view === view;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
  });
  elements.incidentFilters.hidden = view !== "incidents";
  elements.cameraFilters.hidden = view !== "cameras";
  elements.resultsTitle.textContent = view === "incidents" ? "Incidencias activas" : "Cámaras de tráfico";
  elements.resultEyebrow.textContent = view === "incidents" ? "Red viaria" : "Observación visual";
  loadCurrentView();
}

async function loadCurrentView() {
  showState("loading");
  elements.refreshButton.classList.add("is-loading");
  try {
    const params = buildParams();
    const endpoint = state.view === "incidents" ? "/api/incidents" : "/api/cameras";
    const response = await fetch(`${endpoint}?${params.toString()}`, { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(response.status === 502 ? "La fuente de datos DGT no está disponible temporalmente." : `El servidor respondió con código ${response.status}.`);
    const payload = await response.json();
    if (state.view === "incidents") renderIncidents(payload);
    else renderCameras(payload);
    updateTimestamp(payload.updated_at);
    setConnection(true);
  } catch (error) {
    elements.errorMessage.textContent = error.message || "Revisa la conexión y vuelve a intentarlo.";
    showState("error");
    setConnection(false);
  } finally {
    elements.refreshButton.classList.remove("is-loading");
  }
}

function buildParams() {
  const params = new URLSearchParams();
  addParam(params, "province", elements.provinceFilter.value);
  addParam(params, "road", elements.roadFilter.value.toUpperCase());
  if (state.view === "incidents") {
    addParam(params, "municipality", elements.municipalityFilter.value);
    addParam(params, "severity", elements.severityFilter.value);
  } else {
    addParam(params, "km", elements.kmFilter.value);
    addParam(params, "limit", elements.limitFilter.value);
  }
  return params;
}

function addParam(params, key, value) {
  const clean = value.trim();
  if (clean) params.set(key, clean);
}

function renderIncidents(payload) {
  state.incidents = payload.items || [];
  state.incidentLimit = 100;
  const stats = payload.stats || {};
  elements.statTotal.textContent = stats.total ?? payload.count ?? 0;
  elements.statAccidents.textContent = stats.accidents ?? 0;
  elements.statRoadworks.textContent = stats.roadworks ?? 0;
  elements.statObstructions.textContent = stats.obstructions ?? 0;
  elements.incidentTabCount.textContent = payload.count ?? state.incidents.length;
  elements.resultCount.textContent = `${payload.count ?? state.incidents.length} resultados`;
  renderIncidentRows();
  showState(state.incidents.length ? "incidents" : "empty");
}

function renderIncidentRows() {
  const visible = state.incidents.slice(0, state.incidentLimit);
  elements.incidentRows.replaceChildren(...visible.map(createIncidentRow));
  elements.loadMoreWrap.hidden = visible.length >= state.incidents.length;
  elements.loadMoreButton.textContent = `Mostrar ${Math.min(100, state.incidents.length - visible.length)} más`;
}

function showMoreIncidents() {
  state.incidentLimit += 100;
  renderIncidentRows();
}

function createIncidentRow(incident) {
  const row = document.createElement("tr");
  const severity = incident.severity || "unknown";
  row.append(
    cell(badge(formatSeverity(severity), `severity-${safeClass(severity)}`)),
    cell(text("strong", incident.road || "--", "road")),
    cell(locationContent(incident)),
    cell(text("span", incident.type_label || incident.type || "Sin clasificar", "badge")),
    cell(document.createTextNode(incident.direction_label || incident.direction || "--")),
    cell(coverageContent(incident))
  );
  return row;
}

function renderCameras(payload) {
  state.cameras = payload.items || [];
  elements.cameraTabCount.textContent = payload.count ?? state.cameras.length;
  elements.resultCount.textContent = `${payload.count ?? state.cameras.length} resultados`;
  elements.cameraResults.replaceChildren(...state.cameras.map(createCameraCard));
  if (window.lucide) window.lucide.createIcons();
  showState(state.cameras.length ? "cameras" : "empty");
}

function createCameraCard(camera) {
  const card = document.createElement("article");
  card.className = "camera-card";
  const media = document.createElement("div");
  media.className = "camera-media";
  if (camera.image_url) {
    const image = document.createElement("img");
    image.src = camera.image_url;
    image.alt = `Cámara ${camera.road || "DGT"} PK ${camera.km || "sin dato"}`;
    image.loading = "lazy";
    image.addEventListener("error", () => media.replaceChildren(imageFallback()));
    media.append(image);
  } else media.append(imageFallback());
  const body = document.createElement("div");
  body.className = "camera-body";
  const label = document.createElement("div");
  label.append(text("strong", camera.road || "Carretera sin identificar"), text("small", camera.province || "Provincia no disponible"));
  body.append(label, text("span", camera.km ? `PK ${camera.km}` : "PK --", "camera-km"));
  card.append(media, body);
  return card;
}

function locationContent(incident) {
  const wrapper = document.createElement("div");
  wrapper.className = "location";
  wrapper.append(text("strong", incident.municipality || "Ubicación no disponible"), text("small", [incident.province, incident.km && `PK ${incident.km}`].filter(Boolean).join(" · ")));
  return wrapper;
}

function coverageContent(incident) {
  const wrapper = document.createElement("span");
  wrapper.className = incident.has_camera_coverage ? "coverage" : "coverage no-coverage";
  wrapper.innerHTML = incident.has_camera_coverage ? `<i data-lucide="camera"></i>${incident.camera_coverage_count || 1}` : "Sin cobertura";
  if (window.lucide) queueMicrotask(() => window.lucide.createIcons());
  return wrapper;
}

function imageFallback() {
  const fallback = document.createElement("div");
  fallback.className = "image-fallback";
  fallback.innerHTML = `<i data-lucide="image-off"></i><small>Imagen no disponible</small>`;
  if (window.lucide) queueMicrotask(() => window.lucide.createIcons());
  return fallback;
}

function badge(value, className) { return text("span", value, `badge ${className}`); }
function text(tag, value, className = "") { const node = document.createElement(tag); node.textContent = value; node.className = className; return node; }
function cell(content) { const td = document.createElement("td"); td.append(content); return td; }
function safeClass(value) { return String(value).toLowerCase().replace(/[^a-z0-9_-]/g, ""); }
function formatSeverity(value) { return ({ highest: "Muy alta", high: "Alta", medium: "Media", low: "Baja" })[String(value).toLowerCase()] || value || "Sin dato"; }

function showState(active) {
  elements.loadingState.hidden = active !== "loading";
  elements.errorState.hidden = active !== "error";
  elements.emptyState.hidden = active !== "empty";
  elements.incidentResults.hidden = active !== "incidents";
  elements.cameraResults.hidden = active !== "cameras";
  document.querySelector(".results").setAttribute("aria-busy", String(active === "loading"));
}

function setConnection(online) {
  elements.connectionStatus.classList.toggle("is-online", online);
  elements.connectionStatus.classList.toggle("is-offline", !online);
  elements.connectionStatus.lastChild.textContent = online ? "En línea" : "Sin conexión";
}

function updateTimestamp(value) {
  const date = value ? new Date(value) : new Date();
  elements.lastUpdate.dateTime = date.toISOString();
  elements.lastUpdate.textContent = `Actualizado ${date.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" })}`;
}

function clearFilters() {
  elements.filterForm.reset();
  elements.limitFilter.value = "12";
  loadCurrentView();
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
    <div class="detail-row"><span>Dirección</span>${escapeHtml(incident.direction_label || "N/A")}</div>
    <div class="detail-row"><span>Inicio</span>${escapeHtml(incident.start_time || "N/A")}</div>
    <div class="detail-row"><span>Fin previsto</span>${escapeHtml(incident.end_time || "N/A")}</div>
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