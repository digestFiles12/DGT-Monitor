"""Application facade consumed by API and GUI adapters."""

from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

from dgt_monitor.application.cameras import CameraService
from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.application.statistics import build_statistics, group_incidents
from dgt_monitor.core.localization import SUPPORTED_LOCALES, Translator, normalize_locale
from dgt_monitor.core.models import CameraFilters, IncidentFilters
from dgt_monitor.core.regions import region_for_province


class DgtApplicationService:
    def __init__(self, incidents: IncidentService, cameras: CameraService) -> None:
        self._incidents = incidents
        self._cameras = cameras

    def get_incident_payload(self, filters: IncidentFilters | None = None, refresh: bool = False, language: str = "es") -> dict[str, Any]:
        filters = filters or IncidentFilters()
        translator = Translator(normalize_locale(language))
        incident_items = self._incidents.get_all(refresh=refresh)
        camera_items = self._cameras.get_all()
        covered = self._cameras.annotate_coverage(incident_items, camera_items)
        stats_scope = self._incidents.filter(covered, self._filters_without_kind(filters))
        filtered = self._incidents.filter(covered, filters)
        return {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "count": len(filtered),
            "stats": self._incidents.stats(stats_scope).to_dict(),
            "language": translator.locale,
            "items": [self._localized_incident(item.to_dict(), translator) for item in filtered],
        }

    @staticmethod
    def _localized_incident(item: dict[str, Any], translator: Translator) -> dict[str, Any]:
        localized = dict(item)
        translatable_fields = {
            "severity": "severity_label",
            "type": "type_label",
            "cause": "cause_label",
            "direction": "direction_label",
            "direction_road": "direction_road_label",
            "lane_usage": "lane_usage_label",
            "management_type": "management_type_label",
            "maintenance_type": "maintenance_type_label",
            "information_status": "information_status_label",
            "probability": "probability_label",
            "compliance": "compliance_label",
            "vehicle_type": "vehicle_type_label",
            "environment_type": "environment_type_label",
            "road_condition_type": "road_condition_type_label",
        }
        for source_key, label_key in translatable_fields.items():
            value = localized.get(source_key)
            localized[label_key] = translator.translate_compound(value) if source_key == "cause" else translator.translate(value)
        return localized

    @staticmethod
    def _filters_without_kind(filters: IncidentFilters) -> IncidentFilters:
        return IncidentFilters(
            province=filters.province,
            municipality=filters.municipality,
            road=filters.road,
            severity=filters.severity,
            camera=filters.camera,
            match_mode=filters.match_mode,
        )

    def get_statistics(self, level: str = "province", refresh: bool = False) -> dict[str, Any]:
        """Return the 4 indicators grouped by province or region, with max/min per indicator."""
        return build_statistics(self._incidents.get_all(refresh=refresh), level=level)

    def get_grouped_incidents(self, refresh: bool = False) -> dict[str, Any]:
        """Return incidents grouped by province, region, type and weekday, plus display labels per locale."""
        grouped = group_incidents(self._incidents.get_all(refresh=refresh))
        grouped["labels"] = {
            "by_type": {
                locale: {code: Translator(locale).translate(code) for code in grouped["by_type"]}
                for locale in sorted(SUPPORTED_LOCALES)
            }
        }
        region_provinces: dict[str, list[str]] = {}
        for province in grouped["by_province"]:
            region_provinces.setdefault(region_for_province(province), []).append(province)
        grouped["region_provinces"] = {region: sorted(names) for region, names in sorted(region_provinces.items())}
        return grouped

    def get_cameras(self, filters: CameraFilters | None = None, refresh: bool = False) -> dict[str, Any]:
        filters = filters or CameraFilters()
        camera_items = self._cameras.get_all(refresh=refresh)
        search_filters = replace(filters, limit=None) if filters.incident_coverage else filters
        items = self._cameras.filter(camera_items, search_filters)
        if filters.incident_coverage:
            items = self._cameras.with_incident_coverage(items, self._incidents.get_all(refresh=refresh))
            if filters.limit is not None:
                items = items[:filters.limit]
        return {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "count": len(items),
            "items": [item.to_dict() for item in items],
        }