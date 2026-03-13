from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query.coordination import (
    CoordinationQueryService,
    CoordinationSearchParams,
)
from watchtower_core.repo_ops.sync.coordination_index import CoordinationIndexSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def _load_initiative_index(repo_root: Path) -> dict[str, object]:
    initiative_index_path = (
        repo_root / "core/control_plane/indexes/initiatives/initiative_index.v1.json"
    )
    return json.loads(initiative_index_path.read_text(encoding="utf-8"))


def _write_initiative_index(repo_root: Path, document: dict[str, object]) -> None:
    initiative_index_path = (
        repo_root / "core/control_plane/indexes/initiatives/initiative_index.v1.json"
    )
    initiative_index_path.write_text(
        f"{json.dumps(document, indent=2)}\n",
        encoding="utf-8",
    )


def test_coordination_index_reports_active_work_when_actionable_tasks_exist(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    initiative_index = _load_initiative_index(repo_root)
    entries = initiative_index["entries"]
    assert isinstance(entries, list)
    active_entry = entries[0]
    assert isinstance(active_entry, dict)
    active_entry["trace_id"] = "trace.example_active"
    active_entry["title"] = "Example Active Initiative"
    active_entry["initiative_status"] = "active"
    active_entry["current_phase"] = "execution"
    active_entry["updated_at"] = "2026-03-10T19:06:55Z"
    active_entry["open_task_count"] = 1
    active_entry["blocked_task_count"] = 0
    active_entry["next_action"] = "Continue the active task."
    active_entry["next_surface_path"] = "docs/planning/tasks/open/example_active.md"
    active_entry["primary_owner"] = "repository_maintainer"
    active_entry["active_owners"] = ["repository_maintainer"]
    active_entry["active_task_ids"] = ["task.example_active.execution.001"]
    active_entry["active_task_summaries"] = [
        {
            "task_id": "task.example_active.execution.001",
            "title": "Do the active work",
            "task_status": "in_progress",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": "docs/planning/tasks/open/example_active.md",
            "is_actionable": True,
        }
    ]
    active_entry["task_ids"] = ["task.example_active.execution.001"]
    for entry in entries[1:]:
        assert isinstance(entry, dict)
        entry["initiative_status"] = "completed"
        entry["current_phase"] = "closed"
        entry["closed_at"] = "2026-03-10T18:00:00Z"
        entry["closure_reason"] = "Closed for fixture setup."
        entry.pop("active_task_ids", None)
        entry.pop("active_task_summaries", None)
        entry["open_task_count"] = 0
        entry["blocked_task_count"] = 0

    _write_initiative_index(repo_root, initiative_index)

    loader = ControlPlaneLoader(repo_root)
    service = CoordinationIndexSyncService(loader)

    document = service.build_document()

    assert document["id"] == "index.coordination"
    assert document["coordination_mode"] == "active_work"
    assert document["active_initiative_count"] == 1
    assert document["actionable_task_count"] == 1
    assert document["recommended_surface_path"] == "docs/planning/tasks/open/example_active.md"
    assert len(document["entries"]) == 1
    assert document["entries"][0]["trace_id"] == "trace.example_active"
    assert all(entry["initiative_status"] == "active" for entry in document["entries"])
    assert document["recent_closed_initiatives"]


def test_coordination_index_reports_ready_for_bootstrap_when_no_active_initiatives(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    initiative_index = _load_initiative_index(repo_root)
    entries = initiative_index["entries"]
    assert isinstance(entries, list)
    for entry in entries:
        assert isinstance(entry, dict)
        entry["initiative_status"] = "completed"
        entry["current_phase"] = "closed"
        entry["closed_at"] = "2026-03-10T18:00:00Z"
        entry["closure_reason"] = "Closed for fixture setup."
        entry.pop("active_task_ids", None)
        entry.pop("active_task_summaries", None)
        entry["open_task_count"] = 0
        entry["blocked_task_count"] = 0

    _write_initiative_index(repo_root, initiative_index)

    loader = ControlPlaneLoader(repo_root)
    service = CoordinationIndexSyncService(loader)

    document = service.build_document()

    assert document["coordination_mode"] == "ready_for_bootstrap"
    assert document["active_initiative_count"] == 0
    assert document["actionable_task_count"] == 0
    assert document["recommended_surface_path"] == "docs/planning/README.md"
    assert document["entries"] == []
    assert document["recent_closed_initiatives"]


def test_coordination_index_reports_blocked_work_when_execution_has_only_blocked_tasks(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    initiative_index = _load_initiative_index(repo_root)
    entries = initiative_index["entries"]
    assert isinstance(entries, list)
    blocked_entry = entries[0]
    assert isinstance(blocked_entry, dict)
    blocked_entry["trace_id"] = "trace.example_blocked"
    blocked_entry["title"] = "Example Blocked Initiative"
    blocked_entry["initiative_status"] = "active"
    blocked_entry["current_phase"] = "execution"
    blocked_entry["updated_at"] = "2026-03-10T19:06:55Z"
    blocked_entry["open_task_count"] = 1
    blocked_entry["blocked_task_count"] = 1
    blocked_entry["next_action"] = "Resolve the blocker before continuing."
    blocked_entry["next_surface_path"] = "docs/planning/tasks/open/example_blocked.md"
    blocked_entry["primary_owner"] = "repository_maintainer"
    blocked_entry["active_owners"] = ["repository_maintainer"]
    blocked_entry["active_task_ids"] = ["task.example_blocked.execution.001"]
    blocked_entry["active_task_summaries"] = [
        {
            "task_id": "task.example_blocked.execution.001",
            "title": "Wait on dependency resolution",
            "task_status": "blocked",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": "docs/planning/tasks/open/example_blocked.md",
            "is_actionable": False,
            "depends_on": ["task.example_blocked.prerequisite.001"],
        }
    ]
    blocked_entry["task_ids"] = ["task.example_blocked.execution.001"]
    for entry in entries[1:]:
        assert isinstance(entry, dict)
        entry["initiative_status"] = "completed"
        entry["current_phase"] = "closed"
        entry["closed_at"] = "2026-03-10T18:00:00Z"
        entry["closure_reason"] = "Closed for fixture setup."
        entry.pop("active_task_ids", None)
        entry.pop("active_task_summaries", None)
        entry["open_task_count"] = 0
        entry["blocked_task_count"] = 0

    _write_initiative_index(repo_root, initiative_index)

    loader = ControlPlaneLoader(repo_root)
    service = CoordinationIndexSyncService(loader)

    document = service.build_document()

    assert document["coordination_mode"] == "blocked_work"
    assert document["active_initiative_count"] == 1
    assert document["actionable_task_count"] == 0
    assert document["blocked_task_count"] == 1
    assert document["recommended_surface_path"] == "docs/planning/tasks/open/example_blocked.md"
    assert len(document["entries"]) == 1
    assert all(entry["initiative_status"] == "active" for entry in document["entries"])


def test_coordination_query_uses_initiative_index_for_explicit_historical_lookup(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    initiative_index = _load_initiative_index(repo_root)
    entries = initiative_index["entries"]
    assert isinstance(entries, list)

    active_entry = entries[0]
    assert isinstance(active_entry, dict)
    active_entry["trace_id"] = "trace.example_active"
    active_entry["title"] = "Example Active Initiative"
    active_entry["initiative_status"] = "active"
    active_entry["current_phase"] = "execution"
    active_entry["updated_at"] = "2026-03-10T19:06:55Z"
    active_entry["open_task_count"] = 1
    active_entry["blocked_task_count"] = 0
    active_entry["next_action"] = "Continue the active task."
    active_entry["next_surface_path"] = "docs/planning/tasks/open/example_active.md"
    active_entry["primary_owner"] = "repository_maintainer"
    active_entry["active_owners"] = ["repository_maintainer"]
    active_entry["active_task_ids"] = ["task.example_active.execution.001"]
    active_entry["active_task_summaries"] = [
        {
            "task_id": "task.example_active.execution.001",
            "title": "Do the active work",
            "task_status": "in_progress",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": "docs/planning/tasks/open/example_active.md",
            "is_actionable": True,
        }
    ]
    active_entry["task_ids"] = ["task.example_active.execution.001"]

    completed_entry = entries[1]
    assert isinstance(completed_entry, dict)
    completed_entry["trace_id"] = "trace.example_completed"
    completed_entry["title"] = "Example Completed Initiative"
    completed_entry["initiative_status"] = "completed"
    completed_entry["current_phase"] = "closed"
    completed_entry["closed_at"] = "2026-03-10T20:00:00Z"
    completed_entry["closure_reason"] = "Closed for historical lookup coverage."
    completed_entry["open_task_count"] = 0
    completed_entry["blocked_task_count"] = 0
    completed_entry.pop("active_task_ids", None)
    completed_entry.pop("active_task_summaries", None)

    for entry in entries[2:]:
        assert isinstance(entry, dict)
        entry["initiative_status"] = "completed"
        entry["current_phase"] = "closed"
        entry["closed_at"] = "2026-03-10T18:00:00Z"
        entry["closure_reason"] = "Closed for fixture setup."
        entry["open_task_count"] = 0
        entry["blocked_task_count"] = 0
        entry.pop("active_task_ids", None)
        entry.pop("active_task_summaries", None)

    _write_initiative_index(repo_root, initiative_index)

    loader = ControlPlaneLoader(repo_root)
    sync_service = CoordinationIndexSyncService(loader)
    sync_service.write_document(sync_service.build_document())

    result = CoordinationQueryService(loader).search(
        CoordinationSearchParams(
            initiative_status="completed",
            trace_id="trace.example_completed",
        )
    )

    assert len(result.index.entries) == 1
    assert result.index.entries[0].trace_id == "trace.example_active"
    assert all(entry.initiative_status == "active" for entry in result.index.entries)
    assert len(result.entries) == 1
    assert result.entries[0].trace_id == "trace.example_completed"
    assert result.entries[0].initiative_status == "completed"
