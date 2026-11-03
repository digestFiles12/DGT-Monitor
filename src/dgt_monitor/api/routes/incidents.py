import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from dgt_monitor.api.dependencies import get_service
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.exceptions import DgtError
from dgt_monitor.core.models import IncidentFilters

router = APIRouter(tags=["incidents"])


@router.get("/api/incidents")
def incidents(
    service: Annotated[DgtApplicationService, Depends(get_service)],
    province: str | None = None,
    municipality: str | None = None,
    road: str | None = None,
    severity: str | None = None,
    kind: str | None = None,
    camera: str | None = None,
    match_mode: str = "contains",
    lang: str = "es",
    community: str | None = None,
) -> dict:
    filters = IncidentFilters(province, municipality, road, severity, kind, camera, match_mode, community)
    return service.get_incident_payload(filters, language=lang)


@router.websocket("/ws/incidents")
async def incidents_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    query = websocket.query_params
    interval = max(5, min(int(query.get("interval", "120")), 300))
    filters = IncidentFilters(
        query.get("province"), query.get("municipality"), query.get("road"),
        query.get("severity"), query.get("kind"), query.get("camera"), query.get("match_mode", "contains"), query.get("community"),
    )
    language = query.get("lang", "es")
    service: DgtApplicationService = websocket.app.state.dgt_service
    try:
        while True:
            try:
                payload = await asyncio.to_thread(service.get_incident_payload, filters, False, language)
                payload.update(transport="websocket", refresh_interval_seconds=interval)
                await websocket.send_json(payload)
            except DgtError as exc:
                await websocket.send_json({"error": str(exc)})
            await asyncio.sleep(interval)
    except WebSocketDisconnect:
        return