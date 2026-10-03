from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config.defaults import DEFAULT_SETTINGS
from app.config.paths import ensure_app_directories, get_settings_path


class Settings:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or get_settings_path()
        self._data: dict[str, Any] = dict(DEFAULT_SETTINGS)

    def load(self) -> None:
        ensure_app_directories()

        if not self._path.exists():
            return

        try:
            with self._path.open("r", encoding="utf-8") as file:
                stored = json.load(file)

            if isinstance(stored, dict):
                self._data.update(stored)
        except (OSError, json.JSONDecodeError):
            self._data = dict(DEFAULT_SETTINGS)

    def save(self) -> None:
        ensure_app_directories()

        with self._path.open("w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def reset(self) -> None:
        self._data = dict(DEFAULT_SETTINGS)

    @property
    def path(self) -> Path:
        return self._path
