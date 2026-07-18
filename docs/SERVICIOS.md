# Servicios de aplicación

## IncidentService

Obtiene incidentes mediante un repositorio, aplica caché, filtra por provincia, municipio, carretera, severidad y categoría, y calcula estadísticas.

## CameraService

Obtiene cámaras mediante caché, filtra por ubicación y punto kilométrico, calcula distancia Haversine y limita resultados. Para anotar cobertura crea un índice por carretera normalizada y considera cercana una cámara situada a un máximo de 1 km.

## DgtApplicationService

Es la fachada compartida por FastAPI y PyQt6. Sus métodos actuales son:

- `get_incident_payload()`: devuelve fecha, total, estadísticas e incidentes serializados.
- `get_cameras()`: devuelve fecha, total y cámaras serializadas.

## Caché

`TtlCache` usa `RLock`, carga una sola vez por clave y devuelve copias profundas para impedir que una capa de presentación modifique el valor almacenado. Los TTL iniciales son 120 segundos para incidentes y 300 para cámaras.