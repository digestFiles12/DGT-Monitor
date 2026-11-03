# Development

## Requirements

- Python 3.12 or later, as specified by `requires-python` in `pyproject.toml`.
- Git.

## Set up the environment

From the repository root, create a virtual environment and install the development dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

The project uses a `src/` layout; the package is in `src/dgt_monitor`. The `[dev]` extra installs the `[web]`, `[gui]`, and `[console]` extras as well as test dependencies. To install only the optional dependencies for a specific mode, the available extras are `[web]`, `[gui]`, and `[console]`.

## Tests and checks

Run the test suite from the repository root with Qt in headless mode:

```powershell
$env:QT_QPA_PLATFORM='offscreen'
.\.venv\Scripts\python.exe -m pytest tests -q
```

Continuous integration also checks syntax compilation with `compileall`, imports the packages, and checks whitespace changes. In the current workflow, compilation and `git diff --check` are non-blocking checks.

## Run the web application locally

The ASGI entry point is `dgt_monitor.web.app:app`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn dgt_monitor.web.app:app --reload
```

## Related guides

- [Deployment](deployment.md)
- [Git workflow](gitflow.md)
