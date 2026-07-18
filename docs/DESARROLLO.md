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

## Flujo GitKraken

Publica commits pequenos, revisa el diff y crea un pull request hacia `main` cuando todas las validaciones esten verdes.

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
