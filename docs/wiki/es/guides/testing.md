# Estrategia de pruebas
## Estado
La suite contiene 148 pruebas (`pytest tests`), todas en verde, organizadas por capa:
```text
tests/
  conftest.py            # fixtures compartidas (autouse)
  fixtures/incidents_sample.xml
  unit/                  # núcleo, regiones, estadísticas, caché, stores, parsers, menú
  integration/           # fachada y persistencia de incidencias
  api/                   # REST, WebSocket, estadísticas y Activity API
  gui/                   # PyQt6 en modo offscreen
```
## Comandos
```powershell
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m pytest tests\unit -q
.\.venv\Scripts\python.exe -m pytest tests\integration -q
.\.venv\Scripts\python.exe -m pytest tests\api -q
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests\gui -q
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```
## Fixtures y datos
- `isolated_incident_db` (autouse, en `tests/conftest.py`): fija `INCIDENT_DB_PATH` en un directorio temporal para que el SQLite de incidencias nunca toque el proyecto.
- `init_activity_store` (autouse): crea un almacén de actividad por prueba y lo reinicializa si cambia `ACTIVITY_DB_PATH`.
- `tests/fixtures/incidents_sample.xml`: XML DATEX2 de ejemplo usado por las pruebas de regiones, estadísticas, API de estadísticas, persistencia y menú de consola.
## Reglas
- No usar la DGT real: inyectar repositorios o una fachada falsos.
- Añadir una prueba de contrato por cada endpoint o ruta PWA.
- Para la GUI usar `QT_QPA_PLATFORM=offscreen`.
- Mantener un checklist manual para ventanas no modales, imágenes, cierre de hilos y despliegue.
## Qué debe cubrirse
- Expiración e invalidación de caché, y acceso concurrente.
- XML inválido y campos opcionales; serialización de modelos.
- Filtros y límites de la API, incluidos `match_mode`, regex inválida e `incident_coverage`.
- `/api/stats` (`level`, extremos) y `/api/stats/grouped`; `/ws/incidents`.
- Activity API: autenticación, revocación, SSE, CSV y paginación.
- Mapeo de provincias a comunidades y estadísticas agrupadas.
- Menú de consola (`src/dgt_monitor/menu.py`) con entrada y salida inyectadas.
- Ciclo de vida de `QThread`, carga fallida de imágenes y errores de workers.
- Contratos del dashboard/PWA (rutas estáticas, manifiesto y service worker).
Véanse también [la guía de la API](api.md) y [la guía de la GUI](gui.md).
