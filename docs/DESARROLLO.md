# Desarrollo

## Requisitos

- Python 3.12
- Git y GitKraken

## Entorno

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Flujo GitKraken

El desarrollo se realiza en `feature/initial-oop-architecture`. Publica commits pequenos, revisa el diff y crea un pull request hacia `main` cuando todas las validaciones esten verdes.
