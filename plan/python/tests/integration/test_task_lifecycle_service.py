from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest
from watchtower_plan.query import (
    InitiativeQueryService,
    ReadinessQueryService,
    ReadinessSearchParams,
    TaskQueryService,
)
from watchtower_plan.tasks import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskTransitionParams,
    TaskUpdateParams,
)
from watchtower_plan.testing.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_governed_applies_to_targets,
    materialize_minimal_plan_pack,
)

from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "core" / "docs", repo_root / "core" / "docs")
    (repo_root / "core" / "python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    materialize_governed_applies_to_targets(repo_root, REPO_ROOT)
    return repo_root


def test_task_create_write_refreshes_task_and_initiative_surfaces(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.workflow_system_operationalization"
    task_id = "task.workflow_system_operationalization.validate_task_lifecycle_slice"
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Workflow System Operationalization",
        summary="Bootstraps the live initiative package for task lifecycle validation.",
    )
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.create(
        TaskCreateParams(
            task_id=task_id,
            trace_id=trace_id,
            title="Validate the task lifecycle slice",
            summary="Validates the bounded live task lifecycle slice after implementation lands.",
            task_kind="validation",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Write the live task lifecycle command coverage.",),
            done_when_items=("The live task lifecycle slice validates cleanly.",),
            applies_to=("core/python/src/watchtower_core/",),
            related_ids=("initiative.workflow_routing_and_authoring",),
        ),
        write=True,
    )

    assert result.wrote is True
    assert (
        result.doc_path == "plan/initiatives/workflow_system_operationalization/.wt/tasks/"
        "validate_the_task_lifecycle_slice/task.json"
    )
    assert (repo_root / result.doc_path).exists()

    loader = ControlPlaneLoader(repo_root)
    task_entry = TaskQueryService(loader).get(task_id)
    assert task_entry.doc_path == result.doc_path
    assert task_entry.status == "active"
    assert task_entry.task_status == "planned"

    initiative_entry = InitiativeQueryService(loader).get(trace_id)
    assert task_id in initiative_entry.active_task_ids
    assert initiative_entry.open_task_count >= 2


def test_task_update_write_keeps_terminal_task_at_stable_live_path(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.workflow_system_operationalization_terminal"
    task_id = "task.workflow_system_operationalization_terminal.finish_task_lifecycle_slice"
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Workflow System Operationalization Terminal",
        summary="Bootstraps the live initiative package for terminal task updates.",
        approve=True,
    )
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))
    create_result = service.create(
        TaskCreateParams(
            task_id=task_id,
            trace_id=trace_id,
            title="Finish the task lifecycle slice",
            summary="Finishes the live task lifecycle slice after validation passes.",
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
            task_status="completed",
            owner="validation_engineer",
            scope_items=("Close the lifecycle slice without moving the live task path.",),
            done_when_items=("The live task remains at its initiative-local JSON path.",),
        ),
        write=True,
    )

    assert result.wrote is True
    assert result.moved is False
    assert result.previous_doc_path is None
    assert result.doc_path == create_result.doc_path
    assert (repo_root / result.doc_path).exists()

    loader = ControlPlaneLoader(repo_root)
    task_entry = TaskQueryService(loader).get(task_id)
    assert task_entry.status == "active"
    assert task_entry.task_status == "completed"
    assert task_entry.owner == "validation_engineer"
    assert task_entry.doc_path == result.doc_path


def test_task_transition_dry_run_can_recommend_closeout_for_last_traced_task(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.task_lifecycle_service_preview"
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Task Lifecycle Service Preview",
        summary="Bootstraps one traced task for dry-run closeout coverage.",
        approve=True,
    )
    task_id = "task.task_lifecycle_service_preview.seed_bootstrap"
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    result = service.transition(
        TaskTransitionParams(task_id=task_id, task_status="completed"),
        write=False,
    )

    assert result.wrote is False
    assert result.changed is True
    assert result.closeout_recommended is True

    task_entry = TaskQueryService(ControlPlaneLoader(repo_root)).get(task_id)
    assert task_entry.status == "active"
    assert task_entry.task_status == "planned"


def test_task_create_rejects_unknown_dependency_ids(tmp_path: Path) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.task_lifecycle_service_invalid_dependency"
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Task Lifecycle Invalid Dependency",
        summary="Bootstraps one initiative package before invalid task creation.",
    )
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    with pytest.raises(ValueError, match="unknown task ID"):
        service.create(
            TaskCreateParams(
                task_id="task.task_lifecycle_service_invalid_dependency.reject_invalid_dependency",
                trace_id=trace_id,
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


def test_task_update_write_preserves_governed_companion_paths_when_task_status_changes(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.task_lifecycle_service_path_repair"
    task_id = "task.task_lifecycle_service_path_repair.repair_companion_task_paths"
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Task Lifecycle Service Path Stability",
        summary="Bootstraps one initiative package before stable-path task updates.",
        approve=True,
    )
    service = TaskLifecycleService(ControlPlaneLoader(repo_root))

    created = service.create(
        TaskCreateParams(
            task_id=task_id,
            trace_id=trace_id,
            title="Repair companion task paths",
            summary="Exercises stable companion paths when a live task reaches terminal state.",
            task_kind="governance",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Create the traced live task.",),
            done_when_items=("The traced live task exists.",),
        ),
        write=True,
    )

    contract_relative_path = (
        "core/control_plane/contracts/acceptance/task_lifecycle_service_path_repair_acceptance.json"
    )
    evidence_relative_path = (
        "core/control_plane/records/validation_evidence/"
        "task_lifecycle_service_path_repair_planning_baseline.json"
    )
    (repo_root / contract_relative_path).write_text(
        json.dumps(
            {
                "$schema": "urn:watchtower:schema:artifacts:contracts:acceptance-contract:v1",
                "id": "contract.acceptance.task_lifecycle_service_path_repair",
                "title": "Task Lifecycle Service Path Repair Acceptance Contract",
                "status": "active",
                "trace_id": trace_id,
                "source_surface_path": created.doc_path,
                "entries": [
                    {
                        "acceptance_id": "ac.task_lifecycle_service_path_repair.001",
                        "summary": "Stable task paths remain valid in governed companions.",
                        "validation_targets": [created.doc_path],
                        "related_paths": [created.doc_path],
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / evidence_relative_path).write_text(
        json.dumps(
            {
                "$schema": "urn:watchtower:schema:artifacts:records:validation-evidence:v1",
                "id": "evidence.task_lifecycle_service_path_repair.planning_baseline",
                "title": "Task Lifecycle Service Path Repair Evidence",
                "status": "active",
                "trace_id": trace_id,
                "overall_result": "passed",
                "recorded_at": "2026-03-13T02:00:00Z",
                "source_acceptance_contract_ids": [
                    "contract.acceptance.task_lifecycle_service_path_repair"
                ],
                "checks": [
                    {
                        "check_id": "check.task_lifecycle_service_path_repair.001",
                        "title": "Stable task paths remain valid in evidence.",
                        "result": "passed",
                        "subject_paths": [created.doc_path],
                    }
                ],
                "related_paths": [created.doc_path],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    result = service.update(
        TaskUpdateParams(
            task_id=task_id,
            task_status="completed",
        ),
        write=True,
    )

    assert result.doc_path == created.doc_path

    contract = json.loads((repo_root / contract_relative_path).read_text(encoding="utf-8"))
    targets = contract["entries"][0]["validation_targets"]
    assert targets == [created.doc_path]
    assert contract["entries"][0]["related_paths"] == [created.doc_path]

    evidence = json.loads((repo_root / evidence_relative_path).read_text(encoding="utf-8"))
    assert evidence["related_paths"] == [created.doc_path]
    assert evidence["checks"][0]["subject_paths"] == [created.doc_path]


def test_task_transition_marks_execution_started_on_approved_initiative(
    tmp_path: Path,
) -> None:
    repo_root = _copy_repo_subset(tmp_path)
    trace_id = "trace.task_lifecycle_service_execution_start"
    task_id = "task.task_lifecycle_service_execution_start.seed_bootstrap"
    bootstrap_packwide_initiative(
        repo_root,
        trace_id=trace_id,
        title="Task Lifecycle Execution Start",
        summary="Bootstraps one initiative package before the first execution transition.",
        approve=True,
    )
    loader = ControlPlaneLoader(repo_root)
    service = TaskLifecycleService(loader)

    result = service.transition(
        TaskTransitionParams(task_id=task_id, task_status="in_progress"),
        write=True,
    )

    assert result.wrote is True

    initiative_state = json.loads(
        (
            repo_root
            / "plan"
            / "initiatives"
            / "task_lifecycle_service_execution_start"
            / ".wt"
            / "initiative.json"
        ).read_text(encoding="utf-8")
    )
    assert initiative_state["lifecycle_stage"] == "in_progress"
    assert initiative_state["gate_state"]["approval_status"] == "approved"
    assert initiative_state["gate_state"]["ready_for_execution"] is True

    events_root = (
        repo_root
        / "plan"
        / "initiatives"
        / "task_lifecycle_service_execution_start"
        / ".wt"
        / "events"
    )
    event_types = [
        json.loads(path.read_text(encoding="utf-8"))["event_type"]
        for path in sorted(events_root.glob("*.json"))
    ]
    assert "execution_started" in event_types

    readiness_entry = ReadinessQueryService(loader).search(
        ReadinessSearchParams(trace_id=trace_id)
    )[0]
    assert readiness_entry.lifecycle_stage == "in_progress"
