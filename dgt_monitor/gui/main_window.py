"""Main desktop window for DGT Monitor."""

from datetime import datetime
from typing import Any

from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QComboBox,
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
from dgt_monitor.gui.theme import ThemeName, main_window_stylesheet, next_theme, normalize_theme
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
        self._theme: ThemeName = "light"
        self._kind_filter = ""
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
        self.theme_button = QPushButton("Modo oscuro")
        self.theme_button.clicked.connect(self.toggle_theme)
        header.addWidget(self.status_label)
        header.addWidget(self.theme_button)
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
        self.match_mode_input = QComboBox()
        self.match_mode_input.addItem("Contiene", "contains")
        self.match_mode_input.addItem("Exacta", "exact")
        self.match_mode_input.addItem("Regex", "regex")
        self.severity_input = QComboBox()
        self.severity_input.addItem("Todas las gravedades", "")
        self.severity_input.addItem("Muy alta", "highest")
        self.severity_input.addItem("Alta", "high")
        self.severity_input.addItem("Media", "medium")
        self.severity_input.addItem("Baja", "low")
        self.camera_input = QComboBox()
        self.camera_input.addItem("Todas las cámaras", "")
        self.camera_input.addItem("Con cámara", "with")
        self.camera_input.addItem("Sin cámara", "without")
        for widget in (self.province_input, self.municipality_input, self.road_input, self.match_mode_input, self.severity_input, self.camera_input):
            controls_layout.addWidget(widget)
        apply_button = QPushButton("Aplicar filtros")
        apply_button.setObjectName("primaryButton")
        apply_button.clicked.connect(self.reload)
        controls_layout.addWidget(apply_button)
        clear_button = QPushButton("Limpiar")
        clear_button.clicked.connect(self.clear_filters)
        controls_layout.addWidget(clear_button)
        root_layout.addWidget(controls)

        stats = QGridLayout()
        stats.setSpacing(12)
        self.stat_labels: dict[str, QLabel] = {}
        self.stat_buttons: dict[str, QPushButton] = {}
        for column, (key, label) in enumerate((
            ("total", "Total"),
            ("accidents", "Accidentes"),
            ("roadworks", "Obras"),
            ("stuck", "Averías"),
            ("obstructions", "Obstáculos"),
            ("weather", "Clima"),
        )):
            card = QPushButton()
            card.setObjectName("statCard")
            card.setProperty("kind", self._kind_for_stat(key))
            card.clicked.connect(lambda _checked=False, kind=self._kind_for_stat(key): self._set_kind_filter(kind))
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(label), alignment=Qt.AlignmentFlag.AlignCenter)
            value = QLabel("--")
            value.setObjectName("statValue")
            value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(value)
            self.stat_labels[key] = value
            self.stat_buttons[key] = card
            stats.addWidget(card, 0, column)
        self._sync_stat_buttons()
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
        self.setTabOrder(self.road_input, self.match_mode_input)
        self.setTabOrder(self.match_mode_input, self.severity_input)
        self.setTabOrder(self.severity_input, self.camera_input)
        self.setTabOrder(self.camera_input, self.refresh_button)

    def reload(self) -> None:
        if self._thread and self._thread.isRunning():
            return
        filters = IncidentFilters(
            province=self.province_input.text().strip() or None,
            municipality=self.municipality_input.text().strip() or None,
            road=self.road_input.text().strip().upper() or None,
            severity=self.severity_input.currentData() or None,
            kind=self._kind_filter or None,
            camera=self.camera_input.currentData() or None,
            match_mode=self.match_mode_input.currentData() or "contains",
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

    def clear_filters(self) -> None:
        self.province_input.clear()
        self.municipality_input.clear()
        self.road_input.clear()
        self.match_mode_input.setCurrentIndex(0)
        self.severity_input.setCurrentIndex(0)
        self.camera_input.setCurrentIndex(0)
        self._set_kind_filter("", reload=False)
        self.reload()

    def _set_kind_filter(self, kind: str, reload: bool = True) -> None:
        self._kind_filter = kind
        self._sync_stat_buttons()
        if reload:
            self.reload()

    def _sync_stat_buttons(self) -> None:
        for key, button in self.stat_buttons.items():
            active = self._kind_for_stat(key) == self._kind_filter
            button.setProperty("active", active)
            style = button.style()
            if style:
                style.unpolish(button)
                style.polish(button)

    @staticmethod
    def _kind_for_stat(key: str) -> str:
        return {
            "total": "",
            "accidents": "accident",
            "roadworks": "roadworks",
            "stuck": "stuck",
            "obstructions": "obstruction",
            "weather": "weather",
        }[key]

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
            ("Inicio", self._format_datetime(incident.get("start_time"))),
            ("Fin", self._format_datetime(incident.get("end_time"))),
            ("Cobertura de cámaras", incident.get("camera_coverage_count", 0)),
        )
        rows = "".join(f"<tr><th>{name}</th><td>{value or '--'}</td></tr>" for name, value in fields)
        self.detail.setHtml(f"<table>{rows}</table>")

    def open_cameras_dialog(self) -> CamerasDialog | None:
        if not self._selected_incident:
            return None
        dialog = CamerasDialog(self._service, self._selected_incident, self, theme=self._theme)
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

    def toggle_theme(self) -> None:
        self.set_theme(next_theme(self._theme))

    def set_theme(self, theme: str) -> None:
        self._theme = normalize_theme(theme)
        self.theme_button.setText("Modo claro" if self._theme == "dark" else "Modo oscuro")
        self._apply_style()
        for dialog in list(self._camera_dialogs):
            dialog.set_theme(self._theme)

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

    @staticmethod
    def _format_datetime(value: object) -> str:
        if not value:
            return ""
        text = str(value)
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return text
        return parsed.strftime("%d/%m/%Y %H:%M")

    def _apply_style(self) -> None:
        self.setStyleSheet(main_window_stylesheet(self._theme))