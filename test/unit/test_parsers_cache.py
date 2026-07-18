from dgt_monitor.infrastructure.cache import TtlCache
from dgt_monitor.infrastructure.parsers import CameraParser, IncidentParser


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