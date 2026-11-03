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
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```

Estado esperado actual: 53 tests pasando. Si se cambia dashboard/API, ejecutar tambien una prueba enfocada de API antes de la suite completa:

```powershell
.\.venv\Scripts\python.exe -m pytest test\api\test_api.py -q
```

Para probar el dashboard/API local:

```powershell
.\.venv\Scripts\python.exe -m uvicorn dgt_monitor.web.app:app --reload
```

Pruebas manuales recomendadas del dashboard:

- Buscar carretera con `contains`, `exact` y `regex`.
- Activar `Incidencia con camara` en la pestana de camaras.
- Comprobar que la pagina completa hace scroll en movil/escritorio y que tabla/grid conservan scroll interno.
- Validar que los contadores de incidencias, camaras y mapa permanecen sincronizados.

Para probar la GUI de escritorio:

```powershell
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```
