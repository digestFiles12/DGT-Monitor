# dgt_monitor/web/static/sw.js
Implements the installable app's service worker: pre-caches assets, removes old caches, and serves saved resources when the network fails.
## Dependencies
Browser `ServiceWorkerGlobalScope`, Cache Storage, `install`/`activate`/`fetch` events, and network `fetch`.
## Contents
### Active service worker
- The current cache is `dgt-monitor-v57`; `APP_SHELL` pre-caches `/`, CSS and JavaScript `v=57`, local Chart.js `v=1`, and the manifest. On `install` it stores these resources and calls `skipWaiting`; on `activate` it deletes differently named caches and claims clients.
- For GET requests outside `/api/`, it tries the network first and stores a response copy; if the network fails, it returns the cached request or `/`. It neither intercepts nor caches `/api/`: operational data should be fetched from the server rather than presented as a potentially stale copy.
### Legacy block
- The commented `Legacy service worker retained for reference` block is an earlier version and does not participate in active event handling.
