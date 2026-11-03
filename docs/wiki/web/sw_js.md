# dgt_monitor/web/static/sw.js
**ES:** Implementa el service worker de la aplicación instalable: precarga recursos, limpia cachés antiguas y sirve recursos guardados si la red falla.
**EN:** Implements the installable app's service worker: pre-caches assets, removes old caches, and serves saved resources when the network fails.
## Dependencies / Dependencias
API del navegador `ServiceWorkerGlobalScope`, Cache Storage, eventos `install`/`activate`/`fetch` y `fetch` de red.
Browser `ServiceWorkerGlobalScope`, Cache Storage, `install`/`activate`/`fetch` events, and network `fetch`.
## Contents / Contenido
### Active service worker
- **ES:** La caché actual se llama `dgt-monitor-v54`; `APP_SHELL` precarga `/`, CSS y JavaScript `v=54`, Chart.js local `v=1` y el manifiesto. En `install` guarda esos recursos y llama a `skipWaiting`; en `activate` borra cachés con otro nombre y reclama los clientes.
- **EN:** The current cache is `dgt-monitor-v54`; `APP_SHELL` pre-caches `/`, CSS and JavaScript `v=54`, local Chart.js `v=1`, and the manifest. On `install` it stores these resources and calls `skipWaiting`; on `activate` it deletes differently named caches and claims clients.
- **ES:** Para GET que no sea de `/api/`, intenta primero la red y guarda una copia de la respuesta; si la red falla, devuelve la respuesta en caché o `/`. No intercepta ni almacena `/api/`: los datos operativos deben consultarse al servidor, no presentarse como una copia potencialmente obsoleta.
- **EN:** For GET requests outside `/api/`, it tries the network first and stores a response copy; if the network fails, it returns the cached request or `/`. It neither intercepts nor caches `/api/`: operational data should be fetched from the server rather than presented as a potentially stale copy.
### Legacy block
- **ES:** El bloque comentado `Legacy service worker retained for reference` es una versión anterior y no participa en los eventos activos.
- **EN:** The commented `Legacy service worker retained for reference` block is an earlier version and does not participate in active event handling.
