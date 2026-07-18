"""Ports implemented by infrastructure adapters."""

from typing import Protocol, Sequence

from dgt_monitor.core.models import Camera, Incident


class XmlClient(Protocol):
    def get(self, url: str) -> str: ...


class IncidentRepository(Protocol):
    def fetch(self) -> Sequence[Incident]: ...


class CameraRepository(Protocol):
    def fetch(self) -> Sequence[Camera]: ...