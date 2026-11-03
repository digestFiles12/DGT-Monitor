import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from dgt_monitor import menu

SAMPLE_XML = Path(__file__).resolve().parents[1] / "fixtures" / "incidents_sample.xml"


@pytest.fixture(scope="module")
def data(tmp_path_factory):
    output = tmp_path_factory.mktemp("menu") / "grouped.json"
    return menu.load_grouped_data(str(SAMPLE_XML), None, str(output))


def scripted(answers):
    remaining = iter(answers)
    return lambda _prompt: next(remaining)


def test_exercise_1_writes_grouped_json(tmp_path):
    output = tmp_path / "out" / "grouped.json"
    data = menu.load_grouped_data(str(SAMPLE_XML), None, str(output))
    assert json.loads(output.read_text(encoding="utf-8"))["total"] == data["total"] == 90


def test_existing_json_is_reused(tmp_path):
    source = tmp_path / "grouped.json"
    source.write_text(json.dumps({"total": 3}), encoding="utf-8")
    assert menu.load_grouped_data(None, str(source), str(tmp_path / "unused.json")) == {"total": 3}
    assert not (tmp_path / "unused.json").exists()


def test_top_groups_limits_and_merges_others():
    groups = {name: {"total": value} for name, value in {"a": 5, "b": 4, "c": 3, "d": 2, "e": 0}.items()}
    assert menu.top_groups(groups, "total", 2, add_others=False) == [("a", 5), ("b", 4)]
    assert menu.top_groups(groups, "total", 2, add_others=True) == [("a", 5), ("b", 4), ("Otros", 5)]


def test_describe_extremes_reports_max_and_min(data):
    text = menu.describe_extremes(data["by_province"], "total")
    assert text.startswith("Máximo: ") and "\nMínimo: " in text
    assert menu.describe_extremes({}, "total") == "No hay datos para este indicador."


def test_pie_menu_loops_until_exit(data):
    shown, lines = [], []
    menu.run_chart_menu(
        data["by_province"], "pie",
        ask=scripted(["1", "x", "4", "7"]), say=lines.append, show=lambda figure: shown.append(figure),
    )
    assert len(shown) == 2
    assert any("no válida" in line for line in lines)
    assert sum(line.startswith("Máximo:") for line in lines) == 2
    plt.close("all")


def test_main_menu_bar_charts_by_region(data):
    shown, lines = [], []
    menu.run_main_menu(
        data, ask=scripted(["1", "2", "2", "7", "3"]), say=lines.append, show=lambda figure: shown.append(figure)
    )
    assert len(shown) == 1
    assert lines[-1] == "Hasta luego."
    plt.close("all")


def test_main_menu_rejects_invalid_options(data):
    lines = []
    menu.run_main_menu(data, ask=scripted(["9", "1", "7", "3"]), say=lines.append, show=lambda _figure: None)
    assert sum("no válida" in line for line in lines) == 2


def test_main_runs_offline_with_xml_file(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", scripted(["3"]))
    menu.main(["--xml", str(SAMPLE_XML), "--output", str(tmp_path / "grouped.json")])
    assert "90 incidencias" in capsys.readouterr().out
    assert (tmp_path / "grouped.json").exists()
