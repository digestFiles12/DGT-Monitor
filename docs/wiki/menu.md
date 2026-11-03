# dgt_monitor/menu.py
**ES:** Implementa el menú de consola del proyecto final: prepara datos agrupados desde el XML de la DGT o un JSON existente y permite explorar gráficos por provincia o comunidad autónoma.
**EN:** Implements the final project's console menu: prepares grouped data from DGT XML or an existing JSON file and lets users explore charts by province or autonomous community.
## Dependencies / Dependencias
Usa las funciones de agrupación/extremos/escritura de `application.statistics`, la URL DGT, cliente XML y parser de incidentes. Matplotlib se importa de forma diferida solo al construir o mostrar gráficos.
## Contents / Contenido
### `INDICATOR_OPTIONS`, `EXIT_OPTION`, `MAX_BARS`, `MAX_SLICES`
- **ES:** Asocian las opciones 1–4 a indicadores/etiquetas, fijan la opción de salida en 5 y limitan las gráficas a 15 barras o 8 sectores antes de agrupar el resto.
- **EN:** Map options 1–4 to indicators/labels, set exit to option 5, and cap charts at 15 bars or 8 pie slices before combining the remainder.
### `load_grouped_data(xml_path, json_path, output_path)`
- **ES:** Ejercicio 1: carga el JSON indicado si `json_path` existe; si no, lee XML local o lo descarga de DGT, lo analiza, agrupa incidentes y escribe `output_path`. Devuelve el diccionario agrupado. El JSON existente evita ejecutar el ejercicio de construcción.
- **EN:** Exercise 1: loads the specified JSON when `json_path` is given; otherwise reads local XML or downloads it from DGT, parses and groups incidents, and writes `output_path`. Returns the grouped dictionary. An existing JSON skips the build exercise.
### `top_groups(groups, indicator, limit, add_others)`
- **ES:** Devuelve pares nombre-valor de grupos con valor positivo, ordenados de mayor a menor y alfabéticamente en empates. Recorta a `limit`; si `add_others` es verdadero, agrega los restantes como `Otros` cuando su suma no sea cero.
- **EN:** Returns name-value pairs for groups with positive values, sorted descending and alphabetically for ties. Truncates to `limit`; when `add_others` is true, combines the remainder as `Otros` if its sum is nonzero.
### `describe_extremes(groups, indicator)`
- **ES:** Formatea máximo y mínimo provistos por `find_extremes`; si no existen ambos, devuelve `No hay datos para este indicador.`
- **EN:** Formats the maximum and minimum from `find_extremes`; if either is absent, returns `No hay datos para este indicador.`
### `build_bar_chart(groups, indicator, title)`
- **ES:** Ejercicio 2: construye una figura Matplotlib de barras horizontales para hasta 15 grupos positivos principales, con título y eje X `Incidencias`; devuelve la figura, no la muestra.
- **EN:** Exercise 2: builds a Matplotlib horizontal bar figure for up to 15 highest positive groups, with a title and `Incidencias` X-axis; returns the figure without displaying it.
### `build_pie_chart(groups, indicator, title)`
- **ES:** Ejercicio 3: crea una figura de sectores para hasta ocho grupos positivos; los grupos restantes se combinan en `Otros`. Muestra porcentajes y devuelve la figura sin abrirla.
- **EN:** Exercise 3: creates a pie figure for up to eight positive groups; remaining groups are combined into `Otros`. Shows percentages and returns the figure without opening it.
### `show_figure(figure)`
- **ES:** Abre la figura en una ventana y espera a que se cierre; después la cierra mediante Matplotlib.
- **EN:** Opens the figure in a window and waits for it to close; then closes it through Matplotlib.
### `run_chart_menu(groups, kind, ask=input, say=print, show=show_figure)`
- **ES:** Mantiene un bucle con opciones para los cuatro indicadores y salida; construye barra salvo que `kind == "pie"`, muestra la figura y, después de cualquier gráfico, imprime máximo y mínimo. Las funciones inyectables facilitan probar el menú.
- **EN:** Runs a loop with choices for the four indicators and exit; builds bars unless `kind == "pie"`, displays the figure, and prints maximum and minimum after every chart. Injectable functions make the menu easier to test.
### `run_main_menu(data, ask=input, say=print, show=show_figure)`
- **ES:** Menú principal: conecta la opción 1 con el menú de barras del ejercicio 2 y la opción 2 con el de sectores del ejercicio 3; permite agrupar por provincia o región y vuelve al menú principal al terminar un submenú.
- **EN:** Main menu: connects option 1 to the Exercise 2 bar menu and option 2 to the Exercise 3 pie menu; allows grouping by province or region and returns to the main menu when a submenu ends.
### `main(argv=None)`
- **ES:** Define `--xml`, `--json` y `--output`, carga los datos, muestra el total y lanza el menú principal. Si se ejecuta como módulo, se invoca desde el bloque `__main__`.
- **EN:** Defines `--xml`, `--json`, and `--output`, loads the data, prints the total, and starts the main menu. When run as a module, it is invoked by the `__main__` block.
## Example / Ejemplo
`python -m dgt_monitor.menu --xml incidencias.xml --output agrupadas.json` ejecuta la construcción del ejercicio 1 antes de abrir el menú de ejercicios 2 y 3.
