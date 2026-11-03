# Plan de refactorizacion

## Objetivo

Reimplementar DGT Monitor con programacion orientada a objetos, separando dominio, infraestructura, casos de uso, API FastAPI y GUI PyQt6.

## Fases

1. [x] Crear paquete, configuracion y documentacion base.
2. [x] Implementar modelos, contratos y utilidades de dominio.
3. [x] Implementar cliente HTTP, parsers DATEX2, repositorios y cache TTL.
4. [x] Implementar servicios compartidos de incidentes y camaras.
5. [x] Implementar dashboard FastAPI, WebSocket y PWA.
6. [~] Implementar GUI PyQt6 modular y dialogos no modales. Ventana, filtros, estadisticas, tabla, detalle, dialogo no modal de camaras cercanas y visor asincrono de imagenes completados; wrappers, temporizador y registro visible pendientes.
7. [~] Completar pruebas, CI, despliegue y documentacion. Suite actual con 53 tests, Render y Actions configurados; quedan smoke manual de produccion y cierre de wrappers.

## Estado actual

El flujo compartido, la API modular, el dashboard web/PWA y la GUI modular ya funcionan. La GUI carga incidencias, camaras e imagenes en `QThread`, filtra mediante modelos de dominio y presenta filtros completos, estadisticas clicables, tabla, detalle, camaras cercanas, miniaturas, visor fullscreen y modo claro/oscuro sin duplicar logica de aplicacion. El dashboard web se sirve desde `/` para Render e incluye filtros completos, modo de busqueda `contains`/`exact`/`regex`, filtro de camaras con incidencia, mapa con conteos sincronizados, scroll general e interno, modo claro/oscuro persistente, icono rojo de camara tachada cuando no hay cobertura y visor de camaras con fallback visual localizado para imagenes no disponibles.

## Compatibilidad

`src/dgt_monitor/web/app.py` ya se conserva como wrapper ASGI estable. Quedan por crear los wrappers de escritorio `DGT.py` y `DGT_V2.py` sobre `gui.entrypoints`.

## Criterios de aceptacion

- La GUI y la API consumen los mismos servicios.
- No hay parsing DATEX2 ni peticiones HTTP dentro de widgets o rutas.
- Las pruebas automatizadas no dependen de la red de DGT.
- La cache es segura para hilos.
- La cobertura incidencia-camara usa `CAMERA_MATCH_RANGE_KM = 2.0` y esta documentada en servicios, API y modelos.
- Los comandos de escritorio y Render permanecen estables.
