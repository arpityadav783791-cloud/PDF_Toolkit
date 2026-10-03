from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal

from app.core.pdf.merger import PdfMerger
from app.services.document_service import DocumentService
from app.services.export_service import ExportService
from app.controllers.operation_controller import OperationController


class ToolController(QObject):
    """Coordinates tool-level operations."""

    finished = Signal(object)
    error = Signal(object)
    progress = Signal(int)
    status = Signal(str)

    def __init__(
        self,
        document_service: DocumentService | None = None,
        export_service: ExportService | None = None,
        operation_controller: OperationController | None = None,
        merger: PdfMerger | None = None,
    ) -> None:
        super().__init__()

        self.document_service = document_service or DocumentService()
        self.export_service = export_service or ExportService()
        self.operation_controller = (
            operation_controller or OperationController()
        )
        self.merger = merger or PdfMerger()

        self.operation_controller.finished.connect(self.finished.emit)
        self.operation_controller.error.connect(self.error.emit)
        self.operation_controller.progress.connect(self.progress.emit)
        self.operation_controller.status.connect(self.status.emit)

    def execute_merge(
        self,
        input_paths: list[str],
        output_path: str,
    ):
        if not input_paths:
            raise ValueError("Select at least one PDF.")

        if not output_path.strip():
            raise ValueError("Choose an output PDF.")

        self.document_service.validate_pdf_inputs(input_paths)
        self.export_service.validate_output_path(output_path)

        output = Path(output_path).resolve()

        for input_path in input_paths:
            if Path(input_path).resolve() == output:
                raise ValueError(
                    "Output PDF cannot be the same as an input PDF."
                )

        return self.operation_controller.start(
            "Merge PDF",
            self._merge,
            input_paths,
            output_path,
        )

    def cancel_current_operation(self) -> None:
        self.operation_controller.cancel()

    def is_running(self) -> bool:
        return self.operation_controller.is_running()

    def _merge(
        self,
        input_paths: list[str],
        output_path: str,
    ):
        return self.merger.merge(
            input_paths,
            output_path,
        )
