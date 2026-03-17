from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kivy.app import App


def get_storage_dir() -> Path:
    app = App.get_running_app()
    if app and getattr(app, "user_data_dir", None):
        storage_dir = Path(app.user_data_dir)
    else:
        storage_dir = Path.home() / ".snake_game"

    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


def load_json(filename: str, default: dict[str, Any]) -> dict[str, Any]:
    file_path = get_storage_dir() / filename
    if not file_path.exists():
        return default.copy()

    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default.copy()


def save_json(filename: str, payload: dict[str, Any]) -> None:
    file_path = get_storage_dir() / filename
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")