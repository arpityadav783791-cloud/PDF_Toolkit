from __future__ import annotations

from pathlib import Path

import pymupdf as fitz
from PIL import Image

from app.config.constants import DEFAULT_DPI


class PdfRenderer:
    """Render PDF pages into images for the viewer and previews."""

    def render_page(
        self,
        document: fitz.Document,
        page_index: int,
        dpi: int = DEFAULT_DPI,
    ) -> Image.Image:
        if page_index < 0 or page_index >= document.page_count:
            raise IndexError(f"Page index out of range: {page_index}")

        page = document.load_page(page_index)

        scale = dpi / 72.0
        matrix = fitz.Matrix(scale, scale)

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        image = Image.frombytes(
            "RGB",
            (pixmap.width, pixmap.height),
            pixmap.samples,
        )

        return image

    def render_thumbnail(
        self,
        document: fitz.Document,
        page_index: int,
        max_size: tuple[int, int] = (200, 280),
    ) -> Image.Image:
        image = self.render_page(
            document=document,
            page_index=page_index,
            dpi=72,
        )

        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        return image

    def render_pages(
        self,
        document: fitz.Document,
        page_indexes: list[int] | None = None,
        dpi: int = DEFAULT_DPI,
    ) -> list[Image.Image]:
        indexes = (
            page_indexes
            if page_indexes is not None
            else list(range(document.page_count))
        )

        return [
            self.render_page(document, index, dpi)
            for index in indexes
        ]

    def save_rendered_page(
        self,
        document: fitz.Document,
        page_index: int,
        output_path: str | Path,
        dpi: int = DEFAULT_DPI,
    ) -> Path:
        image = self.render_page(document, page_index, dpi)

        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)

        image.save(destination)

        return destination
