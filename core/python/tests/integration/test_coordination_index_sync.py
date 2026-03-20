from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_minimal_plan_pack,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.initiatives import InitiativeTaskSpec
from watchtower_plan.plan_workspace import (
    PLAN_COORDINATION_INDEX_PATH,
    PLAN_INITIATIVE_INDEX_PATH,
)
from watchtower_plan.query.coordination import (
    CoordinationQueryService,
    CoordinationSearchParams,
)
from watchtower_plan.sync.coordination_index import CoordinationIndexSyncService
from watchtower_plan.tasks import TaskLifecycleService, TaskUpdateParams

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_control_plane_fixture_repo(repo_root: Path) -> Path:
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


@pytest.fixture(scope="module")
def control_plane_fixture_baseline(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_control_plane_fixture_repo(
        tmp_path_factory.mktemp("coordination_index_baseline") / "repo"
    )


@pytest.fixture
def control_plane_fixture_repo(tmp_path: Path, control_plane_fixture_baseline: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(control_plane_fixture_baseline, repo_root)
    return repo_root


@pytest.fixture(scope="module")
def approved_initiative_fixture_baseline(
    tmp_path_factory: pytest.TempPathFactory,
    control_plane_fixture_baseline: Path,
) -> Path:
    repo_root = tmp_path_factory.mktemp("coordination_index_live_baseline") / "repo"
    copytree(control_plane_fixture_baseline, repo_root)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_active",
        title="Example Active Initiative",
        summary="Exercises coordination work selection.",
        task_specs=(
            InitiativeTaskSpec(
                title="Do the active work",
                summary="Carries the active work item.",
                slug="execution",
                task_id="task.example_active.execution.001",
                priority="high",
            ),
        ),
        approve=True,
    )
    return repo_root


@pytest.fixture
def approved_initiative_fixture_repo(
    tmp_path: Path,
    approved_initiative_fixture_baseline: Path,
) -> Path:
    repo_root = tmp_path / "repo"
    copytree(approved_initiative_fixture_baseline, repo_root)
    return repo_root


def _task_service(repo_root: Path) -> TaskLifecycleService:
    return TaskLifecycleService(ControlPlaneLoader(repo_root))


def _load_json(repo_root: Path, relative_path: str) -> dict[str, object]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def _write_json(repo_root: Path, relative_path: str, document: dict[str, object]) -> None:
    (repo_root / relative_path).write_text(
        f"{json.dumps(document, indent=2)}\n",
        encoding="utf-8",
    )


def _seed_historical_lookup_indexes(repo_root: Path) -> None:
    initiative_index = _load_json(repo_root, PLAN_INITIATIVE_INDEX_PATH)
    entries = initiative_index.get("entries")
    assert isinstance(entries, list) and entries
    template = dict(entries[0])

    active_entry = dict(template)
    active_entry.update(
        {
            "trace_id": "trace.example_active",
            "title": "Example Active Initiative",
            "summary": "Keeps one active initiative in the coordination slice.",
            "initiative_status": "active",
            "current_phase": "execution",
            "updated_at": "2026-03-10T20:00:00Z",
            "open_task_count": 1,
            "blocked_task_count": 0,
            "key_surface_path": "plan/initiatives/example_active/plan.md",
            "next_action": "Start active work.",
            "next_surface_path": "plan/initiatives/example_active/implementation_slice.md",
            "initiative_id": "initiative.example_active",
            "slug": "example_active",
            "source_surface_paths": [
                "plan/initiatives/example_active/initiative_brief.md",
                "plan/initiatives/example_active/design_record.md",
                "plan/initiatives/example_active/implementation_slice.md",
            ],
            "active_task_ids": ["task.example_active.execution.001"],
            "active_task_summaries": [
                {
                    "task_id": "task.example_active.execution.001",
                    "title": "Do the active work",
                    "task_status": "ready",
                    "priority": "high",
                    "owner": "repository_maintainer",
                    "doc_path": "plan/initiatives/example_active/.wt/tasks/execution/task.json",
                    "is_actionable": True,
                }
            ],
            "task_ids": ["task.example_active.execution.001"],
            "evidence_ids": ["evidence.example_active.validation_baseline"],
            "related_paths": [
                "plan/initiatives/example_active/initiative_brief.md",
                "plan/initiatives/example_active/design_record.md",
                "plan/initiatives/example_active/implementation_slice.md",
            ],
        }
    )
    active_entry.pop("closed_at", None)
    active_entry.pop("closure_reason", None)

    completed_entry = dict(template)
    completed_entry.update(
        {
            "trace_id": "trace.example_completed",
            "title": "Example Completed Initiative",
            "summary": "Provides one closed initiative for historical lookup coverage.",
            "initiative_status": "completed",
            "current_phase": "closed",
            "updated_at": "2026-03-10T20:00:00Z",
            "open_task_count": 0,
            "blocked_task_count": 0,
            "key_surface_path": "plan/initiatives/example_completed/plan.md",
            "next_action": "No further default action. Initiative is completed.",
            "next_surface_path": "plan/initiatives/example_completed/summary.md",
            "initiative_id": "initiative.example_completed",
            "slug": "example_completed",
            "source_surface_paths": [
                "plan/initiatives/example_completed/initiative_brief.md",
                "plan/initiatives/example_completed/design_record.md",
                "plan/initiatives/example_completed/implementation_slice.md",
            ],
            "task_ids": ["task.example_completed.closeout.001"],
            "evidence_ids": ["evidence.example_completed.validation_baseline"],
            "closed_at": "2026-03-10T20:00:00Z",
            "closure_reason": "Closed for historical lookup coverage.",
            "related_paths": [
                "plan/initiatives/example_completed/initiative_brief.md",
                "plan/initiatives/example_completed/design_record.md",
                "plan/initiatives/example_completed/implementation_slice.md",
            ],
        }
    )

    initiative_index["entries"] = [active_entry, completed_entry]
    _write_json(repo_root, PLAN_INITIATIVE_INDEX_PATH, initiative_index)

    coordination_index = _load_json(repo_root, PLAN_COORDINATION_INDEX_PATH)
    coordination_index.update(
        {
            "updated_at": "2026-03-10T20:00:00Z",
            "coordination_mode": "active_work",
            "summary": "One active initiative has actionable work.",
            "recommended_next_action": "Open the active initiative plan and start the ready task.",
            "recommended_surface_path": "plan/initiatives/example_active/plan.md",
            "active_initiative_count": 1,
            "blocked_task_count": 0,
            "actionable_task_count": 1,
            "entries": [active_entry],
            "actionable_tasks": [
                {
                    "trace_id": "trace.example_active",
                    "initiative_title": "Example Active Initiative",
                    "task_id": "task.example_active.execution.001",
                    "title": "Do the active work",
                    "task_status": "ready",
                    "priority": "high",
                    "owner": "repository_maintainer",
                    "doc_path": "plan/initiatives/example_active/.wt/tasks/execution/task.json",
                    "is_actionable": True,
                }
            ],
            "recent_closed_initiatives": [
                {
                    "trace_id": "trace.example_completed",
                    "title": "Example Completed Initiative",
                    "initiative_status": "completed",
                    "closed_at": "2026-03-10T20:00:00Z",
                    "key_surface_path": "plan/initiatives/example_completed/plan.md",
                    "closure_reason": "Closed for historical lookup coverage.",
                }
            ],
        }
    )
    _write_json(repo_root, PLAN_COORDINATION_INDEX_PATH, coordination_index)


def test_coordination_index_reports_active_work_when_actionable_tasks_exist(
    approved_initiative_fixture_repo: Path,
) -> None:
    repo_root = approved_initiative_fixture_repo
    _task_service(repo_root).update(
        TaskUpdateParams(
            task_id="task.example_active.execution.001",
            task_status="ready",
        ),
        write=True,
    )

    document = CoordinationIndexSyncService(ControlPlaneLoader(repo_root)).build_document()

    assert document["id"] == "index.coordination"
    assert document["coordination_mode"] == "active_work"
    assert document["active_initiative_count"] == 1
    assert document["actionable_task_count"] == 1
    assert document["recommended_surface_path"] == "plan/initiatives/example_active/plan.md"
    assert len(document["entries"]) == 1
    assert document["entries"][0]["trace_id"] == "trace.example_active"
    assert all(entry["initiative_status"] == "active" for entry in document["entries"])
    assert document["actionable_tasks"][0]["doc_path"] == (
        "plan/initiatives/example_active/.wt/tasks/execution/task.json"
    )
    assert isinstance(document["recent_closed_initiatives"], list)


def test_coordination_index_reports_ready_for_bootstrap_when_no_active_initiatives(
    control_plane_fixture_repo: Path,
) -> None:
    repo_root = control_plane_fixture_repo

    document = CoordinationIndexSyncService(ControlPlaneLoader(repo_root)).build_document()

    assert document["coordination_mode"] == "ready_for_bootstrap"
    assert document["active_initiative_count"] == 0
    assert document["actionable_task_count"] == 0
    assert document["recommended_surface_path"] == "plan/plan_overview.md"
    assert document["entries"] == []
    assert document["recent_closed_initiatives"] == []


def test_coordination_index_reports_blocked_work_when_execution_has_only_blocked_tasks(
    approved_initiative_fixture_repo: Path,
) -> None:
    repo_root = approved_initiative_fixture_repo
    _task_service(repo_root).update(
        TaskUpdateParams(
            task_id="task.example_active.execution.001",
            task_status="blocked",
        ),
        write=True,
    )

    document = CoordinationIndexSyncService(ControlPlaneLoader(repo_root)).build_document()

    assert document["coordination_mode"] == "blocked_work"
    assert document["active_initiative_count"] == 1
    assert document["actionable_task_count"] == 0
    assert document["blocked_task_count"] == 1
    assert document["recommended_surface_path"] == "plan/initiatives/example_active/plan.md"
    assert len(document["entries"]) == 1
    assert all(entry["initiative_status"] == "active" for entry in document["entries"])


def test_coordination_query_uses_initiative_index_for_explicit_historical_lookup(
    control_plane_fixture_repo: Path,
) -> None:
    repo_root = control_plane_fixture_repo
    _seed_historical_lookup_indexes(repo_root)

    result = CoordinationQueryService(ControlPlaneLoader(repo_root)).search(
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
