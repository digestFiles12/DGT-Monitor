# Continuidad para un nuevo chat

Este documento es el punto de entrada para reanudar el proyecto con el contexto vacio. Leerlo primero y despues abrir `docs/INDEX.md` si hace falta mas detalle.

---

## Estado al cerrar el chat

- Fecha de cierre: 2026-07-19.
- Rama de integracion actual: `develop`.
- `develop`: actualizado en `020f0b1` tras la PR #12 `feature/GUI` -> `develop`.
- `release`: actualizada desde `develop` y usada para promocion estable.
- `main`: actualizado mediante PR #13 `release` -> `main`, merge commit `5d75d6f91ba3b79c72c6d0ab2632621873d54f7c`.
- Tag publicado: `20260719.06`, creado sobre el merge commit final de `main`.
- API FastAPI, WebSocket, SSE y Activity API operativas.
- Dashboard web/PWA servido desde `/`, con filtros completos, busqueda `contains`/`exact`/`regex`, celdas estadisticas clicables, mapa sincronizado, scroll general e interno, modo claro/oscuro, icono rojo de camara tachada sin cobertura, fallback localizado para imagenes no disponibles, visor fullscreen de camaras y desplegable en Render.
- GUI PyQt6 modular con filtros completos, modo de busqueda contiene/exacta/regex, celdas estadisticas clicables, incidencias, dialogo de camaras alineado con el rango compartido de cobertura, imagenes asincronas, visor fullscreen y modo claro/oscuro.
- Activity system con backend en memoria o SQLite.
- Render y GitHub Actions configurados.
- 53 tests pasando.

Ver `docs/PHASE_7_COMPLETED.md` para estado completo y checklist de handoff.

---

## Que quedo implementado

- Dashboard web/PWA servido desde `/` con filtros, metricas, filas desplegables, selector ES/EN, modo claro/oscuro y visor de camaras.
- Tabs del dashboard corregidos para no duplicar idioma/label: cada pestana usa `.tab-label` y `.tab-count`.
- Fechas de detalle de incidencias humanizadas: los campos `creation_time`, `start_time` y `end_time` se muestran con `Intl.DateTimeFormat` segun idioma activo.
- Tabla de incidencias en movil con scroll horizontal interno, columnas clave sticky y detalle limitado al ancho visible.
- Scroll general restaurado en movil y escritorio; tabla de incidencias y grid de camaras conservan scroll interno.
- Filtro de camaras con incidencia mediante `incident_coverage=true`.
- Busqueda textual con `contains`, `exact` y `regex` mediante `match_mode`.
- Cobertura incidencia-camara centralizada en `CAMERA_MATCH_RANGE_KM = 2.0`.
- Mapa sincronizado con filtros y conteos de incidencias/camaras.
- Fallback visual localizado para imagenes de camara no disponibles.
- Icono rojo `camera-off` para incidencias sin cobertura de camara.
- GUI PyQt6 modular con filtros, modo oscuro, dialogo/visor de camaras y pruebas deterministas de imagen.
- CI actualizada con librerias Qt necesarias en Ubuntu.
- Cache PWA actualizada hasta `dgt-monitor-v51` para forzar carga de assets recientes.

---

## Comandos de validacion recomendados

Ejecutar desde la raiz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pytest test\api\test_api.py -q
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest test -q
.\.venv\Scripts\python.exe -m compileall -q dgt_monitor dashboard
git diff --check
git status --short --branch
```

Resultado esperado:

```text
53 passed
sin errores de compileall
git diff --check sin salida
working tree limpio
```

---

## Servidor local y comprobacion visual

Arrancar dashboard local:

```powershell
.\.venv\Scripts\python.exe -m uvicorn dashboard.app:app --host 127.0.0.1 --port 8766
```

Abrir:

```text
http://127.0.0.1:8766/
```

Comprobaciones visuales importantes:

- En movil y escritorio, la pagina debe permitir scroll general.
- La tabla de incidencias debe tener scroll horizontal dentro de su contenedor.
- El grid de camaras debe tener scroll interno cuando haya muchas tarjetas.
- Las columnas `Gravedad` y `Carretera` deben permanecer visibles al desplazar horizontalmente.
- Las tabs deben mostrar solo un idioma activo: `Incidencias/Camaras` o `Incidents/Cameras`, nunca ambos.
- En detalles, timestamps tipo `2025-12-12T08:11:34.000+01:00` deben verse como fecha/hora humana.
- Probar `match_mode=exact` y `match_mode=regex` desde el dashboard o API.
- Probar `incident_coverage=true` en camaras y confirmar que mapa/conteos se mantienen sincronizados.

---

## Git y release

Ramas principales:

- `main`: produccion. Contiene la release `20260719.06` tras mergear PR #13.
- `develop`: integracion diaria. Actualmente contiene PR #12 y esta alineada con la funcionalidad publicada.
- `release`: estabilizacion permanente. Fue actualizada desde `develop` y promocionada a `main` por PR #13.

PRs relevantes:

- PR #13: `release` -> `main`, release `20260719.06`, mergeada.
- PR #12: `feature/GUI` -> `develop`, mejoras de GUI y fix del visor fullscreen, mergeada.
- PR #9: `feature/scroll` -> `develop`, integrada con filtros exact/regex, cobertura, scroll y fix de sintaxis.
- PR #10: `develop` -> `main`, release `20260719.02`.
- PR #5: `Release v20260719.01`, `develop` -> `main`, mergeada anteriormente.

Tags relevantes:

- `20260719.06`: tag actual de produccion sobre `main` (`5d75d6f91ba3b79c72c6d0ab2632621873d54f7c`).
- `20260719.05` y `20260719.04`: tags sobre el estado de `develop` tras PR #12.
- `20260719.02`: tag de release documental/dashboard anterior.
- `v20260719.02`: tag previo existente sobre el estado anterior de `develop`.
- `v20260719.01`: release anterior en `main`.

---

## Archivos clave modificados recientemente

- `README.md`: resumen actualizado, API rapida, validacion y enlaces.
- `CHANGELOG.md`: historial de cambios de 2026-07-19 y 2026-07-18.
- `docs/`: documentacion completa actualizada para filtros, cobertura, scroll, Render, GitFlow y pruebas.
- `dashboard/static/index.html`: filtros de modo de busqueda y camaras con incidencia.
- `dashboard/static/styles.css`: scroll general, scroll interno y responsive.
- `dashboard/static/app.js`: i18n, tabs, detalles, fechas humanas, camaras, fallbacks, mapa y filtros avanzados.
- `dashboard/static/sw.js`: cache PWA `dgt-monitor-v51`.
- `test/api/test_api.py`: contratos de assets/PWA y filtros API.

---

## Como continuar en un chat nuevo

1. Leer este documento.
2. Ejecutar `git status --short --branch`.
3. Si se va a trabajar desde produccion, partir de `main` actualizado.
4. Si se va a desarrollar funcionalidad, crear rama desde `develop` actualizada.
5. Validar con la suite completa antes de abrir PR.

Documentacion complementaria:

- `docs/INDEX.md`: indice general.
- `docs/PHASE_7_COMPLETED.md`: handoff historico y estado completo.
- `docs/GITFLOW.md`: flujo de ramas.
- `docs/PRUEBAS.md`: guia de pruebas.
- `docs/DESPLIEGUE.md`: despliegue.
- `CHANGELOG.md`: historial de cambios.
