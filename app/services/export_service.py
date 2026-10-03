from __future__ import annotations

import os
import tempfile
from pathlib import Path

from app.exceptions.file import FileError


class ExportService:
    """Prepare, validate and finalize generated output files."""

    def create_temp_output(self, output_path: str | Path) -> Path:
        destination = Path(output_path)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_descriptor, temp_name = tempfile.mkstemp(
            prefix=".pdf_toolkit_",
            suffix=destination.suffix or ".pdf",
            dir=destination.parent,
        )

        os.close(file_descriptor)

        temp_path = Path(temp_name)

        # PdfWriter/PdfMerger needs to create the file itself.
        temp_path.unlink(missing_ok=True)

        return temp_path

    def prepare_output(self, output_path: str | Path) -> Path:
        return self.create_temp_output(output_path)

    def save_output(
        self,
        temp_path: str | Path,
        output_path: str | Path,
        overwrite: bool = False,
    ) -> Path:
        source = Path(temp_path)
        destination = Path(output_path)

        if not source.is_file():
            raise FileError(
                f"Temporary output does not exist: {source}"
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.exists() and not overwrite:
            raise FileError(
                f"Output file already exists: {destination}"
            )

        try:
            source.replace(destination)

            # Normal user-readable PDF permission.
            destination.chmod(0o644)

        except OSError as exc:
            raise FileError(
                f"Unable to save output PDF: {destination}"
            ) from exc

        return destination

    def validate_output_path(
        self,
        output_path: str | Path,
    ) -> bool:
        destination = Path(output_path)

        if not destination.name:
            raise FileError("An output filename is required.")

        if destination.suffix.lower() != ".pdf":
            raise FileError("Output file must have a .pdf extension.")

        return True

    def cleanup_temp(self, path: str | Path | None) -> None:
        if path is None:
            return

        Path(path).unlink(missing_ok=True)
