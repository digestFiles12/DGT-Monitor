"""Camera search and incident coverage use cases."""

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import replace

from dgt_monitor.core.geometry import DistanceCalculator
from dgt_monitor.core.models import Camera, CameraFilters, Incident
from dgt_monitor.core.ports import CameraRepository
from dgt_monitor.core.text import matches_text, normalize_road, parse_kilometer_point
from dgt_monitor.infrastructure.cache import TtlCache


class CameraService:
    def __init__(self, repository: CameraRepository, cache: TtlCache[list[Camera]], distance: DistanceCalculator | None = None) -> None:
        self._repository = repository
        self._cache = cache
        self._distance = distance or DistanceCalculator()

    def get_all(self, refresh: bool = False) -> list[Camera]:
        if refresh:
            self._cache.invalidate("cameras")
        return self._cache.get_or_load("cameras", lambda: list(self._repository.fetch()))

    def filter(self, cameras: Sequence[Camera], filters: CameraFilters) -> list[Camera]:
        incident_km = parse_kilometer_point(filters.kilometer)
        results: list[Camera] = []
        for camera in cameras:
            province_match = matches_text(camera.province, filters.province)
            road_match = matches_text(camera.road, filters.road)
            if filters.province and filters.road:
                if not province_match and not road_match:
                    continue
            elif filters.province and not province_match:
                continue
            elif filters.road and not road_match:
                continue
            camera_km = parse_kilometer_point(camera.km)
            km_delta = abs(camera_km - incident_km) if camera_km is not None and incident_km is not None else None
            if incident_km is not None and (km_delta is None or km_delta > filters.max_km_delta):
                continue
            distance_km = None
            if None not in (filters.latitude, filters.longitude, camera.latitude, camera.longitude):
                distance_km = self._distance.haversine_km(
                    filters.latitude, filters.longitude, camera.latitude, camera.longitude  # type: ignore[arg-type]
                )
            results.append(replace(camera, km_delta=km_delta, distance_km=distance_km))
        results.sort(key=lambda item: item.distance_km if item.distance_km is not None else float("inf"))
        return results[:filters.limit]

    def annotate_coverage(self, incidents: Sequence[Incident], cameras: Sequence[Camera], range_km: float = 1.0) -> list[Incident]:
        by_road: dict[str, list[Camera]] = defaultdict(list)
        for camera in cameras:
            by_road[normalize_road(camera.road)].append(camera)
        annotated: list[Incident] = []
        for incident in incidents:
            incident_km = parse_kilometer_point(incident.km)
            deltas = []
            if incident_km is not None:
                for camera in by_road.get(normalize_road(incident.road), []):
                    if incident.province and camera.province and not matches_text(camera.province, incident.province):
                        continue
                    camera_km = parse_kilometer_point(camera.km)
                    if camera_km is not None and abs(camera_km - incident_km) <= range_km:
                        deltas.append(abs(camera_km - incident_km))
            annotated.append(replace(
                incident,
                has_camera_coverage=bool(deltas),
                camera_coverage_count=len(deltas),
                nearest_camera_km_delta=round(min(deltas), 3) if deltas else None,
            ))
        return annotated