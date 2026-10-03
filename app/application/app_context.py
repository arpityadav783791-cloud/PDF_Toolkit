from __future__ import annotations

from app.application.application_state import ApplicationState
from app.application.service_container import ServiceContainer
from app.config.settings import Settings
from app.controllers.operation_controller import OperationController
from app.controllers.tool_controller import ToolController
from app.services.document_service import DocumentService
from app.services.export_service import ExportService


class AppContext:
    def __init__(self) -> None:
        self.settings = Settings()
        self.state = ApplicationState()
        self.services = ServiceContainer()

    def initialize(self) -> None:
        self.settings.load()

        self.services.register(Settings, self.settings)
        self.services.register(ApplicationState, self.state)

        document_service = DocumentService()
        export_service = ExportService()
        operation_controller = OperationController()

        tool_controller = ToolController(
            document_service=document_service,
            export_service=export_service,
            operation_controller=operation_controller,
        )

        self.services.register(
            DocumentService,
            document_service,
        )
        self.services.register(
            ExportService,
            export_service,
        )
        self.services.register(
            OperationController,
            operation_controller,
        )
        self.services.register(
            ToolController,
            tool_controller,
        )

        self.services.initialize()

    def get_service(self, service_type: type):
        return self.services.resolve(service_type)

    def shutdown(self) -> None:
        self.settings.save()
        self.services.shutdown()
