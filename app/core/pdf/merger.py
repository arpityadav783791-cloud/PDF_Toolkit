from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

from pypdf import PdfReader as PypdfReader
from pypdf import PdfWriter as PypdfWriter

from app.core.pdf.validator import PdfValidator
from app.exceptions.pdf import InvalidPdfError, PdfValidationError


class PdfMerger:
    """Merge multiple PDF documents into a single PDF."""

    def __init__(self) -> None:
        self._validator = PdfValidator()

    def validate_inputs(self, input_paths: list[str | Path]) -> None:
        if not input_paths:
            raise InvalidPdfError("At least one PDF is required.")

        for path in input_paths:
            self._validator.validate_file(path)

    def merge(
        self,
        input_paths: list[str | Path],
        output_path: str | Path,
    ) -> Path:
        self.validate_inputs(input_paths)

        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)

        writer = PypdfWriter()
        temporary_path: Path | None = None

        try:
            for input_path in input_paths:
                reader = PypdfReader(str(input_path))

                for page in reader.pages:
                    writer.add_page(page)

            if len(writer.pages) == 0:
                raise InvalidPdfError("No pages were found in the input PDFs.")

            with NamedTemporaryFile(
                mode="wb",
                suffix=".pdf",
                prefix=".pdf_toolkit_merge_",
                dir=destination.parent,
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                writer.write(temporary_file)

            self._validator.validate_output(temporary_path)

            temporary_path.replace(destination)
            temporary_path = None

            return destination

        except OSError as exc:
            raise PdfValidationError(
                f"Unable to create merged PDF: {destination}"
            ) from exc

        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    def build_output(
        self,
        input_paths: list[str | Path],
        output_path: str | Path,
    ) -> Path:
        return self.merge(input_paths, output_path)
