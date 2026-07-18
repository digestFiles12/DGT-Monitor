from typing import cast

from fastapi.testclient import TestClient

from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.api.factory import create_app
from dgt_monitor.core.models import IncidentFilters


class FakeService:
    def __init__(self):
        self.last_filters: IncidentFilters | None = None
        self.last_language: str | None = None

    def get_incident_payload(self, filters, refresh=False, language="es"):
        self.last_filters = filters
        self.last_language = language
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 1, "language": language, "stats": {"total": 1}, "items": [{"id": "sit-1", "province": filters.province}]}

    def get_cameras(self, filters, refresh=False):
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 1, "items": [{"id": "cam-1", "limit": filters.limit}]}


def service() -> DgtApplicationService:
    return cast(DgtApplicationService, FakeService())


def test_health_and_rest_contracts():
    fake = FakeService()
    client = TestClient(create_app(cast(DgtApplicationService, fake)))

    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/api/incidents", params={"province": "Madrid"}).json()["items"][0]["province"] == "Madrid"
    client.get("/api/incidents", params={"kind": "weather", "camera": "with", "lang": "en"})
    assert fake.last_filters is not None
    assert fake.last_filters.kind == "weather"
    assert fake.last_filters.camera == "with"
    assert fake.last_language == "en"
    assert client.get("/api/cameras", params={"limit": 5}).json()["items"][0]["limit"] == 5


def test_dashboard_and_pwa_assets_are_served():
    client = TestClient(create_app(service()))

    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert "DGT Monitor" in dashboard.text
    assert "themeButton" in dashboard.text
    assert "language-button" in dashboard.text
    assert "data-language=\"en\"" in dashboard.text
    assert "statStuck" in dashboard.text
    assert "statWeather" in dashboard.text
    assert "cameraCoverageFilter" in dashboard.text
    styles = client.get("/static/styles.css")
    assert styles.status_code == 200
    assert ':root[data-theme="dark"]' in styles.text
    assert ".image-viewer" in styles.text
    assert ".image-viewer-frame" in styles.text
    assert ".image-viewer-fallback" in styles.text
    assert ".incident-detail-panel" in styles.text
    assert ".coverage-menu" in styles.text
    app_js = client.get("/static/app.js")
    assert app_js.status_code == 200
    assert "dgt-monitor-theme" in app_js.text
    assert "dgt-monitor-language" in app_js.text
    assert "applyLanguage" in app_js.text
    assert "openCameraViewer" in app_js.text
    assert "openIncidentCameras" in app_js.text
    assert "camera-off" in app_js.text
    assert "disconnectedFallback" in app_js.text
    assert "isUnavailableCameraImage" in app_js.text
    assert "createIncidentDetailRow" in app_js.text
    assert "formatHumanDateTime" in app_js.text
    assert "detailLabels" in app_js.text
    assert client.get("/manifest.webmanifest").headers["content-type"].startswith("application/manifest+json")
    service_worker = client.get("/sw.js")
    assert service_worker.status_code == 200
    assert "dgt-monitor-v16" in service_worker.text


def test_websocket_sends_filtered_payload():
    client = TestClient(create_app(service()))
    with client.websocket_connect("/ws/incidents?province=Madrid&interval=5") as websocket:
        payload = websocket.receive_json()

    assert payload["transport"] == "websocket"
    assert payload["refresh_interval_seconds"] == 5
    assert payload["items"][0]["province"] == "Madrid"