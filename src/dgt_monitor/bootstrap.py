"""Dependency composition for production adapters."""

import logging

from dgt_monitor.application.cameras import CameraService
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.application.incidents import IncidentService
from dgt_monitor.core import activity
from dgt_monitor.core.constants import CAMERA_CACHE_SECONDS, INCIDENT_CACHE_SECONDS
from dgt_monitor.core.models import Camera, Incident
from dgt_monitor.infrastructure.activity_store import build_activity_store
from dgt_monitor.infrastructure.cache import TtlCache
from dgt_monitor.infrastructure.http import RequestsXmlClient
from dgt_monitor.infrastructure.incident_store import build_incident_store
from dgt_monitor.infrastructure.parsers import CameraParser, IncidentParser
from dgt_monitor.infrastructure.repositories import DgtCameraRepository, DgtIncidentRepository

logger = logging.getLogger(__name__)


def build_activity_store_and_init():
    """Build and initialize the activity store."""
    store = build_activity_store()
    activity.set_store(store)
    return store


def build_application() -> DgtApplicationService:
    build_activity_store_and_init()
    client = RequestsXmlClient()
    incident_repository = DgtIncidentRepository(client, IncidentParser())
    camera_repository = DgtCameraRepository(client, CameraParser())
    try:
        incident_store = build_incident_store()
    except Exception:
        logger.exception("Could not initialize incident storage; continuing without persistence")
        incident_store = None
    incident_service = IncidentService(
        incident_repository,
        TtlCache[list[Incident]](INCIDENT_CACHE_SECONDS),
        store=incident_store,
    )
    camera_service = CameraService(camera_repository, TtlCache[list[Camera]](CAMERA_CACHE_SECONDS))
    return DgtApplicationService(incident_service, camera_service)