from pathlib import Path

from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.infrastructure.cache import TtlCache
from dgt_monitor.infrastructure.incident_store import SqliteIncidentStore
from dgt_monitor.infrastructure.parsers import IncidentParser


class FakeIncidentRepository:
    def __init__(self, incidents):
        self._incidents = incidents

    def fetch(self):
        return self._incidents


def test_service_persists_parsed_fixture_without_duplicates(tmp_path):
    fixture_path = Path(__file__).parents[1] / "fixtures" / "incidents_sample.xml"
    incidents = IncidentParser().parse(fixture_path.read_text(encoding="utf-8"))
    store = SqliteIncidentStore(tmp_path / "incidents.db")
    service = IncidentService(
        FakeIncidentRepository(incidents), TtlCache(60), store=store
    )

    first = service.get_all(refresh=True)
    second = service.get_all(refresh=True)

    unique_ids = {incident.id for incident in incidents if incident.id}
    assert first == incidents
    assert second == incidents
    assert store.count() == len(unique_ids)


def test_store_failure_does_not_break_serving_incidents():
    class BrokenStore:
        def save(self, incidents):
            raise OSError("database unavailable")

        def load_all(self):
            return []

        def count(self):
            return 0

    incidents = IncidentParser().parse(
        '<payload><situation id="situation-1"><situationRecord id="record-1" />'
        "</situation></payload>"
    )
    service = IncidentService(
        FakeIncidentRepository(incidents), TtlCache(60), store=BrokenStore()
    )

    assert service.get_all(refresh=True) == incidents
