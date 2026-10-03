from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from app.application.app_context import AppContext
from app.controllers.tool_controller import ToolController
from app.ui.tools.base_tool import BaseToolWidget


class MergeTool(BaseToolWidget):
    """User interface for merging multiple PDF files."""

    def __init__(
        self,
        context: AppContext,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(context, parent)

        self.tool_controller = context.get_service(ToolController)

        self.setWindowTitle("Merge PDF")

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("Merge PDF")
        title.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )

        description = QLabel(
            "Combine multiple PDF files into one document."
        )
        description.setStyleSheet(
            "font-size: 14px; color: #666666;"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        input_label = QLabel("PDF files")

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(
            QListWidget.SelectionMode.ExtendedSelection
        )
        self.file_list.setMinimumHeight(250)

        layout.addWidget(input_label)
        layout.addWidget(self.file_list)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Add PDFs")
        self.remove_button = QPushButton("Remove")
        self.up_button = QPushButton("Move Up")
        self.down_button = QPushButton("Move Down")
        self.clear_button = QPushButton("Clear")

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addWidget(self.up_button)
        buttons_layout.addWidget(self.down_button)
        buttons_layout.addWidget(self.clear_button)

        layout.addLayout(buttons_layout)

        output_label = QLabel("Output PDF")

        output_layout = QHBoxLayout()

        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText(
            "Choose where the merged PDF should be saved..."
        )

        self.output_button = QPushButton("Browse")

        output_layout.addWidget(self.output_input)
        output_layout.addWidget(self.output_button)

        layout.addWidget(output_label)
        layout.addLayout(output_layout)

        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.setMinimumHeight(50)
        self.merge_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                font-weight: 600;
            }
            """
        )

        layout.addWidget(self.merge_button)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.status_label)

        layout.addStretch()

    def _connect_signals(self) -> None:
        self.add_button.clicked.connect(self._add_files)
        self.remove_button.clicked.connect(self._remove_files)
        self.up_button.clicked.connect(self._move_up)
        self.down_button.clicked.connect(self._move_down)
        self.clear_button.clicked.connect(self._clear_files)

        self.output_button.clicked.connect(
            self._select_output
        )

        self.merge_button.clicked.connect(
            self.execute
        )

        self.tool_controller.status.connect(
            self._on_status
        )

        self.tool_controller.progress.connect(
            self._on_progress
        )

        self.tool_controller.finished.connect(
            self._on_finished
        )

        self.tool_controller.error.connect(
            self._on_error
        )

    def _add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF files",
            "",
            "PDF Files (*.pdf)",
        )

        for file_path in files:
            self._add_file(file_path)

    def _add_file(self, file_path: str) -> None:
        existing = [
            self.file_list.item(index).data(
                Qt.ItemDataRole.UserRole
            )
            for index in range(self.file_list.count())
        ]

        if file_path in existing:
            return

        item = QListWidgetItem(
            Path(file_path).name
        )

        item.setData(
            Qt.ItemDataRole.UserRole,
            file_path,
        )

        self.file_list.addItem(item)

    def _remove_files(self) -> None:
        rows = sorted(
            {
                index.row()
                for index in self.file_list.selectedIndexes()
            },
            reverse=True,
        )

        for row in rows:
            self.file_list.takeItem(row)

    def _move_up(self) -> None:
        selected = self.file_list.selectedItems()

        if not selected:
            return

        row = self.file_list.row(selected[0])

        if row <= 0:
            return

        item = self.file_list.takeItem(row)
        self.file_list.insertItem(row - 1, item)
        self.file_list.setCurrentItem(item)

    def _move_down(self) -> None:
        selected = self.file_list.selectedItems()

        if not selected:
            return

        row = self.file_list.row(selected[0])

        if row >= self.file_list.count() - 1:
            return

        item = self.file_list.takeItem(row)
        self.file_list.insertItem(row + 1, item)
        self.file_list.setCurrentItem(item)

    def _clear_files(self) -> None:
        self.file_list.clear()

    def _select_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save merged PDF",
            "",
            "PDF Files (*.pdf)",
        )

        if path:
            if not path.lower().endswith(".pdf"):
                path += ".pdf"

            self.output_input.setText(path)

    def _get_input_paths(self) -> list[str]:
        paths: list[str] = []

        for index in range(self.file_list.count()):
            path = self.file_list.item(index).data(
                Qt.ItemDataRole.UserRole
            )

            if path:
                paths.append(path)

        return paths

    def validate(self) -> bool:
        input_paths = self._get_input_paths()
        output_path = self.output_input.text().strip()

        if not input_paths:
            QMessageBox.warning(
                self,
                "No PDF files",
                "Add at least one PDF file.",
            )
            return False

        if not output_path:
            QMessageBox.warning(
                self,
                "No output file",
                "Choose where the merged PDF should be saved.",
            )
            return False

        return True

    def execute(self) -> None:
        if not self.validate():
            return

        input_paths = self._get_input_paths()
        output_path = self.output_input.text().strip()

        if Path(output_path).exists():
            answer = QMessageBox.question(
                self,
                "File already exists",
                "The output file already exists. Replace it?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if answer != QMessageBox.StandardButton.Yes:
                return

        try:
            self.merge_button.setEnabled(False)

            self.tool_controller.execute_merge(
                input_paths,
                output_path,
            )

            self.status_label.setText(
                "Merging PDFs..."
            )

        except Exception as exc:
            self.merge_button.setEnabled(True)

            QMessageBox.critical(
                self,
                "Merge failed",
                str(exc),
            )

    def _on_status(self, message: str) -> None:
        self.status_label.setText(message)

    def _on_progress(self, value: int) -> None:
        self.status_label.setText(
            f"Merging PDFs... {value}%"
        )

    def _on_finished(self, result) -> None:
        self.merge_button.setEnabled(True)

        output_path = Path(str(result))

        self.status_label.setText(
            "Merge completed."
        )

        QMessageBox.information(
            self,
            "Merge completed",
            f"PDF successfully created:\n\n{output_path}",
        )

    def _on_error(self, exception: Exception) -> None:
        self.merge_button.setEnabled(True)

        self.status_label.setText(
            "Merge failed."
        )

        QMessageBox.critical(
            self,
            "Merge failed",
            str(exception),
        )
