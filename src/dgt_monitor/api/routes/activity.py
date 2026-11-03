"""Activity log API endpoints."""

import asyncio
import json
import os
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.responses import StreamingResponse

from dgt_monitor.core import activity

router = APIRouter(prefix="/api/activity", tags=["activity"])


def _split_env(env_var: str) -> set[str]:
    """Parse comma-separated environment variable."""
    value = os.getenv(env_var, "")
    return {k.strip() for k in value.split(",") if k.strip()}


def _require_api_key(x_api_key: Annotated[str | None, Header()] = None) -> str:
    """Validate API key using constant-time comparison."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")
    
    # Check revocation list first (fail-fast)
    revoked_keys = _split_env("ACTIVITY_REVOKED_API_KEYS")
    if x_api_key in revoked_keys:
        raise HTTPException(status_code=401, detail="API key revoked")
    
    # Check acceptance list with constant-time comparison
    valid_keys = _split_env("ACTIVITY_API_KEYS")
    legacy_key = os.getenv("ACTIVITY_API_KEY")
    
    if legacy_key and secrets.compare_digest(x_api_key, legacy_key):
        return x_api_key
    
    # Check against acceptance list
    for valid_key in valid_keys:
        if secrets.compare_digest(x_api_key, valid_key):
            return x_api_key
    
    raise HTTPException(status_code=401, detail="Invalid API key")


@router.get("/")
async def list_activity(
    _: str = Depends(_require_api_key),
    level: str | None = None,
    source: str | None = None,
    event_type: str | None = None,
    user: str | None = None,
    start_ts: str | None = None,
    end_ts: str | None = None,
    offset: int = 0,
    limit: int = 100
):
    """List activity log entries with optional filtering and pagination."""
    if limit < 1 or limit > 1000:
        limit = 100
    
    entries = activity.get_entries()
    
    # Apply filters
    if level:
        entries = [e for e in entries if e.get("level") == level]
    if source:
        entries = [e for e in entries if e.get("source") == source]
    if event_type:
        entries = [e for e in entries if e.get("event_type") == event_type]
    if user:
        entries = [e for e in entries if e.get("user") == user]
    
    # Apply pagination
    total = len(entries)
    entries = entries[offset:offset + limit]
    
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "entries": entries
    }


@router.get("/csv")
async def export_csv(_: str = Depends(_require_api_key)):
    """Export activity log as CSV."""
    entries = activity.get_entries()
    
    # Build CSV content
    lines = ["timestamp,level,source,event_type,user,message"]
    for entry in entries:
        row = [
            entry.get("timestamp", ""),
            entry.get("level", ""),
            entry.get("source", ""),
            entry.get("event_type", ""),
            entry.get("user", ""),
            entry.get("message", "")
        ]
        # Escape quotes and wrap in quotes if contains comma
        row = [f'"{v.replace('"', '""')}"' if "," in v else v for v in row]
        lines.append(",".join(row))
    
    content = "\n".join(lines)
    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=activity.csv"}
    )


@router.get("/stream")
async def stream_activity(_: str = Depends(_require_api_key), replay: int = 0, once: bool = False):
    """Stream activity log as Server-Sent Events."""
    async def event_generator():
        entries = activity.get_entries()
        cursor = max(0, len(entries) - replay) if replay > 0 else len(entries)
        
        # Yield existing entries if replay requested
        for i in range(cursor, len(entries)):
            entry = entries[i]
            data = json.dumps(entry)
            yield f"id: {i}\nevent: activity\ndata: {data}\n\n"
        cursor = len(entries)
        
        if once:
            return
        
        # Continue streaming new entries
        while True:
            await asyncio.sleep(0.5)
            new_entries = activity.get_entries()
            if cursor > len(new_entries):
                cursor = 0
            while cursor < len(new_entries):
                entry = new_entries[cursor]
                data = json.dumps(entry)
                yield f"id: {cursor}\nevent: activity\ndata: {data}\n\n"
                cursor += 1
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )


@router.post("/clear")
async def clear_activity(_: str = Depends(_require_api_key)):
    """Clear all activity log entries."""
    activity.clear()
    return {"status": "cleared"}
