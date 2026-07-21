# Documentacion de DGT Monitor

Estado actual: API FastAPI, dashboard web/PWA, GUI PyQt6 local, Activity API, Render y GitHub Actions operativos. El dashboard incluye filtros completos, modo de busqueda `contains`/`exact`/`regex`, cobertura de camaras a 2 km por punto kilometrico, filtro de camaras con incidencia, pestaña de camaras favoritas persistidas en el navegador, mapa con conteos sincronizados, scroll general en movil/escritorio y scroll interno en tabla/grid. La GUI incluye modo de busqueda contiene/exacta/regex, fechas humanizadas, dialogo de camaras con rango compartido y visor fullscreen corregido. La suite automatizada actual contiene 53 tests. La version publicada actual es `20260719.06` en `main`, promocionada desde `release` por PR #13.

## Leer primero

- [Continuidad para un nuevo chat](CONTINUIDAD_NUEVO_CHAT.md): quick-start para retomar el proyecto.
- [Estado completo del proyecto](PHASE_7_COMPLETED.md): handoff detallado, estado validado y checklist.
- [Changelog](../CHANGELOG.md): cambios recientes por fecha, incluida la entrega de filtros avanzados y cobertura.

## Guia por tema

- [Arquitectura](ARQUITECTURA.md): capas, dependencias y fronteras de responsabilidad.
- [Modelos](MODELOS.md): `Incident`, `Camera`, filtros, estadisticas y serializacion.
- [Servicios](SERVICIOS.md): reglas de filtrado, cobertura, cache y fachada de aplicacion.
- [API](API.md): endpoints REST/WebSocket/SSE, parametros y contrato del dashboard.
- [GUI](GUI.md): comportamiento PyQt6, workers, dialogos y reglas de interfaz.
- [DATEX2](DATEX2.md): fuentes DGT, parsers y normalizacion de datos.
- [Pruebas](PRUEBAS.md): comandos, cobertura esperada y riesgos cubiertos.
- [Desarrollo](DESARROLLO.md): entorno local, validacion y flujo de trabajo.
- [Despliegue](DESPLIEGUE.md): Render, variables y smoke manual.
- [Render Deployment Guide](RENDER_DEPLOYMENT.md): pasos operativos en Render.
- [GitFlow](GITFLOW.md): ramas permanentes, PRs y promocion a release/main.
- [Decisiones](DECISIONES.md): ADRs vigentes.
- [Migracion desde DGT30_GUI](MIGRACION.md): equivalencias con la aplicacion anterior.
- [Plan de refactorizacion](PLAN_REFACTORIZACION.md): fases completadas y pendientes.

## Invariantes documentales

- Ninguna capa de presentacion descarga ni parsea DATEX2.
- Los filtros de API/dashboard/GUI deben viajar como `IncidentFilters` o `CameraFilters`.
- Las respuestas `/api/` no se cachean en el service worker.
- Cada cambio funcional debe actualizar README, changelog y el documento tecnico afectado.
- Antes de cerrar un incremento: `pytest`, `compileall` y `git diff --check` deben estar limpios.
