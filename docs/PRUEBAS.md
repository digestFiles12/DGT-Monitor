# Estrategia de pruebas

## Estado

La suite actual contiene 9 pruebas y cubre modelos, texto, distancia, parsers, caché, servicios, fachada, REST y WebSocket.

## Comandos

```powershell
.\.venv\Scripts\python.exe -m pytest test -q
.\.venv\Scripts\python.exe -m pytest test\unit -q
.\.venv\Scripts\python.exe -m pytest test\integration -q
.\.venv\Scripts\python.exe -m pytest test\api -q
.\.venv\Scripts\python.exe -m compileall -q dgt_monitor dashboard
```

## Reglas

- No usar la DGT real.
- Inyectar repositorios o fachada falsos.
- Añadir una prueba de contrato por cada endpoint/ruta PWA.
- Para GUI usar `QT_QPA_PLATFORM=offscreen` cuando sea posible.
- Mantener un checklist manual para ventanas no modales, imágenes y cierre de threads.

## Riesgos que deben cubrirse

- Expiración e invalidación de caché.
- Acceso concurrente y carga única.
- XML inválido y campos opcionales.
- Serialización exacta de modelos.
- Límites y filtros API.
- Ciclo de vida QThread.
- Aspect ratio y carga fallida de imágenes.