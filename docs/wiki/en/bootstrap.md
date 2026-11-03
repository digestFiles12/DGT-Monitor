# dgt_monitor/bootstrap.py
Composes production dependencies to build the main application service. It configures concrete stores, clients, repositories, parsers, and caches.
## Dependencies
Imports services from `application`, activity, constants and models from the core, and adapters from `infrastructure`. The application uses `build_application` as its composition root.
## Contents
### `logger`
- Module logger used to report failures while initializing incident persistence.
### `build_activity_store_and_init()`
- Creates the activity store, registers it in `core.activity`, and returns the instance.
### `build_application() -> DgtApplicationService`
- Initializes activity, creates an HTTP client and DGT repositories, and attempts to build the incident store. If persistence initialization fails, it logs the exception and continues with `store=None`; it creates services with TTL caches and returns `DgtApplicationService`.
