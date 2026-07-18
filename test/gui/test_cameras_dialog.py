from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QApplication

from dgt_monitor.gui.dialogs import CamerasDialog


class FakeService:
    def get_cameras(self, filters) -> dict:
        return {
            "count": 1,
            "items": [{
                "road": filters.road,
                "province": filters.province,
                "km": "10.6",
                "image_url": "https://example.invalid/camera.jpg",
                "km_delta": 0.1,
                "distance_km": 0.5,
            }],
        }


def test_cameras_dialog_loads_nearby_cameras():
    app = QApplication.instance() or QApplication([])
    incident = {"road": "A-6", "province": "Madrid", "municipality": "Madrid", "km": "10.5"}
    dialog = CamerasDialog(FakeService(), incident, autoload=False)
    completed = QSignalSpy(dialog.load_completed)

    dialog.reload()

    assert completed.wait(1000)
    assert dialog.items[0]["road"] == "A-6"
    assert "1 cámaras" in dialog.status_label.text()
    dialog.close()
    app.processEvents()