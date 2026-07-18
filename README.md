# DGT Monitor

Aplicacion modular para consultar incidentes y camaras de trafico de la DGT desde una GUI PyQt6 y un dashboard FastAPI/PWA. El dashboard incluye selector ES/EN, modo claro/oscuro, filtros completos, celdas estadisticas clicables, detalle desplegable de incidencias, acceso a camaras cercanas y visor modal con fallback localizado cuando una imagen no esta disponible.

El proyecto esta siendo implementado desde cero con arquitectura orientada a objetos. Consulta [docs/INDEX.md](docs/INDEX.md) para ver el plan y la documentacion tecnica. Para reanudar el trabajo en otro chat, empieza por [docs/CONTINUIDAD_NUEVO_CHAT.md](docs/CONTINUIDAD_NUEVO_CHAT.md). El flujo de ramas esta definido en [docs/GITFLOW.md](docs/GITFLOW.md).

## Desarrollo

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```

## Ejecución

```powershell
# Dashboard web
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --reload

# Aplicación de escritorio
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```

## Validacion rapida

```powershell
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest test -q
.\.venv\Scripts\python.exe -m compileall -q dgt_monitor dashboard
git diff --check
```
