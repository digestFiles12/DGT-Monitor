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
    weekday_of,
    write_grouped_json,
)
from dgt_monitor.core.indicators import is_accident, is_breakdown, is_obstruction, is_roadworks, is_weather
from dgt_monitor.core.models import Incident
from dgt_monitor.infrastructure.parsers.incident import IncidentParser


def make_incident(**values):
    return Incident(**values)


def zeros(**values):
    return {"total": 0, "accidents": 0, "roadworks": 0, "breakdowns": 0, "obstructions": 0, "weather": 0, **values}


def test_indicator_counts_and_classifiers():
    incidents = [
        make_incident(cause="roadMaintenance - roadworks"),
        make_incident(cause="Routine maintenance"),
        make_incident(cause="accident"),
        make_incident(cause="vehicleStuck"),
        make_incident(cause="Breakdown"),
        make_incident(cause="obstruction"),
        make_incident(cause="fog"),
        make_incident(cause="other"),
    ]

    assert [is_roadworks(item) for item in incidents] == [True, True, False, False, False, False, False, False]
    assert [is_accident(item) for item in incidents] == [False, False, True, False, False, False, False, False]
    assert [is_breakdown(item) for item in incidents] == [False, False, False, True, True, False, False, False]
    assert [is_obstruction(item) for item in incidents] == [False] * 5 + [True, False, False]
    assert [is_weather(item) for item in incidents] == [False] * 6 + [True, False]
    assert INDICATORS == ("total", "accidents", "roadworks", "breakdowns", "obstructions", "weather")
    assert count_indicators(incidents) == zeros(
        total=8, accidents=1, roadworks=2, breakdowns=2, obstructions=1, weather=1,
    )

def test_weekday_uses_start_time_then_creation_time():
    assert weekday_of(make_incident(start_time="2025-12-12T08:05:19.000+01:00")) == "friday"
    assert weekday_of(make_incident(start_time="invalid", creation_time="2025-12-14T08:00:00+01:00")) == "sunday"
    assert weekday_of(make_incident(start_time="invalid", creation_time="")) is None


def test_grouping_has_expected_shape_and_region_counts():
    incidents = [
        make_incident(province="Madrid", type="Accident", cause="roadworks", start_time="2025-12-12T08:00:00+01:00"),
        make_incident(province="Barcelona", type="Roadworks", cause="accident", start_time="2025-12-13T08:00:00+01:00"),
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
        "Barcelona": zeros(total=1, accidents=1),
        "Madrid": zeros(total=1, roadworks=1),
        "Unknown": zeros(total=1, roadworks=1),
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
        "Zulu": zeros(total=2, accidents=1),
        "Alpha": zeros(total=2, roadworks=3),
        "Beta": zeros(),
    }
    extremes = find_extremes(groups)

    assert extremes["total"] == {"max": {"name": "Alpha", "value": 2}, "min": {"name": "Alpha", "value": 2}}
    assert extremes["accidents"] == {"max": {"name": "Zulu", "value": 1}, "min": {"name": "Zulu", "value": 1}}
    assert extremes["roadworks"] == {"max": {"name": "Alpha", "value": 3}, "min": {"name": "Alpha", "value": 3}}
    assert extremes["weather"] == {"max": {"name": "Alpha", "value": 0}, "min": None}
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

