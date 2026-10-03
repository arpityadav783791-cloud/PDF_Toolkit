from __future__ import annotations

from typing import Any, Callable

from PySide6.QtCore import QObject, QThread, Signal

from app.models.operation import Operation
from app.workers.pdf_worker import PdfWorker


class OperationController(QObject):
    """Coordinates asynchronous PDF operations."""

    started = Signal(object)
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(object)
    error = Signal(object)
    cancelled = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._thread: QThread | None = None
        self._worker: PdfWorker | None = None
        self.current_operation: Operation | None = None

    def start(
        self,
        name: str,
        operation: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Operation:
        if self.is_running():
            raise RuntimeError("Another operation is already running.")

        operation_model = Operation(name)
        operation_model.start()

        worker = PdfWorker(
            operation,
            *args,
            **kwargs,
        )

        thread = QThread()

        self._thread = thread
        self._worker = worker
        self.current_operation = operation_model

        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        worker.progress.connect(self._on_progress)
        worker.status.connect(self._on_status)

        worker.finished.connect(
            lambda result: self._on_finished(
                result,
                operation_model,
                thread,
            )
        )

        worker.error.connect(
            lambda exception: self._on_error(
                exception,
                operation_model,
                thread,
            )
        )

        worker.cancelled.connect(
            lambda: self._on_cancelled(
                operation_model,
                thread,
            )
        )

        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)
        worker.cancelled.connect(thread.quit)

        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        worker.cancelled.connect(worker.deleteLater)

        thread.finished.connect(self._on_thread_finished)
        thread.finished.connect(thread.deleteLater)

        self.started.emit(operation_model)

        thread.start()

        return operation_model

    def cancel(self) -> None:
        if self._worker is not None:
            self._worker.cancel()

    def is_running(self) -> bool:
        return self._thread is not None

    def _on_progress(self, value: int) -> None:
        if self.current_operation is not None:
            self.current_operation.update_progress(value)

        self.progress.emit(value)

    def _on_status(self, message: str) -> None:
        if self.current_operation is not None:
            self.current_operation.message = message

        self.status.emit(message)

    def _on_finished(
        self,
        result: Any,
        operation: Operation,
        thread: QThread,
    ) -> None:
        operation.complete()
        self.finished.emit(result)

    def _on_error(
        self,
        exception: Exception,
        operation: Operation,
        thread: QThread,
    ) -> None:
        operation.fail(str(exception))
        self.error.emit(exception)

    def _on_cancelled(
        self,
        operation: Operation,
        thread: QThread,
    ) -> None:
        operation.cancel()
        self.cancelled.emit()

    def _on_thread_finished(self) -> None:
        self._worker = None
        self._thread = None
