from __future__ import annotations

import json

import pytest

from tests.pack_fixture_support import REPO_ROOT
from watchtower_host.cli.main import main


def test_validate_all_reports_current_repo_baseline_via_cli_json(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    monkeypatch.chdir(REPO_ROOT / "core" / "python")

    result = main(["validate", "all", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == (0 if payload["passed"] else 1)
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert isinstance(payload["passed"], bool)
