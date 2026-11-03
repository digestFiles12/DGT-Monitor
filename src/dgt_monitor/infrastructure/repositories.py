"""DGT repository adapters."""

from dgt_monitor.core.constants import DGT_CAMERAS_URL, DGT_INCIDENTS_URL
from dgt_monitor.core.models import Camera, Incident
from dgt_monitor.core.ports import XmlClient
from dgt_monitor.infrastructure.parsers.camera import CameraParser
from dgt_monitor.infrastructure.parsers.incident import IncidentParser


class DgtIncidentRepository:
    def __init__(self, client: XmlClient, parser: IncidentParser, url: str = DGT_INCIDENTS_URL) -> None:
        self._client, self._parser, self._url = client, parser, url

    def fetch(self) -> list[Incident]:
        return self._parser.parse(self._client.get(self._url))


class DgtCameraRepository:
    def __init__(self, client: XmlClient, parser: CameraParser, url: str = DGT_CAMERAS_URL) -> None:
        self._client, self._parser, self._url = client, parser, url

    def fetch(self) -> list[Camera]:
        return self._parser.parse(self._client.get(self._url))