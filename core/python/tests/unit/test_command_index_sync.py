from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.adapters.markdown import (
    extract_code_spans,
    extract_sections,
    load_markdown_body,
    parse_markdown_table,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.command_index import CommandIndexSyncService
from watchtower_host.cli.introspection import iter_command_parser_specs
from watchtower_host.cli.parser import build_parser

REPO_ROOT = Path(__file__).resolve().parents[4]


def _command_doc_source_surfaces(doc_path: Path) -> tuple[str, str]:
    sections = extract_sections(load_markdown_body(doc_path))
    command_rows = parse_markdown_table(sections["Command"])
    table_source_surface = next(
        row["Value"] for row in command_rows if row.get("Field") == "Source Surface"
    )
    primary_source_surface = extract_code_spans(sections["Source Surface"])[0]
    return table_source_surface, primary_source_surface


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
    output_path = tmp_path / "command_index.json"

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
    assert "command.watchtower_core.pack" in spec_by_id
    assert "command.watchtower_core.pack.bootstrap" in spec_by_id
    assert "command.watchtower_core.pack.list" in spec_by_id
    assert "command.watchtower_core.pack.describe" in spec_by_id
    assert "command.watchtower_core.pack.validate" in spec_by_id
    assert "command.watchtower_core.plan" in spec_by_id
    assert "command.watchtower_core.plan.approve" in spec_by_id
    assert "command.watchtower_core.plan.bootstrap" in spec_by_id
    assert "command.watchtower_core.plan.closeout" in spec_by_id
    assert "command.watchtower_core.plan.closeout.initiative" in spec_by_id
    assert "command.watchtower_core.plan.closeout.purge_trace" in spec_by_id
    assert "command.watchtower_core.plan.confirm_inputs" in spec_by_id
    assert "command.watchtower_core.plan.query" in spec_by_id
    assert "command.watchtower_core.plan.query.artifacts" in spec_by_id
    assert "command.watchtower_core.plan.query.authority" in spec_by_id
    assert "command.watchtower_core.plan.query.coordination" in spec_by_id
    assert "command.watchtower_core.plan.query.initiatives" in spec_by_id
    assert "command.watchtower_core.plan.query.tasks" in spec_by_id
    assert "command.watchtower_core.plan.query.trace" in spec_by_id
    assert "command.watchtower_core.plan.task" in spec_by_id
    assert "command.watchtower_core.plan.task.create" in spec_by_id
    assert "command.watchtower_core.plan.task.update" in spec_by_id
    assert "command.watchtower_core.plan.task.transition" in spec_by_id
    assert "command.watchtower_core.sync.command_index" in spec_by_id
    assert "command.watchtower_core.sync.route_index" in spec_by_id
    assert (
        spec_by_id["command.watchtower_core"].implementation_path
        == "core/python/src/watchtower_host/cli/parser.py"
    )
    assert (
        spec_by_id["command.watchtower_core"].package_entrypoint
        == "watchtower_host.cli.main:main"
    )
    assert (
        spec_by_id["command.watchtower_core.doctor"].implementation_path
        == "core/python/src/watchtower_host/cli/doctor_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.route"].implementation_path
        == "core/python/src/watchtower_host/cli/route_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.route.preview"].implementation_path
        == "core/python/src/watchtower_host/cli/route_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan"].implementation_path
        == "plan/python/src/watchtower_plan/cli/namespace.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.approve"].implementation_path
        == "plan/python/src/watchtower_plan/cli/handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.bootstrap"].implementation_path
        == "plan/python/src/watchtower_plan/cli/handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.closeout"].implementation_path
        == "plan/python/src/watchtower_plan/cli/closeout.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.closeout.initiative"].implementation_path
        == "plan/python/src/watchtower_plan/cli/closeout.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.closeout.purge_trace"].implementation_path
        == "plan/python/src/watchtower_plan/cli/closeout.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.confirm_inputs"].implementation_path
        == "plan/python/src/watchtower_plan/cli/handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query.artifacts"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query.authority"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query.coordination"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query.initiatives"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query.tasks"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.query.trace"].implementation_path
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.task"].implementation_path
        == "plan/python/src/watchtower_plan/cli/tasks.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.task.create"].implementation_path
        == "plan/python/src/watchtower_plan/cli/tasks.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.task.update"].implementation_path
        == "plan/python/src/watchtower_plan/cli/tasks.py"
    )
    assert (
        spec_by_id["command.watchtower_core.plan.task.transition"].implementation_path
        == "plan/python/src/watchtower_plan/cli/tasks.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query"].implementation_path
        == "core/python/src/watchtower_host/cli/query_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.commands"].implementation_path
        == "core/python/src/watchtower_host/cli/query_discovery_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.paths"].implementation_path
        == "core/python/src/watchtower_host/cli/query_discovery_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.foundations"].implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.references"].implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.standards"].implementation_path
        == "core/python/src/watchtower_host/cli/query_knowledge_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.acceptance"].implementation_path
        == "core/python/src/watchtower_host/cli/query_records_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.query.evidence"].implementation_path
        == "core/python/src/watchtower_host/cli/query_records_family.py"
    )
    assert "command.watchtower_core.query.artifacts" not in spec_by_id
    assert "command.watchtower_core.query.authority" not in spec_by_id
    assert "command.watchtower_core.query.coordination" not in spec_by_id
    assert "command.watchtower_core.query.discrepancies" not in spec_by_id
    assert "command.watchtower_core.query.initiatives" not in spec_by_id
    assert "command.watchtower_core.query.projects" not in spec_by_id
    assert "command.watchtower_core.query.readiness" not in spec_by_id
    assert "command.watchtower_core.query.tasks" not in spec_by_id
    assert "command.watchtower_core.query.trace" not in spec_by_id
    assert (
        spec_by_id["command.watchtower_core.pack.bootstrap"].implementation_path
        == "core/python/src/watchtower_host/cli/pack_handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.pack.list"].implementation_path
        == "core/python/src/watchtower_host/cli/pack_handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.pack.describe"].implementation_path
        == "core/python/src/watchtower_host/cli/pack_handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.pack.validate"].implementation_path
        == "core/python/src/watchtower_host/cli/pack_handlers.py"
    )
    assert (
        spec_by_id["command.watchtower_core.sync.command_index"].implementation_path
        == "core/python/src/watchtower_host/cli/sync_family.py"
    )
    assert (
        spec_by_id["command.watchtower_core.sync.route_index"].implementation_path
        == "core/python/src/watchtower_host/cli/sync_family.py"
    )
    assert "command.watchtower_core.closeout" not in spec_by_id
    assert "command.watchtower_core.closeout.initiative" not in spec_by_id
    assert "command.watchtower_core.closeout.purge_trace" not in spec_by_id
    assert (
        spec_by_id["command.watchtower_core.validate.all"].implementation_path
        == "core/python/src/watchtower_host/cli/validate_family.py"
    )
    for spec in specs:
        assert (REPO_ROOT / spec.doc_path).exists()
        assert (REPO_ROOT / spec.implementation_path).exists()


def test_registry_backed_parser_specs_require_matching_command_doc_source_surfaces() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = CommandIndexSyncService(loader)

    document = service.build_document()
    implementation_by_doc = {
        entry["doc_path"]: entry["implementation_path"]
        for entry in document["entries"]
        if "implementation_path" in entry
    }

    assert (
        implementation_by_doc["core/docs/commands/core_python/watchtower_core.md"]
        == "core/python/src/watchtower_host/cli/parser.py"
    )
    package_entrypoint_by_doc = {
        entry["doc_path"]: entry["package_entrypoint"]
        for entry in document["entries"]
        if "package_entrypoint" in entry
    }
    assert (
        package_entrypoint_by_doc["core/docs/commands/core_python/watchtower_core.md"]
        == "watchtower_host.cli.main:main"
    )
    assert (
        implementation_by_doc["core/docs/commands/core_python/watchtower_core_doctor.md"]
        == "core/python/src/watchtower_host/cli/doctor_family.py"
    )
    assert (
        implementation_by_doc["plan/docs/commands/core_python/watchtower_core_plan_query.md"]
        == "plan/python/src/watchtower_plan/cli/query.py"
    )
    assert (
        implementation_by_doc["core/docs/commands/core_python/watchtower_core_sync_command_index.md"]
        == "core/python/src/watchtower_host/cli/sync_family.py"
    )
    assert (
        implementation_by_doc["core/docs/commands/core_python/watchtower_core_validate_all.md"]
        == "core/python/src/watchtower_host/cli/validate_family.py"
    )

    for doc_path, implementation_path in implementation_by_doc.items():
        table_source_surface, primary_source_surface = _command_doc_source_surfaces(
            REPO_ROOT / doc_path
        )
        assert table_source_surface == implementation_path
        assert primary_source_surface == implementation_path
