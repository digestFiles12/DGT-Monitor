# Desarrollo

## Requisitos

- Python 3.12
- Git

## Entorno

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Flujo GitFlow

El repositorio usa GitFlow. Las ramas permanentes son `main` para produccion, `develop` para integracion y `release` para estabilizacion. El trabajo funcional se hace en `feature/<nombre>` desde `develop` y vuelve por pull request. Las entregas se promueven con PR `develop` -> `release` y despues `release` -> `main`.

Consulta [GITFLOW.md](GITFLOW.md) para el detalle de ramas, hotfixes y politica de PRs.

## Validacion local

```powershell
$env:QT_QPA_PLATFORM='offscreen'
.\.venv\Scripts\python.exe -m pytest test -q
.\.venv\Scripts\python.exe -m compileall -q dgt_monitor dashboard
git diff --check
```

Para probar el dashboard/API local:

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --reload
```

Para probar la GUI de escritorio:

```powershell
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```
