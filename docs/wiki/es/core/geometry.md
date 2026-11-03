# dgt_monitor/core/geometry.py
Proporciona el cálculo geográfico de distancia empleado por la aplicación. Convierte coordenadas de latitud y longitud en una distancia aproximada en kilómetros.
## Dependencias
Importa funciones trigonométricas de `math`. La clase puede ser utilizada por servicios que comparen ubicaciones.
## Contenido
### `DistanceCalculator`
- Calculadora de distancias basada en la fórmula de Haversine.
### `DistanceCalculator.EARTH_RADIUS_KM`
- Radio terrestre utilizado por la fórmula: 6371,0 km.
### `DistanceCalculator.haversine_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float`
- Calcula la distancia entre dos puntos expresados en grados; convierte a radianes y devuelve el resultado en kilómetros.
