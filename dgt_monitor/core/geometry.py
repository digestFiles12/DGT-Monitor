"""Geographical calculations."""

from math import atan2, cos, radians, sin, sqrt


class DistanceCalculator:
    EARTH_RADIUS_KM = 6371.0

    def haversine_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad
        value = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        return self.EARTH_RADIUS_KM * 2 * atan2(sqrt(value), sqrt(1 - value))