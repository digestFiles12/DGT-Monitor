# dgt_monitor/core/constants.py
**ES:** Centraliza las direcciones DGT y los valores predeterminados que usan las peticiones HTTP, la caché y la asociación de cámaras. Así se comparten estos ajustes entre módulos.
**EN:** Centralizes DGT URLs and default values used by HTTP requests, caching, and camera matching. This lets modules share the same settings.
## Dependencies / Dependencias
No importa módulos del proyecto ni de terceros. Los adaptadores HTTP, repositorios y bootstrap usan estas constantes.
## Contents / Contenido
### `DGT_INCIDENTS_URL`, `DGT_CAMERAS_URL`
- **ES:** Direcciones de los documentos DGT DATEX2 de incidencias y cámaras, respectivamente.
- **EN:** URLs for the DGT DATEX2 incident and camera documents, respectively.
### `HTTP_TIMEOUT_SECONDS`, `HTTP_HEADERS`
- **ES:** Tiempo de espera HTTP predeterminado (15 segundos) y cabeceras enviadas por el cliente, incluidos `User-Agent` y `Accept`.
- **EN:** Default HTTP timeout (15 seconds) and headers sent by the client, including `User-Agent` and `Accept`.
### `INCIDENT_CACHE_SECONDS`, `CAMERA_CACHE_SECONDS`
- **ES:** Duraciones de caché predeterminadas: 120 segundos para incidencias y 300 para cámaras.
- **EN:** Default cache durations: 120 seconds for incidents and 300 for cameras.
### `CAMERA_MATCH_RANGE_KM`
- **ES:** Distancia kilométrica predeterminada de asociación de cámaras: 2,0 km.
- **EN:** Default kilometer-distance range for matching cameras: 2.0 km.
