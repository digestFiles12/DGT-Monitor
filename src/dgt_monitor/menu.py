"""Console menu for the final project (exercises 1, 2 and 3 of the assignment).

Run with: python -m dgt_monitor.menu [--xml FILE] [--json FILE] [--output FILE]

Exercise 1: build the grouped JSON file from the DGT XML.
Exercise 2: menu (infinite loop) with one bar chart per indicator.
Exercise 3: menu (infinite loop) with one pie chart per indicator, followed by
            the group with the maximum and the group with the minimum.
"""

import argparse
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dgt_monitor.application.statistics import DEFAULT_GROUPED_JSON, find_extremes, group_incidents, write_grouped_json
from dgt_monitor.core.constants import DGT_INCIDENTS_URL
from dgt_monitor.infrastructure.http import RequestsXmlClient
from dgt_monitor.infrastructure.parsers import IncidentParser

# Menu option -> (indicator key in the JSON, label shown to the user).
INDICATOR_OPTIONS = {
    "1": ("total", "Incidencias totales"),
    "2": ("severe", "Incidencias graves"),
    "3": ("roadworks", "Obras"),
    "4": ("road_closures", "Cortes de carretera"),
}
EXIT_OPTION = "5"
MAX_BARS = 15
MAX_SLICES = 8

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]
ShowFunction = Callable[[Any], None]


def load_grouped_data(xml_path: str | None, json_path: str | None, output_path: str) -> dict[str, Any]:
    """Exercise 1: return the grouped data, writing it to the JSON file when it is built from XML."""
    if json_path:
        return json.loads(Path(json_path).read_text(encoding="utf-8"))
    if xml_path:
        xml_content = Path(xml_path).read_text(encoding="utf-8")
    else:
        xml_content = RequestsXmlClient().get(DGT_INCIDENTS_URL)
    data = group_incidents(IncidentParser().parse(xml_content))
    write_grouped_json(data, output_path)
    return data


def top_groups(groups: dict[str, dict[str, int]], indicator: str, limit: int, add_others: bool) -> list[tuple[str, int]]:
    """Return (name, value) pairs sorted from highest to lowest, ignoring zeros.

    When add_others is True, everything after the first `limit` groups is merged into "Otros".
    """
    pairs = sorted(
        ((name, leaf[indicator]) for name, leaf in groups.items() if leaf[indicator] > 0),
        key=lambda pair: (-pair[1], pair[0]),
    )
    if not add_others:
        return pairs[:limit]
    rest = sum(value for _, value in pairs[limit:])
    return pairs[:limit] + ([("Otros", rest)] if rest else [])


def describe_extremes(groups: dict[str, dict[str, int]], indicator: str) -> str:
    """Return the text with the group that has the maximum and the one with the minimum."""
    extremes = find_extremes(groups)[indicator]
    if extremes["max"] is None or extremes["min"] is None:
        return "No hay datos para este indicador."
    maximum, minimum = extremes["max"], extremes["min"]
    return (
        f"Máximo: {maximum['name']} ({maximum['value']})\n"
        f"Mínimo: {minimum['name']} ({minimum['value']})"
    )


def build_bar_chart(groups: dict[str, dict[str, int]], indicator: str, title: str):
    """Build a horizontal bar chart of the top groups for one indicator."""
    import matplotlib.pyplot as plt

    pairs = top_groups(groups, indicator, MAX_BARS, add_others=False)
    figure, axes = plt.subplots(figsize=(9, 6))
    axes.barh([name for name, _ in pairs][::-1], [value for _, value in pairs][::-1], color="#2563eb")
    axes.set_title(title)
    axes.set_xlabel("Incidencias")
    figure.tight_layout()
    return figure


def build_pie_chart(groups: dict[str, dict[str, int]], indicator: str, title: str):
    """Build a pie chart ('queso') of the share of every group for one indicator."""
    import matplotlib.pyplot as plt

    pairs = top_groups(groups, indicator, MAX_SLICES, add_others=True)
    figure, axes = plt.subplots(figsize=(8, 8))
    axes.pie([value for _, value in pairs], labels=[name for name, _ in pairs], autopct="%1.1f%%", startangle=90)
    axes.set_title(title)
    figure.tight_layout()
    return figure


def show_figure(figure: Any) -> None:
    """Open the figure in a window and wait until the user closes it."""
    import matplotlib.pyplot as plt

    plt.show()
    plt.close(figure)

def run_chart_menu(
    groups: dict[str, dict[str, int]],
    kind: str,
    ask: InputFunction = input,
    say: OutputFunction = print,
    show: ShowFunction = show_figure,
) -> None:
    """Infinite menu loop: options 1-4 show a chart, option 5 goes back."""
    builder = build_pie_chart if kind == "pie" else build_bar_chart
    while True:
        say("\n¿Qué gráfica quieres visualizar?")
        for option, (_, label) in INDICATOR_OPTIONS.items():
            say(f"{option}. {label}")
        say(f"{EXIT_OPTION}. Salir")
        answer = ask("Opción: ").strip()
        if answer == EXIT_OPTION:
            return
        if answer not in INDICATOR_OPTIONS:
            say("Opción no válida, elige un número del 1 al 5.")
            continue
        indicator, label = INDICATOR_OPTIONS[answer]
        show(builder(groups, indicator, label))
        say(describe_extremes(groups, indicator))


def run_main_menu(
    data: dict[str, Any],
    ask: InputFunction = input,
    say: OutputFunction = print,
    show: ShowFunction = show_figure,
) -> None:
    """Main menu: choose the grouping level and the kind of chart."""
    levels = {"1": ("by_province", "provincia"), "2": ("by_region", "comunidad autónoma")}
    while True:
        say("\n=== DGT Monitor ===")
        say("1. Gráficas de barras (ejercicio 2)")
        say("2. Gráficas de queso (ejercicio 3)")
        say("3. Salir")
        answer = ask("Opción: ").strip()
        if answer == "3":
            say("Hasta luego.")
            return
        if answer not in ("1", "2"):
            say("Opción no válida, elige un número del 1 al 3.")
            continue
        say("\nAgrupar por:")
        say("1. Provincia")
        say("2. Comunidad autónoma")
        level = ask("Opción: ").strip()
        if level not in levels:
            say("Opción no válida, elige 1 o 2.")
            continue
        key, _ = levels[level]
        run_chart_menu(data[key], "bar" if answer == "1" else "pie", ask, say, show)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Console menu with the DGT incident charts.")
    parser.add_argument("--xml", help="read incidents from a local DATEX II XML file instead of downloading them")
    parser.add_argument("--json", help="reuse an existing grouped JSON file (skips exercise 1)")
    parser.add_argument("--output", default=DEFAULT_GROUPED_JSON, help="grouped JSON file to write")
    args = parser.parse_args(argv)
    data = load_grouped_data(args.xml, args.json, args.output)
    print(f"Datos cargados: {data['total']} incidencias.")
    run_main_menu(data, ask=input)


if __name__ == "__main__":
    main()
