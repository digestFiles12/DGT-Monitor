# Estrategia de pruebas

## Estado

La suite actual contiene 50 pruebas y cubre modelos, texto, distancia, parsers, caché, servicios, fachada, REST, WebSocket, Activity API, dashboard/PWA con filtros completos, modo oscuro, selector ES/EN, fallback localizado de imágenes de cámara y estado sin cobertura con icono, y GUI PyQt6 offscreen con filtros completos y visor fullscreen de cámaras.

## Comandos

```powershell
.\.venv\Scripts\python.exe -m pytest test -q
.\.venv\Scripts\python.exe -m pytest test\unit -q
.\.venv\Scripts\python.exe -m pytest test\integration -q
.\.venv\Scripts\python.exe -m pytest test\api -q
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest test\gui -q
.\.venv\Scripts\python.exe -m compileall -q dgt_monitor dashboard
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
- Límites y filtros API.
- Ciclo de vida QThread.
- Aspect ratio y carga fallida de imágenes.
- Activity API: autenticación, revocación, SSE, CSV y paginación.
- Dashboard/PWA: rutas estáticas, service worker, manifest, selector de idioma, fallback de imágenes y estados de cobertura de cámara.