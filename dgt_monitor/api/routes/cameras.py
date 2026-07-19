from typing import Annotated

from fastapi import APIRouter, Depends, Query

from dgt_monitor.api.dependencies import get_service
from dgt_monitor.application.facade import DgtApplicationService
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
    max_km_delta: float = Query(1.0, ge=0.1, le=20),
    max_distance_km: float | None = Query(None, ge=1, le=100),
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
    ))