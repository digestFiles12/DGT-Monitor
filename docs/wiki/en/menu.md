# dgt_monitor/menu.py
Implements the final project's console menu: prepares grouped data from DGT XML or an existing JSON file and lets users explore charts by province or autonomous community.
## Dependencies
Uses grouping, extremes, and writing functions from `application.statistics`, the DGT URL, an XML client, and the incident parser. Matplotlib is imported lazily only when building or showing charts.
## Contents
### `INDICATOR_OPTIONS`, `EXIT_OPTION`, `MAX_BARS`, `MAX_SLICES`
- Map options 1–6 to total, accidents, roadworks, breakdowns, obstructions, and weather, and set exit to option 7, and cap charts at 15 bars or 8 pie slices before combining the remainder.
### `load_grouped_data(xml_path, json_path, output_path)`
- Exercise 1: loads the specified JSON when `json_path` is given; otherwise reads local XML or downloads it from DGT, parses and groups incidents, and writes `output_path`. Returns the grouped dictionary. An existing JSON skips the build exercise.
### `top_groups(groups, indicator, limit, add_others)`
- Returns name-value pairs for groups with positive values, sorted descending and alphabetically for ties. Truncates to `limit`; when `add_others` is true, combines the remainder as `Otros` if its sum is nonzero.
### `describe_extremes(groups, indicator)`
- Formats the maximum and minimum from `find_extremes`; if either is absent, returns `No hay datos para este indicador.`
### `build_bar_chart(groups, indicator, title)`
- Exercise 2: builds a Matplotlib horizontal bar figure for up to 15 highest positive groups, with a title and `Incidencias` X-axis; returns the figure without displaying it.
### `build_pie_chart(groups, indicator, title)`
- Exercise 3: creates a pie figure for up to eight positive groups; remaining groups are combined into `Otros`. Shows percentages and returns the figure without opening it.
### `show_figure(figure)`
- Opens the figure in a window and waits for it to close; then closes it through Matplotlib.
### `run_chart_menu(groups, kind, ask=input, say=print, show=show_figure)`
- Runs a loop with choices 1–6 for total, accidents, roadworks, breakdowns, obstructions, and weather, plus option 7 to exit; builds bars unless `kind == "pie"`, displays the figure, and prints maximum and minimum after every chart. Injectable functions make the menu easier to test.
### `run_main_menu(data, ask=input, say=print, show=show_figure)`
- Main menu: connects option 1 to the Exercise 2 bar menu and option 2 to the Exercise 3 pie menu; allows grouping by province or region and returns to the main menu when a submenu ends.
### `main(argv=None)`
- Defines `--xml`, `--json`, and `--output`, loads the data, prints the total, and starts the main menu. When run as a module, it is invoked by the `__main__` block.
## Example
`python -m dgt_monitor.menu --xml incidents.xml --output grouped.json` builds the data for Exercise 1 before opening the menus for Exercises 2 and 3.
