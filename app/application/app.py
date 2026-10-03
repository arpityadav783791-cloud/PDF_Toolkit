from __future__ import annotations

from PySide6.QtWidgets import QApplication

from app.application.app_context import AppContext
from app.ui.main_window.main_window import MainWindow


class PdfToolkitApplication:
    def __init__(self, qt_app: QApplication) -> None:
        self.qt_app = qt_app
        self.context = AppContext()
        self.main_window: MainWindow | None = None

    def initialize(self) -> None:
        self.context.initialize()

        self.main_window = MainWindow(self.context)
        self.main_window.show()

    def run(self) -> int:
        return self.qt_app.exec()

    def shutdown(self) -> None:
        self.context.shutdown()
