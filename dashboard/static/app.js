/* DGT Monitor — Frontend */
"use strict";

/* ── Service Worker registration ── */
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(console.warn);
  });
}

/* ── DOM refs ── */
const incidentsList  = document.getElementById("incidents-list");
const statTotal      = document.getElementById("stat-total");
const statHigh       = document.getElementById("stat-high");
const statUpdated    = document.getElementById("stat-updated");
const statusBadge    = document.getElementById("status-badge");
const filterForm     = document.getElementById("filter-form");
const refreshBtn     = document.getElementById("refresh-btn");

/* ── State ── */
let ws       = null;
let filters  = {};

/* ── WebSocket ── */
function buildWsUrl(params) {
  const base = `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/incidents`;
  const qs   = new URLSearchParams({ interval: "30", ...params }).toString();
  return qs ? `${base}?${qs}` : base;
}

function setStatus(state) {
  statusBadge.textContent = state === "live" ? "En directo" : state === "error" ? "Error" : "Conectando…";
  statusBadge.className   = `badge badge--${state}`;
}

function connect() {
  if (ws) { ws.close(); ws = null; }
  setStatus("connecting");
  ws = new WebSocket(buildWsUrl(filters));

  ws.onopen    = () => setStatus("live");
  ws.onmessage = (ev) => render(JSON.parse(ev.data));
  ws.onerror   = () => setStatus("error");
  ws.onclose   = () => {
    setStatus("connecting");
    setTimeout(connect, 5000);
  };
}

/* ── Rendering ── */
function formatTime(iso) {
  if (!iso) return "—";
  try { return new Date(iso).toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }); }
  catch { return iso; }
}

function severityClass(sev) {
  if (!sev) return "";
  const s = String(sev).toLowerCase();
  if (s === "high"   || s === "alta")   return "high";
  if (s === "medium" || s === "media")  return "medium";
  if (s === "low"    || s === "baja")   return "low";
  return "";
}

function renderIncident(item) {
  const sev  = severityClass(item.severity);
  const card = document.createElement("article");
  card.className = `incident-card${sev ? ` incident-card--${sev}` : ""}`;

  const body = document.createElement("div");
  body.className = "incident-card__body";

  const title = document.createElement("p");
  title.className = "incident-card__title";
  title.textContent = item.description || item.id || "Incidente";
  body.appendChild(title);

  const detail = document.createElement("p");
  detail.className = "incident-card__detail";
  detail.textContent = [item.province, item.municipality].filter(Boolean).join(" · ");
  body.appendChild(detail);

  if (item.road) {
    const road = document.createElement("p");
    road.className = "incident-card__road";
    road.textContent = item.road;
    body.appendChild(road);
  }

  const meta = document.createElement("div");
  meta.className = "incident-card__meta";
  if (item.severity) {
    meta.appendChild(document.createTextNode(item.severity));
  }
  if (item.start_time) {
    meta.appendChild(document.createElement("br"));
    meta.appendChild(document.createTextNode(formatTime(item.start_time)));
  }

  card.appendChild(body);
  card.appendChild(meta);
  return card;
}

function render(payload) {
  if (payload.error) {
    setStatus("error");
    return;
  }
  setStatus("live");

  const items = payload.items || [];
  const stats = payload.stats || {};

  statTotal.textContent   = payload.count   ?? "—";
  statHigh.textContent    = stats.high      ?? "—";
  statUpdated.textContent = formatTime(payload.updated_at);

  incidentsList.replaceChildren();
  if (!items.length) {
    const p = document.createElement("p");
    p.className = "placeholder";
    p.textContent = "Sin incidentes con los filtros actuales.";
    incidentsList.appendChild(p);
    return;
  }
  const frag = document.createDocumentFragment();
  items.forEach((item) => frag.appendChild(renderIncident(item)));
  incidentsList.appendChild(frag);
}

/* ── Utils ── */

/* ── Event listeners ── */
filterForm.addEventListener("submit", (ev) => {
  ev.preventDefault();
  const data = new FormData(filterForm);
  filters = {};
  for (const [k, v] of data.entries()) { if (v.trim()) filters[k] = v.trim(); }
  connect();
});

refreshBtn.addEventListener("click", () => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    /* Server will push on next interval; force reconnect for immediate refresh */
    connect();
  }
});

/* ── Init ── */
connect();
