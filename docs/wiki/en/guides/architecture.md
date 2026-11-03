# Architecture

DGT-Monitor separates the domain, data adapters, and use cases. The runtime package is under `src/dgt_monitor/` and is organized into `core`, `infrastructure`, `application`, `api`, `web`, and `gui`; the console menu is in `menu.py`.

## Components

- `core/` contains models, ports, domain utilities, localization, and province-to-autonomous-community mapping.
- `infrastructure/` implements HTTP access, DATEX II repositories and parsers, the in-memory cache, and SQLite stores.
- `application/` coordinates incident and camera services, the shared facade, and statistics calculations.
- `api/` adapts use cases to FastAPI. `web/` contains the ASGI application and the dashboard's static assets.
- `gui/` provides the PyQt6 desktop interface; `menu.py` implements the console menu for generating and exploring statistics.

The ASGI entry point is `dgt_monitor.web.app:app`. `bootstrap.build_application()` wires repositories, parsers, caches, and storage. The `create_app(service=...)` factory accepts an already-built facade, for example in tests.

## Data flow

Repositories retrieve DGT XML and parsers convert it into domain models. `IncidentService` applies caching and persists incidents when storage is available. The facade supplies data to the API and GUI; `application.statistics` builds groupings and statistics also consumed by the dashboard's charts tab.

Camera coverage is calculated by the application: it compares normalized road names, compatible provinces, and kilometer-point distance. It is not a relationship supplied by the XML.

## Diagram

The [architecture and flow diagram](../diagrams.md) documents the layers, data paths, and deployment. It is linked here instead of duplicating its content.

See also [Models](models.md) and [Services](services.md).
