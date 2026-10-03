from __future__ import annotations

import os
import sys
from pathlib import Path


APP_DATA_NAME = "PDF Toolkit"


def get_app_data_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.getenv("APPDATA") or str(Path.home())
        return Path(base) / APP_DATA_NAME

    if sys.platform.startswith("linux"):
        base = os.getenv("XDG_CONFIG_HOME")
        if base:
            return Path(base) / "pdf-toolkit"
        return Path.home() / ".config" / "pdf-toolkit"

    return Path.home() / ".pdf-toolkit"


def get_cache_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.getenv("LOCALAPPDATA") or str(Path.home())
        return Path(base) / APP_DATA_NAME / "cache"

    if sys.platform.startswith("linux"):
        base = os.getenv("XDG_CACHE_HOME")
        if base:
            return Path(base) / "pdf-toolkit"
        return Path.home() / ".cache" / "pdf-toolkit"

    return Path.home() / ".cache" / "pdf-toolkit"


def get_temp_dir() -> Path:
    path = get_cache_dir() / "temp"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_settings_path() -> Path:
    return get_app_data_dir() / "settings.json"


def get_log_path() -> Path:
    return get_app_data_dir() / "pdf_toolkit.log"


def ensure_app_directories() -> None:
    get_app_data_dir().mkdir(parents=True, exist_ok=True)
    get_cache_dir().mkdir(parents=True, exist_ok=True)
    get_temp_dir().mkdir(parents=True, exist_ok=True)
