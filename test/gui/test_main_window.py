from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QApplication

from dgt_monitor.gui.main_window import MainWindow


class FakeService:
    def get_incident_payload(self, filters) -> dict:
        return {
            "count": 1,
            "stats": {"total": 1, "accidents": 1},
            "items": [{
                "severity": "high",
                "road": "A-6",
                "municipality": "Madrid",
                "province": filters.province or "Madrid",
                "type_label": "Accidente",
                "km": "10.5",
                "latitude": 40.4,
                "longitude": -3.7,
                "camera_coverage_count": 2,
            }],
        }

    def get_cameras(self, filters) -> dict:
        return {"count": 1, "items": [{"road": filters.road, "province": filters.province, "km": "10.6"}]}


def test_main_window_loads_and_renders_incidents():
    app = QApplication.instance() or QApplication([])
    window = MainWindow(FakeService(), autoload=False)
    completed = QSignalSpy(window.load_completed)
    window.province_input.setText("Madrid")

    window.reload()

    assert completed.wait(1000)
    assert window.table.rowCount() == 1
    assert window.table.item(0, 1).text() == "A-6"
    assert window.stat_labels["total"].text() == "1"
    assert window.refresh_button.isEnabled()
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