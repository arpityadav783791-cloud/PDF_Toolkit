from __future__ import annotations

from PySide6.QtWidgets import QWidget

from app.application.app_context import AppContext


class BaseToolWidget(QWidget):
    """Base widget for all PDF Toolkit tools."""

    def __init__(
        self,
        context: AppContext,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.context = context

    def setup_ui(self) -> None:
        pass

    def select_input(self) -> None:
        pass

    def validate(self) -> bool:
        return True

    def preview(self) -> None:
        pass

    def execute(self) -> None:
        pass

    def save_result(self) -> None:
        pass

    def reset(self) -> None:
        pass
