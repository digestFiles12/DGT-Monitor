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
) -> dict:
    return service.get_cameras(CameraFilters(province, road, km, lat, lon, None if all else limit, max_km_delta))