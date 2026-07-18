"""Tests for PWA routes and static assets."""
import json

from fastapi.testclient import TestClient

from dgt_monitor.api.factory import create_app


class FakeService:
    def get_incident_payload(self, filters, refresh=False):
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 0, "stats": {}, "items": []}

    def get_cameras(self, filters, refresh=False):
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 0, "items": []}


def _client():
    return TestClient(create_app(FakeService()))


def test_index_returns_html():
    resp = _client().get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert b"DGT Monitor" in resp.content


def test_manifest_is_valid_json():
    resp = _client().get("/manifest.webmanifest")
    assert resp.status_code == 200
    assert "manifest" in resp.headers["content-type"]
    data = json.loads(resp.content)
    assert data["name"] == "DGT Monitor"
    assert isinstance(data["icons"], list)
    assert len(data["icons"]) >= 1


def test_service_worker_is_javascript():
    resp = _client().get("/sw.js")
    assert resp.status_code == 200
    assert "javascript" in resp.headers["content-type"]
    assert b"CACHE_NAME" in resp.content


def test_static_css_served():
    resp = _client().get("/static/styles.css")
    assert resp.status_code == 200
    assert "css" in resp.headers["content-type"]


def test_static_js_served():
    resp = _client().get("/static/app.js")
    assert resp.status_code == 200
    assert "javascript" in resp.headers["content-type"]


def test_icons_served():
    client = _client()
    for size in (192, 512):
        resp = client.get(f"/static/icons/icon-{size}.png")
        assert resp.status_code == 200, f"icon-{size}.png not found"
        assert resp.headers["content-type"] == "image/png"
