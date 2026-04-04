from __future__ import annotations

from pathlib import Path

import pytest

import watchtower_host.cli.introspection as introspection_module
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.command_index import CommandIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_command_index_sync_ignores_stale_current_process_host_parser_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    original_specs = introspection_module.CORE_COMMAND_GROUP_SPECS
    assert any(spec.name == "git" for spec in original_specs)

    monkeypatch.setattr(
        introspection_module,
        "CORE_COMMAND_GROUP_SPECS",
        tuple(spec for spec in original_specs if spec.name != "git"),
    )

    document = CommandIndexSyncService(loader).build_document()
    commands = {
        entry["command"]
        for entry in document["entries"]
        if isinstance(entry, dict) and isinstance(entry.get("command"), str)
    }

    assert "watchtower-core git" in commands
    assert "watchtower-core git hygiene" in commands
