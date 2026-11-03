# dgt_monitor/core/constants.py
Centraliza las direcciones DGT y los valores predeterminados que usan las peticiones HTTP, la caché y la asociación de cámaras. Así se comparten estos ajustes entre módulos.
## Dependencias
No importa módulos del proyecto ni de terceros. Los adaptadores HTTP, repositorios y bootstrap usan estas constantes.
## Contenido
### `DGT_INCIDENTS_URL`, `DGT_CAMERAS_URL`
- Direcciones de los documentos DGT DATEX2 de incidencias y cámaras, respectivamente.
### `HTTP_TIMEOUT_SECONDS`, `HTTP_HEADERS`
- Tiempo de espera HTTP predeterminado (15 segundos) y cabeceras enviadas por el cliente, incluidos `User-Agent` y `Accept`.
### `INCIDENT_CACHE_SECONDS`, `CAMERA_CACHE_SECONDS`
- Duraciones de caché predeterminadas: 120 segundos para incidencias y 300 para cámaras.
### `CAMERA_MATCH_RANGE_KM`
- Distancia kilométrica predeterminada de asociación de cámaras: 2,0 km.
