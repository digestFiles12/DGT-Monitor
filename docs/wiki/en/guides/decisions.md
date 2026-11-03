# Technical decisions

This guide summarizes decisions reflected in the current implementation. See [Architecture](architecture.md) for component structure and data paths.

## Typed domain models

`Incident`, `Camera`, and filters are represented as dataclasses in `core/models.py`. Their `to_dict()` methods convert models at the output boundary, keeping the domain independent of FastAPI serialization.

## Adapters and composition

Repository and store contracts are defined as protocols in `core/ports.py`; HTTP, parsers, cache, and SQLite are implemented in infrastructure. `bootstrap.build_application()` composes production dependencies, and `create_app(service=...)` accepts an injected facade. Routes call use cases through the facade.

## Cache and storage

The TTL cache keeps recent data in memory and returns deep copies so consumers cannot mutate the stored value. Incidents can also be saved to SQLite through `SqliteIncidentStore`: `id` is the upsert key, `first_seen` is retained, and `last_seen` is updated when the record is received again. `INCIDENT_DB_PATH` controls the path; persistence errors are logged without discarding the downloaded response.

## Geographic normalization and coverage

`core.regions` normalizes province-name variants to resolve autonomous communities, using `Unknown` when there is no match. Camera coverage is calculated in the application using normalized roads, compatible provinces, and a 2 km threshold; DATEX II is not assumed to provide that association.

## Shared statistics

Indicators and groupings are calculated in `application.statistics` and served through the API, dashboard, and console menu. The presentations therefore reuse the same definitions for province, autonomous community, type, and weekday.
