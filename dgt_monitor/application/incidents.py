"""Incident use cases."""

from collections.abc import Sequence

from dgt_monitor.core.models import Incident, IncidentFilters, IncidentStats
from dgt_monitor.core.ports import IncidentRepository
from dgt_monitor.core.text import matches_text
from dgt_monitor.infrastructure.cache import TtlCache


class IncidentService:
    def __init__(self, repository: IncidentRepository, cache: TtlCache[list[Incident]]) -> None:
        self._repository = repository
        self._cache = cache

    def get_all(self, refresh: bool = False) -> list[Incident]:
        if refresh:
            self._cache.invalidate("incidents")
        return self._cache.get_or_load("incidents", lambda: list(self._repository.fetch()))

    def filter(self, incidents: Sequence[Incident], filters: IncidentFilters) -> list[Incident]:
        return [item for item in incidents if self._matches(item, filters)]

    def stats(self, incidents: Sequence[Incident]) -> IncidentStats:
        causes = [item.cause.casefold() for item in incidents]
        return IncidentStats(
            total=len(incidents),
            accidents=sum("accident" in cause for cause in causes),
            roadworks=sum("roadworks" in cause or "maintenance" in cause for cause in causes),
            stuck=sum("stuck" in cause or "breakdown" in cause for cause in causes),
            obstructions=sum("obstruction" in cause for cause in causes),
            weather=sum(any(word in cause for word in ("weather", "fog", "snow", "flooding", "ice", "rain")) for cause in causes),
        )

    @staticmethod
    def _matches(item: Incident, filters: IncidentFilters) -> bool:
        cause = item.cause.casefold()
        kind_matches = {
            None: True,
            "": True,
            "accident": "accident" in cause,
            "roadworks": "roadworks" in cause or "maintenance" in cause,
            "stuck": "stuck" in cause or "breakdown" in cause,
            "obstruction": "obstruction" in cause,
            "weather": any(word in cause for word in ("weather", "fog", "snow", "flooding", "ice", "rain")),
        }
        camera_matches = {
            None: True,
            "": True,
            "with": item.has_camera_coverage,
            "without": not item.has_camera_coverage,
        }
        return (
            matches_text(item.province, filters.province)
            and matches_text(item.municipality, filters.municipality)
            and matches_text(item.road, filters.road)
            and (not filters.severity or item.severity.casefold() == filters.severity.casefold())
            and kind_matches.get(filters.kind, True)
            and camera_matches.get(filters.camera, True)
        )