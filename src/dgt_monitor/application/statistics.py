"""Incident indicators and grouped statistics."""

from collections.abc import Iterable
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from dgt_monitor.core.models import Incident
from dgt_monitor.core.regions import UNKNOWN_REGION, region_for_province

INDICATORS = ("total", "severe", "roadworks", "road_closures")
WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
DEFAULT_GROUPED_JSON = "grouped_incidents.json"


def is_severe(incident: Incident) -> bool:
    """Return whether the incident has the highest severity."""
    return incident.severity.casefold() == "highest"


def is_roadworks(incident: Incident) -> bool:
    """Return whether the incident cause describes roadworks or maintenance."""
    cause = incident.cause.casefold()
    return "roadworks" in cause or "maintenance" in cause


def is_road_closure(incident: Incident) -> bool:
    """Return whether traffic management indicates a road closure."""
    return incident.management_type in {"roadClosed", "carriagewayClosures"}


def count_indicators(incidents: Iterable[Incident]) -> dict[str, int]:
    """Count the four dashboard indicators."""
    counts = dict.fromkeys(INDICATORS, 0)
    for incident in incidents:
        counts["total"] += 1
        counts["severe"] += is_severe(incident)
        counts["roadworks"] += is_roadworks(incident)
        counts["road_closures"] += is_road_closure(incident)
    return counts


def weekday_of(incident: Incident) -> str | None:
    """Return the start weekday, falling back to the creation timestamp."""
    for value in (incident.start_time, incident.creation_time):
        if not value:
            continue
        try:
            return WEEKDAYS[datetime.fromisoformat(value).weekday()]
        except ValueError:
            continue
    return None


def _empty_leaf() -> dict[str, int]:
    return dict.fromkeys(INDICATORS, 0)


def _add_incident(groups: dict[str, dict[str, int]], key: str, incident: Incident) -> None:
    if key not in groups:
        groups[key] = _empty_leaf()
    leaf = groups[key]
    leaf["total"] += 1
    leaf["severe"] += is_severe(incident)
    leaf["roadworks"] += is_roadworks(incident)
    leaf["road_closures"] += is_road_closure(incident)


def _sorted_groups(groups: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    return {name: groups[name] for name in sorted(groups)}


def group_incidents(
    incidents: Iterable[Incident], generated_at: str | None = None
) -> dict[str, Any]:
    """Group incidents by province, region, type, weekday, and weekday geography."""
    provinces: dict[str, dict[str, int]] = {}
    regions: dict[str, dict[str, int]] = {}
    types: dict[str, dict[str, int]] = {}
    weekdays: dict[str, dict[str, int]] = {day: _empty_leaf() for day in WEEKDAYS}
    weekday_provinces: dict[str, dict[str, dict[str, int]]] = {day: {} for day in WEEKDAYS}
    weekday_regions: dict[str, dict[str, dict[str, int]]] = {day: {} for day in WEEKDAYS}
    total = 0

    for incident in incidents:
        province = incident.province or UNKNOWN_REGION
        region = region_for_province(incident.province) if incident.province else UNKNOWN_REGION
        day = weekday_of(incident) or "unknown"
        if day == "unknown" and day not in weekdays:
            weekdays[day] = _empty_leaf()
            weekday_provinces[day] = {}
            weekday_regions[day] = {}
        _add_incident(provinces, province, incident)
        _add_incident(regions, region, incident)
        _add_incident(types, incident.type, incident)
        _add_incident(weekdays, day, incident)
        _add_incident(weekday_provinces[day], province, incident)
        _add_incident(weekday_regions[day], region, incident)
        total += 1

    if "unknown" not in weekdays or weekdays["unknown"]["total"] == 0:
        weekdays.pop("unknown", None)
        weekday_provinces.pop("unknown", None)
        weekday_regions.pop("unknown", None)

    return {
        "generated_at": generated_at if generated_at is not None else datetime.now().astimezone().isoformat(timespec="seconds"),
        "total": total,
        "indicators": list(INDICATORS),
        "by_province": _sorted_groups(provinces),
        "by_region": _sorted_groups(regions),
        "by_type": _sorted_groups(types),
        "by_weekday": weekdays,
        "by_weekday_province": {
            day: _sorted_groups(groups) for day, groups in weekday_provinces.items()
        },
        "by_weekday_region": {
            day: _sorted_groups(groups) for day, groups in weekday_regions.items()
        },
    }


def find_extremes(groups: dict[str, dict[str, int]]) -> dict[str, dict[str, dict[str, str | int] | None]]:
    """Find alphabetical-tiebroken maxima and positive minima for each indicator.

    Groups with zero incidents are ignored for minima so the minimum is meaningful.
    """
    result: dict[str, dict[str, dict[str, str | int] | None]] = {}
    for indicator in INDICATORS:
        values = sorted((name, leaf[indicator]) for name, leaf in groups.items())
        maximum = min(values, key=lambda item: (-item[1], item[0]), default=None)
        positive = [item for item in values if item[1] > 0]
        minimum = min(positive, key=lambda item: (item[1], item[0]), default=None)
        result[indicator] = {
            "max": {"name": maximum[0], "value": maximum[1]} if maximum else None,
            "min": {"name": minimum[0], "value": minimum[1]} if minimum else None,
        }
    return result


def build_statistics(
    incidents: Iterable[Incident], level: str = "province", generated_at: str | None = None
) -> dict[str, Any]:
    """Build grouped statistics at province or region level."""
    if level not in {"province", "region"}:
        raise ValueError("level must be 'province' or 'region'")
    grouped = group_incidents(incidents, generated_at)
    groups = grouped["by_province" if level == "province" else "by_region"]
    return {
        "level": level,
        "total": grouped["total"],
        "groups": groups,
        "extremes": find_extremes(groups),
    }


def write_grouped_json(data: dict[str, Any], path: str | Path) -> Path:
    """Write grouped statistics as UTF-8 JSON, creating parent directories."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


