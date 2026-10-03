from __future__ import annotations

from app.application.application_state import ApplicationState
from app.application.service_container import ServiceContainer
from app.config.settings import Settings


class AppContext:
    def __init__(self) -> None:
        self.settings = Settings()
        self.state = ApplicationState()
        self.services = ServiceContainer()

    def initialize(self) -> None:
        self.settings.load()

        self.services.register(Settings, self.settings)
        self.services.register(ApplicationState, self.state)

        self.services.initialize()

    def get_service(self, service_type: type):
        return self.services.resolve(service_type)

    def shutdown(self) -> None:
        self.settings.save()
        self.services.shutdown()
