from dgt_monitor.application.cameras import CameraService
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.core.models import Camera, CameraFilters, Incident, IncidentFilters
from dgt_monitor.infrastructure.cache import TtlCache


class FakeIncidentRepository:
    def __init__(self):
        self.calls = 0

    def fetch(self):
        self.calls += 1
        return [
            Incident(id="accident", cause="accident", road="A-3", province="Madrid", km="12.5", severity="high"),
            Incident(id="weather", cause="weatherRelatedRoadConditions - fog", road="AP-7", province="Valencia", km="330"),
        ]


class FakeCameraRepository:
    def __init__(self):
        self.calls = 0

    def fetch(self):
        self.calls += 1
        return [
            Camera(id="near", road="A-3", province="Madrid", km="13", image_url="https://example.test/near.jpg", latitude=40.417, longitude=-3.704),
            Camera(id="far", road="A-3", province="Madrid", km="48", image_url="https://example.test/far.jpg"),
        ]


def build_facade():
    incidents = FakeIncidentRepository()
    cameras = FakeCameraRepository()
    facade = DgtApplicationService(
        IncidentService(incidents, TtlCache(120)),
        CameraService(cameras, TtlCache(300)),
    )
    return facade, incidents, cameras


def test_facade_filters_builds_stats_and_annotates_coverage():
    facade, incident_repository, camera_repository = build_facade()

    payload = facade.get_incident_payload(IncidentFilters(kind="accident"))
    second = facade.get_incident_payload()

    assert payload["count"] == 1
    assert payload["stats"]["accidents"] == 1
    assert payload["items"][0]["has_camera_coverage"] is True
    assert payload["items"][0]["nearest_camera_km_delta"] == 0.5
    assert second["count"] == 2
    assert incident_repository.calls == 1
    assert camera_repository.calls == 1


def test_facade_filters_cameras_by_kilometer_and_distance():
    facade, _, _ = build_facade()

    payload = facade.get_cameras(CameraFilters(
        province="Madrid", road="A-3", kilometer="12.5",
        latitude=40.4168, longitude=-3.7038, max_km_delta=1.0,
    ))

    assert payload["count"] == 1
    assert payload["items"][0]["id"] == "near"
    assert payload["items"][0]["km_delta"] == 0.5
    assert payload["items"][0]["distance_km"] < 0.1