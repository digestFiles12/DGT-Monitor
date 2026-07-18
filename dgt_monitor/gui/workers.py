"""Background workers used by the desktop adapter."""

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.models import IncidentFilters


class IncidentLoadWorker(QObject):
    loaded = pyqtSignal(object)
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, service: DgtApplicationService, filters: IncidentFilters) -> None:
        super().__init__()
        self._service = service
        self._filters = filters

    @pyqtSlot()
    def run(self) -> None:
        try:
            self.loaded.emit(self._service.get_incident_payload(self._filters))
        except Exception as exc:
            self.error.emit(str(exc))
        finally:
            self.finished.emit()