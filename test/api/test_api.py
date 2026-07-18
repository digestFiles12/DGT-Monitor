from fastapi.testclient import TestClient

from dgt_monitor.api.factory import create_app


class FakeService:
    def get_incident_payload(self, filters, refresh=False):
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 1, "stats": {"total": 1}, "items": [{"id": "sit-1", "province": filters.province}]}

    def get_cameras(self, filters, refresh=False):
        return {"updated_at": "2026-07-18T00:00:00+00:00", "count": 1, "items": [{"id": "cam-1", "limit": filters.limit}]}


def test_health_and_rest_contracts():
    client = TestClient(create_app(FakeService()))

    assert client.get("/api/health").json()["status"] == "ok"
    assert client.get("/api/incidents", params={"province": "Madrid"}).json()["items"][0]["province"] == "Madrid"
    assert client.get("/api/cameras", params={"limit": 5}).json()["items"][0]["limit"] == 5


def test_websocket_sends_filtered_payload():
    client = TestClient(create_app(FakeService()))
    with client.websocket_connect("/ws/incidents?province=Madrid&interval=5") as websocket:
        payload = websocket.receive_json()

    assert payload["transport"] == "websocket"
    assert payload["refresh_interval_seconds"] == 5
    assert payload["items"][0]["province"] == "Madrid"