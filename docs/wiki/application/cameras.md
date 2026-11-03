# dgt_monitor/application/cameras.py
**ES:** Implementa los casos de uso para cargar, filtrar y ordenar cámaras, y para relacionarlas con incidentes por carretera, provincia y kilómetro.
**EN:** Implements use cases for loading, filtering, and sorting cameras, and relating them to incidents by road, province, and kilometer point.
## Dependencies / Dependencias
Importa modelos y puertos de `core`, funciones de normalización y comparación textual, geometría para distancias, la constante de radio y una caché TTL. `CameraService` es usado por la fachada de aplicación.
## Contents / Contenido
### `CameraService`
- **ES:** Servicio de aplicación que coordina repositorio, caché y cálculo espacial para búsquedas y cobertura de cámaras.
- **EN:** Application service coordinating the repository, cache, and spatial calculation for camera search and coverage.
### `CameraService.__init__(repository, cache, distance=None)`
- **ES:** Guarda el repositorio y la caché; usa el calculador de distancia recibido o crea uno predeterminado.
- **EN:** Stores the repository and cache; uses the supplied distance calculator or creates a default one.
### `CameraService.get_all(refresh=False)`
- **ES:** Devuelve las cámaras en caché, cargándolas del repositorio cuando hace falta; con `refresh=True` invalida primero la clave `cameras`.
- **EN:** Returns cached cameras, loading them from the repository when needed; `refresh=True` first invalidates the `cameras` cache key.
### `CameraService.filter(cameras, filters)`
- **ES:** Filtra por provincia/carretera y por distancia al kilómetro y/o coordenadas, añade `km_delta` y `distance_km`, ordena por distancia (los valores no calculados al final) y aplica `limit`. Si el punto kilométrico no se puede analizar, no puede satisfacer un filtro de kilómetro activo.
- **EN:** Filters by province/road and kilometer and/or coordinate distance, adds `km_delta` and `distance_km`, sorts by distance (uncomputed values last), and applies `limit`. An unparseable kilometer point cannot satisfy an active kilometer filter.
### `CameraService.with_incident_coverage(cameras, incidents, range_km=CAMERA_MATCH_RANGE_KM)`
- **ES:** Devuelve cámaras con al menos un incidente en la misma carretera normalizada y dentro del radio; si ambas provincias existen, también deben coincidir. Ignora incidentes o cámaras sin kilómetro analizable.
- **EN:** Returns cameras with at least one incident on the same normalized road and within range; when both provinces exist, they must also match. Incidents or cameras without a parseable kilometer are ignored.
### `CameraService.annotate_coverage(incidents, cameras, range_km=CAMERA_MATCH_RANGE_KM)`
- **ES:** Copia cada incidente con indicadores de cobertura: booleano, cantidad de cámaras coincidentes y diferencia mínima en km redondeada a tres decimales. No elimina incidentes sin cobertura.
- **EN:** Copies each incident with coverage fields: boolean, number of matching cameras, and minimum kilometer difference rounded to three decimals. Incidents without coverage are retained.
