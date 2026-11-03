"""Background workers used by the desktop adapter."""

from collections.abc import Callable

import requests
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.models import CameraFilters, IncidentFilters


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


class CameraLoadWorker(QObject):
    loaded = pyqtSignal(object)
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, service: DgtApplicationService, filters: CameraFilters) -> None:
        super().__init__()
        self._service = service
        self._filters = filters

    @pyqtSlot()
    def run(self) -> None:
        try:
            self.loaded.emit(self._service.get_cameras(self._filters))
        except Exception as exc:
            self.error.emit(str(exc))
        finally:
            self.finished.emit()


class ImageLoadWorker(QObject):
    loaded = pyqtSignal(str, object)
    error = pyqtSignal(str, str)
    finished = pyqtSignal()

    def __init__(self, url: str, downloader: Callable[[str], bytes] | None = None) -> None:
        super().__init__()
        self._url = url
        self._downloader = downloader or self._download

    @pyqtSlot()
    def run(self) -> None:
        try:
            self.loaded.emit(self._url, self._downloader(self._url))
        except Exception as exc:
            self.error.emit(self._url, str(exc))
        finally:
            self.finished.emit()

    @staticmethod
    def _download(url: str) -> bytes:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        return response.content