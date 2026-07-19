# Changelog

Todos los cambios relevantes del proyecto se documentan aqui. El repositorio sigue GitFlow: las features entran en `develop`, se estabilizan en `release` y se publican desde `main`.

## 2026-07-19 - Dashboard, filtros avanzados y cobertura de camaras

### Aniadido

- Selector de modo de busqueda en el dashboard: `contains`, `exact` y `regex`.
- Parametro `match_mode` en `/api/incidents`, `/api/cameras` y `/ws/incidents`.
- Filtro de camaras `incident_coverage=true` para mostrar solo camaras relacionadas con incidencias activas.
- Campo `match_mode` en `IncidentFilters` y `CameraFilters`.
- Utilidad `matches_text()` con busqueda por contiene, coincidencia exacta y expresion regular insensible a mayusculas.
- Conteos relacionados en tabs: al filtrar incidencias se actualizan las camaras relevantes y el total del mapa.
- Documentacion del flujo GitFlow y verificacion de PRs.

### Cambiado

- La cobertura entre incidencias y camaras usa `CAMERA_MATCH_RANGE_KM = 2.0` como rango compartido por dominio, servicios y API.
- El filtro de camaras por cobertura se aplica antes del limite y despues reaplica `limit`, evitando que una camara valida quede fuera por truncado prematuro.
- El dashboard recupera scroll general en movil y escritorio, manteniendo scroll interno en tabla de incidencias y grid de camaras.
- El mapa usa el mismo modo de busqueda y los mismos criterios que los tabs para calcular camaras e incidencias visibles.
- El service worker y assets del dashboard se versionan como `dgt-monitor-v51`.

### Corregido

- Error de sintaxis en `dgt_monitor/api/routes/cameras.py` tras un merge remoto de la PR #9.
- Desalineacion entre conteos de incidencias, camaras y mapa en filtros de carretera/provincia/municipio.
- Casos en los que las camaras cercanas no aparecian por una ventana de punto kilometrico demasiado estrecha.
- Experiencia de scroll de la seccion de camaras y scroll general de pagina.

### Validacion

- `python -m pytest test -q`: 53 tests pasando.
- `python -m compileall -q dgt_monitor dashboard`: sin errores.
- `git diff --check`: limpio.
- PR #9 hacia `develop`: checks `Test & Validate (3.12)` en `SUCCESS` y PR mergeable antes de su integracion.

## 2026-07-18 - Arquitectura modular, API/PWA, GUI y Activity API

### Aniadido

- Arquitectura por capas: `core`, `infrastructure`, `application`, `api`, `dashboard` y `gui`.
- Modelos de dominio tipados para incidencias, camaras, filtros y estadisticas.
- Parsers DATEX2 hermeticos para incidencias y camaras.
- Cache TTL segura para hilos con cargas por clave y copias profundas.
- API FastAPI con healthcheck, incidencias, camaras, WebSocket, Activity API, SSE y export CSV.
- Dashboard web/PWA servido desde `/`, con modo claro/oscuro, selector ES/EN, detalle desplegable, visor de camaras y fallback localizado.
- GUI PyQt6 modular con workers en `QThread`, filtros, estadisticas, tabla, detalle, dialogo no modal de camaras y visor fullscreen.
- Despliegue Render mediante `render.yaml` y CI con GitHub Actions.

### Validacion

- Suite automatizada hermetica sin dependencias de la DGT real.
- Pruebas offscreen para GUI con `QT_QPA_PLATFORM=offscreen`.
