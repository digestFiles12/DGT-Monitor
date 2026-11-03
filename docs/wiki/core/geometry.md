# dgt_monitor/core/geometry.py
**ES:** Proporciona el cálculo geográfico de distancia empleado por la aplicación. Convierte coordenadas de latitud y longitud en una distancia aproximada en kilómetros.
**EN:** Provides the application's geographic distance calculation. It converts latitude and longitude coordinates into an approximate distance in kilometers.
## Dependencies / Dependencias
Importa funciones trigonométricas de `math`. La clase puede ser utilizada por servicios que comparen ubicaciones.
## Contents / Contenido
### `DistanceCalculator`
- **ES:** Calculadora de distancias basada en la fórmula de Haversine.
- **EN:** Distance calculator based on the Haversine formula.
### `DistanceCalculator.EARTH_RADIUS_KM`
- **ES:** Radio terrestre utilizado por la fórmula: 6371,0 km.
- **EN:** Earth radius used by the formula: 6371.0 km.
### `DistanceCalculator.haversine_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float`
- **ES:** Calcula la distancia entre dos puntos expresados en grados; convierte a radianes y devuelve el resultado en kilómetros.
- **EN:** Calculates the distance between two points expressed in degrees; converts them to radians and returns the result in kilometers.
