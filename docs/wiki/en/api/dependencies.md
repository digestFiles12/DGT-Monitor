# dgt_monitor/api/dependencies.py
Provides the FastAPI dependency that retrieves the application service stored on the request state.
## Dependencies
Imports `Request` and `DgtApplicationService`. API routes that need application logic use it with `Depends`.
## Contents
### `get_service(request)`
- Returns `request.app.state.dgt_service`, normally set by `create_app`; if the attribute is absent, access fails at runtime.
