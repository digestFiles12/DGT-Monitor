"""Application facade consumed by API and GUI adapters."""

from datetime import datetime, timezone
from typing import Any

from dgt_monitor.application.cameras import CameraService
from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.core.models import CameraFilters, IncidentFilters


class DgtApplicationService:
    def __init__(self, incidents: IncidentService, cameras: CameraService) -> None:
        self._incidents = incidents
        self._cameras = cameras

    def get_incident_payload(self, filters: IncidentFilters | None = None, refresh: bool = False) -> dict[str, Any]:
        incident_items = self._incidents.get_all(refresh=refresh)
        camera_items = self._cameras.get_all()
        covered = self._cameras.annotate_coverage(incident_items, camera_items)
        filtered = self._incidents.filter(covered, filters or IncidentFilters())
        return {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "count": len(filtered),
            "stats": self._incidents.stats(filtered).to_dict(),
            "items": [item.to_dict() for item in filtered],
        }

    def get_cameras(self, filters: CameraFilters | None = None, refresh: bool = False) -> dict[str, Any]:
        items = self._cameras.filter(self._cameras.get_all(refresh=refresh), filters or CameraFilters())
        return {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "count": len(items),
            "items": [item.to_dict() for item in items],
        }