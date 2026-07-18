import pytest

from dgt_monitor.core.exceptions import DgtParseError
from dgt_monitor.infrastructure.cache import TtlCache
from dgt_monitor.infrastructure.parsers import CameraParser, IncidentParser
from dgt_monitor.infrastructure.parsers.base import Datex2Parser


INCIDENT_XML = """<payload xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<situation id="sit-1"><informationStatus>real</informationStatus>
<situationRecord id="rec-1" version="1" xsi:type="Accident">
<severity>high</severity><causeType>accident</causeType><roadName>A-3</roadName>
<province>Madrid</province><kilometerPoint>12.5</kilometerPoint>
<latitude>40.4168</latitude><longitude>-3.7038</longitude>
</situationRecord></situation></payload>"""

CAMERA_XML = """<payload xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<device id="cam-1" xsi:type="ExtendedDevice"><typeOfDevice>camera</typeOfDevice>
<roadName>A-3</roadName><province>Madrid</province><kilometerPoint>13</kilometerPoint>
<latitude>40.417</latitude><longitude>-3.704</longitude>
<deviceUrl>https://example.test/cam.jpg</deviceUrl></device></payload>"""


def test_parsers_return_domain_models():
    incident = IncidentParser().parse(INCIDENT_XML)[0]
    camera = CameraParser().parse(CAMERA_XML)[0]

    assert incident.id == "sit-1"
    assert incident.cause_label == "Accidente"
    assert incident.latitude == 40.4168
    assert camera.id == "cam-1"
    assert camera.image_url.endswith("cam.jpg")


def test_cache_loads_once_and_returns_isolated_values():
    calls = []
    cache = TtlCache[list[int]](60)

    first = cache.get_or_load("items", lambda: calls.append(1) or [1])
    first.append(2)
    second = cache.get_or_load("items", lambda: calls.append(1) or [3])

    assert calls == [1]
    assert second == [1]


def test_cache_invalidate_forces_reload():
    calls = []
    cache = TtlCache[list[int]](60)

    cache.get_or_load("items", lambda: calls.append(1) or [1])
    cache.invalidate("items")
    cache.get_or_load("items", lambda: calls.append(2) or [2])

    assert calls == [1, 2]


def test_cache_clear_removes_all_entries():
    calls = []
    cache = TtlCache[list[int]](60)

    cache.get_or_load("a", lambda: calls.append("a") or [1])
    cache.get_or_load("b", lambda: calls.append("b") or [2])
    cache.clear()
    cache.get_or_load("a", lambda: calls.append("a2") or [10])

    assert "a2" in calls


def test_parsers_raise_on_invalid_xml():
    with pytest.raises(DgtParseError):
        IncidentParser().parse("not valid xml <<<")
    with pytest.raises(DgtParseError):
        CameraParser().parse("not valid xml <<<")


def test_incident_parser_skips_situation_without_record():
    xml = """<payload xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<situation id="empty-sit"></situation></payload>"""
    incidents = IncidentParser().parse(xml)
    assert incidents == []


def test_incident_parser_appends_detailed_cause():
    xml = """<payload xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<situation id="sit-2">
<situationRecord id="rec-2" version="1" xsi:type="WeatherRelatedRoadConditions">
<causeType>weatherRelatedRoadConditions</causeType>
<detailedCauseType><value>fog</value></detailedCauseType>
<roadName>AP-7</roadName><province>Valencia</province>
</situationRecord></situation></payload>"""
    incident = IncidentParser().parse(xml)[0]
    assert incident.cause == "weatherRelatedRoadConditions - fog"
    assert "Niebla" in incident.cause_label


def test_datex2_optional_float_returns_none_for_invalid():
    assert Datex2Parser.optional_float("not-a-number") is None
    assert Datex2Parser.optional_float("") is None