"""Tests for application-layer use cases not covered by integration tests."""

from dgt_monitor.application.cameras import CameraService
from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.core.models import Camera, CameraFilters, Incident, IncidentFilters
from dgt_monitor.infrastructure.cache import TtlCache


class FakeIncidentRepo:
    def __init__(self, items):
        self._items = items
        self.calls = 0

    def fetch(self):
        self.calls += 1
        return self._items


class FakeCameraRepo:
    def __init__(self, items):
        self._items = items
        self.calls = 0

    def fetch(self):
        self.calls += 1
        return self._items


def test_incident_service_refresh_invalidates_cache():
    repo = FakeIncidentRepo([Incident(id="i1")])
    service = IncidentService(repo, TtlCache(60))

    service.get_all()
    service.get_all(refresh=True)

    assert repo.calls == 2


def test_camera_service_refresh_invalidates_cache():
    repo = FakeCameraRepo([Camera(id="c1")])
    service = CameraService(repo, TtlCache(60))

    service.get_all()
    service.get_all(refresh=True)

    assert repo.calls == 2


def test_camera_filter_skips_when_province_and_road_both_set_and_neither_matches():
    repo = FakeCameraRepo([
        Camera(id="cam-a", road="N-1", province="Burgos", km="10"),
        Camera(id="cam-b", road="A-3", province="Madrid", km="10"),
    ])
    service = CameraService(repo, TtlCache(60))
    cameras = service.get_all()

    # Both province AND road set, camera must match at least one
    result = service.filter(cameras, CameraFilters(province="Sevilla", road="AP-9"))

    assert result == []


def test_camera_filter_includes_when_province_or_road_matches():
    repo = FakeCameraRepo([
        Camera(id="cam-b", road="A-3", province="Madrid", km="10"),
    ])
    service = CameraService(repo, TtlCache(60))
    cameras = service.get_all()

    # province doesn't match but road does — should be included
    result = service.filter(cameras, CameraFilters(province="Valencia", road="A-3"))

    assert len(result) == 1
    assert result[0].id == "cam-b"


def test_camera_filter_skips_when_only_province_set_and_does_not_match():
    repo = FakeCameraRepo([Camera(id="cam-x", road="A-3", province="Madrid", km="10")])
    service = CameraService(repo, TtlCache(60))
    cameras = service.get_all()

    result = service.filter(cameras, CameraFilters(province="Sevilla"))

    assert result == []


def test_camera_filter_skips_when_only_road_set_and_does_not_match():
    repo = FakeCameraRepo([Camera(id="cam-x", road="A-3", province="Madrid", km="10")])
    service = CameraService(repo, TtlCache(60))
    cameras = service.get_all()

    result = service.filter(cameras, CameraFilters(road="AP-9"))

    assert result == []


def test_annotate_coverage_skips_camera_with_different_province():
    incident = Incident(id="i1", road="A-3", province="Madrid", km="10",
                        latitude=40.4168, longitude=-3.7038)
    camera_same = Camera(id="c1", road="A-3", province="Madrid", km="10")
    camera_other = Camera(id="c2", road="A-3", province="Barcelona", km="10")

    repo = FakeCameraRepo([camera_same, camera_other])
    service = CameraService(repo, TtlCache(60))
    annotated = service.annotate_coverage([incident], [camera_same, camera_other])

    assert annotated[0].camera_coverage_count == 1
    assert annotated[0].has_camera_coverage is True
