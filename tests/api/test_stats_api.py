from pathlib import Path

from fastapi.testclient import TestClient

from dgt_monitor.api.factory import create_app
from dgt_monitor.application.cameras import CameraService
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.core.regions import UNKNOWN_REGION
from dgt_monitor.infrastructure.cache import TtlCache
from dgt_monitor.infrastructure.parsers import IncidentParser

SAMPLE_XML = Path(__file__).resolve().parents[1] / "fixtures" / "incidents_sample.xml"


class StaticRepository:
    def __init__(self, items):
        self._items = items

    def fetch(self):
        return self._items


def build_client() -> TestClient:
    incidents = IncidentParser().parse(SAMPLE_XML.read_text(encoding="utf-8"))
    incident_service = IncidentService(StaticRepository(incidents), TtlCache(60))
    camera_service = CameraService(StaticRepository([]), TtlCache(60))
    return TestClient(create_app(DgtApplicationService(incident_service, camera_service)))


def test_stats_by_province_has_indicators_and_extremes():
    body = build_client().get("/api/stats").json()
    assert body["level"] == "province"
    assert body["total"] == 90
    assert sum(group["total"] for group in body["groups"].values()) == 90
    for indicator in ("total", "accidents", "roadworks", "breakdowns", "obstructions", "weather"):
        extreme = body["extremes"][indicator]
        if indicator == "weather":  # no weather incidents in the sample: every group is 0
            assert extreme["min"] is None and extreme["max"]["value"] == 0
            continue
        assert extreme["max"]["value"] >= extreme["min"]["value"] >= 1


def test_stats_by_region_groups_provinces_into_communities():
    body = build_client().get("/api/stats", params={"level": "region"}).json()
    assert body["level"] == "region"
    assert UNKNOWN_REGION not in body["groups"]
    assert "Andalucía" in body["groups"]
    assert len(body["groups"]) < 20


def test_stats_rejects_invalid_level():
    assert build_client().get("/api/stats", params={"level": "city"}).status_code == 422


def test_grouped_json_has_all_groupings():
    body = build_client().get("/api/stats/grouped").json()
    for key in ("by_province", "by_region", "by_type", "by_weekday", "by_weekday_province", "by_weekday_region", "by_province_type", "by_region_type"):
        assert key in body
    assert sum(day["total"] for day in body["by_weekday"].values()) == body["total"]
    assert all(isinstance(v, list) and v for v in body["region_provinces"].values())
    assert sorted(p for v in body["region_provinces"].values() for p in v) == sorted(body["by_province"])
    for key in ("by_province_type", "by_region_type"):
        for kind, groups in body[key].items():
            assert sum(leaf["total"] for leaf in groups.values()) == body["by_type"][kind]["total"]


def test_grouped_type_labels_are_translated_in_both_languages():
    body = build_client().get("/api/stats/grouped").json()
    labels = body["labels"]["by_type"]
    assert set(labels) == {"es", "en"}
    for code in body["by_type"]:
        assert set(labels["es"]) >= {code} and set(labels["en"]) >= {code}
        assert labels["es"][code] and labels["en"][code]
    assert labels["es"]["RoadOrCarriagewayOrLaneManagement"] == "Gestión de vía o carril"
    assert labels["en"]["RoadOrCarriagewayOrLaneManagement"] == "Road, carriageway or lane management"


def test_dashboard_script_uses_type_labels_and_unknown_translation():
    script = build_client().get("/static/app.js").text
    assert "grouped.labels?.by_type?.[state.language]" in script
    assert "unknownGroup: \"Sin datos\"" in script and "unknownGroup: \"Unknown\"" in script
