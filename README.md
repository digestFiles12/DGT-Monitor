# DGT Monitor

Aplicacion modular para consultar incidencias y camaras de trafico de la DGT desde un dashboard FastAPI/PWA y una GUI PyQt6. El sistema esta reimplementado con arquitectura por capas: dominio tipado, infraestructura DATEX2/cache, servicios de aplicacion, API, dashboard web y escritorio.

El dashboard incluye selector ES/EN, modo claro/oscuro, filtros por provincia, municipio, carretera, severidad, tipo, cobertura de camara y modo de busqueda (`contains`, `exact`, `regex`). La pestaña de camaras puede mostrar todas las camaras filtradas o solo las que cubren alguna incidencia activa mediante `incident_coverage=true`. El mapa reutiliza los mismos filtros y calcula el total combinado de incidencias y camaras visibles.

La cobertura incidencia-camara se calcula por carretera normalizada, provincia compatible y punto kilometrico dentro de `CAMERA_MATCH_RANGE_KM = 2.0`. El dashboard mantiene scroll general en movil/escritorio y scroll interno en tabla de incidencias y grid de camaras, de modo que la navegacion funciona tanto por pagina completa como dentro de cada superficie densa.

Consulta [docs/INDEX.md](docs/INDEX.md) para la documentacion tecnica completa, [CHANGELOG.md](CHANGELOG.md) para el historial de cambios y [docs/HANDOFF.md](docs/HANDOFF.md) para reanudar el trabajo en otro chat. El flujo de ramas esta definido en [docs/GITFLOW.md](docs/GITFLOW.md).

## Funcionalidades principales

- API FastAPI con REST, WebSocket, Activity API, SSE y export CSV.
- Dashboard web/PWA servido desde `/`, con assets versionados y service worker sin cachear respuestas `/api/`.
- GUI PyQt6 local con workers en `QThread`, dialogos no modales de camaras e imagenes asincronas.
- Filtros compartidos por API, dashboard y servicios mediante `IncidentFilters` y `CameraFilters`.
- Busqueda textual por contiene, exacta o regex insensible a mayusculas.
- Cobertura de camaras anotada en incidencias y filtro inverso de camaras con incidencia.
- Pruebas hermeticas sin depender de la DGT real.

## Desarrollo

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest
```

## Ejecución

```powershell
# Dashboard web
.\.venv\Scripts\python.exe -m uvicorn dgt_monitor.web.app:app --reload

# Menu de consola (proyecto final): descarga el XML, genera grouped_incidents.json y muestra el menu
.\.venv\Scripts\python.exe -m dgt_monitor.menu
# Sin conexion, con un XML local
.\.venv\Scripts\python.exe -m dgt_monitor.menu --xml tests\fixtures\incidents_sample.xml

# Aplicación de escritorio
.\.venv\Scripts\python.exe -m dgt_monitor.gui
```

## API rapida

```powershell
# Incidencias por carretera exacta
Invoke-RestMethod "http://127.0.0.1:8000/api/incidents?road=A-52&match_mode=exact"

# Incidencias por regex
Invoke-RestMethod "http://127.0.0.1:8000/api/incidents?road=^A-\d+$&match_mode=regex"

# Camaras asociadas a incidencias activas
Invoke-RestMethod "http://127.0.0.1:8000/api/cameras?road=A-52&incident_coverage=true"
```

## Validacion rapida

```powershell
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```

Estado validado el 2026-07-19: 53 tests pasando, compilacion limpia y checks de GitHub Actions en verde. La release actual publicada es `20260719.06`, promocionada desde `release` a `main` mediante PR #13.
