from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.cli.introspection import iter_command_parser_specs
from watchtower_core.cli.parser import build_parser
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import CommandIndexSyncService

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
    assert any(entry["command_id"] == "command.watchtower_core.route.preview" for entry in entries)


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
    spec_by_id = {spec.command_id: spec for spec in specs}

    assert "command.watchtower_core" in spec_by_id
    assert "command.watchtower_core.route" in spec_by_id
    assert "command.watchtower_core.route.preview" in spec_by_id
    assert "command.watchtower_core.plan" in spec_by_id
    assert "command.watchtower_core.plan.scaffold" in spec_by_id
    assert "command.watchtower_core.plan.bootstrap" in spec_by_id
    assert "command.watchtower_core.task" in spec_by_id
    assert "command.watchtower_core.task.create" in spec_by_id
    assert "command.watchtower_core.task.update" in spec_by_id
    assert "command.watchtower_core.task.transition" in spec_by_id
    assert "command.watchtower_core.sync.command_index" in spec_by_id
    assert "command.watchtower_core.sync.route_index" in spec_by_id
    assert (
        spec_by_id["command.watchtower_core"].implementation_path
        == "core/python/src/watchtower_core/cli/parser.py"
    )
    assert (
        spec_by_id["command.watchtower_core.doctor"].implementation_path
        == "core/python/src/watchtower_core/cli/doctor_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.route"].implementation_path
        == "core/python/src/watchtower_core/cli/route_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.route.preview"].implementation_path
        == "core/python/src/watchtower_core/cli/route_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan"].implementation_path
        == "core/python/src/watchtower_core/cli/plan_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.scaffold"].implementation_path
        == "core/python/src/watchtower_core/cli/plan_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.bootstrap"].implementation_path
        == "core/python/src/watchtower_core/cli/plan_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.task"].implementation_path
        == "core/python/src/watchtower_core/cli/task_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.task.create"].implementation_path
        == "core/python/src/watchtower_core/cli/task_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.task.update"].implementation_path
        == "core/python/src/watchtower_core/cli/task_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.task.transition"].implementation_path
        == "core/python/src/watchtower_core/cli/task_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.commands"].implementation_path
        == "core/python/src/watchtower_core/cli/query_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.sync.command_index"].implementation_path
        == "core/python/src/watchtower_core/cli/sync_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.sync.route_index"].implementation_path
        == "core/python/src/watchtower_core/cli/sync_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.closeout.initiative"].implementation_path
        == "core/python/src/watchtower_core/cli/closeout_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.validate.all"].implementation_path
        == "core/python/src/watchtower_core/cli/validate_family.py"
    )
    for spec in specs:
        assert (REPO_ROOT / spec.doc_path).exists()
        assert (REPO_ROOT / spec.implementation_path).exists()
