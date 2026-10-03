from __future__ import annotations

from pathlib import Path

import pymupdf as fitz

from app.exceptions.file import FileNotFoundError as PdfToolkitFileNotFoundError
from app.exceptions.pdf import PdfValidationError


class PdfValidator:
    """Validate input and generated PDF files."""

    def validate_file(self, path: str | Path) -> bool:
        pdf_path = Path(path)

        if not pdf_path.exists():
            raise PdfToolkitFileNotFoundError(
                f"PDF file does not exist: {pdf_path}"
            )

        if not pdf_path.is_file():
            raise PdfValidationError(
                f"PDF path is not a file: {pdf_path}"
            )

        if pdf_path.stat().st_size == 0:
            raise PdfValidationError(
                f"PDF file is empty: {pdf_path}"
            )

        try:
            document = fitz.open(pdf_path)
        except Exception as exc:
            raise PdfValidationError(
                f"PDF cannot be opened: {pdf_path}"
            ) from exc

        try:
            if document.page_count <= 0:
                raise PdfValidationError(
                    f"PDF contains no pages: {pdf_path}"
                )

            return True
        finally:
            document.close()

    def validate_document(self, document: fitz.Document) -> bool:
        if document is None:
            raise PdfValidationError("PDF document is None.")

        if document.is_closed:
            raise PdfValidationError("PDF document is closed.")

        if document.page_count <= 0:
            raise PdfValidationError("PDF document contains no pages.")

        return True

    def validate_output(self, path: str | Path) -> bool:
        return self.validate_file(path)

    def check_readable(self, path: str | Path) -> bool:
        return self.validate_file(path)

    def check_page_count(self, path: str | Path) -> int:
        pdf_path = Path(path)

        if not self.validate_file(pdf_path):
            return 0

        document = fitz.open(pdf_path)

        try:
            return document.page_count
        finally:
            document.close()

    def check_file_exists(self, path: str | Path) -> bool:
        return Path(path).is_file()
