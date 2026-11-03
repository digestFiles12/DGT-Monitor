"""Statistics endpoints: indicators grouped by province or region."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends

from dgt_monitor.api.dependencies import get_service
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.regions import PROVINCE_TO_REGION

router = APIRouter(tags=["statistics"])


@router.get("/api/stats")
def stats(
    service: Annotated[DgtApplicationService, Depends(get_service)],
    level: Literal["province", "region"] = "province",
    refresh: bool = False,
) -> dict:
    """Indicators per province or region, with the maximum and minimum of each one."""
    return service.get_statistics(level=level, refresh=refresh)


@router.get("/api/stats/grouped")
def grouped(
    service: Annotated[DgtApplicationService, Depends(get_service)],
    refresh: bool = False,
) -> dict:
    """Full grouped JSON: by province, region, type and weekday."""
    return service.get_grouped_incidents(refresh=refresh)

@router.get("/api/regions")
def regions() -> dict:
    """Autonomous communities with their provinces, used to populate filters."""
    mapping: dict[str, list[str]] = {}
    for province, region in PROVINCE_TO_REGION.items():
        mapping.setdefault(region, []).append(province)
    return {"regions": [{"name": name, "provinces": sorted(items)} for name, items in sorted(mapping.items())]}
