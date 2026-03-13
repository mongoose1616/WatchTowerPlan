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


def test_traceability_index_sync_reopens_completed_initiative_when_active_task_reappears(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    trace_id = "trace.machine_first_coordination_surface"
    traceability_path = (
        repo_root / "core/control_plane/indexes/traceability/traceability_index.v1.json"
    )
    task_index_path = repo_root / "core/control_plane/indexes/tasks/task_index.v1.json"

    traceability_document = json.loads(traceability_path.read_text(encoding="utf-8"))
    trace_entries = traceability_document["entries"]
    assert isinstance(trace_entries, list)
    target_trace = next(entry for entry in trace_entries if entry["trace_id"] == trace_id)
    target_trace["initiative_status"] = "completed"
    target_trace["updated_at"] = "2026-03-10T20:00:00Z"
    target_trace["closed_at"] = "2026-03-10T20:30:00Z"
    target_trace["closure_reason"] = "Closed before a follow-up task was discovered."
    traceability_path.write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )

    task_index_document = json.loads(task_index_path.read_text(encoding="utf-8"))
    task_entries = task_index_document["entries"]
    assert isinstance(task_entries, list)
    target_task = next(entry for entry in task_entries if entry.get("trace_id") == trace_id)
    target_task["status"] = "active"
    target_task["task_status"] = "ready"
    target_task["doc_path"] = "docs/planning/tasks/open/machine_first_coordination_surface.md"
    target_task["updated_at"] = "2026-03-10T23:59:59Z"
    task_index_path.write_text(
        f"{json.dumps(task_index_document, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    rebuilt_target = next(entry for entry in rebuilt_entries if entry["trace_id"] == trace_id)
    assert rebuilt_target["initiative_status"] == "active"
    assert rebuilt_target["updated_at"] == "2026-03-10T23:59:59Z"
    assert "closed_at" not in rebuilt_target
    assert "closure_reason" not in rebuilt_target
