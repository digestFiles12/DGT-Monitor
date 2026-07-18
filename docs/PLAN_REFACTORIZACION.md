# Plan de refactorizacion

## Objetivo

Reimplementar DGT Monitor con programacion orientada a objetos, separando dominio, infraestructura, casos de uso, API FastAPI y GUI PyQt6.

## Fases

1. [x] Crear paquete, configuracion y documentacion base.
2. [x] Implementar modelos, contratos y utilidades de dominio.
3. [x] Implementar cliente HTTP, parsers DATEX2, repositorios y cache TTL.
4. [x] Implementar servicios compartidos de incidentes y camaras.
5. [x] Implementar dashboard FastAPI, WebSocket y PWA. REST, WebSocket, frontend y PWA completados.
6. Implementar GUI PyQt6 modular y dialogos no modales.
7. Completar pruebas, CI, despliegue y documentacion.

## Estado actual

El flujo compartido y la API modular ya funcionan con dobles de prueba. FastAPI dispone de app factory inyectable, endpoints REST, WebSocket, wrapper ASGI estable, dashboard PWA completo (HTML/CSS/JS, service worker, manifiesto e iconos). A continuación se implementa la GUI PyQt6.

## Compatibilidad

Los puntos de entrada `DGT.py`, `DGT_V2.py` y `dashboard/app.py` se conservaran como wrappers pequenos sobre la arquitectura nueva.

## Criterios de aceptacion

- La GUI y la API consumen los mismos servicios.
- No hay parsing DATEX2 ni peticiones HTTP dentro de widgets o rutas.
- Las pruebas automatizadas no dependen de la red de DGT.
- La cache es segura para hilos.
- Los comandos de escritorio y Render permanecen estables.
