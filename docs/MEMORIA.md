# Memoria del proyecto final / Final project report

**Proyecto 3 – Dashboard científico generado con Python y variables dinámicas**
**Proyecto / Project:** DGT Monitor · **Alumno / Student:** _(nombre y apellidos)_ · **Curso / Course:** _(curso)_

## 1. Introducción

DGT Monitor consulta las incidencias de tráfico que publica la Dirección General de Tráfico (DGT), las guarda, las agrupa y las muestra en un dashboard web con gráficas. El proyecto sigue el espíritu del Proyecto 3 (tomar datos, procesarlos y mostrar indicadores) pero usa datos reales de tráfico en lugar del CSV de COVID.

**Qué hace, de principio a fin:**

1. Descarga el XML DATEX II de la DGT con `requests`.
2. Lo interpreta con `xml.etree.ElementTree` (con espacios de nombres) y lo convierte en objetos `Incident`.
3. Asigna a cada incidencia su comunidad autónoma (CCAA) a partir de la provincia.
4. Guarda las incidencias en SQLite usando el identificador de la DGT como clave, para no duplicarlas.
5. Agrupa los datos por CCAA, provincia, tipo y día de la semana y calcula 4 indicadores.
6. Expone todo con FastAPI y lo muestra en el dashboard (pestaña **Gráficas**) y en un menú de consola.

## 2. Cómo se cumple el enunciado

| Enunciado | Dónde está | Cómo se cumple |
|---|---|---|
| Datos desde un fichero (`csv.DictReader`) | `infrastructure/http.py`, `infrastructure/parsers/incident.py` | La fuente es el XML de la DGT, que se descarga con `requests` y se parsea. El fichero de ejemplo `tests/fixtures/incidents_sample.xml` permite trabajar sin conexión. |
| **Ejercicio 1**: JSON agrupado por día de la semana y provincia, con 4 indicadores | `application/statistics.py` (`group_incidents`, `write_grouped_json`), `GET /api/stats/grouped` | El JSON incluye `by_weekday_province`, `by_weekday_region`, `by_province`, `by_region` y `by_type`. Cada grupo lleva `total`, `severe`, `roadworks` y `road_closures`. |
| **Ejercicio 2**: 4 gráficas con menú en bucle infinito | `menu.py` (`run_chart_menu`), pestaña **Gráficas** del dashboard | Una gráfica de barras por indicador. El dashboard añade líneas y agrupación por día de la semana y por tipo. |
| **Ejercicio 3**: 4 gráficas de queso y provincia máxima y mínima | `menu.py` (`build_pie_chart`, `describe_extremes`), pestaña **Gráficas** (modo queso) | Un gráfico circular por indicador. Debajo de cada gráfica se indica el máximo y el mínimo. |
| Menú con `input()` y opción de salir | `python -m dgt_monitor.menu` | Mismo esquema 1–4 gráficas, 5 salir. |
| Provincia y CCAA | `core/regions.py` | Todo se puede ver por provincia o por CCAA (`level=province\|region`). |

### Los 4 indicadores

| Indicador | Regla |
|---|---|
| `total` | Todas las incidencias. |
| `severe` | Incidencias con gravedad `highest`. |
| `roadworks` | La causa contiene `roadworks` o `maintenance`. |
| `road_closures` | El tipo de gestión es `roadClosed` o `carriagewayClosures`. |

### Máximo y mínimo

Para cada indicador se busca el grupo con el valor más alto y el más bajo. **El mínimo ignora los grupos con 0**, porque un mínimo de 0 no aporta información. En caso de empate gana el nombre que va primero alfabéticamente. Si ningún grupo tiene datos, se muestra «sin datos».

## 3. Arquitectura

```
src/dgt_monitor/
  core/            modelos, constantes, regiones (CCAA), traducciones
  infrastructure/  descarga HTTP, parsers XML, caché, SQLite
  application/     casos de uso: incidencias, cámaras, estadísticas, fachada
  api/             FastAPI: rutas y fábrica de la aplicación
  web/             app ASGI y dashboard estático (HTML, JS, CSS, Chart.js local)
  gui/             interfaz PyQt6 (opcional, solo local)
  menu.py          menú de consola
tests/             pruebas (unit, integration, api, gui) y fixtures
docs/              documentación, requisitos y wiki bilingüe
```

Cada capa solo depende de las inferiores (`core` no depende de nada). Esto permite probar la lógica sin red ni servidor. La wiki detallada, con una página por fichero y cada función explicada en español e inglés, está en [docs/wiki/](wiki/README.md).

## 4. Decisiones técnicas

- **Sin duplicados.** La tabla `incidents` usa el `id` de la DGT como clave primaria y se guarda con `INSERT ... ON CONFLICT DO UPDATE`: si la incidencia ya existe se actualiza (`last_seen`, datos), conservando `first_seen`.
- **La persistencia nunca rompe la aplicación.** Si SQLite falla, se registra el error y se sigue sirviendo el dato de la DGT.
- **Caché de 2 minutos** en las incidencias para no consultar a la DGT en cada petición.
- **Chart.js local** (`static/chart.umd.min.js`, versión 4.4.7). No se usa CDN, así que las gráficas funcionan sin internet.
- **Tests con un XML real.** `tests/fixtures/incidents_sample.xml` es un recorte del feed real (90 incidencias de 47 provincias). Los tests y GitHub Actions no dependen de que responda la DGT.
- **Nombres de provincia.** El feed usa nombres bilingües («Alacant/Alicante», «València/Valencia») y a veces con la codificación rota. `regions.py` los normaliza (tildes, mayúsculas, cada lado de la barra) antes de buscar la CCAA. Una provincia desconocida se agrupa como `Unknown` y se registra un aviso.
- **Estructura `src/`** y nombres de ficheros, funciones, variables y comentarios en inglés.

## 5. Fuente de datos: condiciones de uso

- **Origen:** Punto de Acceso Nacional de Tráfico y Movilidad de la DGT (`nap.dgt.es`), formato DATEX II.
- **Licencia:** los conjuntos de datos constan como «Licence and Free of charge» (gratuitos), y los términos de uso son el [aviso legal de la DGT](https://www.dgt.es/contenido/aviso-legal/). Hay que citar a la DGT como fuente.
- **Método:** consulta por demanda (pull). La DGT **no envía** los eventos, es la aplicación la que consulta cada cierto tiempo.
- **Actualización:** las incidencias cambian «cuando ocurren». La aplicación consulta como máximo cada 2 minutos gracias a la caché.
- **Cobertura:** el feed de la DGT no incluye toda España. El conjunto de cámaras, por ejemplo, excluye País Vasco y Cataluña, que tienen sus propios servicios de tráfico. Por eso en los datos de ejemplo Cataluña tiene muy pocas incidencias y el País Vasco ninguna. Los resultados reflejan el feed de la DGT, no todo el tráfico de España.
- **Cámaras:** se enlazan o muestran las imágenes con moderación, solo las de la incidencia consultada.

## 6. Despliegue en Render y limitación de SQLite

La aplicación se despliega en Render con `render.yaml`. En el **plan gratuito el disco no es persistente**: la base SQLite se pierde en cada reinicio o despliegue. Por eso la base se guarda en `/tmp/incidents.db` (variable `INCIDENT_DB_PATH`).

Para una demo no es un problema, porque **al arrancar vuelve a cargar los datos**: la primera petición consulta la DGT, y desde ese momento la base se rellena otra vez. Lo que se pierde es solo el histórico entre reinicios. Para conservarlo haría falta un disco persistente de pago o una base de datos externa.

Además, el plan gratuito pone la aplicación en suspensión tras un rato sin visitas, y la primera petición después tarda unos segundos en responder.

## 7. Pruebas

- Más de 140 pruebas automáticas (`pytest tests -q`) y GitHub Actions en cada push y pull request.
- Las pruebas cubren modelos, parsers, regiones, SQLite sin duplicados, estadísticas, API, menú de consola (con entradas simuladas), recursos estáticos del dashboard y la interfaz PyQt6.
- La pestaña de gráficas se comprobó además en un navegador real (Edge sin ventana) con el XML de ejemplo: se dibujan las 4 gráficas de barras y las 4 de queso, y funcionan el cambio de nivel y de agrupación.

## 8. Flujo de trabajo

Se ha usado GitFlow: `feature/*` → `develop` mediante pull requests → `release` → `main`. Cada paso del proyecto fue un PR con CI en verde (por ejemplo: SQLite y CCAA, API de estadísticas, menú de consola, gráficas del dashboard, wiki y memoria).

## 9. Uso de herramientas de IA

He usado GitHub Copilot (asistente de IA en VS Code y agentes en paralelo) para:

- Proponer la estructura de carpetas (`src/`, `tests/`) y reorganizar el proyecto.
- Escribir la primera versión de módulos como el mapa de CCAA, la persistencia SQLite, las estadísticas, el menú de consola y la pestaña de gráficas.
- Generar los tests y recortar el XML real para usarlo como fichero de ejemplo.
- Redactar la wiki bilingüe y borradores de esta memoria.

**Qué he hecho yo:** definir los requisitos y el alcance, decidir los indicadores, revisar el código generado, probar el resultado y asegurarme de entender cada parte para poder explicarla.

## 10. Limitaciones y trabajo futuro

- Las estadísticas se calculan sobre el feed actual de la DGT; la base SQLite acumula las incidencias vistas pero todavía no se usa para consultas históricas.
- WebSocket en tiempo real: ya existe el canal `/ws/incidents`, que refresca periódicamente; falta una tarea en el servidor que detecte solo las incidencias nuevas y las emita.
- Datos limitados a lo que publica la DGT (sin Cataluña ni País Vasco en todos los conjuntos).
- La interfaz PyQt6 es opcional y no se ha ampliado.

---

## English summary

DGT Monitor downloads the DGT (Spanish traffic authority) DATEX II XML with `requests`, parses it with `xml.etree.ElementTree`, maps each province to its autonomous community, stores incidents in SQLite keyed by the DGT id (upsert, no duplicates), groups them by region, province, type and weekday, and serves four indicators (total, severe, roadworks, road closures) through FastAPI. The dashboard has a **Charts** tab with an indicator menu, bar/line/pie charts and the maximum and minimum group under each chart. A console menu (`python -m dgt_monitor.menu`) reproduces exercises 1–3 of the assignment. Tests use a real, trimmed XML fixture and never call the DGT.

**Source terms:** data from the DGT National Access Point is published free of charge under the DGT legal notice and must be attributed; it is pulled on demand, the feed does not cover all of Spain (e.g. Basque Country and Catalonia have their own services).

**Render free plan:** the disk is ephemeral, so the SQLite file is lost on every restart or deploy; the app refills it from the DGT on the first request. Only the history between restarts is lost.

**AI tools:** GitHub Copilot was used for project structure, first drafts of modules and tests, and documentation; requirements, indicators, review, testing and understanding of the code are the student's own work.
