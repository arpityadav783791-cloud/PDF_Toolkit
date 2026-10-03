from __future__ import annotations

from typing import Any


class ServiceContainer:
    def __init__(self) -> None:
        self._services: dict[type[Any] | str, Any] = {}

    def register(self, key: type[Any] | str, service: Any) -> None:
        self._services[key] = service

    def resolve(self, key: type[Any] | str) -> Any:
        try:
            return self._services[key]
        except KeyError as exc:
            raise KeyError(f"Service is not registered: {key}") from exc

    def has(self, key: type[Any] | str) -> bool:
        return key in self._services

    def initialize(self) -> None:
        for service in self._services.values():
            initializer = getattr(service, "initialize", None)
            if callable(initializer):
                initializer()

    def shutdown(self) -> None:
        for service in reversed(list(self._services.values())):
            shutdown = getattr(service, "shutdown", None)
            if callable(shutdown):
                shutdown()

        self._services.clear()
