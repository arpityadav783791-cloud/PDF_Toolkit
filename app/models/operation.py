from __future__ import annotations

from datetime import datetime
from enum import Enum


class OperationStatus(Enum):
    IDLE = "idle"
    VALIDATING = "validating"
    READY = "ready"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Operation:
    def __init__(self, name: str) -> None:
        self.id: str = f"{name}-{id(self)}"
        self.name = name
        self.status = OperationStatus.IDLE
        self.progress = 0
        self.message = ""
        self.started_at: datetime | None = None
        self.finished_at: datetime | None = None
        self.error: str | None = None

    def start(self) -> None:
        self.started_at = datetime.now()
        self.status = OperationStatus.PROCESSING
        self.progress = 0

    def update_progress(
        self,
        progress: int,
        message: str = "",
    ) -> None:
        self.progress = max(0, min(100, progress))
        self.message = message

    def complete(self) -> None:
        self.progress = 100
        self.status = OperationStatus.COMPLETED
        self.finished_at = datetime.now()

    def fail(self, error: str) -> None:
        self.status = OperationStatus.FAILED
        self.error = error
        self.finished_at = datetime.now()

    def cancel(self) -> None:
        self.status = OperationStatus.CANCELLED
        self.finished_at = datetime.now()
