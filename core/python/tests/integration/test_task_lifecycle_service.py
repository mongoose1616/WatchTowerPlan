from __future__ import annotations

from pathlib import Path
from shutil import copytree

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query import InitiativeQueryService, TaskQueryService
from watchtower_core.repo_ops.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskTransitionParams,
    TaskUpdateParams,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    copytree(REPO_ROOT / "docs", repo_root / "docs")
    return repo_root


def test_task_create_write_refreshes_task_and_initiative_surfaces(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    task_id = "task.workflow_system_operationalization.task_cli.validation.001"
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id=task_id,
            trace_id="trace.workflow_system_operationalization",
            title="Validate the task lifecycle slice",
            summary="Validates the bounded task lifecycle slice after implementation lands.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Write the task lifecycle command family.",),
            done_when_items=("The task lifecycle slice validates cleanly.",),
            applies_to=("core/python/src/watchtower_core/",),
            related_ids=("design.features.workflow_routing_and_authoring",),
        ),
        write=True,
    )

    assert result.wrote is True
    assert result.doc_path == "docs/planning/tasks/open/validate_the_task_lifecycle_slice.md"
    assert (repo_root / result.doc_path).exists()

    loader = ControlPlaneLoader(repo_root)
    task_entry = TaskQueryService(loader).get(task_id)
    assert task_entry.doc_path == result.doc_path
    assert task_entry.task_status == "backlog"

    initiative_entry = InitiativeQueryService(loader).get(
        "trace.workflow_system_operationalization"
    )
    assert task_id in initiative_entry.active_task_ids


def test_task_update_write_moves_terminal_task_to_closed(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    task_id = "task.workflow_system_operationalization.task_cli.validation.002"
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))
    create_result = service.create(
        TaskCreateParams(
            task_id=task_id,
            trace_id="trace.workflow_system_operationalization",
            title="Finish the task lifecycle slice",
            summary="Finishes the task lifecycle slice after validation passes.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Close the bounded lifecycle slice.",),
            done_when_items=("The lifecycle slice is closed cleanly.",),
        ),
        write=True,
    )

    result = service.update(
        TaskUpdateParams(
            task_id=task_id,
            task_status="done",
            owner="validation_engineer",
            scope_items=("Close the lifecycle slice and archive the task.",),
            done_when_items=("The task record is moved under closed/.",),
        ),
        write=True,
    )

    assert result.wrote is True
    assert result.moved is True
    assert result.previous_doc_path == create_result.doc_path
    assert result.doc_path == "docs/planning/tasks/closed/finish_the_task_lifecycle_slice.md"
    assert not (repo_root / create_result.doc_path).exists()
    assert (repo_root / result.doc_path).exists()

    loader = ControlPlaneLoader(repo_root)
    task_entry = TaskQueryService(loader).get(task_id)
    assert task_entry.task_status == "done"
    assert task_entry.owner == "validation_engineer"
    assert task_entry.doc_path == result.doc_path


def test_task_transition_dry_run_can_recommend_closeout_for_last_traced_task(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    task_id = "task.task_lifecycle_service.preview.001"
    trace_id = "trace.task_lifecycle_service_preview"
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    service.create(
        TaskCreateParams(
            task_id=task_id,
            trace_id=trace_id,
            title="Preview the closeout recommendation",
            summary="Previews whether the last traced task can recommend closeout.",
            task_kind="documentation",
            priority="medium",
            owner="repository_maintainer",
            scope_items=("Create one traced task for dry-run transition coverage.",),
            done_when_items=("The task exists in the open task corpus.",),
        ),
        write=True,
    )

    result = service.transition(
        TaskTransitionParams(task_id=task_id, task_status="done"),
        write=False,
    )

    assert result.wrote is False
    assert result.changed is True
    assert result.closeout_recommended is True

    task_entry = TaskQueryService(ControlPlaneLoader(repo_root)).get(task_id)
    assert task_entry.task_status == "backlog"


def test_task_create_rejects_unknown_dependency_ids(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(ValueError, match="unknown task ID"):
        service.create(
            TaskCreateParams(
                task_id="task.task_lifecycle_service.invalid_dependency.001",
                title="Reject the invalid dependency",
                summary="Rejects task creation when a dependency task ID is unknown.",
                task_kind="documentation",
                priority="medium",
                owner="repository_maintainer",
                scope_items=("Attempt invalid task creation.",),
                done_when_items=("The command fails closed.",),
                depends_on=("task.missing.dependency.001",),
            ),
            write=False,
        )
