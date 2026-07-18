"""Tests for activity log API endpoints."""

import pytest
from fastapi.testclient import TestClient

from dgt_monitor.api.factory import create_app
from dgt_monitor.core.activity import record


@pytest.fixture
def client(tmp_path, monkeypatch):
    """FastAPI test client with activity store initialized."""
    # Set activity DB path for this test
    db_path = tmp_path / "activity.db"
    monkeypatch.setenv("ACTIVITY_DB_PATH", str(db_path))
    monkeypatch.setenv("ACTIVITY_API_KEYS", "test-key-1,test-key-2")
    monkeypatch.setenv("ACTIVITY_REVOKED_API_KEYS", "revoked-key")
    
    # Create app and client
    app = create_app(service=None)  # Tests don't need a service for activity endpoints
    return TestClient(app)


def test_activity_requires_api_key(client):
    """Verify activity endpoint requires valid API key."""
    # Missing key
    response = client.get("/api/activity/")
    assert response.status_code == 401
    
    # Wrong key
    response = client.get("/api/activity/", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_activity_revoked_key_rejected(client):
    """Verify revoked API keys are rejected."""
    response = client.get("/api/activity/", headers={"X-API-Key": "revoked-key"})
    assert response.status_code == 401


def test_activity_list_with_valid_key(client):
    """Verify activity list returns entries with valid key."""
    # Record some entries
    record({"level": "info", "source": "test", "message": "Entry 1"})
    record({"level": "warning", "source": "test", "message": "Entry 2"})
    
    # Fetch with valid key
    response = client.get("/api/activity/", headers={"X-API-Key": "test-key-1"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 2
    assert len(data["entries"]) >= 2


def test_activity_list_filtering(client):
    """Verify activity list filtering by level and source."""
    # Record entries with different levels
    record({"level": "info", "source": "gui", "message": "Info msg"})
    record({"level": "warning", "source": "api", "message": "Warning msg"})
    record({"level": "error", "source": "gui", "message": "Error msg"})
    
    headers = {"X-API-Key": "test-key-1"}
    
    # Filter by level
    response = client.get("/api/activity/?level=error", headers=headers)
    assert response.status_code == 200
    data = response.json()["entries"]
    assert all(entry["level"] == "error" for entry in data)
    
    # Filter by source
    response = client.get("/api/activity/?source=gui", headers=headers)
    assert response.status_code == 200
    data = response.json()["entries"]
    assert all(entry["source"] == "gui" for entry in data)


def test_activity_csv_export(client):
    """Verify CSV export includes header and entries."""
    record({"level": "info", "source": "test", "message": "CSV test"})
    
    response = client.get("/api/activity/csv", headers={"X-API-Key": "test-key-1"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    
    # Check header is present
    content = response.text
    assert "timestamp" in content
    assert "level" in content
    assert "source" in content


def test_activity_clear(client):
    """Verify activity clear endpoint removes all entries."""
    record({"level": "info", "source": "test", "message": "To clear"})
    
    # Verify entry exists
    response = client.get("/api/activity/", headers={"X-API-Key": "test-key-1"})
    assert response.json()["total"] > 0
    
    # Clear
    response = client.post("/api/activity/clear", headers={"X-API-Key": "test-key-1"})
    assert response.status_code == 200
    
    # Verify cleared
    response = client.get("/api/activity/", headers={"X-API-Key": "test-key-1"})
    assert response.json()["total"] == 0


def test_activity_sse_stream(client):
    """Verify SSE streaming endpoint returns proper format."""
    record({"level": "info", "source": "test", "message": "Stream test"})
    
    response = client.get(
        "/api/activity/stream?replay=1&once=true",
        headers={"X-API-Key": "test-key-1"},
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    # Content should have SSE format
    content = response.text
    assert "event: activity" in content or "data:" in content
