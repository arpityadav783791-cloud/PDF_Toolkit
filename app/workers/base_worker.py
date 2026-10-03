from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class BaseWorker(QObject):
    """Base class for long-running background operations."""

    progress = Signal(int)
    status = Signal(str)
    finished = Signal(object)
    error = Signal(Exception)
    cancelled = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._cancel_requested = False

    def run(self) -> None:
        raise NotImplementedError(
            "Worker subclasses must implement run()."
        )

    def cancel(self) -> None:
        self._cancel_requested = True

    @property
    def is_cancelled(self) -> bool:
        return self._cancel_requested
