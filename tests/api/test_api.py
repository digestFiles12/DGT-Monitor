from typing import cast

from fastapi.testclient import TestClient

from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.api.factory import create_app
from dgt_monitor.core.models import CameraFilters, IncidentFilters


class FakeService:
    def __init__(self):
        self.last_filters: IncidentFilters | None = None
        self.last_camera_filters: CameraFilters | None = None
        self.last_language: str | None = None

    def get_incident_payload(self, filters, refresh=False, language="es"):
        self.last_filters = filters
        self.last_language = language
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 1, "language": language, "stats": {"total": 1}, "items": [{"id": "sit-1", "province": filters.province}]}

    def get_cameras(self, filters, refresh=False):
        self.last_camera_filters = filters
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 1, "items": [{"id": "cam-1", "limit": filters.limit, "incident_coverage": filters.incident_coverage}]}


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
    assert client.get("/api/incidents", params={"province": "^Mad", "match_mode": "regex"}).json()["items"][0]["province"] == "^Mad"
    assert fake.last_filters.match_mode == "regex"
    assert client.get("/api/cameras", params={"limit": 5}).json()["items"][0]["limit"] == 5
    assert client.get("/api/cameras", params={"all": "true"}).json()["items"][0]["limit"] is None
    assert client.get("/api/cameras", params={"incident_coverage": "true"}).json()["items"][0]["incident_coverage"] is True
    assert client.get("/api/cameras", params={"road": "^A-", "match_mode": "regex"}).json()["items"][0]["limit"] == 12
    assert fake.last_camera_filters is not None
    assert fake.last_camera_filters.match_mode == "regex"

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
    assert "matchModeFilter" in dashboard.text
    assert "cameraIncidentFilter" in dashboard.text
    assert "favoriteTabCount" in dashboard.text
    assert "data-view=\"favorites\"" in dashboard.text
    assert "data-view=\"charts\"" in dashboard.text
    assert "id=\"chartsView\"" in dashboard.text
    assert "id=\"chartCanvas\"" in dashboard.text
    assert "/static/chart.umd.min.js?v=1" in dashboard.text
    assert "mapResults" in dashboard.text
    assert "filterToggle" in dashboard.text
    assert "pageTitle" not in dashboard.text
    styles = client.get("/static/styles.css")
    assert styles.status_code == 200
    assert ':root[data-theme="dark"]' in styles.text
    assert ".image-viewer" in styles.text
    assert ".image-viewer-frame" in styles.text
    assert ".image-viewer-fallback" in styles.text
    assert ".incident-detail-panel" in styles.text
    assert ".map-window" in styles.text
    assert ".coverage-menu" in styles.text
    assert ".camera-favorite" in styles.text
    assert ".coverage-camera-preview" in styles.text
    assert ".image-viewer-favorite" in styles.text
    chart_js = client.get("/static/chart.umd.min.js")
    assert chart_js.status_code == 200
    assert "4.4.7" in chart_js.text
    app_js = client.get("/static/app.js")
    assert app_js.status_code == 200
    assert "dgt-monitor-theme" in app_js.text
    assert "dgt-monitor-language" in app_js.text
    assert "applyLanguage" in app_js.text
    assert "openCameraViewer" in app_js.text
    assert "openIncidentCameras" in app_js.text
    assert "dgt-monitor-camera-favorites" in app_js.text
    assert "loadChartsData" in app_js.text
    assert "refresh=true" in app_js.text
    assert "renderChart" in app_js.text
    assert "by_weekday" in app_js.text
    assert "by_type" in app_js.text
    assert "obstructions" in app_js.text
    assert "chartSelection" in app_js.text
    assert "toggleCameraFavorite" in app_js.text
    assert "coverage-camera-preview" in app_js.text
    assert "image-viewer-favorite" in app_js.text
    assert "camera-off" in app_js.text
    assert "disconnectedFallback" in app_js.text
    assert "isUnavailableCameraImage" in app_js.text
    assert "createIncidentDetailRow" in app_js.text
    assert "formatHumanDateTime" in app_js.text
    assert "formatDirectionValue" in app_js.text
    assert "detailEntries" in app_js.text
    assert "detailLabels" in app_js.text
    assert "mapCameraScopes" in app_js.text
    assert "updateRelatedTabCounts" in app_js.text
    assert "max_distance_km" in app_js.text
    assert "incident_coverage" in app_js.text
    assert "match_mode" in app_js.text
    assert "requestId" in app_js.text
    assert "document.body.classList.toggle" in app_js.text
    assert "Meteorología" in app_js.text
    assert "Carretera de dirección" in app_js.text
    assert client.get("/manifest.webmanifest").headers["content-type"].startswith("application/manifest+json")
    service_worker = client.get("/sw.js")
    assert service_worker.status_code == 200
    assert "dgt-monitor-v58" in service_worker.text
    assert "/static/app.js?v=58" in service_worker.text
    assert "/static/chart.umd.min.js?v=1" in service_worker.text


def test_websocket_sends_filtered_payload():
    client = TestClient(create_app(service()))
    with client.websocket_connect("/ws/incidents?province=Madrid&interval=5") as websocket:
        payload = websocket.receive_json()

    assert payload["transport"] == "websocket"
    assert payload["refresh_interval_seconds"] == 5
    assert payload["items"][0]["province"] == "Madrid"