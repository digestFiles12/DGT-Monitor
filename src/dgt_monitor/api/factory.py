"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from dgt_monitor.api.routes import activity, cameras, health, incidents, stats
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.bootstrap import build_application
from dgt_monitor.core.exceptions import DgtError


def create_app(service: DgtApplicationService | None = None) -> FastAPI:
    app = FastAPI(title="DGT Monitor API", version="0.1.0")
    app.state.dgt_service = service or build_application()
    static_dir = Path(__file__).resolve().parents[1] / "web" / "static"
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], allow_credentials=False,
        allow_methods=["*"], allow_headers=["*"],
    )

    @app.exception_handler(DgtError)
    async def handle_dgt_error(_request: Request, exc: DgtError) -> JSONResponse:
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    app.include_router(health.router)
    app.include_router(incidents.router)
    app.include_router(stats.router)
    app.include_router(cameras.router)
    app.include_router(activity.router)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def dashboard() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    @app.get("/manifest.webmanifest", include_in_schema=False)
    async def manifest() -> FileResponse:
        return FileResponse(static_dir / "manifest.webmanifest", media_type="application/manifest+json")

    @app.get("/sw.js", include_in_schema=False)
    async def service_worker() -> FileResponse:
        return FileResponse(static_dir / "sw.js", media_type="application/javascript")

    return app