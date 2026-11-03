from dataclasses import replace

from dgt_monitor.core.models import Incident
from dgt_monitor.infrastructure.incident_store import SqliteIncidentStore


def test_save_inserts_incidents(tmp_path):
    store = SqliteIncidentStore(tmp_path / "incidents.db")
    incidents = [Incident(id="situation-1", road="A-1"), Incident(id="situation-2")]

    result = store.save(incidents)

    assert result.inserted == 2
    assert result.updated == 0
    assert store.count() == 2


def test_saving_same_incident_updates_without_duplicates_and_preserves_first_seen(tmp_path):
    store = SqliteIncidentStore(tmp_path / "incidents.db")
    original = Incident(id="situation-1", road="A-1")
    store.save([original])
    connection = store._connect()
    try:
        first_seen = connection.execute(
            "SELECT first_seen FROM incidents WHERE id = ?", (original.id,)
        ).fetchone()[0]
    finally:
        connection.close()

    changed = replace(original, road="A-2")
    result = store.save([changed])

    assert result.inserted == 0
    assert result.updated == 1
    assert store.count() == 1
    assert store.load_all() == [changed]
    connection = store._connect()
    try:
        row = connection.execute(
            "SELECT first_seen, last_seen FROM incidents WHERE id = ?", (original.id,)
        ).fetchone()
    finally:
        connection.close()
    assert row["first_seen"] == first_seen
    assert row["last_seen"] >= first_seen


def test_load_all_round_trips_incidents(tmp_path):
    store = SqliteIncidentStore(tmp_path / "nested" / "incidents.db")
    incidents = [
        Incident(id="situation-1", road="A-1", latitude=40.2, has_camera_coverage=True),
        Incident(id="situation-2", cause="roadworks"),
    ]

    store.save(incidents)

    assert store.load_all() == incidents


def test_save_skips_incidents_without_an_id(tmp_path):
    store = SqliteIncidentStore(tmp_path / "incidents.db")

    result = store.save([Incident(id=""), Incident(id="situation-1")])

    assert result.inserted == 1
    assert result.updated == 0
    assert store.count() == 1
