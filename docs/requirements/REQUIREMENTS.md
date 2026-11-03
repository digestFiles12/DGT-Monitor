# Requisitos del proyecto final / Final project requirements

Documento de referencia para humanos y agentes. Todo trabajo debe cumplir estos requisitos.

## 1. Contexto

- Proyecto final de curso: **Proyecto 3 – Dashboard científico generado con Python y variables dinámicas**.
- Objetivo del enunciado: tomar datos, procesarlos, agruparlos en JSON y mostrar indicadores en gráficas.
- Objetivo de nuestro proyecto: adaptar DGT Monitor (datos DATEX II de la DGT en lugar del CSV de COVID) para cumplir los mismos criterios de evaluación. Meta: nota máxima.
- El profesor puede pedir al alumno que explique cualquier parte del código: el código debe ser claro y simple de explicar.

## 2. Enunciado original (resumen)

Datos originales: CSV con `num_def`, `new_cases`, `num_hosp`, `num_uci`, por provincia y fecha.

1. **Ejercicio 1**: guardar los datos en un fichero `.txt` en formato JSON, agrupados por día de la semana y por provincia, con los acumulados de los 4 indicadores. Leer con el módulo `csv` (`csv.DictReader`).
2. **Ejercicio 2**: 4 gráficas de los datos del fichero del ejercicio 1, con un menú en bucle infinito para acceder a cada una.
3. **Ejercicio 3**: a partir del fichero del ejercicio 1, obtener la provincia con más defunciones, casos, hospitalizados y UCI. Mostrar 4 gráficas de queso (circulares) con menú como el anterior. Tras mostrar cada gráfica, indicar la provincia con el **máximo** y la del **mínimo** de la variable.

Menú de referencia:

```
¿Qué gráfica quieres visualizar?
1. Defunciones
2. Casos
3. Hospitalizados
4. UCI
5. Salir
```

## 3. Adaptación a DGT Monitor

| Enunciado | Proyecto |
|---|---|
| CSV | XML DATEX II de la DGT (descargado con `requests`) |
| Fichero JSON agrupado | `incidencias_agrupadas.json` (también se puede guardar como `.txt`) |
| Agrupar por día de la semana y provincia | Agrupar por **provincia**, **tipo** y **día de la semana** |
| 4 indicadores (def., casos, hosp., UCI) | 4 indicadores: **total de incidencias**, **graves**, **obras**, **cortes de carretera** (pendiente de confirmar con el alumno; si cambian, actualizar este documento) |
| 4 gráficas + menú | ≥ 4 gráficas (barras/líneas) con menú de pestañas en el dashboard |
| 4 gráficas de queso + máx/mín | 4 gráficas circulares, una por indicador, indicando provincia máxima y mínima |
| Menú `input()` con bucle infinito | Menú del dashboard + script de consola opcional `python -m dgt_monitor.menu` con el bucle literal del enunciado |

## 4. Requisitos obligatorios (Fase 1)

1. Descargar el XML de la DGT con `requests` y parsearlo con `xml.etree.ElementTree` (o `lxml`) indicando los namespaces.
2. Guardar las incidencias en **SQLite**, usando el identificador de la incidencia como clave para **evitar duplicados** en consultas repetidas.
3. Generar el **JSON agrupado** (provincia, tipo, día de la semana) con los acumulados de cada indicador.
4. Exponer los datos y las estadísticas con **FastAPI** (endpoint de estadísticas, p. ej. `/api/stats`, con máximo y mínimo por indicador).
5. Dashboard web con **al menos 4 gráficas**, incluyendo **gráficas de queso (circulares)**, y un **menú de navegación** entre ellas.
6. Cada indicador muestra la **provincia con el máximo y la del mínimo**.
7. Librería de gráficas: **Chart.js descargado en `dashboard/static`** (sin CDN, funciona sin internet).
8. Tests con un **XML real de ejemplo** guardado en `test/fixtures`. Los tests y GitHub Actions **no dependen** de que responda el servidor de la DGT.

## 5. Requisitos extra (Fase 2, después de la Fase 1)

- WebSocket: tarea periódica en el servidor que consulta a la DGT, detecta incidencias nuevas y las emite. Alternativa mínima: el JavaScript recarga los datos cada X minutos.
- GitHub Actions (ya existe `.github/workflows/test.yml`).
- Wiki y despliegue en Render.
- La GUI PyQt6 es **opcional**: se deja como está, sin ampliarla ni eliminarla.

## 6. Documentación

- **Wiki bilingüe (ES/EN)** en `docs/wiki/`: una página por fichero del código; para cada función, una explicación breve en español y en inglés.
- **Memoria** en `docs/MEMORIA.md`, que debe incluir:
  - Para qué se han usado herramientas de IA (breve).
  - Limitación de Render gratuito: el disco no es persistente, la base SQLite se pierde en cada reinicio/despliegue; la app recarga datos al arrancar. Explicarlo.
  - Condiciones de la fuente: disponibilidad, frecuencia de actualización y condiciones de reutilización de los datos de la DGT. En cámaras, enlazar o mostrar imágenes con moderación.
  - Cómo cumple cada ejercicio del enunciado.

## 7. Orden de trabajo

1. Persistencia SQLite sin duplicados + JSON agrupado.
2. Endpoint `/api/stats` con máximos y mínimos.
3. Pestaña de gráficas en el dashboard con menú.
4. Script de consola opcional con menú `input()`.
5. Tests con el XML de ejemplo.
6. Wiki bilingüe y memoria.
7. Fase 2 (extras).

## 8. Reglas para agentes

- Priorizar lo imprescindible (Fase 1) antes que los extras.
- Cambios simples, legibles y fáciles de explicar por el alumno; evitar sobreingeniería.
- No depender de la red real de la DGT en tests ni CI.
- Mantener la arquitectura por capas existente (`core`, `infrastructure`, `application`, `api`, `dashboard`).
- Actualizar la documentación afectada (wiki, memoria, `docs/INDEX.md`) con cada cambio.
- Ejecutar los tests antes de dar una tarea por terminada:
  `$env:QT_QPA_PLATFORM='offscreen'; .\.venv\Scripts\python.exe -m pytest tests -q`
