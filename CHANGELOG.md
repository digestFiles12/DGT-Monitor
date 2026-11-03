## 2026-11-03 - Seis indicadores en estadísticas

### Cambiado

- Las estadísticas y gráficas usan ahora 6 indicadores: total, accidentes, obras, averías, obstrucciones y meteorología (antes: total, graves, obras, cortes). Son los mismos que las celdas de la pestaña de incidencias.
- Nuevo módulo `core/indicators.py` con las reglas de clasificación, compartido por `IncidentService` y `statistics`.
- Menú de consola con 6 opciones de indicador; salir pasa a la opción 7.
- Service worker y recursos estáticos a la versión 56.

## 2026-11-03 - Gráficas traducidas

### Corregido

- La leyenda del gráfico por tipo mostraba códigos DATEX II sin traducir; ahora usa `labels.by_type` (es/en) de `/api/stats/grouped`.
- El grupo `Unknown` se muestra como `Sin datos` / `Unknown` según el idioma.
- Service worker y recursos estáticos a la versión 55 para invalidar la caché.

## 2026-11-03 - Wiki independiente por idioma

### Añadido

- Wiki en `docs/wiki/es` y `docs/wiki/en` con una página por fichero, guías técnicas y diagramas Mermaid.
- Memoria del proyecto (`docs/MEMORIA.md`).

### Eliminado

- Documentos técnicos antiguos de `docs/` (API, ARCHITECTURE, HANDOFF, PROJECT_STATUS, etc.), integrados y actualizados en la wiki.

## 2026-11-03 - Pestaña de gráficas

### Añadido

- Nueva vista de gráficas con indicadores de incidencias totales, graves, obras y cortes de carretera.
- Gráficas de barras, líneas y circulares por provincia/CCAA, día de la semana y tipo, con extremos y selector de nivel.
- Chart.js local en el shell PWA, gráficos adaptados a los temas claro/oscuro y textos ES/EN.

### Validación

- Tests estáticos de los recursos y controles de la pestaña de gráficas.

# Changelog

Todos los cambios relevantes del proyecto se documentan aqui. El repositorio sigue GitFlow: las features entran en `develop`, se estabilizan en `release` y se publican desde `main`.

## 2026-11-03 - Final project (Project 3)

### Aniadido

- `core/regions.py`: mapa provincia a comunidad autonoma (CCAA) para las 52 provincias.
- `infrastructure/incident_store.py`: persistencia SQLite de incidencias sin duplicados (clave: id de la DGT).
- `application/statistics.py`: 4 indicadores agrupados por provincia, CCAA, tipo y dia de la semana, con maximo y minimo.
- `GET /api/stats` y `GET /api/stats/grouped`.
- `python -m dgt_monitor.menu`: menu de consola con graficas de barras y de queso (ejercicios 1, 2 y 3).
- Estructura `src/` y `tests/`, con fixture XML real en `tests/fixtures`.

## 2026-07-19 - Release 20260719.06 y GUI actualizada

### Aniadido

- Pestaña `Favoritas` en el dashboard para conservar cámaras marcadas aunque las incidencias cambien.
- Estrella amarilla sobre la imagen de cada cámara para marcar/desmarcar favoritos persistidos en `localStorage`.
- Estrella de favoritos tambien en detalle de camara del mapa, visor fullscreen y menu de camaras cercanas de incidencias.
- Miniatura clicable en el menu de camaras de incidencias para abrir la imagen en pantalla completa.
- Modo de busqueda `contains`/`exact`/`regex` disponible tambien en la GUI PyQt6.
- Fechas de detalle en GUI formateadas como fecha/hora humana.
- Pruebas de GUI para modo de busqueda, reseteo de filtros, fechas y click de visor fullscreen.

### Cambiado

- El dialogo de camaras de la GUI usa el rango compartido `CAMERA_MATCH_RANGE_KM` para alinearse con dashboard/API.
- El service worker del dashboard pasa a `dgt-monitor-v53` para publicar los assets con favoritos ampliados.
- La rama `release` se actualizo desde `develop` y se promociono a `main` mediante PR #13.
- `main` quedo en el merge commit `5d75d6f91ba3b79c72c6d0ab2632621873d54f7c`.

### Corregido

- Click sobre imagen de camara en GUI: el handler del visor fullscreen devuelve `None` y evita `TypeError: invalid argument to sipBadCatcherResult()`.

### Validacion

- PR #12 `feature/GUI` -> `develop`: integrada.
- PR #13 `release` -> `main`: integrada con checks `Test & Validate (3.12)` en `SUCCESS`.
- Tag `20260719.06`: creado y subido sobre el commit final de `main`.
- `QT_QPA_PLATFORM=offscreen python -m pytest tests -q`: 53 tests pasando.

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

- `python -m pytest tests -q`: 53 tests pasando.
- `python -m compileall -q src`: sin errores.
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
