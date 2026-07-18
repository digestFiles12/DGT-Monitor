"""FastAPI application factory."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from dgt_monitor.api.routes import activity, cameras, health, incidents
from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.bootstrap import build_application
from dgt_monitor.core.exceptions import DgtError


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
    app.include_router(activity.router)
    return app