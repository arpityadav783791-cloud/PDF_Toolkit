from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.application.app_context import AppContext


class Dashboard(QWidget):
    merge_pdf_requested = Signal()

    def __init__(self, context: AppContext) -> None:
        super().__init__()

        self.context = context

        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            50,
            40,
            50,
            40,
        )
        main_layout.setSpacing(24)

        title = QLabel("PDF Toolkit")

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 34px;
                font-weight: 700;
            }
            """
        )

        subtitle = QLabel(
            "Professional PDF workstation for Windows and Linux"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #666666;
            }
            """
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        actions_frame = QFrame()

        actions_frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        actions_layout = QGridLayout(
            actions_frame
        )

        actions_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        actions_layout.setSpacing(15)

        tools = [
            "Open PDF",
            "Merge PDF",
            "Split PDF",
            "Compress PDF",
            "PDF to Images",
            "Images to PDF",
        ]

        for index, name in enumerate(tools):
            button = QPushButton(name)

            button.setMinimumHeight(60)

            button.setStyleSheet(
                """
                QPushButton {
                    font-size: 15px;
                    padding: 10px;
                }
                """
            )

            button.clicked.connect(
                lambda checked=False,
                tool_name=name: self._tool_clicked(
                    tool_name
                )
            )

            row = index // 3
            column = index % 3

            actions_layout.addWidget(
                button,
                row,
                column,
            )

        main_layout.addWidget(actions_frame)
        main_layout.addStretch()

        footer = QLabel("Ready")

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(
            """
            QLabel {
                color: #777777;
                font-size: 13px;
            }
            """
        )

        main_layout.addWidget(footer)

    def _tool_clicked(self, tool_name: str) -> None:
        self.context.state.set_active_tool(tool_name)

        if tool_name == "Merge PDF":
            self.merge_pdf_requested.emit()
            return

        QMessageBox.information(
            self,
            tool_name,
            f"{tool_name} will be implemented in a later milestone.",
        )
