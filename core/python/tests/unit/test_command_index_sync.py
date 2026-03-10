from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.cli.introspection import iter_command_parser_specs
from watchtower_core.cli.parser import build_parser
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync import CommandIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_command_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CommandIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["command_id"] == "command.watchtower_core.sync.command_index"
        for entry in entries
    )


def test_command_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CommandIndexSyncService(loader)
    output_path = tmp_path / "command_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.commands"


def test_registry_backed_parser_specs_require_companion_docs() -> None:
    specs = iter_command_parser_specs(build_parser())

    assert any(spec.command_id == "command.watchtower_core" for spec in specs)
    assert any(spec.command_id == "command.watchtower_core.sync.command_index" for spec in specs)
    for spec in specs:
        assert (REPO_ROOT / spec.doc_path).exists()
        assert (REPO_ROOT / spec.implementation_path).exists()
