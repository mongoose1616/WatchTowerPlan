from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import TaskIndexEntry
from watchtower_core.repo_ops.sync.initiative_index import (
    InitiativeIndexSyncService,
    _build_active_task_summaries,
    _select_coordination_task,
    _task_is_blocked,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def _task(
    *,
    task_id: str,
    title: str,
    doc_path: str,
    task_status: str = "ready",
    priority: str = "high",
    depends_on: tuple[str, ...] = (),
    blocked_by: tuple[str, ...] = (),
) -> TaskIndexEntry:
    return TaskIndexEntry(
        task_id=task_id,
        title=title,
        summary=title,
        status="active",
        task_status=task_status,
        task_kind="feature",
        priority=priority,
        owner="repository_maintainer",
        doc_path=doc_path,
        updated_at="2026-03-10T18:10:36Z",
        trace_id="trace.preimplementation_repo_review_and_hardening",
        depends_on=depends_on,
        blocked_by=blocked_by,
    )


def test_select_coordination_task_prefers_actionable_dependency_root() -> None:
    machine_coordination = _task(
        task_id="task.preimplementation_repo_review_and_hardening.machine_coordination.001",
        title="Strengthen the machine coordination start-here surface",
        doc_path="docs/planning/tasks/open/preimplementation_machine_coordination.md",
    )
    core_modularity = _task(
        task_id="task.preimplementation_repo_review_and_hardening.core_modularity.001",
        title="Split core monoliths and add supplemental schema loading",
        doc_path="docs/planning/tasks/open/preimplementation_core_modularity.md",
        depends_on=(machine_coordination.task_id,),
    )
    active_tasks = (core_modularity, machine_coordination)
    task_lookup = {task.task_id: task for task in active_tasks}

    chosen = _select_coordination_task(active_tasks, task_lookup)

    assert chosen is not None
    assert chosen.task_id == machine_coordination.task_id


def test_active_task_summaries_mark_dependency_blocked_tasks() -> None:
    blocker = _task(
        task_id="task.example.blocker.001",
        title="Finish the prerequisite task",
        doc_path="docs/planning/tasks/open/example_blocker.md",
    )
    blocked = _task(
        task_id="task.example.blocked.001",
        title="Land the dependent task",
        doc_path="docs/planning/tasks/open/example_blocked.md",
        depends_on=(blocker.task_id,),
    )
    active_tasks = (blocked, blocker)
    task_lookup = {task.task_id: task for task in active_tasks}

    summaries = _build_active_task_summaries(active_tasks, task_lookup)

    blocker_summary = next(item for item in summaries if item["task_id"] == blocker.task_id)
    blocked_summary = next(item for item in summaries if item["task_id"] == blocked.task_id)

    assert blocker_summary["is_actionable"] is True
    assert blocked_summary["is_actionable"] is False
    assert blocked_summary["depends_on"] == [blocker.task_id]
    assert _task_is_blocked(blocked, task_lookup) is True


def test_initiative_index_allows_validation_phase_without_active_tasks(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    trace_id = "trace.core_python_foundation"
    traceability_path = (
        repo_root / "core/control_plane/indexes/traceability/traceability_index.v1.json"
    )
    task_index_path = repo_root / "core/control_plane/indexes/tasks/task_index.v1.json"

    traceability_document = json.loads(traceability_path.read_text(encoding="utf-8"))
    trace_entries = traceability_document["entries"]
    assert isinstance(trace_entries, list)
    trace_entry = next(entry for entry in trace_entries if entry["trace_id"] == trace_id)
    trace_entry["initiative_status"] = "active"
    trace_entry["updated_at"] = "2026-03-11T06:21:01Z"
    trace_entry.pop("closed_at", None)
    trace_entry.pop("closure_reason", None)
    trace_entry.pop("superseded_by_trace_id", None)
    trace_entry.pop("evidence_ids", None)
    traceability_path.write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )

    task_index_document = json.loads(task_index_path.read_text(encoding="utf-8"))
    task_entries = task_index_document["entries"]
    assert isinstance(task_entries, list)
    for entry in task_entries:
        if entry.get("trace_id") != trace_id:
            continue
        entry["status"] = "active"
        entry["task_status"] = "done"
    task_index_path.write_text(
        f"{json.dumps(task_index_document, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    rebuilt = InitiativeIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    initiative_entry = next(entry for entry in rebuilt_entries if entry["trace_id"] == trace_id)
    assert initiative_entry["initiative_status"] == "active"
    assert initiative_entry["current_phase"] == "validation"
    assert initiative_entry["open_task_count"] == 0
    assert "active_task_ids" not in initiative_entry
    assert "active_task_summaries" not in initiative_entry
    assert (
        initiative_entry["next_surface_path"]
        == "docs/commands/core_python/watchtower_core_validate_acceptance.md"
    )
