from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.initiative_packages import (
    DeferredItemSpec,
    InitiativeBootstrapParams,
    InitiativePackageService,
    InitiativeTaskSpec,
)
from watchtower_core.repo_ops.plan_workspace import (
    PLAN_COORDINATION_INDEX_PATH,
    PLAN_INITIATIVE_INDEX_PATH,
    PLAN_OVERVIEW_PATH,
    PLAN_READINESS_INDEX_PATH,
    PLAN_TASK_INDEX_PATH,
    PLAN_DISCREPANCY_INDEX_PATH,
    PlanDiscrepancySearchParams,
    PlanReadinessSearchParams,
    PlanTaskSearchParams,
    PlanWorkspaceService,
)
from watchtower_core.repo_ops.query.common import RenderedSearchFilters

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "plan", repo_root / "plan")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _bootstrap_params(
    *,
    initiative_slug: str,
    title: str,
    updated_at: str,
    deferred_items: tuple[DeferredItemSpec, ...] = (),
) -> InitiativeBootstrapParams:
    task_id = f"task.{initiative_slug}.seed_contracts"
    return InitiativeBootstrapParams(
        trace_id=f"trace.{initiative_slug}",
        title=title,
        summary=f"Bootstraps {title} for plan-workspace tests.",
        initiative_slug=initiative_slug,
        task_specs=(
            InitiativeTaskSpec(
                title="Seed initiative contracts",
                summary="Creates the initiative-local package state.",
                slug="seed_contracts",
                task_id=task_id,
            ),
            InitiativeTaskSpec(
                title="Validate readiness gate",
                summary="Confirms the readiness gate behavior.",
                slug="validate_gate",
                depends_on=(task_id,),
            ),
        ),
        deferred_items=deferred_items,
        updated_at=updated_at,
    )


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_plan_workspace_sync_writes_indexes_views_and_query_surfaces(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_alpha",
            title="Workspace Alpha",
            updated_at="2026-03-17T16:00:00Z",
        ),
        write=True,
    )
    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_beta",
            title="Workspace Beta",
            updated_at="2026-03-17T16:05:00Z",
            deferred_items=(
                DeferredItemSpec(
                    category="promotion_target",
                    summary="Resolve the final promotion target after implementation findings.",
                    reason="The durable output family is not known yet.",
                    resolution_trigger="before_closeout",
                    blocks_ready_for_execution=True,
                ),
            ),
        ),
        write=True,
    )

    sync_result = workspace_service.sync(write=True)

    assert sync_result.wrote is True
    assert sync_result.initiative_count == 2
    assert sync_result.task_count == 4
    assert sync_result.discrepancy_count == 0

    for relative_path in (
        PLAN_INITIATIVE_INDEX_PATH,
        PLAN_TASK_INDEX_PATH,
        PLAN_READINESS_INDEX_PATH,
        PLAN_DISCREPANCY_INDEX_PATH,
        PLAN_COORDINATION_INDEX_PATH,
        PLAN_OVERVIEW_PATH,
        "plan/initiatives/workspace_alpha/plan.md",
        "plan/initiatives/workspace_alpha/progress.md",
        "plan/initiatives/workspace_alpha/summary.md",
        "plan/initiatives/workspace_beta/plan.md",
        "plan/initiatives/workspace_beta/progress.md",
        "plan/initiatives/workspace_beta/summary.md",
    ):
        assert (repo_root / relative_path).exists()

    initiative_index = workspace_service.load_initiative_index()
    assert len(initiative_index.entries) == 2
    assert {entry.trace_id for entry in initiative_index.entries} == {
        "trace.workspace_alpha",
        "trace.workspace_beta",
    }

    coordination_index = workspace_service.load_coordination_index()
    assert coordination_index.active_initiative_count == 2
    assert coordination_index.recommended_surface_path == "plan/initiatives/workspace_alpha/progress.md"

    readiness_blocked = workspace_service.search_readiness(
        PlanReadinessSearchParams(blocked_only=True)
    )
    assert len(readiness_blocked) == 1
    assert readiness_blocked[0].initiative_id == "initiative.workspace_beta"
    assert readiness_blocked[0].blocking_reasons == ("blocking_deferred_items",)

    task_entries = workspace_service.search_tasks(
        PlanTaskSearchParams(status="planned", initiative_id="initiative.workspace_alpha")
    )
    assert len(task_entries) == 2
    assert all(entry.trace_id == "trace.workspace_alpha" for entry in task_entries)

    coordination_entries = workspace_service.search_coordination(RenderedSearchFilters(limit=5))
    assert len(coordination_entries) == 2
    assert coordination_entries[0].trace_id == "trace.workspace_alpha"

    discrepancy_entries = workspace_service.search_discrepancies(
        PlanDiscrepancySearchParams(limit=5)
    )
    assert discrepancy_entries == ()

    plan_overview = (repo_root / PLAN_OVERVIEW_PATH).read_text(encoding="utf-8")
    assert "Workspace Alpha" in plan_overview
    assert "Workspace Beta" in plan_overview


def test_plan_workspace_stale_surface_drift_blocks_readiness_until_explicit_rebuild(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_gamma",
            title="Workspace Gamma",
            updated_at="2026-03-17T16:10:00Z",
        ),
        write=True,
    )

    plan_overview_path = repo_root / PLAN_OVERVIEW_PATH
    plan_overview_path.write_text(
        plan_overview_path.read_text(encoding="utf-8")
        + "\n## Drift\nThis manual edit should block readiness.\n",
        encoding="utf-8",
    )
    readiness_index_path = repo_root / PLAN_READINESS_INDEX_PATH
    readiness_index = _load_json(readiness_index_path)
    readiness_index["title"] = "Stale Readiness Index"
    readiness_index_path.write_text(f"{json.dumps(readiness_index, indent=2)}\n", encoding="utf-8")

    readiness = package_service.validate_packwide("workspace_gamma", write=True)

    assert readiness.passed is False
    assert "stale_derived_surfaces" in readiness.blocking_reasons
    assert set(readiness.open_discrepancy_ids) == {
        "discrepancy.workspace_gamma.plan_overview_surface_drift",
        "discrepancy.workspace_gamma.readiness_index_index_drift",
    }

    discrepancy_entries = workspace_service.search_discrepancies(
        PlanDiscrepancySearchParams(status="open", blocking_only=True)
    )
    assert {entry.discrepancy_id for entry in discrepancy_entries} == {
        "discrepancy.workspace_gamma.plan_overview_surface_drift",
        "discrepancy.workspace_gamma.readiness_index_index_drift",
    }

    workspace_service.sync(write=True)
    restored = package_service.validate_packwide("workspace_gamma", write=True)

    assert restored.passed is True
    assert restored.blocking_reasons == ()
    assert workspace_service.search_discrepancies(
        PlanDiscrepancySearchParams(status="open")
    ) == ()
