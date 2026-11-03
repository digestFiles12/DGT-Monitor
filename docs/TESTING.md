# Estrategia de pruebas

## Estado

La suite actual contiene 53 pruebas y cubre modelos, texto, distancia, parsers, cache, servicios, fachada, REST, WebSocket, Activity API, dashboard/PWA con filtros completos, `match_mode`, regex/exact, filtro `incident_coverage`, modo oscuro, selector ES/EN, fallback localizado de imagenes de camara, estado sin cobertura con icono, scroll/contratos estaticos y GUI PyQt6 offscreen con filtros completos y visor fullscreen de camaras.

## Comandos

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m pytest test\unit -q
.\.venv\Scripts\python.exe -m pytest test\integration -q
.\.venv\Scripts\python.exe -m pytest test\api -q
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest test\gui -q
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```

## Reglas

- No usar la DGT real.
- Inyectar repositorios o fachada falsos.
- Añadir una prueba de contrato por cada endpoint/ruta PWA.
- Para GUI usar `QT_QPA_PLATFORM=offscreen` cuando sea posible.
- Mantener un checklist manual para ventanas no modales, imágenes, cierre de threads y Render.

## Riesgos que deben cubrirse

- Expiración e invalidación de caché.
- Acceso concurrente y carga única.
- XML inválido y campos opcionales.
- Serialización exacta de modelos.
- Limites y filtros API, incluidos `match_mode`, regex invalido y `incident_coverage`.
- Ciclo de vida QThread.
- Aspect ratio y carga fallida de imágenes.
- Activity API: autenticación, revocación, SSE, CSV y paginación.
- Dashboard/PWA: rutas estaticas, service worker `dgt-monitor-v51`, manifest, selector de idioma, fallback de imagenes, estados de cobertura de camara, scroll general e interno y sincronizacion de conteos entre incidencias, camaras y mapa.

## Validacion actual

Ultima validacion local documentada, 2026-07-19:

```powershell
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests -q
# 53 passed

.\.venv\Scripts\python.exe -m pytest --collect-only | Select-String "collected"
# 53 tests collected

.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```