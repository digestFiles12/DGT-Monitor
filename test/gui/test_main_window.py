from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QApplication

from dgt_monitor.gui.main_window import MainWindow


class FakeService:
    def __init__(self):
        self.last_filters = None

    def get_incident_payload(self, filters) -> dict:
        self.last_filters = filters
        return {
            "count": 1,
            "stats": {"total": 1, "accidents": 1, "roadworks": 0, "stuck": 0, "obstructions": 0, "weather": 0},
            "items": [{
                "severity": "high",
                "road": "A-6",
                "municipality": "Madrid",
                "province": filters.province or "Madrid",
                "type_label": "Accidente",
                "km": "10.5",
                "start_time": "2026-07-19T10:30:00+00:00",
                "end_time": "2026-07-19T11:45:00+00:00",
                "latitude": 40.4,
                "longitude": -3.7,
                "camera_coverage_count": 2,
            }],
        }

    def get_cameras(self, filters) -> dict:
        return {"count": 1, "items": [{"road": filters.road, "province": filters.province, "km": "10.6"}]}


def test_main_window_loads_and_renders_incidents():
    app = QApplication.instance() or QApplication([])
    fake = FakeService()
    window = MainWindow(fake, autoload=False)
    completed = QSignalSpy(window.load_completed)
    window.province_input.setText("Madrid")
    window.match_mode_input.setCurrentIndex(1)

    window.reload()

    assert completed.wait(1000)
    assert window.table.rowCount() == 1
    assert window.table.item(0, 1).text() == "A-6"
    assert window.stat_labels["total"].text() == "1"
    assert "stuck" in window.stat_labels
    assert window.refresh_button.isEnabled()
    assert fake.last_filters.province == "Madrid"
    assert fake.last_filters.match_mode == "exact"
    window.table.selectRow(0)
    app.processEvents()
    assert "19/07/2026 10:30" in window.detail.toHtml()
    window.close()
    app.processEvents()


def test_main_window_applies_camera_and_stat_filters():
    app = QApplication.instance() or QApplication([])
    fake = FakeService()
    window = MainWindow(fake, autoload=False)
    completed = QSignalSpy(window.load_completed)
    window.camera_input.setCurrentIndex(1)

    window._set_kind_filter("roadworks", reload=False)
    window.reload()

    assert completed.wait(1000)
    assert fake.last_filters.camera == "with"
    assert fake.last_filters.kind == "roadworks"
    assert window.stat_buttons["roadworks"].property("active") is True
    window.clear_filters()
    assert completed.wait(1000)
    assert fake.last_filters.camera is None
    assert fake.last_filters.kind is None
    assert fake.last_filters.match_mode == "contains"
    window.close()
    app.processEvents()


def test_main_window_opens_non_modal_camera_dialog():
    app = QApplication.instance() or QApplication([])
    window = MainWindow(FakeService(), autoload=False)
    completed = QSignalSpy(window.load_completed)
    window.reload()
    assert completed.wait(1000)

    window.table.selectRow(0)
    app.processEvents()
    dialog = window.open_cameras_dialog()

    assert dialog is not None
    assert not dialog.isModal()
    assert dialog in window._camera_dialogs
    dialog.close()
    window.close()
    app.processEvents()


def test_main_window_toggles_dark_theme():
    app = QApplication.instance() or QApplication([])
    window = MainWindow(FakeService(), autoload=False)

    window.toggle_theme()

    assert window.theme_button.text() == "Modo claro"
    assert "#101820" in window.styleSheet()
    window.close()
    app.processEvents()