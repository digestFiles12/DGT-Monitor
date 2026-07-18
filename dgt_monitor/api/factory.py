"""FastAPI application factory."""

import pathlib

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from dgt_monitor.api.routes import cameras, health, incidents
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.bootstrap import build_application
from dgt_monitor.core.exceptions import DgtError

_STATIC_DIR = pathlib.Path(__file__).parent.parent.parent / "dashboard" / "static"


def create_app(service: DgtApplicationService | None = None) -> FastAPI:
    app = FastAPI(title="DGT Monitor API", version="0.1.0")
    app.state.dgt_service = service or build_application()
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
    app.include_router(cameras.router)

    @app.get("/manifest.webmanifest", include_in_schema=False)
    def manifest() -> FileResponse:
        return FileResponse(_STATIC_DIR / "manifest.webmanifest", media_type="application/manifest+json")

    @app.get("/sw.js", include_in_schema=False)
    def service_worker() -> FileResponse:
        return FileResponse(_STATIC_DIR / "sw.js", media_type="application/javascript")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(_STATIC_DIR / "index.html", media_type="text/html")

    app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

    return app