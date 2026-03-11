from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import pytest


@pytest.fixture
def json_writer() -> Callable[[Path, dict[str, object]], None]:
    def _write_json(path: Path, document: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")

    return _write_json
