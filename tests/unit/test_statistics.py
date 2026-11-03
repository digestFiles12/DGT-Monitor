import json
from pathlib import Path

import pytest

from dgt_monitor.application.statistics import (
    DEFAULT_GROUPED_JSON,
    INDICATORS,
    WEEKDAYS,
    build_statistics,
    count_indicators,
    find_extremes,
    group_incidents,
    is_road_closure,
    is_roadworks,
    is_severe,
    weekday_of,
    write_grouped_json,
)
from dgt_monitor.core.models import Incident
from dgt_monitor.infrastructure.parsers.incident import IncidentParser


def make_incident(**values):
    return Incident(**values)


def test_indicator_counts_and_classifiers():
    incidents = [
        make_incident(severity="Highest", cause="roadMaintenance - roadworks", management_type="roadClosed"),
        make_incident(severity="high", cause="Routine maintenance", management_type="carriagewayClosures"),
        make_incident(severity="highest", cause="accident", management_type="laneRestrictions"),
    ]

    assert [is_severe(item) for item in incidents] == [True, False, True]
    assert [is_roadworks(item) for item in incidents] == [True, True, False]
    assert [is_road_closure(item) for item in incidents] == [True, True, False]
    assert count_indicators(incidents) == {
        "total": 3, "severe": 2, "roadworks": 2, "road_closures": 2,
    }


def test_weekday_uses_start_time_then_creation_time():
    assert weekday_of(make_incident(start_time="2025-12-12T08:05:19.000+01:00")) == "friday"
    assert weekday_of(make_incident(start_time="invalid", creation_time="2025-12-14T08:00:00+01:00")) == "sunday"
    assert weekday_of(make_incident(start_time="invalid", creation_time="")) is None


def test_grouping_has_expected_shape_and_region_counts():
    incidents = [
        make_incident(province="Madrid", type="Accident", severity="highest", cause="roadworks", start_time="2025-12-12T08:00:00+01:00"),
        make_incident(province="Barcelona", type="Roadworks", management_type="roadClosed", start_time="2025-12-13T08:00:00+01:00"),
        make_incident(province="", type="Roadworks", cause="maintenance", creation_time="invalid"),
    ]

    data = group_incidents(incidents, generated_at="2025-12-15T10:00:00+01:00")

    assert set(data) == {
        "generated_at", "total", "indicators", "by_province", "by_region", "by_type",
        "by_weekday", "by_weekday_province", "by_weekday_region",
    }
    assert data["generated_at"] == "2025-12-15T10:00:00+01:00"
    assert data["indicators"] == list(INDICATORS)
    assert data["total"] == 3
    assert data["by_province"] == {
        "Barcelona": {"total": 1, "severe": 0, "roadworks": 0, "road_closures": 1},
        "Madrid": {"total": 1, "severe": 1, "roadworks": 1, "road_closures": 0},
        "Unknown": {"total": 1, "severe": 0, "roadworks": 1, "road_closures": 0},
    }
    assert data["by_region"]["Cataluña"]["total"] == 1
    assert data["by_region"]["Comunidad de Madrid"]["total"] == 1
    assert data["by_region"]["Unknown"]["total"] == 1
    assert set(data["by_weekday"]) == set(WEEKDAYS) | {"unknown"}
    assert data["by_weekday"]["friday"]["total"] == 1
    assert data["by_weekday"]["saturday"]["total"] == 1
    assert data["by_weekday"]["unknown"]["total"] == 1
    assert data["by_weekday_province"]["unknown"]["Unknown"]["total"] == 1


def test_extremes_handle_max_min_ties_zero_and_empty_groups():
    groups = {
        "Zulu": {"total": 2, "severe": 1, "roadworks": 0, "road_closures": 0},
        "Alpha": {"total": 2, "severe": 0, "roadworks": 3, "road_closures": 0},
        "Beta": {"total": 0, "severe": 0, "roadworks": 0, "road_closures": 0},
    }
    extremes = find_extremes(groups)

    assert extremes["total"] == {"max": {"name": "Alpha", "value": 2}, "min": {"name": "Alpha", "value": 2}}
    assert extremes["severe"] == {"max": {"name": "Zulu", "value": 1}, "min": {"name": "Zulu", "value": 1}}
    assert extremes["roadworks"] == {"max": {"name": "Alpha", "value": 3}, "min": {"name": "Alpha", "value": 3}}
    assert extremes["road_closures"] == {"max": {"name": "Alpha", "value": 0}, "min": None}
    assert find_extremes({}) == {indicator: {"max": None, "min": None} for indicator in INDICATORS}


def test_build_statistics_rejects_invalid_level():
    with pytest.raises(ValueError):
        build_statistics([], level="type")


def test_write_grouped_json_round_trips(tmp_path):
    path = tmp_path / "nested" / DEFAULT_GROUPED_JSON
    data = group_incidents([make_incident(province="Málaga", start_time="2025-12-12T08:00:00+01:00")])

    result = write_grouped_json(data, path)

    assert result == path
    serialized = result.read_text(encoding="utf-8")
    assert "Málaga" in serialized
    assert json.loads(serialized) == data


def test_sample_xml_totals_match_all_groupings():
    fixture_path = Path(__file__).parents[1] / "fixtures" / "incidents_sample.xml"
    incidents = IncidentParser().parse(fixture_path.read_text(encoding="utf-8"))
    data = group_incidents(incidents)

    assert sum(group["total"] for group in data["by_province"].values()) == data["total"]
    assert sum(group["total"] for group in data["by_weekday"].values()) == data["total"]
    assert sum(group["total"] for group in data["by_region"].values()) == data["total"]
    assert "Unknown" not in data["by_region"]

