from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync import TraceabilityIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_traceability_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = TraceabilityIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert any(
        entry["trace_id"] == "trace.command_documentation_and_lookup"
        for entry in entries
    )
    assert any(entry["trace_id"] == "trace.core_python_foundation" for entry in entries)


def test_traceability_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = TraceabilityIndexSyncService(loader)
    output_path = tmp_path / "traceability_index.v1.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.traceability"


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def test_traceability_index_sync_uses_closed_at_as_effective_updated_at(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    traceability_path = (
        repo_root / "core/control_plane/indexes/traceability/traceability_index.v1.json"
    )
    document = json.loads(traceability_path.read_text(encoding="utf-8"))
    entries = document["entries"]
    assert isinstance(entries, list)
    target = next(
        entry
        for entry in entries
        if entry["trace_id"] == "trace.machine_first_coordination_surface"
    )
    target["initiative_status"] = "completed"
    target["updated_at"] = "2026-03-10T19:00:00Z"
    target["closed_at"] = "2026-03-10T23:59:59Z"
    target["closure_reason"] = "Closed for sync regression coverage."
    traceability_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")

    loader = ControlPlaneLoader(repo_root)
    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    rebuilt_target = next(
        entry
        for entry in rebuilt_entries
        if entry["trace_id"] == "trace.machine_first_coordination_surface"
    )
    assert rebuilt_target["updated_at"] == "2026-03-10T23:59:59Z"
