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
                "camera_coverage_count": 2,
            }],
        }


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