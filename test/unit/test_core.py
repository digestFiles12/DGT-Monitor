from dgt_monitor.core.geometry import DistanceCalculator
from dgt_monitor.core.localization import Translator
from dgt_monitor.core.models import Incident, IncidentStats
from dgt_monitor.core.text import TextCleaner, matches_text, normalize_road, parse_kilometer_point


def test_models_serialize_stable_contract():
    incident = Incident(id="sit-1", road="A-3", has_camera_coverage=True)
    stats = IncidentStats(total=1, accidents=1)

    assert incident.to_dict()["has_camera_coverage"] is True
    assert stats.to_dict() == {
        "total": 1, "accidents": 1, "roadworks": 0, "stuck": 0,
        "obstructions": 0, "weather": 0,
    }


def test_text_translation_and_location_helpers():
    assert TextCleaner().clean("ValÃ©ncia") == "Valéncia"
    assert Translator().translate("highest") == "Crítica"
    assert Translator("en").translate("highest") == "Critical"
    assert Translator().translate("RoadOrCarriagewayOrLaneManagement") == "Gestión de vía o carril"
    assert Translator("en").translate("RoadOrCarriagewayOrLaneManagement") == "Road, carriageway or lane management"
    assert Translator().translate("positive") == "Sentido positivo"
    assert Translator().translate("Lanes Deviated") == "Carriles desviados"
    assert Translator().translate("unknownFutureCode") == "Unknown Future Code"
    assert Translator().translate(None) == "Sin dato"
    assert Translator().translate("N/A") == "Sin dato"
    assert Translator("en").translate(None) == "N/A"
    assert normalize_road("AP-7") == "AP7"
    assert parse_kilometer_point("PK 12+500") == 12.5
    assert parse_kilometer_point("330,2") == 330.2
    assert matches_text("Madrid", "mad")
    assert matches_text("Madrid", "madrid", "exact")
    assert not matches_text("Madrid Norte", "madrid", "exact")
    assert matches_text("A-52", r"^A-\d+$", "regex")
    assert not matches_text("A-52", "[", "regex")


def test_haversine_distance_for_nearby_points():
    distance = DistanceCalculator().haversine_km(40.4168, -3.7038, 40.4170, -3.7040)
    assert 0 < distance < 0.1