# dgt_monitor/application/cameras.py
Implementa los casos de uso para cargar, filtrar y ordenar cámaras, y para relacionarlas con incidentes por carretera, provincia y kilómetro.
## Dependencias
Importa modelos y puertos de `core`, funciones de normalización y comparación textual, geometría para distancias, la constante de radio y una caché TTL. La fachada de aplicación usa `CameraService`.
## Contenido
### `CameraService`
- Servicio de aplicación que coordina repositorio, caché y cálculo espacial para búsquedas y cobertura de cámaras.
### `CameraService.__init__(repository, cache, distance=None)`
- Guarda el repositorio y la caché; usa el calculador de distancia recibido o crea uno predeterminado.
### `CameraService.get_all(refresh=False)`
- Devuelve las cámaras en caché, cargándolas del repositorio cuando hace falta; con `refresh=True` invalida primero la clave `cameras`.
### `CameraService.filter(cameras, filters)`
- Filtra por provincia, comunidad (derivada de `camera.province` con `region_for_province` y comparada sin distinguir mayúsculas), carretera y distancia al kilómetro y/o coordenadas; añade `km_delta` y `distance_km`, ordena por distancia (los valores no calculados al final) y aplica `limit`. Si el punto kilométrico no se puede analizar, no puede satisfacer un filtro de kilómetro activo.
### `CameraService.with_incident_coverage(cameras, incidents, range_km=CAMERA_MATCH_RANGE_KM)`
- Devuelve cámaras con al menos un incidente en la misma carretera normalizada y dentro del radio; si ambas provincias existen, también deben coincidir. Ignora incidentes o cámaras sin kilómetro analizable.
### `CameraService.annotate_coverage(incidents, cameras, range_km=CAMERA_MATCH_RANGE_KM)`
- Copia cada incidente con indicadores de cobertura: booleano, cantidad de cámaras coincidentes y diferencia mínima en km redondeada a tres decimales. No elimina incidentes sin cobertura.
