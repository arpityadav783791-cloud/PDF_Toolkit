from __future__ import annotations

from typing import Any, Callable

from app.workers.base_worker import BaseWorker


class PdfWorker(BaseWorker):
    """Worker for executing PDF operations outside the UI thread."""

    def __init__(
        self,
        operation: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        self._operation = operation
        self._args = args
        self._kwargs = kwargs

    def run(self) -> None:
        if self.is_cancelled:
            self.cancelled.emit()
            return

        try:
            self.status.emit("Starting operation...")
            self.progress.emit(0)

            result = self._operation(
                *self._args,
                **self._kwargs,
            )

            if self.is_cancelled:
                self.cancelled.emit()
                return

            self.progress.emit(100)
            self.status.emit("Operation completed.")

            self.finished.emit(result)

        except Exception as exc:
            self.error.emit(exc)
