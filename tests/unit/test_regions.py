from pathlib import Path

import pytest

from dgt_monitor.core.regions import (
    PROVINCE_TO_REGION,
    UNKNOWN_REGION,
    normalize_province_name,
    region_for_province,
)
from dgt_monitor.infrastructure.parsers.incident import IncidentParser

SAMPLE = Path(__file__).resolve().parents[1] / "fixtures" / "incidents_sample.xml"


def test_there_are_52_provinces():
    assert len(PROVINCE_TO_REGION) == 52


@pytest.mark.parametrize("province", list(PROVINCE_TO_REGION))
def test_every_province_has_a_region(province):
    assert region_for_province(province) not in (UNKNOWN_REGION, "")


def test_all_communities_plus_ceuta_and_melilla_are_present():
    regions = set(PROVINCE_TO_REGION.values())
    assert len(regions) == 19
    assert {"Ceuta", "Melilla", "Cataluña", "Comunitat Valenciana", "País Vasco"} <= regions


@pytest.mark.parametrize(
    "name, expected",
    [
        ("Alacant/Alicante", "Comunitat Valenciana"),
        ("Alicante", "Comunitat Valenciana"),
        ("Alacant", "Comunitat Valenciana"),
        ("València/Valencia", "Comunitat Valenciana"),
        ("Castelló/Castellón", "Comunitat Valenciana"),
        ("Araba/Álava", "País Vasco"),
        ("Vizcaya", "País Vasco"),
        ("A Coruña", "Galicia"),
        ("Illes Balears", "Illes Balears"),
        ("Girona", "Cataluña"),
        ("Lleida", "Cataluña"),
        ("Ourense", "Galicia"),
    ],
)
def test_bilingual_names_and_aliases(name, expected):
    assert region_for_province(name) == expected


def test_lookup_ignores_case_accents_and_extra_spaces():
    assert region_for_province("  SEVILLA ") == "Andalucía"
    assert region_for_province("malaga") == "Andalucía"
    assert region_for_province("a  coruna") == "Galicia"
    assert normalize_province_name("Málaga") == "malaga"


def test_unknown_or_empty_province_returns_unknown():
    assert region_for_province("Atlantis") == UNKNOWN_REGION
    assert region_for_province("") == UNKNOWN_REGION


def test_unknown_province_is_logged_once(caplog):
    with caplog.at_level("WARNING", logger="dgt_monitor.core.regions"):
        region_for_province("Nowhere Land")
        region_for_province("Nowhere Land")
    assert len(caplog.records) == 1


def test_sample_incidents_all_get_a_known_community():
    incidents = IncidentParser().parse(SAMPLE.read_text(encoding="utf-8"))
    assert incidents
    for incident in incidents:
        assert region_for_province(incident.province) != UNKNOWN_REGION
        assert incident.community not in ("", UNKNOWN_REGION)
