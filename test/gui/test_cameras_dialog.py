from PyQt6.QtCore import QByteArray, QBuffer, QIODevice
from PyQt6.QtGui import QColor, QImage
from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QApplication, QLabel

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


def test_cameras_dialog_loads_camera_image_async():
    app = QApplication.instance() or QApplication([])
    incident = {"road": "A-6", "province": "Madrid", "municipality": "Madrid", "km": "10.5"}
    image_payload = _tiny_png()
    dialog = CamerasDialog(FakeService(), incident, autoload=False)
    image_loaded = QSignalSpy(dialog.image_loaded)
    image_label = QLabel()

    dialog._apply_image("https://example.invalid/camera.jpg", image_payload, image_label)

    assert len(image_loaded) == 1
    assert image_loaded[0][0] == "https://example.invalid/camera.jpg"
    assert image_label.pixmap() is not None
    assert image_label.text() == ""
    dialog.close()
    app.processEvents()


def test_cameras_dialog_opens_loaded_image_fullscreen():
    app = QApplication.instance() or QApplication([])
    incident = {"road": "A-6", "province": "Madrid", "municipality": "Madrid", "km": "10.5"}
    image_payload = _tiny_png()
    dialog = CamerasDialog(FakeService(), incident, autoload=False)
    fullscreen_opened = QSignalSpy(dialog.image_fullscreen_opened)
    dialog._show_fullscreen_dialog = lambda fullscreen_dialog: None
    dialog.show()
    image_label = QLabel()

    dialog._apply_image("https://example.invalid/camera.jpg", image_payload, image_label)
    fullscreen_dialog = dialog._open_fullscreen_image(image_label.pixmap())

    assert len(fullscreen_opened) == 1
    assert fullscreen_dialog in dialog._fullscreen_dialogs
    assert dialog._fullscreen_dialogs
    dialog.close()
    app.processEvents()


def test_cameras_dialog_toggles_dark_theme():
    app = QApplication.instance() or QApplication([])
    incident = {"road": "A-6", "province": "Madrid", "municipality": "Madrid", "km": "10.5"}
    dialog = CamerasDialog(FakeService(), incident, autoload=False)

    dialog.toggle_theme()

    assert dialog.theme_button.text() == "Modo claro"
    assert "#101820" in dialog.styleSheet()
    dialog.close()
    app.processEvents()


def _tiny_png() -> bytes:
    image = QImage(2, 2, QImage.Format.Format_RGB32)
    image.fill(QColor("#b91c1c"))
    payload = QByteArray()
    buffer = QBuffer(payload)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return bytes(payload)