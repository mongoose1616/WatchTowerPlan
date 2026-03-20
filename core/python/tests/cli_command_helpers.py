from __future__ import annotations

import json
from typing import Any

import pytest

from watchtower_core.cli.main import main


def run_json_command(
    capsys: pytest.CaptureFixture[str],
    args: list[str] | tuple[str, ...],
) -> tuple[int, dict[str, Any]]:
    command = list(args)
    if "--format" not in command:
        command.extend(["--format", "json"])
    result = main(command)
    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload, dict)
    return result, payload
