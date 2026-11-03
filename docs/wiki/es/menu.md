# dgt_monitor/menu.py
Implementa el menú de consola del proyecto final: prepara datos agrupados desde el XML de la DGT o un JSON existente y permite explorar gráficos por provincia o comunidad autónoma.
## Dependencias
Usa las funciones de agrupación/extremos/escritura de `application.statistics`, la URL DGT, cliente XML y parser de incidentes. Matplotlib se importa de forma diferida solo al construir o mostrar gráficos.
## Contenido
### `INDICATOR_OPTIONS`, `EXIT_OPTION`, `MAX_BARS`, `MAX_SLICES`
- Asocian las opciones 1–4 a indicadores/etiquetas, fijan la opción de salida en 5 y limitan las gráficas a 15 barras o 8 sectores antes de agrupar el resto.
### `load_grouped_data(xml_path, json_path, output_path)`
- Ejercicio 1: carga el JSON indicado si `json_path` existe; si no, lee XML local o lo descarga de DGT, lo analiza, agrupa incidentes y escribe `output_path`. Devuelve el diccionario agrupado. El JSON existente evita ejecutar el ejercicio de construcción.
### `top_groups(groups, indicator, limit, add_others)`
- Devuelve pares nombre-valor de grupos con valor positivo, ordenados de mayor a menor y alfabéticamente en empates. Recorta a `limit`; si `add_others` es verdadero, agrega los restantes como `Otros` cuando su suma no sea cero.
### `describe_extremes(groups, indicator)`
- Formatea máximo y mínimo provistos por `find_extremes`; si no existen ambos, devuelve `No hay datos para este indicador.`
### `build_bar_chart(groups, indicator, title)`
- Ejercicio 2: construye una figura Matplotlib de barras horizontales para hasta 15 grupos positivos principales, con título y eje X `Incidencias`; devuelve la figura, no la muestra.
### `build_pie_chart(groups, indicator, title)`
- Ejercicio 3: crea una figura de sectores para hasta ocho grupos positivos; los grupos restantes se combinan en `Otros`. Muestra porcentajes y devuelve la figura sin abrirla.
### `show_figure(figure)`
- Abre la figura en una ventana y espera a que se cierre; después la cierra mediante Matplotlib.
### `run_chart_menu(groups, kind, ask=input, say=print, show=show_figure)`
- Mantiene un bucle con opciones para los cuatro indicadores y salida; construye barra salvo que `kind == "pie"`, muestra la figura y, después de cualquier gráfico, imprime máximo y mínimo. Las funciones inyectables facilitan probar el menú.
### `run_main_menu(data, ask=input, say=print, show=show_figure)`
- Menú principal: conecta la opción 1 con el menú de barras del ejercicio 2 y la opción 2 con el de sectores del ejercicio 3; permite agrupar por provincia o región y vuelve al menú principal al terminar un submenú.
### `main(argv=None)`
- Define `--xml`, `--json` y `--output`, carga los datos, muestra el total y lanza el menú principal. Si se ejecuta como módulo, se invoca desde el bloque `__main__`.
## Ejemplo
`python -m dgt_monitor.menu --xml incidencias.xml --output agrupadas.json` ejecuta la construcción del ejercicio 1 antes de abrir el menú de ejercicios 2 y 3.
