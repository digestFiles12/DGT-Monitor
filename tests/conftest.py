"""Pytest configuration and shared fixtures."""

import pytest

from dgt_monitor.core import activity
from dgt_monitor.infrastructure.activity_store import build_activity_store


@pytest.fixture(autouse=True)
def isolated_incident_db(monkeypatch, tmp_path):
    """Keep the incident SQLite file out of the project directory during tests."""
    monkeypatch.setenv("INCIDENT_DB_PATH", str(tmp_path / "incidents.db"))


@pytest.fixture(autouse=True)
def init_activity_store(monkeypatch):
    """Initialize activity store for each test.
    
    Also reinitialize if ACTIVITY_DB_PATH changes during test.
    """
    # Initial setup
    store = build_activity_store()
    activity.set_store(store)
    
    # Wrap monkeypatch.setenv to reinit store on ACTIVITY_DB_PATH changes
    original_setenv = monkeypatch.setenv
    def setenv_with_store_reinit(name, value):
        original_setenv(name, value)
        if name == "ACTIVITY_DB_PATH":
            try:
                new_store = build_activity_store()
                activity.set_store(new_store)
            except ValueError:
                # Expected error for relative paths in some tests
                pass
    monkeypatch.setenv = setenv_with_store_reinit
    
    yield
    if hasattr(store, 'clear'):
        store.clear()
