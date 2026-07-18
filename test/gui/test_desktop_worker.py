from PyQt6.QtTest import QSignalSpy

from dgt_monitor.core.models import IncidentFilters
from dgt_monitor.gui.workers import IncidentLoadWorker


class FakeService:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error

    def get_incident_payload(self, filters: IncidentFilters) -> dict:
        if self.error:
            raise self.error
        return {"count": 1, "items": [{"province": filters.province}], "stats": {"total": 1}}


def test_incident_worker_emits_payload():
    worker = IncidentLoadWorker(FakeService(), IncidentFilters(province="Madrid"))
    loaded = QSignalSpy(worker.loaded)
    finished = QSignalSpy(worker.finished)

    worker.run()

    assert loaded[0][0]["items"][0]["province"] == "Madrid"
    assert len(finished) == 1


def test_incident_worker_emits_error_and_finishes():
    worker = IncidentLoadWorker(FakeService(RuntimeError("offline")), IncidentFilters())
    errors = QSignalSpy(worker.error)
    finished = QSignalSpy(worker.finished)

    worker.run()

    assert errors[0][0] == "offline"
    assert len(finished) == 1