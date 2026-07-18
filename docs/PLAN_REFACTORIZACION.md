# Plan de refactorizacion

## Objetivo

Reimplementar DGT Monitor con programacion orientada a objetos, separando dominio, infraestructura, casos de uso, API FastAPI y GUI PyQt6.

## Fases

1. [x] Crear paquete, configuracion y documentacion base.
2. [x] Implementar modelos, contratos y utilidades de dominio.
3. [x] Implementar cliente HTTP, parsers DATEX2, repositorios y cache TTL.
4. [x] Implementar servicios compartidos de incidentes y camaras.
5. Implementar dashboard FastAPI, WebSocket y PWA.
6. Implementar GUI PyQt6 modular y dialogos no modales.
7. Completar pruebas, CI, despliegue y documentacion.

## Estado actual

El primer flujo completo ya funciona sin frameworks: repositorios, parsers, cache, servicios y fachada producen payloads serializables usando dobles de prueba y XML local. La siguiente fase es adaptar esta fachada a FastAPI mediante una app factory inyectable.

## Compatibilidad

Los puntos de entrada `DGT.py`, `DGT_V2.py` y `dashboard/app.py` se conservaran como wrappers pequenos sobre la arquitectura nueva.

## Criterios de aceptacion

- La GUI y la API consumen los mismos servicios.
- No hay parsing DATEX2 ni peticiones HTTP dentro de widgets o rutas.
- Las pruebas automatizadas no dependen de la red de DGT.
- La cache es segura para hilos.
- Los comandos de escritorio y Render permanecen estables.
