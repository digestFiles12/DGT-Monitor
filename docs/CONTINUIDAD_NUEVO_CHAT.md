# Continuidad para un nuevo chat

Este documento es el punto de entrada para reanudar el proyecto con el contexto vacio. Leerlo primero y despues abrir `docs/INDEX.md` si hace falta mas detalle.

---

## Estado al cerrar el chat

- Fecha de cierre: 2026-07-19.
- Rama local al documentar: `main`.
- `main` local sincronizada con `origin/main` por fast-forward.
- Release mergeada: PR #5 `Release v20260719.01`, `develop` -> `main`.
- Merge commit en `main`: `de96845c9e5e3fde5c7342e091e4aa7298d973f9`.
- Tag publicado: `v20260719.01`, creado sobre `origin/develop` en `0d5dc61729132c90e8fdc36f8559036d1542b1c4`.
- Hotfix previo: PR #4 `hotfix/dashboard-portrait-layout` integrado en `develop` y luego promovido a `main`.
- Tests locales al cierre: `50 passed`.
- Checks GitHub del PR de hotfix/release: verdes antes del cierre.

---

## Que quedo implementado

- Dashboard web/PWA servido desde `/` con filtros, metricas, filas desplegables, selector ES/EN, modo claro/oscuro y visor de camaras.
- Tabs del dashboard corregidos para no duplicar idioma/label: cada pestana usa `.tab-label` y `.tab-count`.
- Fechas de detalle de incidencias humanizadas: los campos `creation_time`, `start_time` y `end_time` se muestran con `Intl.DateTimeFormat` segun idioma activo.
- Tabla de incidencias en movil mejorada: scroll horizontal interno, sin overflow global de pagina, columnas clave sticky (`Gravedad`, `Carretera`) y detalle desplegable limitado al ancho visible de pantalla.
- Filtros en movil compactados en la parte superior como banda sticky con desplazamiento horizontal para dejar mas espacio a la tabla.
- Fallback visual localizado para imagenes de camara no disponibles.
- Icono rojo `camera-off` para incidencias sin cobertura de camara.
- GUI PyQt6 modular con filtros, modo oscuro, dialogo/visor de camaras y pruebas deterministas de imagen.
- CI actualizada con librerias Qt necesarias en Ubuntu.
- Cache PWA actualizada hasta `dgt-monitor-v19` para forzar carga de assets recientes.

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

Resultado esperado al cierre:

```text
50 passed
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

- En movil, la pagina no debe tener overflow horizontal global.
- La tabla de incidencias si debe tener scroll horizontal dentro de su contenedor.
- Las columnas `Gravedad` y `Carretera` deben permanecer visibles al desplazar horizontalmente.
- Las tabs deben mostrar solo un idioma activo: `Incidencias/Camaras` o `Incidents/Cameras`, nunca ambos.
- En detalles, timestamps tipo `2025-12-12T08:11:34.000+01:00` deben verse como fecha/hora humana.

---

## Git y release

Ramas principales:

- `main`: release actual tras PR #5.
- `develop`: rama de integracion ya promovida a `main` en `v20260719.01`.
- `hotfix/dashboard-portrait-layout`: rama usada para los ajustes responsive y de UI; ya integrada.

PRs relevantes:

- PR #4: hotfix responsive/dashboard, integrado antes de la release.
- PR #5: `Release v20260719.01`, `develop` -> `main`, mergeado.

Tags relevantes:

- `v20260719.01`: tag de release solicitado para la promocion `develop` -> `main`.

---

## Archivos clave modificados recientemente

- `dashboard/static/index.html`: estructura de tabs con `.tab-label` y `.tab-count`.
- `dashboard/static/styles.css`: responsive de topbar/tabs, filtros moviles compactos y tabla movil horizontal.
- `dashboard/static/app.js`: i18n, tabs, detalles, fechas humanas, camaras y fallbacks.
- `dashboard/static/sw.js`: version de cache PWA `dgt-monitor-v19`.
- `test/api/test_api.py`: contratos de assets/PWA.
- `test/gui/test_cameras_dialog.py`: pruebas GUI de camaras deterministas.
- `.github/workflows/test.yml`: dependencias Qt para CI.

---

## Como continuar en un chat nuevo

1. Leer este documento.
2. Ejecutar `git status --short --branch`.
3. Si se va a trabajar desde release, partir de `main` actualizado.
4. Si se va a desarrollar funcionalidad, crear rama desde `develop` actualizada.
5. Validar con la suite completa antes de abrir PR.

Documentacion complementaria:

- `docs/INDEX.md`: indice general.
- `docs/PHASE_7_COMPLETED.md`: handoff historico de fase 7.
- `docs/GITFLOW.md`: flujo de ramas.
- `docs/PRUEBAS.md`: guia de pruebas.
- `docs/DESPLIEGUE.md`: despliegue.