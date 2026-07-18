"""Main desktop window for DGT Monitor."""

from typing import Any

from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from dgt_monitor.application.facade import DgtApplicationService
from dgt_monitor.core.models import IncidentFilters
from dgt_monitor.gui.dialogs import CamerasDialog
from dgt_monitor.gui.workers import IncidentLoadWorker


class MainWindow(QMainWindow):
    load_completed = pyqtSignal()

    def __init__(self, service: DgtApplicationService, autoload: bool = True) -> None:
        super().__init__()
        self._service = service
        self._thread: QThread | None = None
        self._worker: IncidentLoadWorker | None = None
        self._items: list[dict[str, Any]] = []
        self._selected_incident: dict[str, Any] | None = None
        self._camera_dialogs: list[CamerasDialog] = []
        self.setWindowTitle("DGT Monitor")
        self.resize(1280, 780)
        self.setMinimumSize(900, 600)
        self._build_ui()
        self._apply_style()
        if autoload:
            self.reload()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(24, 20, 24, 20)
        root_layout.setSpacing(16)

        header = QHBoxLayout()
        title_group = QVBoxLayout()
        eyebrow = QLabel("CENTRO DE OPERACIONES")
        eyebrow.setObjectName("eyebrow")
        title = QLabel("DGT Monitor")
        title.setObjectName("title")
        title_group.addWidget(eyebrow)
        title_group.addWidget(title)
        header.addLayout(title_group)
        header.addStretch()
        self.status_label = QLabel("Listo")
        self.status_label.setObjectName("connectionStatus")
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.reload)
        header.addWidget(self.status_label)
        header.addWidget(self.refresh_button)
        root_layout.addLayout(header)

        controls = QFrame()
        controls.setObjectName("panel")
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(16, 12, 16, 12)
        self.province_input = QLineEdit()
        self.province_input.setPlaceholderText("Provincia")
        self.municipality_input = QLineEdit()
        self.municipality_input.setPlaceholderText("Municipio")
        self.road_input = QLineEdit()
        self.road_input.setPlaceholderText("Carretera")
        self.severity_input = QComboBox()
        self.severity_input.addItem("Todas las gravedades", "")
        self.severity_input.addItem("Muy alta", "highest")
        self.severity_input.addItem("Alta", "high")
        self.severity_input.addItem("Media", "medium")
        self.severity_input.addItem("Baja", "low")
        for widget in (self.province_input, self.municipality_input, self.road_input, self.severity_input):
            controls_layout.addWidget(widget)
        apply_button = QPushButton("Aplicar filtros")
        apply_button.setObjectName("primaryButton")
        apply_button.clicked.connect(self.reload)
        controls_layout.addWidget(apply_button)
        root_layout.addWidget(controls)

        stats = QGridLayout()
        stats.setSpacing(12)
        self.stat_labels: dict[str, QLabel] = {}
        for column, (key, label) in enumerate((
            ("total", "Total"),
            ("accidents", "Accidentes"),
            ("roadworks", "Obras"),
            ("obstructions", "Obstáculos"),
            ("weather", "Clima"),
        )):
            card = QFrame()
            card.setObjectName("statCard")
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(label))
            value = QLabel("--")
            value.setObjectName("statValue")
            card_layout.addWidget(value)
            self.stat_labels[key] = value
            stats.addWidget(card, 0, column)
        root_layout.addLayout(stats)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(("Gravedad", "Carretera", "Municipio", "Provincia", "Tipo", "PK", "Cámaras"))
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        vertical_header = self.table.verticalHeader()
        if vertical_header:
            vertical_header.setVisible(False)
        horizontal_header = self.table.horizontalHeader()
        if horizontal_header:
            horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self._show_selection)
        splitter.addWidget(self.table)

        detail_frame = QFrame()
        detail_frame.setObjectName("panel")
        detail_layout = QVBoxLayout(detail_frame)
        detail_title = QLabel("Detalle del incidente")
        detail_title.setObjectName("sectionTitle")
        self.detail = QTextBrowser()
        self.detail.setOpenExternalLinks(True)
        self.detail.setHtml("<p>Selecciona una incidencia para consultar sus datos.</p>")
        self.cameras_button = QPushButton("Ver cámaras")
        self.cameras_button.setEnabled(False)
        self.cameras_button.clicked.connect(self.open_cameras_dialog)
        detail_layout.addWidget(detail_title)
        detail_layout.addWidget(self.detail)
        detail_layout.addWidget(self.cameras_button)
        splitter.addWidget(detail_frame)
        splitter.setSizes((900, 320))
        root_layout.addWidget(splitter, 1)

        self.setCentralWidget(root)
        self.setTabOrder(self.province_input, self.municipality_input)
        self.setTabOrder(self.municipality_input, self.road_input)
        self.setTabOrder(self.road_input, self.severity_input)
        self.setTabOrder(self.severity_input, self.refresh_button)

    def reload(self) -> None:
        if self._thread and self._thread.isRunning():
            return
        filters = IncidentFilters(
            province=self.province_input.text().strip() or None,
            municipality=self.municipality_input.text().strip() or None,
            road=self.road_input.text().strip().upper() or None,
            severity=self.severity_input.currentData() or None,
        )
        self.refresh_button.setEnabled(False)
        self.status_label.setText("Actualizando...")
        self._thread = QThread(self)
        self._worker = IncidentLoadWorker(self._service, filters)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.loaded.connect(self._apply_payload)
        self._worker.error.connect(self._show_error)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._load_finished)
        self._thread.start()

    def _apply_payload(self, payload: object) -> None:
        data = payload if isinstance(payload, dict) else {}
        self._items = list(data.get("items", []))
        stats = data.get("stats", {})
        for key, label in self.stat_labels.items():
            label.setText(str(stats.get(key, 0)))
        self.table.setRowCount(len(self._items))
        for row, incident in enumerate(self._items):
            values = (
                self._severity_label(incident.get("severity", "")),
                incident.get("road", ""),
                incident.get("municipality", ""),
                incident.get("province", ""),
                incident.get("type_label") or incident.get("type", ""),
                incident.get("km", ""),
                str(incident.get("camera_coverage_count", 0)),
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value or "--"))
                if column == 0:
                    item.setForeground(self._severity_color(incident.get("severity", "")))
                self.table.setItem(row, column, item)
        self.status_label.setText(f"En línea · {len(self._items)} incidencias")

    def _show_selection(self) -> None:
        row = self.table.currentRow()
        if row < 0 or row >= len(self._items):
            self._selected_incident = None
            self.cameras_button.setEnabled(False)
            return
        incident = self._items[row]
        self._selected_incident = incident
        self.cameras_button.setEnabled(True)
        fields = (
            ("Carretera", incident.get("road")),
            ("Punto kilométrico", incident.get("km")),
            ("Ubicación", " · ".join(filter(None, (incident.get("municipality"), incident.get("province"))))),
            ("Tipo", incident.get("type_label") or incident.get("type")),
            ("Causa", incident.get("cause_label") or incident.get("cause")),
            ("Dirección", incident.get("direction_label") or incident.get("direction")),
            ("Inicio", incident.get("start_time")),
            ("Cobertura de cámaras", incident.get("camera_coverage_count", 0)),
        )
        rows = "".join(f"<tr><th>{name}</th><td>{value or '--'}</td></tr>" for name, value in fields)
        self.detail.setHtml(f"<table>{rows}</table>")

    def open_cameras_dialog(self) -> CamerasDialog | None:
        if not self._selected_incident:
            return None
        dialog = CamerasDialog(self._service, self._selected_incident, self)
        self._camera_dialogs.append(dialog)
        dialog.destroyed.connect(lambda _=None, item=dialog: self._forget_camera_dialog(item))
        dialog.show()
        return dialog

    def _forget_camera_dialog(self, dialog: CamerasDialog) -> None:
        if dialog in self._camera_dialogs:
            self._camera_dialogs.remove(dialog)

    def _show_error(self, message: str) -> None:
        self.status_label.setText("Sin conexión")
        QMessageBox.warning(self, "No se pudieron cargar los datos", message)

    def _load_finished(self) -> None:
        self.refresh_button.setEnabled(True)
        if self._worker:
            self._worker.deleteLater()
        if self._thread:
            self._thread.deleteLater()
        self._worker = None
        self._thread = None
        self.load_completed.emit()

    def closeEvent(self, event) -> None:
        for dialog in list(self._camera_dialogs):
            dialog.close()
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(1000)
        super().closeEvent(event)

    @staticmethod
    def _severity_label(value: str) -> str:
        return {"highest": "Muy alta", "high": "Alta", "medium": "Media", "low": "Baja"}.get(value.lower(), value or "Sin dato")

    @staticmethod
    def _severity_color(value: str) -> QColor:
        return QColor({"highest": "#b91c1c", "high": "#dc2626", "medium": "#b45309", "low": "#15803d"}.get(value.lower(), "#475569"))

    def _apply_style(self) -> None:
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #f4f6f5; color: #17212b; font-family: 'Segoe UI'; font-size: 13px; }
            QLabel#eyebrow { color: #b91c1c; font-size: 11px; font-weight: 700; }
            QLabel#title { font-size: 30px; font-weight: 700; }
            QLabel#sectionTitle { font-size: 18px; font-weight: 700; }
            QLabel#connectionStatus { color: #475569; font-weight: 600; padding: 0 10px; }
            QFrame#panel, QFrame#statCard { background: white; border: 1px solid #d7dde1; border-radius: 3px; }
            QFrame#statCard QLabel#statValue { color: #b91c1c; font-size: 26px; font-weight: 700; }
            QLineEdit, QComboBox { min-height: 36px; padding: 0 10px; background: white; border: 1px solid #b8c1c8; border-radius: 3px; }
            QLineEdit:focus, QComboBox:focus { border-color: #b91c1c; }
            QPushButton { min-height: 36px; padding: 0 16px; background: white; border: 1px solid #aeb7be; border-radius: 3px; font-weight: 600; }
            QPushButton:hover { border-color: #17212b; }
            QPushButton#primaryButton { background: #b91c1c; color: white; border: 0; }
            QPushButton#primaryButton:hover { background: #991b1b; }
            QTableWidget { background: white; alternate-background-color: #f8fafb; border: 1px solid #d7dde1; gridline-color: #e2e7ea; selection-background-color: #fee2e2; selection-color: #17212b; }
            QHeaderView::section { min-height: 34px; background: #e9edef; border: 0; border-right: 1px solid #d7dde1; padding: 0 8px; font-weight: 700; }
            QTextBrowser { background: white; border: 0; }
        """)