from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskUpdateParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "docs" / "planning", repo_root / "docs" / "planning")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def test_task_create_can_recommend_closeout_for_terminal_single_trace(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.done.001",
            trace_id="trace.unit_test_trace_done",
            title="Complete the trace",
            summary="Creates the final terminal task for a new trace.",
            task_kind="feature",
            priority="medium",
            owner="repository_maintainer",
            task_status="done",
            scope_items=("Create the task.",),
            done_when_items=("The task exists.",),
            file_stem="unit_test_trace_done",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=False,
    )

    assert result.changed is True
    assert result.wrote is False
    assert result.closeout_recommended is True
    assert result.doc_path == "docs/planning/tasks/closed/unit_test_trace_done.md"


def test_task_update_can_move_task_and_clear_optional_fields(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)

    created = service.create(
        TaskCreateParams(
            task_id="task.unit_test_trace.lifecycle.001",
            trace_id="trace.unit_test_trace_lifecycle",
            title="Lifecycle task",
            summary="A task that will be updated.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Create the task.",),
            done_when_items=("The task exists.",),
            applies_to=("core/python/tests/unit",),
            related_ids=("prd.unit_test_hardening_and_rebalancing",),
            file_stem="lifecycle_task",
            updated_at="2026-03-10T23:59:59Z",
        ),
        write=True,
    )

    result = service.update(
        TaskUpdateParams(
            task_id=created.task_id,
            title="Lifecycle task complete",
            summary="The task is now complete.",
            task_status="done",
            clear_trace_id=True,
            clear_applies_to=True,
            clear_related_ids=True,
            scope_items=("Confirm the final state.",),
            done_when_items=("The task moved to closed.",),
            file_stem="lifecycle_task_complete",
            updated_at="2026-03-11T00:00:00Z",
        ),
        write=True,
    )

    assert result.changed is True
    assert result.moved is True
    assert result.wrote is True
    assert result.previous_doc_path == "docs/planning/tasks/open/lifecycle_task.md"
    assert result.doc_path == "docs/planning/tasks/closed/lifecycle_task_complete.md"
    assert not (repo_root / result.previous_doc_path).exists()

    written_text = (repo_root / result.doc_path).read_text(encoding="utf-8")
    assert "trace_id:" not in written_text
    assert "applies_to:" not in written_text
    assert "related_ids:" not in written_text
    assert "Lifecycle task complete" in written_text
    assert "The task is now complete." in written_text

    coordination_index_path = (
        repo_root / "core/control_plane/indexes/coordination/coordination_index.v1.json"
    )
    coordination_index = json.loads(coordination_index_path.read_text(encoding="utf-8"))
    assert coordination_index["status"] == "active"


def test_task_update_rejects_conflicting_clear_flags(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="Cannot provide replacement values and clear depends_on in the same call.",
    ):
        service.update(
            TaskUpdateParams(
                task_id="task.local_task_tracking.github_sync.001",
                depends_on=("task.bootstrap.001",),
                clear_depends_on=True,
            ),
            write=False,
        )


def test_task_create_rejects_self_reference(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="blocked_by cannot reference the current task: task.unit_test_trace.self.001",
    ):
        service.create(
            TaskCreateParams(
                task_id="task.unit_test_trace.self.001",
                trace_id="trace.unit_test_trace_self",
                title="Self reference",
                summary="A task with an invalid self reference.",
                task_kind="feature",
                priority="medium",
                owner="repository_maintainer",
                scope_items=("Create the task.",),
                done_when_items=("The task exists.",),
                blocked_by=("task.unit_test_trace.self.001",),
            ),
            write=False,
        )
