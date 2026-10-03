from __future__ import annotations

from pathlib import Path
from typing import Any

from app.core.pdf.reader import PdfReader
from app.core.pdf.validator import PdfValidator


class DocumentService:
    """Application-level service for opening and validating PDF documents."""

    def __init__(
        self,
        validator: PdfValidator | None = None,
    ) -> None:
        self._validator = validator or PdfValidator()

    def validate_pdf(self, path: str | Path) -> bool:
        return self._validator.validate_file(path)

    def validate_pdf_inputs(
        self,
        paths: list[str | Path],
    ) -> bool:
        if not paths:
            raise ValueError("At least one PDF file is required.")

        for path in paths:
            self.validate_pdf(path)

        return True

    def get_page_count(self, path: str | Path) -> int:
        reader = PdfReader()

        try:
            reader.open(path)
            return reader.get_page_count()
        finally:
            reader.close()

    def get_document_info(self, path: str | Path) -> dict[str, Any]:
        reader = PdfReader()

        try:
            reader.open(path)

            return {
                "path": str(path),
                "page_count": reader.get_page_count(),
                "metadata": reader.get_metadata(),
                "encrypted": reader.is_encrypted(),
                "permissions": reader.get_permissions(),
            }
        finally:
            reader.close()

    def open_document(
        self,
        path: str | Path,
        password: str | None = None,
    ):
        reader = PdfReader()
        return reader.open(path, password=password)
