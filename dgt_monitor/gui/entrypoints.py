"""Desktop application entrypoints."""

import sys

from PyQt6.QtWidgets import QApplication

from dgt_monitor.bootstrap import build_application
from dgt_monitor.gui.main_window import MainWindow


def run() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("DGT Monitor")
    window = MainWindow(build_application())
    window.show()
    return app.exec()