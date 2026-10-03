from __future__ import annotations

from pathlib import Path
from typing import Any

import pymupdf as fitz

from app.exceptions.file import FileNotFoundError as PdfToolkitFileNotFoundError
from app.exceptions.pdf import EncryptedPdfError, InvalidPdfError


class PdfReader:
    """Read and inspect PDF documents using PyMuPDF."""

    def __init__(self) -> None:
        self._document: fitz.Document | None = None
        self._path: Path | None = None

    def open(self, path: str | Path, password: str | None = None) -> fitz.Document:
        pdf_path = Path(path)

        if not pdf_path.exists():
            raise PdfToolkitFileNotFoundError(
                f"PDF file does not exist: {pdf_path}"
            )

        if not pdf_path.is_file():
            raise InvalidPdfError(f"Path is not a file: {pdf_path}")

        try:
            document = fitz.open(pdf_path)
        except Exception as exc:
            raise InvalidPdfError(
                f"Unable to open PDF: {pdf_path}"
            ) from exc

        if document.is_encrypted:
            if not password:
                document.close()
                raise EncryptedPdfError(
                    "The PDF is password protected."
                )

            authenticated = document.authenticate(password)

            if not authenticated:
                document.close()
                raise EncryptedPdfError(
                    "The supplied PDF password is incorrect."
                )

        self.close()

        self._document = document
        self._path = pdf_path

        return document

    def close(self) -> None:
        if self._document is not None:
            self._document.close()
            self._document = None

        self._path = None

    def get_page_count(self) -> int:
        return self._require_document().page_count

    def get_page(self, index: int) -> fitz.Page:
        document = self._require_document()

        if index < 0 or index >= document.page_count:
            raise IndexError(f"Page index out of range: {index}")

        return document.load_page(index)

    def get_metadata(self) -> dict[str, Any]:
        return dict(self._require_document().metadata)

    def is_encrypted(self) -> bool:
        return self._require_document().is_encrypted

    def get_permissions(self) -> int:
        return self._require_document().permissions

    @property
    def path(self) -> Path | None:
        return self._path

    @property
    def document(self) -> fitz.Document | None:
        return self._document

    def _require_document(self) -> fitz.Document:
        if self._document is None:
            raise InvalidPdfError("No PDF document is currently open.")

        return self._document

    def __enter__(self) -> "PdfReader":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
