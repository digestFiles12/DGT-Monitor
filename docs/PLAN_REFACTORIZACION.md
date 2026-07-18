# Plan de refactorizacion

## Objetivo

Reimplementar DGT Monitor con programacion orientada a objetos, separando dominio, infraestructura, casos de uso, API FastAPI y GUI PyQt6.

## Fases

1. [x] Crear paquete, configuracion y documentacion base.
2. [x] Implementar modelos, contratos y utilidades de dominio.
3. [x] Implementar cliente HTTP, parsers DATEX2, repositorios y cache TTL.
4. [x] Implementar servicios compartidos de incidentes y camaras.
5. [x] Implementar dashboard FastAPI, WebSocket y PWA.
6. [~] Implementar GUI PyQt6 modular y dialogos no modales. Ventana, filtros, estadísticas, tabla, detalle, diálogo no modal de cámaras cercanas y visor asíncrono de imágenes completados; wrappers, temporizador y registro visible pendientes.
7. [~] Completar pruebas, CI, despliegue y documentacion. Suite actual con 50 tests, Render y Actions configurados; quedan smoke manual y cierre de wrappers.

## Estado actual

El flujo compartido, la API modular, el dashboard web/PWA y la GUI modular ya funcionan. La GUI carga incidencias, cámaras e imágenes en `QThread`, filtra mediante modelos de dominio y presenta filtros completos, estadísticas clicables, tabla, detalle, cámaras cercanas, miniaturas, visor fullscreen y modo claro/oscuro sin duplicar lógica de aplicación. El dashboard web se sirve desde `/` para Render e incluye los mismos filtros/celdas, modo claro/oscuro persistente, icono rojo de cámara tachada cuando no hay cobertura y visor de cámaras con fallback visual localizado para imágenes no disponibles.

## Compatibilidad

`dashboard/app.py` ya se conserva como wrapper ASGI estable. Quedan por crear los wrappers de escritorio `DGT.py` y `DGT_V2.py` sobre `gui.entrypoints`.

## Criterios de aceptacion

- La GUI y la API consumen los mismos servicios.
- No hay parsing DATEX2 ni peticiones HTTP dentro de widgets o rutas.
- Las pruebas automatizadas no dependen de la red de DGT.
- La cache es segura para hilos.
- Los comandos de escritorio y Render permanecen estables.
