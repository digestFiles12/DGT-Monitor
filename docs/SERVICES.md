# Servicios de aplicación

## IncidentService

Obtiene incidentes mediante un repositorio, aplica cache, filtra por provincia, municipio, carretera, severidad, categoria y cobertura de camara, y calcula estadisticas. Los filtros textuales usan `matches_text()` y por tanto aceptan `contains`, `exact` y `regex` mediante `IncidentFilters.match_mode`.

## CameraService

Obtiene camaras mediante cache, filtra por provincia, carretera, punto kilometrico, coordenadas, distancia Haversine y limite. Los filtros `province` y `road` respetan `CameraFilters.match_mode` para busqueda parcial, exacta o regex.

Para anotar cobertura crea un indice por carretera normalizada y considera cercana una camara situada a un maximo de `CAMERA_MATCH_RANGE_KM`, actualmente 2.0 km por punto kilometrico. Tambien expone `with_incident_coverage()`, que devuelve solo camaras relacionadas con incidencias activas y se usa para el filtro `incident_coverage=true`.

## DgtApplicationService

Es la fachada compartida por FastAPI y PyQt6. Sus métodos actuales son:

- `get_incident_payload(filters=None)`: devuelve fecha, total, estadísticas e incidentes serializados.
- `get_cameras(filters=None)`: devuelve fecha, total y cámaras serializadas.

La GUI y la API pasan filtros de dominio (`IncidentFilters`, `CameraFilters`) a esta fachada. Ningun widget ni ruta descarga XML ni instancia repositorios directamente.

Cuando `CameraFilters.incident_coverage` esta activo, la fachada filtra camaras sin limite, calcula la relacion con incidencias activas y despues reaplica `limit`. Este orden evita que el limite inicial oculte una camara valida situada mas tarde en la lista original.

## Activity service

El sistema de actividad registra eventos en memoria o SQLite según `ACTIVITY_DB_PATH`. La API expone paginación, SSE, limpieza y export CSV con autenticación por `X-API-Key`.

## Caché

`TtlCache` usa `RLock`, carga una sola vez por clave y devuelve copias profundas para impedir que una capa de presentacion modifique el valor almacenado. Los TTL iniciales son 120 segundos para incidentes y 300 para camaras.