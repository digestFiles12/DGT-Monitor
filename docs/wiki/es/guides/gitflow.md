# Flujo de trabajo Git

El repositorio integra cambios mediante ramas y solicitudes de incorporación de cambios (PR); no se deben hacer cambios de trabajo directamente en las ramas compartidas.

## Ramas y destinos

- `main`: rama de producción.
- `develop`: rama de integración; punto de partida del trabajo habitual.
- `release`: rama de estabilización antes de producción.
- `feature/<nombre>`: funcionalidad nueva, creada desde `develop` y propuesta mediante PR a `develop`.
- `fix/<nombre>`: corrección no urgente, creada desde `develop` y propuesta mediante PR a `develop`.
- `hotfix/<nombre>`: corrección urgente basada en `main`; al completarla, intégrala en `main`, `release` y `develop` mediante PR para que las ramas permanezcan sincronizadas.

## Flujo normal

1. Actualiza `develop` y crea desde allí una rama `feature/*` o `fix/*` con un nombre descriptivo.
2. Implementa el cambio, añade o actualiza pruebas y documentación pertinente.
3. Abre una PR hacia `develop`. Describe el propósito, resume los cambios y anota las pruebas ejecutadas.
4. Cuando la integración esté lista para una entrega, abre una PR de `develop` a `release` y valida esa rama.
5. Tras la estabilización, abre una PR de `release` a `main` para publicar.

Para un `hotfix/*`, basa la rama en `main`, valida la corrección y abre las PR de sincronización hacia las ramas compartidas indicadas arriba.

## Integración continua

El flujo `.github/workflows/test.yml` se ejecuta en inserciones a `main`, `develop`, `release`, `feature/**`, `release/**` y `hotfix/**`, y en PR dirigidas a `develop`, `release` o `main`. Usa Ubuntu y Python 3.12, instala `.[dev]`, ejecuta `pytest` con `QT_QPA_PLATFORM=offscreen` y comprueba las importaciones. `compileall` y `git diff --check` también se ejecutan, pero sus pasos no bloquean el flujo si fallan. Los pushes a ramas `fix/*` no están enumerados como disparador; la suite sí se ejecuta al abrir o actualizar su PR hacia `develop`. Para el comando local, consulta [Desarrollo](development.md).

El trabajo de publicación de CI solo se ejecuta tras las pruebas para inserciones a `release` o `main`. Informa que Render despliega automáticamente; el servicio y la rama observada se configuran en Render. Para conocer las variables y la prueba de humo, consulta [Despliegue](deployment.md).
