# dgt_monitor/web/static/sw.js
Implementa el service worker de la aplicación instalable: precarga recursos, limpia cachés antiguas y sirve recursos guardados si la red falla.
## Dependencias
API del navegador `ServiceWorkerGlobalScope`, Cache Storage, eventos `install`/`activate`/`fetch` y `fetch` de red.
## Contenido
### Service worker activo
- La caché actual se llama `dgt-monitor-v55`; `APP_SHELL` precarga `/`, CSS y JavaScript `v=55`, Chart.js local `v=1` y el manifiesto. En `install` guarda esos recursos y llama a `skipWaiting`; en `activate` borra cachés con otro nombre y reclama los clientes.
- Para GET que no sea de `/api/`, intenta primero la red y guarda una copia de la respuesta; si la red falla, devuelve la respuesta en caché o `/`. No intercepta ni almacena `/api/`: los datos operativos deben consultarse al servidor, no presentarse como una copia potencialmente obsoleta.
### Bloque heredado
- El bloque comentado `Legacy service worker retained for reference` es una versión anterior y no participa en los eventos activos.
