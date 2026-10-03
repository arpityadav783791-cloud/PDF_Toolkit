from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from app.application.app_context import AppContext
from app.config.constants import (
    APP_NAME,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
)
from app.ui.dashboard.dashboard import Dashboard


class MainWindow(QMainWindow):
    def __init__(self, context: AppContext) -> None:
        super().__init__()

        self.context = context

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.dashboard = Dashboard(self.context)
        self.setCentralWidget(self.dashboard)

    def show_dashboard(self) -> None:
        self.setCentralWidget(self.dashboard)
