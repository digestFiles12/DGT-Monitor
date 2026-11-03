from typing import Annotated

from fastapi import APIRouter, Depends, Query

from dgt_monitor.api.dependencies import get_service
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.constants import CAMERA_MATCH_RANGE_KM
from dgt_monitor.core.models import CameraFilters

router = APIRouter(tags=["cameras"])


@router.get("/api/cameras")
def cameras(
    service: Annotated[DgtApplicationService, Depends(get_service)],
    province: str | None = None,
    road: str | None = None,
    km: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    limit: int = Query(12, ge=1, le=50),
    all: bool = False,
    max_km_delta: float = Query(CAMERA_MATCH_RANGE_KM, ge=0.1, le=20),
    max_distance_km: float | None = Query(None, ge=1, le=100),
    incident_coverage: bool = False,
    match_mode: str = "contains",
) -> dict:
    return service.get_cameras(CameraFilters(
        province=province,
        road=road,
        kilometer=km,
        latitude=lat,
        longitude=lon,
        limit=None if all else limit,
        max_km_delta=max_km_delta,
        max_distance_km=max_distance_km,
        incident_coverage=incident_coverage,
        match_mode=match_mode,
    ))