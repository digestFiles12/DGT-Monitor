"""FastAPI dependencies."""

from fastapi import Request

from dgt_monitor.application.facade import DgtApplicationService


def get_service(request: Request) -> DgtApplicationService:
    return request.app.state.dgt_service