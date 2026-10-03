from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from pypdf import PdfReader as PypdfReader
from pypdf import PdfWriter as PypdfWriter

from app.exceptions.pdf import PdfValidationError


class PdfWriter:
    """Create and save PDF documents using pypdf."""

    def __init__(self) -> None:
        self._writer = PypdfWriter()

    def create(self) -> None:
        self._writer = PypdfWriter()

    def add_page(self, page: Any) -> None:
        self._writer.add_page(page)

    def insert_page(self, page: Any, index: int) -> None:
        self._writer.insert_page(page, index)

    def delete_page(self, index: int) -> None:
        self._writer.remove_page(index)

    def save(self, output_path: str | Path) -> Path:
        destination = Path(output_path)

        destination.parent.mkdir(parents=True, exist_ok=True)

        try:
            with destination.open("wb") as file:
                self._writer.write(file)
        except OSError as exc:
            raise PdfValidationError(
                f"Unable to write PDF: {destination}"
            ) from exc

        return destination

    def save_atomic(self, output_path: str | Path) -> Path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)

        temporary_path: Path | None = None

        try:
            with NamedTemporaryFile(
                mode="wb",
                suffix=".pdf",
                prefix=".pdf_toolkit_",
                dir=destination.parent,
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                self._writer.write(temporary_file)

            temporary_path.replace(destination)

            return destination

        except OSError as exc:
            raise PdfValidationError(
                f"Unable to atomically save PDF: {destination}"
            ) from exc

        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink(missing_ok=True)

    @staticmethod
    def copy_pages(
        input_path: str | Path,
        output_path: str | Path,
        page_indexes: list[int],
    ) -> Path:
        reader = PypdfReader(str(input_path))
        writer = PypdfWriter()

        page_count = len(reader.pages)

        for index in page_indexes:
            if index < 0 or index >= page_count:
                raise IndexError(f"Page index out of range: {index}")

            writer.add_page(reader.pages[index])

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("wb") as file:
            writer.write(file)

        return output
