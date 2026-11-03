# dgt_monitor/core/geometry.py
Provides the application's geographic distance calculation. It converts latitude and longitude coordinates into an approximate distance in kilometers.
## Dependencies
Imports trigonometric functions from `math`. Services comparing locations can use the class.
## Contents
### `DistanceCalculator`
- Distance calculator based on the Haversine formula.
### `DistanceCalculator.EARTH_RADIUS_KM`
- Earth radius used by the formula: 6371.0 km.
### `DistanceCalculator.haversine_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float`
- Calculates the distance between two points expressed in degrees; converts them to radians and returns the result in kilometers.
