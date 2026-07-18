"""ASGI entry point kept stable for Render and local development."""

from dgt_monitor.api.factory import create_app

app = create_app()