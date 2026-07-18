"""Non-modal camera dialog for selected incidents."""

from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.models import CameraFilters
from dgt_monitor.gui.workers import CameraLoadWorker, ImageLoadWorker


class CamerasDialog(QDialog):
    load_completed = pyqtSignal()
    image_loaded = pyqtSignal(str)

    def __init__(
        self,
        service: DgtApplicationService,
        incident: dict[str, Any],
        parent: QWidget | None = None,
        autoload: bool = True,
        image_downloader: Callable[[str], bytes] | None = None,
    ) -> None:
        super().__init__(parent)
        self._service = service
        self._incident = incident
        self._image_downloader = image_downloader
        self._thread: QThread | None = None
        self._worker: CameraLoadWorker | None = None
        self._image_jobs: list[tuple[QThread, ImageLoadWorker]] = []
        self._items: list[dict[str, Any]] = []
        self.setModal(False)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setWindowTitle(self._title_for_incident())
        self.resize(720, 520)
        self._build_ui()
        self._apply_style()
        if autoload:
            self.reload()

    @property
    def items(self) -> list[dict[str, Any]]:
        return list(self._items)

    def reload(self) -> None:
        if self._thread and self._thread.isRunning():
            return
        self.refresh_button.setEnabled(False)
        self.status_label.setText("Buscando cámaras cercanas...")
        self._clear_cards()
        self._thread = QThread(self)
        self._worker = CameraLoadWorker(self._service, self._filters())
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.loaded.connect(self._apply_payload)
        self._worker.error.connect(self._show_error)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._load_finished)
        self._thread.start()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title_group = QVBoxLayout()
        title = QLabel(self._title_for_incident())
        title.setObjectName("dialogTitle")
        subtitle = QLabel(self._subtitle_for_incident())
        subtitle.setObjectName("dialogSubtitle")
        title_group.addWidget(title)
        title_group.addWidget(subtitle)
        header.addLayout(title_group)
        header.addStretch()
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.reload)
        header.addWidget(self.refresh_button)
        layout.addLayout(header)

        self.status_label = QLabel("Listo")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.cards_host = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_host)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()
        self.scroll.setWidget(self.cards_host)
        layout.addWidget(self.scroll, 1)

    def _filters(self) -> CameraFilters:
        return CameraFilters(
            province=self._clean(self._incident.get("province")),
            road=self._clean(self._incident.get("road")),
            kilometer=self._clean(self._incident.get("km")),
            latitude=self._incident.get("latitude"),
            longitude=self._incident.get("longitude"),
            limit=12,
            max_km_delta=1.0,
        )

    def _apply_payload(self, payload: object) -> None:
        data = payload if isinstance(payload, dict) else {}
        self._items = list(data.get("items", []))
        self._clear_cards()
        if not self._items:
            self.cards_layout.insertWidget(0, self._empty_card("No hay cámaras cercanas para esta incidencia."))
        else:
            for camera in self._items:
                self.cards_layout.insertWidget(self.cards_layout.count() - 1, self._camera_card(camera))
        self.status_label.setText(f"{len(self._items)} cámaras encontradas")

    def _camera_card(self, camera: dict[str, Any]) -> QFrame:
        card = QFrame()
        card.setObjectName("cameraCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        title = QLabel(f"{camera.get('road') or 'Carretera sin dato'} · PK {camera.get('km') or '--'}")
        title.setObjectName("cameraTitle")
        meta = QLabel(self._camera_meta(camera))
        meta.setObjectName("cameraMeta")
        image = QLabel("Cargando imagen..." if camera.get("image_url") else "Imagen no disponible")
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setMinimumHeight(190)
        image.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        image.setWordWrap(True)
        image.setObjectName("cameraImage")
        layout.addWidget(title)
        layout.addWidget(meta)
        layout.addWidget(image)
        if camera.get("image_url"):
            self._load_image(str(camera["image_url"]), image)
        return card

    def _empty_card(self, message: str) -> QFrame:
        card = QFrame()
        card.setObjectName("cameraCard")
        layout = QVBoxLayout(card)
        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)
        return card

    def _show_error(self, message: str) -> None:
        self._items = []
        self._clear_cards()
        self.cards_layout.insertWidget(0, self._empty_card(message or "No se pudieron cargar las cámaras."))
        self.status_label.setText("Error al cargar cámaras")

    def _load_finished(self) -> None:
        self.refresh_button.setEnabled(True)
        if self._worker:
            self._worker.deleteLater()
        if self._thread:
            self._thread.deleteLater()
        self._worker = None
        self._thread = None
        self.load_completed.emit()

    def _load_image(self, url: str, label: QLabel) -> None:
        thread = QThread(self)
        worker = ImageLoadWorker(url, self._image_downloader)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.loaded.connect(lambda loaded_url, payload, target=label: self._apply_image(loaded_url, payload, target))
        worker.error.connect(lambda _url, message, target=label: target.setText(message or "Imagen no disponible"))
        worker.finished.connect(thread.quit)
        thread.finished.connect(lambda item=(thread, worker): self._forget_image_job(item))
        self._image_jobs.append((thread, worker))
        thread.start()

    def _apply_image(self, url: str, payload: object, label: QLabel) -> None:
        image_bytes = payload if isinstance(payload, bytes) else bytes(payload)
        pixmap = QPixmap()
        if pixmap.loadFromData(image_bytes):
            label.setPixmap(pixmap.scaledToWidth(460, Qt.TransformationMode.SmoothTransformation))
            label.setText("")
        else:
            label.setText("Imagen no disponible")
        self.image_loaded.emit(url)

    def _forget_image_job(self, item: tuple[QThread, ImageLoadWorker]) -> None:
        thread, worker = item
        if item in self._image_jobs:
            self._image_jobs.remove(item)
        worker.deleteLater()
        thread.deleteLater()

    def _clear_cards(self) -> None:
        for thread, _worker in list(self._image_jobs):
            if thread.isRunning():
                thread.quit()
                thread.wait(1000)
        self._image_jobs.clear()
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def closeEvent(self, event) -> None:
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(1000)
        for thread, _worker in list(self._image_jobs):
            if thread.isRunning():
                thread.quit()
                thread.wait(1000)
        self._image_jobs.clear()
        super().closeEvent(event)

    def _title_for_incident(self) -> str:
        road = self._incident.get("road") or "incidencia"
        km = self._incident.get("km")
        return f"Cámaras cercanas · {road}{f' PK {km}' if km else ''}"

    def _subtitle_for_incident(self) -> str:
        location = " · ".join(filter(None, (self._incident.get("municipality"), self._incident.get("province"))))
        return location or "Búsqueda por carretera, provincia y punto kilométrico"

    @staticmethod
    def _camera_meta(camera: dict[str, Any]) -> str:
        parts = [camera.get("province") or "Provincia no disponible"]
        km_delta = camera.get("km_delta")
        distance_km = camera.get("distance_km")
        if km_delta is not None:
            parts.append(f"Δ PK {float(km_delta):.3f}")
        if distance_km is not None:
            parts.append(f"{float(distance_km):.2f} km")
        return " · ".join(parts)

    @staticmethod
    def _clean(value: object) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def _apply_style(self) -> None:
        self.setStyleSheet("""
            QDialog { background: #f4f6f5; color: #17212b; font-family: 'Segoe UI'; font-size: 13px; }
            QLabel#dialogTitle { font-size: 20px; font-weight: 700; }
            QLabel#dialogSubtitle, QLabel#statusLabel, QLabel#cameraMeta { color: #64717d; }
            QScrollArea { border: 0; background: transparent; }
            QFrame#cameraCard { background: white; border: 1px solid #d7dde1; border-radius: 3px; }
            QLabel#cameraTitle { font-size: 16px; font-weight: 700; color: #b91c1c; }
            QLabel#cameraImage { color: #475569; background: #eef1f2; padding: 8px; border-radius: 3px; }
            QPushButton { min-height: 34px; padding: 0 14px; background: white; border: 1px solid #aeb7be; border-radius: 3px; font-weight: 600; }
            QPushButton:hover { border-color: #17212b; }
        """)