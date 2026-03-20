from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree, rmtree

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.initiatives import (
    DeferredItemSpec,
    InitiativeBootstrapParams,
    InitiativePackageService,
    InitiativeTaskSpec,
)
from watchtower_plan.tasks import (
    TaskCreateParams,
    TaskLifecycleService,
)
from watchtower_plan.plan_workspace import PlanWorkspaceService
from watchtower_plan.projects import (
    ProjectBootstrapParams,
    ProjectRepositoryLinkSpec,
    ProjectWorkspaceService,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
INITIATIVE_SLUG = "unit_test_plan_workspace"
TRACE_ID = f"trace.{INITIATIVE_SLUG}"
UPDATED_AT = "2026-03-17T15:30:00Z"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "plan", repo_root / "plan")
    for path in (repo_root / "plan" / "initiatives").iterdir():
        if path.name == "README.md":
            continue
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()
    for path in (repo_root / "plan" / "projects").iterdir():
        if path.name == "README.md":
            continue
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()
    (repo_root / "core" / "python").mkdir(parents=True)
    loader = ControlPlaneLoader(repo_root)
    PlanWorkspaceService(loader).sync(write=True)
    ProjectWorkspaceService(loader).sync(write=True)
    return repo_root


def _bootstrap_params(
    *,
    deferred_items: tuple[DeferredItemSpec, ...] = (),
    include_decision_notes: bool = False,
) -> InitiativeBootstrapParams:
    seed_task_id = f"task.{INITIATIVE_SLUG}.seed_initiative_contracts"
    return InitiativeBootstrapParams(
        trace_id=TRACE_ID,
        title="Unit Test Plan Workspace",
        summary="Bootstraps one initiative-local package for integration testing.",
        owner="repository_maintainer",
        task_specs=(
            InitiativeTaskSpec(
                title="Seed initiative contracts",
                summary="Creates the initiative-local state, event, and evidence shells.",
                slug="seed_initiative_contracts",
                task_id=seed_task_id,
            ),
            InitiativeTaskSpec(
                title="Validate readiness gate",
                summary="Proves readiness blocks until the package is reviewed and approved.",
                slug="validate_readiness_gate",
                depends_on=(seed_task_id,),
            ),
        ),
        deferred_items=deferred_items,
        include_decision_notes=include_decision_notes,
        updated_at=UPDATED_AT,
    )


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _initiative_root(repo_root: Path) -> Path:
    return repo_root / "plan" / "initiatives" / INITIATIVE_SLUG


def _initiative_state(repo_root: Path) -> dict[str, object]:
    return _load_json(_initiative_root(repo_root) / ".wt" / "initiative.json")


def _bootstrap_project(loader: ControlPlaneLoader) -> None:
    ProjectWorkspaceService(loader).bootstrap(
        ProjectBootstrapParams(
            project_slug="watchtower",
            title="WatchTower",
            summary="Operator-facing implementation target for project-scoped bootstrap tests.",
            repository_links=(
                ProjectRepositoryLinkSpec(
                    repository_role="planning",
                    repository_locator="/home/j/WatchTowerPlan",
                    repository_kind="planning",
                ),
                ProjectRepositoryLinkSpec(
                    repository_role="implementation",
                    repository_locator="/home/j/WatchTower",
                    repository_kind="implementation",
                ),
            ),
            updated_at=UPDATED_AT,
        ),
        write=True,
    )


def _mark_tasks_completed(initiative_root: Path, *, updated_at: str) -> None:
    for task_path in sorted((initiative_root / ".wt" / "tasks").glob("*/task.json")):
        document = _load_json(task_path)
        document["status"] = "active"
        document["task_status"] = "completed"
        document["updated_at"] = updated_at
        task_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def _mark_initiative_closing(initiative_root: Path, *, updated_at: str) -> None:
    state_path = initiative_root / ".wt" / "initiative.json"
    document = _load_json(state_path)
    document["lifecycle_stage"] = "closing"
    document["updated_at"] = updated_at
    state_path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def test_bootstrap_packwide_initiative_writes_full_package_and_stages_review(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = InitiativePackageService(ControlPlaneLoader(repo_root))

    result = service.bootstrap_packwide(_bootstrap_params(), write=True)

    assert result.wrote is True
    assert result.initiative_id == f"initiative.{INITIATIVE_SLUG}"
    assert result.trace_id == TRACE_ID
    assert result.lifecycle_stage == "ready_for_review"
    assert result.review_status == "pending"
    assert result.ready_for_execution is False
    assert result.validation_passed is True

    initiative_root = _initiative_root(repo_root)
    assert (initiative_root / "initiative_brief.md").exists()
    assert (initiative_root / "design_record.md").exists()
    assert (initiative_root / "implementation_slice.md").exists()
    assert (initiative_root / ".wt" / "initiative.json").exists()
    assert (
        initiative_root
        / ".wt"
        / "evidence"
        / "validation_bundle.bootstrap.json"
    ).exists()
    assert (
        initiative_root
        / ".wt"
        / "closeout"
        / "closeout_recap.bootstrap.json"
    ).exists()
    assert (
        initiative_root
        / ".wt"
        / "promotions"
        / "guidance_promotion_record.bootstrap.json"
    ).exists()

    state = _initiative_state(repo_root)
    assert state["task_ids"] == [
        f"task.{INITIATIVE_SLUG}.seed_initiative_contracts",
        f"task.{INITIATIVE_SLUG}.validate_readiness_gate",
    ]
    assert state["lifecycle_stage"] == "ready_for_review"
    assert state["review_status"] == "pending"
    assert state["discrepancy_ids"] == []
    assert state["gate_state"] == {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "pending",
        "ready_for_execution": False,
        "blocking_reasons": [],
    }

    event_paths = sorted((_initiative_root(repo_root) / ".wt" / "events").glob("*.json"))
    assert len(event_paths) == 8
    assert event_paths[-1].name == "0008_ready_for_review_marked.json"


def test_bootstrap_packwide_initiative_blocks_readiness_when_blocking_deferred_items_exist(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = InitiativePackageService(ControlPlaneLoader(repo_root))

    result = service.bootstrap_packwide(
        _bootstrap_params(
            deferred_items=(
                DeferredItemSpec(
                    category="repository_target",
                    summary="Resolve the downstream WatchTower repository linkage.",
                    reason="The target runtime repository contract is not frozen yet.",
                    resolution_trigger="before_ready_for_execution",
                    blocks_ready_for_execution=True,
                ),
            ),
        ),
        write=True,
    )

    assert result.wrote is True
    assert result.validation_passed is False
    assert result.lifecycle_stage == "capture_incomplete"
    assert result.ready_for_execution is False

    readiness = service.validate_packwide(INITIATIVE_SLUG, write=False)
    assert readiness.passed is False
    assert "blocking_deferred_items" in readiness.blocking_reasons
    assert any(
        "Blocking deferred item" in message for message in readiness.issue_messages
    )

    state = _initiative_state(repo_root)
    assert state["lifecycle_stage"] == "capture_incomplete"
    assert state["gate_state"] == {
        "capture_complete": False,
        "machine_valid": False,
        "approval_status": "pending",
        "ready_for_execution": False,
        "blocking_reasons": ["blocking_deferred_items"],
    }


def test_authored_input_drift_requires_confirmation_before_review_is_restored(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = InitiativePackageService(ControlPlaneLoader(repo_root))
    service.bootstrap_packwide(_bootstrap_params(include_decision_notes=True), write=True)

    brief_path = _initiative_root(repo_root) / "initiative_brief.md"
    brief_path.write_text(
        brief_path.read_text(encoding="utf-8")
        + "\n## Drift\nThis edit should require explicit confirmation.\n",
        encoding="utf-8",
    )

    readiness = service.validate_packwide(INITIATIVE_SLUG, write=True)

    assert readiness.passed is False
    assert "authored_input_drift" in readiness.blocking_reasons
    assert readiness.open_discrepancy_ids == (
        f"discrepancy.{INITIATIVE_SLUG}.initiative_brief_drift",
    )

    state = _initiative_state(repo_root)
    assert state["lifecycle_stage"] == "capture_incomplete"
    assert state["discrepancy_ids"] == [
        f"discrepancy.{INITIATIVE_SLUG}.initiative_brief_drift"
    ]
    discrepancy = _load_json(
        _initiative_root(repo_root)
        / ".wt"
        / "discrepancies"
        / "initiative_brief_drift.json"
    )
    assert discrepancy["status"] == "open"
    assert discrepancy["gate_effect"] == "readiness"

    confirm_result = service.confirm_authored_inputs(
        INITIATIVE_SLUG,
        "actor.repository_maintainer",
        write=True,
    )

    assert confirm_result.wrote is True
    assert confirm_result.validation_passed is True
    assert confirm_result.lifecycle_stage == "ready_for_review"

    refreshed_state = _initiative_state(repo_root)
    assert refreshed_state["lifecycle_stage"] == "ready_for_review"
    assert refreshed_state["discrepancy_ids"] == []
    assert refreshed_state["gate_state"] == {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "pending",
        "ready_for_execution": False,
        "blocking_reasons": [],
    }
    resolved_discrepancy = _load_json(
        _initiative_root(repo_root)
        / ".wt"
        / "discrepancies"
        / "initiative_brief_drift.json"
    )
    assert resolved_discrepancy["status"] == "resolved"


def test_machine_root_human_surface_policy_blocks_stray_readme(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = InitiativePackageService(ControlPlaneLoader(repo_root))
    service.bootstrap_packwide(_bootstrap_params(), write=True)

    machine_root = _initiative_root(repo_root) / ".wt"
    (machine_root / "README.md").write_text(
        "This file should not exist inside a machine-only root.\n",
        encoding="utf-8",
    )

    readiness = service.validate_packwide(INITIATIVE_SLUG, write=False)

    assert readiness.passed is False
    assert "machine_root_policy" in readiness.blocking_reasons
    assert any(
        "Forbidden human surface is present" in message
        for message in readiness.issue_messages
    )


def test_packwide_initiative_approval_requires_default_human_maintainer(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = InitiativePackageService(ControlPlaneLoader(repo_root))
    service.bootstrap_packwide(_bootstrap_params(), write=True)

    with pytest.raises(
        ValueError,
        match="Only default human repository maintainers may approve this initiative package.",
    ):
        service.approve_packwide(INITIATIVE_SLUG, "actor.codex", write=False)

    result = service.approve_packwide(
        INITIATIVE_SLUG,
        "actor.repository_maintainer",
        write=True,
    )

    assert result.wrote is True
    assert result.validation_passed is True
    assert result.lifecycle_stage == "ready_for_execution"
    assert result.review_status == "approved"
    assert result.ready_for_execution is True

    state = _initiative_state(repo_root)
    assert state["lifecycle_stage"] == "ready_for_execution"
    assert state["review_status"] == "approved"
    assert state["gate_state"] == {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "approved",
        "ready_for_execution": True,
        "blocking_reasons": [],
    }
    assert state["approvals"] == [
        {
            "approval_kind": "ready_for_execution",
            "actor_id": "actor.repository_maintainer",
            "approved_at": state["updated_at"],
        }
    ]

    event_names = [
        path.name
        for path in sorted((_initiative_root(repo_root) / ".wt" / "events").glob("*.json"))
    ]
    assert event_names.count("0008_ready_for_review_marked.json") == 1
    assert event_names[-2:] == [
        "0009_ready_for_execution_approved.json",
        "0010_ready_for_execution_marked.json",
    ]


def test_packwide_terminal_closeout_updates_local_artifacts_and_terminal_state(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = InitiativePackageService(loader)
    service.bootstrap_packwide(_bootstrap_params(include_decision_notes=True), write=True)
    service.approve_packwide(
        INITIATIVE_SLUG,
        "actor.repository_maintainer",
        write=True,
    )

    initiative_root = _initiative_root(repo_root)
    _mark_tasks_completed(
        initiative_root,
        updated_at="2026-03-17T15:45:00Z",
    )
    _mark_initiative_closing(
        initiative_root,
        updated_at="2026-03-17T15:46:00Z",
    )
    PlanWorkspaceService(loader).sync(write=True)

    result = service.close_packwide(
        INITIATIVE_SLUG,
        initiative_status="completed",
        closure_reason="Delivered the bounded closeout slice.",
        closed_at="2026-03-17T15:50:00Z",
        write=True,
    )

    assert result.wrote is True
    assert result.initiative_status == "completed"
    assert result.scope_type == "pack_wide"

    state = _initiative_state(repo_root)
    assert state["status"] == "completed"
    assert state["lifecycle_stage"] == "completed"
    assert state["closed_at"] == "2026-03-17T15:50:00Z"
    assert state["closure_reason"] == "Delivered the bounded closeout slice."
    assert state["gate_state"] == {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "approved",
        "ready_for_execution": False,
        "blocking_reasons": [],
    }

    evidence_document = _load_json(
        initiative_root / ".wt" / "evidence" / "validation_bundle.bootstrap.json"
    )
    assert evidence_document["status"] == "completed"
    closeout_document = _load_json(
        initiative_root / ".wt" / "closeout" / "closeout_recap.bootstrap.json"
    )
    assert closeout_document["status"] == "completed"
    assert closeout_document["terminal_state"] == "completed"
    assert closeout_document["closed_at"] == "2026-03-17T15:50:00Z"
    assert closeout_document["closure_reason"] == "Delivered the bounded closeout slice."
    promotion_document = _load_json(
        initiative_root / ".wt" / "promotions" / "guidance_promotion_record.bootstrap.json"
    )
    assert promotion_document["status"] == "candidate"

    event_names = [
        path.name for path in sorted((initiative_root / ".wt" / "events").glob("*.json"))
    ]
    assert event_names[-1] == "0011_completed.json"


def test_project_scoped_bootstrap_requires_a_valid_project_container(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = InitiativePackageService(ControlPlaneLoader(repo_root))

    with pytest.raises(
        ValueError,
        match="requires a valid project container",
    ):
        service.bootstrap_project_scoped(
            "watchtower",
            InitiativeBootstrapParams(
                trace_id="trace.watchtower_runtime_bootstrap",
                title="WatchTower Runtime Bootstrap",
                summary="Bootstraps one project-scoped initiative package for WatchTower.",
                initiative_slug="watchtower_runtime_bootstrap",
                task_specs=(
                    InitiativeTaskSpec(
                        title="Seed WatchTower project initiative",
                        summary="Creates the project-scoped initiative package.",
                        slug="seed_watchtower_project_initiative",
                    ),
                ),
                updated_at=UPDATED_AT,
            ),
            write=True,
        )


def test_project_scoped_initiative_bootstrap_and_approval_use_project_root(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    _bootstrap_project(loader)
    service = InitiativePackageService(loader)

    params = InitiativeBootstrapParams(
        trace_id="trace.watchtower_runtime_bootstrap",
        title="WatchTower Runtime Bootstrap",
        summary="Bootstraps one project-scoped initiative package for WatchTower.",
        initiative_slug="watchtower_runtime_bootstrap",
        task_specs=(
            InitiativeTaskSpec(
                title="Seed WatchTower project initiative",
                summary="Creates the project-scoped initiative package.",
                slug="seed_watchtower_project_initiative",
            ),
            InitiativeTaskSpec(
                title="Validate WatchTower project readiness gate",
                summary="Confirms the project-scoped initiative gate behavior.",
                slug="validate_watchtower_project_gate",
            ),
        ),
        updated_at=UPDATED_AT,
    )

    result = service.bootstrap_project_scoped("watchtower", params, write=True)

    assert result.wrote is True
    assert result.validation_passed is True
    assert (
        result.initiative_root
        == "plan/projects/watchtower/initiatives/watchtower_runtime_bootstrap"
    )

    state = _load_json(
        repo_root
        / "plan"
        / "projects"
        / "watchtower"
        / "initiatives"
        / "watchtower_runtime_bootstrap"
        / ".wt"
        / "initiative.json"
    )
    assert state["scope_type"] == "project_scoped"
    assert state["project_id"] == "project.watchtower"
    assert state["review_status"] == "pending"

    readiness = service.validate_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        write=False,
    )
    assert readiness.passed is True

    approved = service.approve_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        "actor.repository_maintainer",
        write=True,
    )
    assert approved.ready_for_execution is True
    assert approved.validation_passed is True

    final_readiness = service.validate_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        write=False,
        require_approved=True,
    )
    assert final_readiness.passed is True


def test_project_scoped_validation_preserves_in_progress_lifecycle_for_approved_packages(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    _bootstrap_project(loader)
    service = InitiativePackageService(loader)

    params = InitiativeBootstrapParams(
        trace_id="trace.watchtower_runtime_bootstrap",
        title="WatchTower Runtime Bootstrap",
        summary="Bootstraps one project-scoped initiative package for WatchTower.",
        initiative_slug="watchtower_runtime_bootstrap",
        task_specs=(
            InitiativeTaskSpec(
                title="Seed WatchTower project initiative",
                summary="Creates the project-scoped initiative package.",
                slug="seed_watchtower_project_initiative",
            ),
        ),
        updated_at=UPDATED_AT,
    )
    service.bootstrap_project_scoped("watchtower", params, write=True)
    service.approve_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        "actor.repository_maintainer",
        write=True,
    )

    initiative_root = (
        repo_root
        / "plan"
        / "projects"
        / "watchtower"
        / "initiatives"
        / "watchtower_runtime_bootstrap"
    )
    events_root = initiative_root / ".wt" / "events"
    execution_started_path = events_root / "0011_execution_started.json"
    execution_started_path.write_text(
        f"{json.dumps({
            '$schema': 'urn:watchtower:schema:artifacts:plan:initiative-event-stream:v1',
            'event_id': 'event.watchtower_runtime_bootstrap.0011_execution_started',
            'initiative_id': 'initiative.watchtower_runtime_bootstrap',
            'trace_id': 'trace.watchtower_runtime_bootstrap',
            'sequence': 11,
            'event_type': 'execution_started',
            'actor_id': 'actor.repository_maintainer',
            'recorded_at': '2026-03-17T17:10:00Z',
            'summary': 'Execution started for the WatchTower project-scoped initiative.',
            'payload': {
                'task_id': 'task.watchtower_runtime_bootstrap.seed_watchtower_project_initiative'
            },
        }, indent=2)}\n",
        encoding="utf-8",
    )

    state_path = (
        initiative_root
        / ".wt"
        / "initiative.json"
    )
    state = _load_json(state_path)
    state["lifecycle_stage"] = "in_progress"
    state_path.write_text(f"{json.dumps(state, indent=2)}\n", encoding="utf-8")
    service._sync_derived_surfaces(  # noqa: SLF001 - integration test exercises real derived sync.
        service._project_scoped_location_for_slug(  # noqa: SLF001
            "watchtower",
            "watchtower_runtime_bootstrap",
        )
    )

    readiness = service.validate_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        write=True,
        require_approved=True,
    )

    assert readiness.passed is True
    assert readiness.lifecycle_stage == "in_progress"

    refreshed_state = _load_json(state_path)
    assert refreshed_state["lifecycle_stage"] == "in_progress"
    assert refreshed_state["gate_state"] == {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "approved",
        "ready_for_execution": True,
        "blocking_reasons": [],
    }


def test_project_scoped_validation_restores_in_progress_after_transient_block(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    _bootstrap_project(loader)
    service = InitiativePackageService(loader)

    params = InitiativeBootstrapParams(
        trace_id="trace.watchtower_runtime_bootstrap",
        title="WatchTower Runtime Bootstrap",
        summary="Bootstraps one project-scoped initiative package for WatchTower.",
        initiative_slug="watchtower_runtime_bootstrap",
        task_specs=(
            InitiativeTaskSpec(
                title="Seed WatchTower project initiative",
                summary="Creates the project-scoped initiative package.",
                slug="seed_watchtower_project_initiative",
            ),
        ),
        updated_at=UPDATED_AT,
    )
    service.bootstrap_project_scoped("watchtower", params, write=True)
    service.approve_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        "actor.repository_maintainer",
        write=True,
    )

    initiative_root = (
        repo_root
        / "plan"
        / "projects"
        / "watchtower"
        / "initiatives"
        / "watchtower_runtime_bootstrap"
    )
    events_root = initiative_root / ".wt" / "events"
    execution_started_path = events_root / "0011_execution_started.json"
    execution_started_path.write_text(
        f"{json.dumps({
            '$schema': 'urn:watchtower:schema:artifacts:plan:initiative-event-stream:v1',
            'event_id': 'event.watchtower_runtime_bootstrap.0011_execution_started',
            'initiative_id': 'initiative.watchtower_runtime_bootstrap',
            'trace_id': 'trace.watchtower_runtime_bootstrap',
            'sequence': 11,
            'event_type': 'execution_started',
            'actor_id': 'actor.repository_maintainer',
            'recorded_at': '2026-03-17T17:10:00Z',
            'summary': 'Execution started for the WatchTower project-scoped initiative.',
            'payload': {
                'task_id': 'task.watchtower_runtime_bootstrap.seed_watchtower_project_initiative'
            },
        }, indent=2)}\n",
        encoding="utf-8",
    )

    state_path = initiative_root / ".wt" / "initiative.json"
    state = _load_json(state_path)
    state["lifecycle_stage"] = "blocked"
    state_path.write_text(f"{json.dumps(state, indent=2)}\n", encoding="utf-8")
    service._sync_derived_surfaces(  # noqa: SLF001 - integration test exercises real derived sync.
        service._project_scoped_location_for_slug(  # noqa: SLF001
            "watchtower",
            "watchtower_runtime_bootstrap",
        )
    )

    readiness = service.validate_project_scoped(
        "watchtower",
        "watchtower_runtime_bootstrap",
        write=True,
        require_approved=True,
    )

    assert readiness.passed is True
    assert readiness.lifecycle_stage == "in_progress"

    refreshed_state = _load_json(state_path)
    assert refreshed_state["lifecycle_stage"] == "in_progress"


def test_validate_packwide_reconciles_stale_approval_and_task_inventory_from_machine_state(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = InitiativePackageService(loader)
    service.bootstrap_packwide(_bootstrap_params(), write=True)
    service.approve_packwide(
        INITIATIVE_SLUG,
        "actor.repository_maintainer",
        write=True,
    )

    new_task_id = f"task.{INITIATIVE_SLUG}.reconcile_stale_initiative_state"
    TaskLifecycleService(loader).create(
        TaskCreateParams(
            task_id=new_task_id,
            title="Reconcile stale initiative state",
            summary="Adds one live task after approval to prove state healing.",
            task_kind="feature",
            priority="high",
            owner="repository_maintainer",
            scope_items=("Reconcile initiative state from machine truth.",),
            done_when_items=("Approval and task inventory reconcile cleanly.",),
            trace_id=TRACE_ID,
        ),
        write=True,
    )

    state_path = _initiative_root(repo_root) / ".wt" / "initiative.json"
    stale_state = _load_json(state_path)
    stale_state["task_ids"] = [
        f"task.{INITIATIVE_SLUG}.seed_initiative_contracts",
    ]
    stale_state["gate_state"] = {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "pending",
        "ready_for_execution": False,
        "blocking_reasons": [],
    }
    stale_state["approvals"] = [
        approval
        for approval in stale_state["approvals"]
        if approval["approval_kind"] != "ready_for_execution"
    ]
    state_path.write_text(f"{json.dumps(stale_state, indent=2)}\n", encoding="utf-8")

    readiness = service.validate_packwide(
        INITIATIVE_SLUG,
        write=True,
        require_approved=False,
    )

    assert readiness.passed is True
    assert readiness.lifecycle_stage == "ready_for_execution"

    refreshed_state = _initiative_state(repo_root)
    assert refreshed_state["review_status"] == "approved"
    assert refreshed_state["gate_state"] == {
        "capture_complete": True,
        "machine_valid": True,
        "approval_status": "approved",
        "ready_for_execution": True,
        "blocking_reasons": [],
    }
    assert refreshed_state["task_ids"] == [
        f"task.{INITIATIVE_SLUG}.reconcile_stale_initiative_state",
        f"task.{INITIATIVE_SLUG}.seed_initiative_contracts",
        f"task.{INITIATIVE_SLUG}.validate_readiness_gate",
    ]
    assert any(
        approval["approval_kind"] == "ready_for_execution"
        for approval in refreshed_state["approvals"]
    )
