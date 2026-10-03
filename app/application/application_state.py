from __future__ import annotations

from typing import Any


class ApplicationState:
    def __init__(self) -> None:
        self.current_document: Any = None
        self.open_documents: list[Any] = []
        self.active_tool: str | None = None
        self.active_operation: Any = None
        self.is_processing: bool = False
        self.unsaved_changes: bool = False

    def set_current_document(self, document: Any | None) -> None:
        self.current_document = document

    def add_document(self, document: Any) -> None:
        if document not in self.open_documents:
            self.open_documents.append(document)

    def remove_document(self, document: Any) -> None:
        if document in self.open_documents:
            self.open_documents.remove(document)

        if self.current_document is document:
            self.current_document = None

    def set_active_tool(self, tool_id: str | None) -> None:
        self.active_tool = tool_id

    def set_active_operation(self, operation: Any | None) -> None:
        self.active_operation = operation

    def mark_modified(self) -> None:
        self.unsaved_changes = True

    def mark_saved(self) -> None:
        self.unsaved_changes = False
