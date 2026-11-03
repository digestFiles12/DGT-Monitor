# GitFlow

Este repositorio usa un GitFlow conservador, sin reescritura de historial y con ramas base persistentes.

## Ramas permanentes

- `main`: codigo de produccion. Solo recibe merges desde `release` o `hotfix/*` cuando una version esta validada.
- `develop`: integracion diaria. Recibe merges desde `feature/*` y sirve como origen normal de nuevas features.
- `release`: estabilizacion previa a produccion. Recibe cambios desde `develop` o PRs de cierre cuando se prepara una entrega.

## Ramas temporales

- `feature/<nombre>`: trabajo funcional. Se crea desde `develop` y vuelve a `develop` por pull request.
- `release/<version>`: rama opcional para preparar una version concreta si la rama `release` permanente necesita aislar varios cierres.
- `hotfix/<nombre>`: correccion urgente creada desde `main`. Al terminar, se mergea a `main`, `release` y `develop`.

## Flujo normal

1. Actualizar `develop`.
2. Crear `feature/<nombre>` desde `develop`.
3. Implementar cambios con tests y documentacion.
4. Abrir PR de `feature/<nombre>` hacia `develop`.
5. Cuando `develop` este listo para entrega, abrir PR de `develop` hacia `release`.
6. Validar `release` con suite completa, smoke manual y revision.
7. Abrir PR de `release` hacia `main`.
8. Etiquetar la version desde `main` si aplica.

## Flujo usado en el incremento mas reciente

La PR #9 integro `feature/scroll` en `develop`. Ese incremento incluyo scroll general/interno del dashboard, filtro de camaras con incidencia, cobertura a 2 km, busqueda exacta/regex y correccion de sintaxis posterior a un merge remoto. `develop` contiene el estado integrado y debe ser la base de nuevas ramas `feature/*`.

## Validacion antes de PR

```powershell
$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m compileall -q src
git diff --check
```

## Politica de pull requests

- `feature/*` -> `develop`: funcionalidades normales.
- `develop` -> `release`: preparacion de entrega.
- `release` -> `main`: publicacion estable.
- `hotfix/*` -> `main`, `release` y `develop`: correcciones urgentes.

No se hacen commits directos en `main`, `develop` o `release` salvo inicializacion de ramas o correcciones acordadas.

## Verificacion de PR

Antes de considerar una PR lista:

- Hacer `git fetch` y asegurar que la rama local contiene el ultimo `origin/<feature>`.
- Reproducir localmente el check relevante si GitHub Actions falla.
- Revisar `gh pr view <n> --json statusCheckRollup,mergeable` o la vista web de GitHub.
- Confirmar que `Test & Validate (3.12)` queda en `SUCCESS` y que la PR es mergeable.