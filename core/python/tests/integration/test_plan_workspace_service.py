from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree, rmtree

import pytest

from watchtower_core.adapters.front_matter import load_front_matter
from watchtower_core.control_plane import DocumentationFamilyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.plan_runtime.artifact_index import PLAN_ARTIFACT_INDEX_PATH
from watchtower_core.plan_runtime.guidance_promotion import GuidancePromotionService
from watchtower_core.plan_runtime.initiative_packages import (
    DeferredItemSpec,
    InitiativeBootstrapParams,
    InitiativePackageService,
    InitiativeTaskSpec,
)
from watchtower_core.plan_runtime.plan_workspace import (
    PLAN_CLOSEOUT_INDEX_PATH,
    PLAN_COORDINATION_INDEX_PATH,
    PLAN_DISCREPANCY_INDEX_PATH,
    PLAN_EVIDENCE_INDEX_PATH,
    PLAN_GUIDANCE_INDEX_PATH,
    PLAN_INITIATIVE_INDEX_PATH,
    PLAN_OVERVIEW_PATH,
    PLAN_PROMOTION_INDEX_PATH,
    PLAN_READINESS_INDEX_PATH,
    PLAN_REVIEW_INDEX_PATH,
    PLAN_TASK_INDEX_PATH,
    PlanCloseoutSearchParams,
    PlanDiscrepancySearchParams,
    PlanEvidenceSearchParams,
    PlanReadinessSearchParams,
    PlanReviewSearchParams,
    PlanTaskSearchParams,
    PlanWorkspaceService,
)
from watchtower_core.plan_runtime.project_workspace import (
    ProjectBootstrapParams,
    ProjectRepositoryLinkSpec,
    ProjectWorkspaceService,
)
from watchtower_core.plan_runtime.query import ArtifactQueryService, ArtifactSearchParams
from watchtower_core.plan_runtime.query.common import RenderedSearchFilters
from watchtower_core.validation.artifact import ArtifactValidationService

REPO_ROOT = Path(__file__).resolve().parents[4]


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
    return repo_root


def _bootstrap_params(
    *,
    initiative_slug: str,
    title: str,
    updated_at: str,
    deferred_items: tuple[DeferredItemSpec, ...] = (),
    include_decision_notes: bool = False,
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
        include_decision_notes=include_decision_notes,
        updated_at=updated_at,
    )


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _bootstrap_project(loader: ControlPlaneLoader) -> None:
    ProjectWorkspaceService(loader).bootstrap(
        ProjectBootstrapParams(
            project_slug="watchtower",
            title="WatchTower",
            summary="Operator-facing implementation target for project-scoped plan-workspace tests.",
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
            updated_at="2026-03-17T16:20:00Z",
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
        PLAN_EVIDENCE_INDEX_PATH,
        PLAN_CLOSEOUT_INDEX_PATH,
        PLAN_REVIEW_INDEX_PATH,
        PLAN_PROMOTION_INDEX_PATH,
        PLAN_GUIDANCE_INDEX_PATH,
        PLAN_COORDINATION_INDEX_PATH,
        PLAN_ARTIFACT_INDEX_PATH,
        PLAN_OVERVIEW_PATH,
        "plan/initiatives/workspace_alpha/plan.md",
        "plan/initiatives/workspace_alpha/progress.md",
        "plan/initiatives/workspace_alpha/summary.md",
        "plan/initiatives/workspace_beta/plan.md",
        "plan/initiatives/workspace_beta/progress.md",
        "plan/initiatives/workspace_beta/summary.md",
    ):
        assert (repo_root / relative_path).exists()

    plan_view = (repo_root / "plan/initiatives/workspace_alpha/plan.md").read_text(
        encoding="utf-8"
    )
    assert "## Planned Slices or Workstreams" in plan_view
    assert "`planned`" in plan_view
    progress_view = (repo_root / "plan/initiatives/workspace_alpha/progress.md").read_text(
        encoding="utf-8"
    )
    assert "## Recent Events or Changes" in progress_view
    assert "## Active Tasks" in progress_view

    initiative_index = workspace_service.load_initiative_index()
    assert len(initiative_index.entries) == 2
    assert {entry.trace_id for entry in initiative_index.entries} == {
        "trace.workspace_alpha",
        "trace.workspace_beta",
    }

    coordination_index = workspace_service.load_coordination_index()
    assert coordination_index.active_initiative_count == 2
    assert coordination_index.recommended_surface_path == "plan/initiatives/workspace_alpha/progress.md"

    artifact_index = loader.load_artifact_index()
    self_entry = artifact_index.get("index.artifacts")
    assert self_entry.path == PLAN_ARTIFACT_INDEX_PATH
    assert self_entry.source_channel == "aggregate_index"

    pack_note_entry = artifact_index.get("note.plan.stage1_bootstrap_record")
    assert pack_note_entry.artifact_family == "pack_work_item_note"
    assert "bootstrap.plan.stage1_bootstrap" in pack_note_entry.context_ids
    assert "trace.capture_first_plan_workspace_bootstrap" in pack_note_entry.context_ids

    artifact_matches = ArtifactQueryService(loader).search(
        ArtifactSearchParams(
            artifact_family="initiative_state",
            context_id="trace.workspace_alpha",
        )
    )
    assert len(artifact_matches) == 1
    assert artifact_matches[0].artifact_id == "initiative.workspace_alpha"

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

    evidence_entries = workspace_service.search_evidence(
        PlanEvidenceSearchParams(status="planned", owner="repository_maintainer")
    )
    assert len(evidence_entries) == 2
    assert {entry.trace_id for entry in evidence_entries} == {
        "trace.workspace_alpha",
        "trace.workspace_beta",
    }
    assert all(entry.target_phases == ("readiness",) for entry in evidence_entries)

    closeout_entries = workspace_service.search_closeouts(
        PlanCloseoutSearchParams(promotion_review_required=True)
    )
    assert len(closeout_entries) == 2
    assert all(entry.status == "planned" for entry in closeout_entries)

    review_entries = workspace_service.search_reviews(
        PlanReviewSearchParams(review_state="pending")
    )
    assert len(review_entries) == 4
    assert {entry.subject_kind for entry in review_entries} == {"initiative", "promotion"}

    plan_overview = (repo_root / PLAN_OVERVIEW_PATH).read_text(encoding="utf-8")
    assert "Workspace Alpha" in plan_overview
    assert "Workspace Beta" in plan_overview


def test_plan_workspace_sync_builds_promotion_and_guidance_indexes_and_validates_them(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_promotions",
            title="Workspace Promotions",
            updated_at="2026-03-17T16:07:00Z",
        ),
        write=True,
    )

    workspace_service.sync(write=True)

    promotion_entries = workspace_service.load_promotion_entries()
    assert len(promotion_entries) == 1
    promotion_entry = promotion_entries[0]
    assert promotion_entry.promotion_id == "promotion.workspace_promotions.bootstrap_shell"
    assert promotion_entry.initiative_id == "initiative.workspace_promotions"
    assert promotion_entry.candidate_count == 3
    assert promotion_entry.target_families == ("decision_record", "pattern", "reference")
    assert promotion_entry.review_paths == ("repository_maintainer_review",)
    assert promotion_entry.initiative_root == "plan/initiatives/workspace_promotions"
    assert promotion_entry.target_paths == (
        "plan/docs/decisions/workspace_promotions_design_record.md",
        "plan/docs/patterns/workspace_promotions_implementation_slice.md",
        "plan/docs/references/workspace_promotions_initiative_brief.md",
    )
    assert promotion_entry.approval_state == "pending"

    guidance_entries = workspace_service.load_guidance_entries()
    guidance_ids = {entry.guidance_id for entry in guidance_entries}
    assert "foundation.repository_scope" in guidance_ids
    assert "foundation.product_direction" in guidance_ids
    repository_scope_entry = next(
        entry for entry in guidance_entries if entry.guidance_id == "foundation.repository_scope"
    )
    assert repository_scope_entry.guidance_family == "foundation"
    assert repository_scope_entry.doc_path == "plan/docs/foundations/repository_scope.md"

    validator = ArtifactValidationService(loader)
    for relative_path in (
        "plan/.wt/registries/promotion_policy_registry.json",
        PLAN_EVIDENCE_INDEX_PATH,
        PLAN_CLOSEOUT_INDEX_PATH,
        PLAN_REVIEW_INDEX_PATH,
        PLAN_PROMOTION_INDEX_PATH,
        PLAN_GUIDANCE_INDEX_PATH,
    ):
        result = validator.validate(relative_path)
        assert result.passed, f"{relative_path} failed schema validation: {result.issues}"


def test_guidance_promotion_service_promotes_outputs_and_updates_indexes(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    package_service = InitiativePackageService(loader)
    promotion_service = GuidancePromotionService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_guidance_promotion",
            title="Workspace Guidance Promotion",
            updated_at="2026-03-17T16:12:00Z",
            include_decision_notes=True,
        ),
        write=True,
    )

    extraction_envelopes = promotion_service.extract_packwide(
        "workspace_guidance_promotion",
        updated_at="2026-03-17T16:12:30Z",
    )
    result = promotion_service.promote_packwide(
        "workspace_guidance_promotion",
        updated_at="2026-03-17T16:13:00Z",
        write=True,
    )
    workspace_service.sync(write=True)

    assert result.status == "promoted"
    assert result.wrote is True
    assert len(extraction_envelopes) == 4
    assert len(result.extraction_envelopes) == 4
    assert {envelope.work_item_id for envelope in extraction_envelopes} == {
        "promotion.workspace_guidance_promotion.bootstrap_shell"
    }
    assert {
        family
        for envelope in extraction_envelopes
        for family in envelope.knowledge_families
    } == {
        "decision_record",
        "pattern",
        "reference",
        "standard",
    }
    assert {
        envelope.source_note_id
        for envelope in result.extraction_envelopes
    } == {
        "note.workspace_guidance_promotion.decision_notes",
        "note.workspace_guidance_promotion.design_record",
        "note.workspace_guidance_promotion.implementation_slice",
        "note.workspace_guidance_promotion.initiative_brief",
    }
    assert {output.target_family for output in result.outputs} == {
        "decision_record",
        "pattern",
        "reference",
        "standard",
    }

    promoted_paths = {output.target_path for output in result.outputs}
    assert promoted_paths == {
        "plan/docs/decisions/workspace_guidance_promotion_design_record.md",
        "plan/docs/patterns/workspace_guidance_promotion_implementation_slice.md",
        "plan/docs/references/workspace_guidance_promotion_initiative_brief.md",
        "plan/docs/standards/workspace_guidance_promotion_decision_notes.md",
    }
    for relative_path in promoted_paths:
        front_matter = load_front_matter(repo_root / relative_path)
        family = DocumentationFamilyHelper.from_loader(
            loader,
            pack_settings_path="plan/.wt/manifests/pack_settings.json",
        ).family(str(front_matter["type"]))
        loader.schema_store.validate_instance(
            front_matter,
            schema_id=family.front_matter_schema_id,
        )

    promotion_record = _load_json(
        repo_root
        / "plan/initiatives/workspace_guidance_promotion/.wt/promotions/guidance_promotion_record.bootstrap.json"
    )
    assert promotion_record["status"] == "promoted"
    assert promotion_record["approval_state"] == "approved"
    assert promotion_record["evidence_refs"] == [
        "evidence.workspace_guidance_promotion.bootstrap_validation_bundle"
    ]

    promotion_entries = workspace_service.load_promotion_entries()
    promoted_entry = next(
        entry
        for entry in promotion_entries
        if entry.promotion_id == "promotion.workspace_guidance_promotion.bootstrap_shell"
    )
    assert promoted_entry.approval_state == "approved"
    assert promoted_entry.target_paths == tuple(sorted(promoted_paths))

    guidance_entries = workspace_service.load_guidance_entries()
    guidance_ids = {entry.guidance_id for entry in guidance_entries}
    assert {
        "decision.workspace_guidance_promotion_design_record",
        "pattern.workspace_guidance_promotion_implementation_slice",
        "reference.workspace_guidance_promotion_initiative_brief",
        "standard.workspace_guidance_promotion_decision_notes",
    }.issubset(guidance_ids)


def test_guidance_promotion_service_fans_out_foundation_mirrors(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    package_service = InitiativePackageService(loader)
    promotion_service = GuidancePromotionService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_foundation_promotion",
            title="Workspace Foundation Promotion",
            updated_at="2026-03-17T16:14:00Z",
        ),
        write=True,
    )

    promotion_record_path = (
        repo_root
        / "plan/initiatives/workspace_foundation_promotion/.wt/promotions/guidance_promotion_record.bootstrap.json"
    )
    promotion_record = _load_json(promotion_record_path)
    promotion_record["candidates"] = [
        {
            "candidate_path": "plan/initiatives/workspace_foundation_promotion/initiative_brief.md",
            "source_artifact_kind": "initiative_brief",
            "target_family": "foundation",
            "review_path": "repository_maintainer_review",
            "provenance_expectation": "Promotions must cite the source initiative id, trace id, and evidence bundle id.",
            "mirror_update_mode": "same_change_set",
        }
    ]
    promotion_record_path.write_text(
        f"{json.dumps(promotion_record, indent=2)}\n",
        encoding="utf-8",
    )

    result = promotion_service.promote_packwide(
        "workspace_foundation_promotion",
        updated_at="2026-03-17T16:15:00Z",
        write=True,
    )

    assert len(result.outputs) == 1
    output = result.outputs[0]
    assert output.target_family == "foundation"
    assert output.target_path == "plan/docs/foundations/workspace_foundation_promotion_initiative_brief.md"
    assert output.mirror_target_paths == (
        "core/docs/foundations/workspace_foundation_promotion_initiative_brief.md",
    )

    plan_doc = repo_root / output.target_path
    core_doc = repo_root / output.mirror_target_paths[0]
    assert plan_doc.read_text(encoding="utf-8") == core_doc.read_text(encoding="utf-8")


def test_plan_workspace_sync_fails_closed_when_guidance_doc_lacks_front_matter(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    bad_doc_path = repo_root / "plan/docs/references/bad_guidance.md"
    bad_doc_path.parent.mkdir(parents=True, exist_ok=True)
    bad_doc_path.write_text("# Missing front matter\n", encoding="utf-8")

    loader = ControlPlaneLoader(repo_root)
    workspace_service = PlanWorkspaceService(loader)

    with pytest.raises(ValueError, match="governed front matter"):
        workspace_service.sync(write=False)


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


def test_plan_workspace_sync_includes_project_scoped_initiatives_in_pack_indexes(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)
    _bootstrap_project(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_alpha",
            title="Workspace Alpha",
            updated_at="2026-03-17T16:30:00Z",
        ),
        write=True,
    )
    package_service.bootstrap_project_scoped(
        "watchtower",
        InitiativeBootstrapParams(
            trace_id="trace.watchtower_scope_flow",
            title="WatchTower Scope Flow",
            summary="Bootstraps one project-scoped initiative for plan-workspace sync coverage.",
            initiative_slug="watchtower_scope_flow",
            task_specs=(
                InitiativeTaskSpec(
                    title="Seed WatchTower scope flow",
                    summary="Creates one project-scoped initiative package.",
                    slug="seed_watchtower_scope_flow",
                ),
                InitiativeTaskSpec(
                    title="Validate WatchTower scope gate",
                    summary="Confirms the project-scoped initiative appears in pack indexes.",
                    slug="validate_watchtower_scope_gate",
                ),
            ),
            updated_at="2026-03-17T16:35:00Z",
        ),
        write=True,
    )

    sync_result = workspace_service.sync(write=True)

    assert sync_result.wrote is True
    assert sync_result.initiative_count == 2
    assert sync_result.task_count == 4
    assert (repo_root / "plan/projects/watchtower/initiatives/watchtower_scope_flow/plan.md").exists()
    assert (repo_root / "plan/projects/watchtower/initiatives/watchtower_scope_flow/progress.md").exists()
    assert (repo_root / "plan/projects/watchtower/initiatives/watchtower_scope_flow/summary.md").exists()

    initiative_entries = workspace_service.load_initiative_index().entries
    project_entry = next(
        entry for entry in initiative_entries if entry.trace_id == "trace.watchtower_scope_flow"
    )
    assert project_entry.scope_type == "project_scoped"
    assert project_entry.project_id == "project.watchtower"
    assert project_entry.key_surface_path == "plan/projects/watchtower/initiatives/watchtower_scope_flow/plan.md"

    readiness_entry = next(
        entry
        for entry in workspace_service.load_readiness_entries()
        if entry.trace_id == "trace.watchtower_scope_flow"
    )
    assert readiness_entry.project_id == "project.watchtower"
    assert readiness_entry.scope_type == "project_scoped"

    task_entries = workspace_service.search_tasks(
        PlanTaskSearchParams(project_id="project.watchtower")
    )
    assert len(task_entries) == 2
    assert all(entry.project_id == "project.watchtower" for entry in task_entries)


def test_plan_workspace_coordination_surfaces_recent_closeouts_after_terminal_closeout(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)
    _bootstrap_project(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_alpha",
            title="Workspace Alpha",
            updated_at="2026-03-17T16:40:00Z",
        ),
        write=True,
    )
    package_service.approve_packwide(
        "workspace_alpha",
        "actor.repository_maintainer",
        write=True,
    )
    package_service.bootstrap_project_scoped(
        "watchtower",
        InitiativeBootstrapParams(
            trace_id="trace.watchtower_scope_flow",
            title="WatchTower Scope Flow",
            summary="Bootstraps one project-scoped initiative for closeout coverage.",
            initiative_slug="watchtower_scope_flow",
            task_specs=(
                InitiativeTaskSpec(
                    title="Seed WatchTower scope flow",
                    summary="Creates one project-scoped initiative package.",
                    slug="seed_watchtower_scope_flow",
                ),
            ),
            updated_at="2026-03-17T16:45:00Z",
        ),
        write=True,
    )
    package_service.approve_project_scoped(
        "watchtower",
        "watchtower_scope_flow",
        "actor.repository_maintainer",
        write=True,
    )

    _mark_tasks_completed(
        repo_root / "plan" / "initiatives" / "workspace_alpha",
        updated_at="2026-03-17T16:50:00Z",
    )
    _mark_initiative_closing(
        repo_root / "plan" / "initiatives" / "workspace_alpha",
        updated_at="2026-03-17T16:51:00Z",
    )
    _mark_tasks_completed(
        repo_root / "plan" / "projects" / "watchtower" / "initiatives" / "watchtower_scope_flow",
        updated_at="2026-03-17T16:50:00Z",
    )
    _mark_initiative_closing(
        repo_root
        / "plan"
        / "projects"
        / "watchtower"
        / "initiatives"
        / "watchtower_scope_flow",
        updated_at="2026-03-17T16:51:00Z",
    )
    workspace_service.sync(write=True)
    ProjectWorkspaceService(loader).sync(write=True)

    package_service.close_packwide(
        "workspace_alpha",
        initiative_status="completed",
        closure_reason="Delivered workspace alpha.",
        closed_at="2026-03-17T16:55:00Z",
        write=True,
    )
    package_service.close_project_scoped(
        "watchtower",
        "watchtower_scope_flow",
        initiative_status="completed",
        closure_reason="Delivered WatchTower scope flow.",
        closed_at="2026-03-17T16:56:00Z",
        write=True,
    )

    coordination_index = workspace_service.load_coordination_index()
    assert coordination_index.active_initiative_count == 0
    assert coordination_index.coordination_mode == "ready_for_bootstrap"
    assert {entry.trace_id for entry in coordination_index.recent_closed_initiatives} == {
        "trace.workspace_alpha",
        "trace.watchtower_scope_flow",
    }
    assert tuple(entry.trace_id for entry in coordination_index.recent_closed_initiatives) == (
        "trace.watchtower_scope_flow",
        "trace.workspace_alpha",
    )

    plan_overview = (repo_root / PLAN_OVERVIEW_PATH).read_text(encoding="utf-8")
    assert "## Recent Closeouts" in plan_overview
    assert "Delivered workspace alpha." in plan_overview
    assert "Delivered WatchTower scope flow." in plan_overview


def test_plan_workspace_sync_uses_latest_task_state_timestamp_for_indexes(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_delta",
            title="Workspace Delta",
            updated_at="2026-03-17T16:00:00Z",
        ),
        write=True,
    )
    package_service.approve_packwide(
        "workspace_delta",
        "actor.repository_maintainer",
        write=True,
    )

    task_path = repo_root / "plan/initiatives/workspace_delta/.wt/tasks/seed_contracts/task.json"
    task_document = _load_json(task_path)
    task_document["status"] = "active"
    task_document["task_status"] = "ready"
    task_document["updated_at"] = "2099-03-17T23:30:00Z"
    task_path.write_text(f"{json.dumps(task_document, indent=2)}\n", encoding="utf-8")

    workspace_service.sync(write=True)

    initiative_index = _load_json(repo_root / PLAN_INITIATIVE_INDEX_PATH)
    initiative_entry = next(
        entry
        for entry in initiative_index["entries"]
        if entry["initiative_id"] == "initiative.workspace_delta"
    )
    assert initiative_entry["updated_at"] == "2099-03-17T23:30:00Z"
    assert initiative_entry["active_task_summaries"][0]["task_status"] == "ready"

    readiness_index = _load_json(repo_root / PLAN_READINESS_INDEX_PATH)
    readiness_entry = next(
        entry
        for entry in readiness_index["entries"]
        if entry["initiative_id"] == "initiative.workspace_delta"
    )
    assert readiness_entry["updated_at"] == "2099-03-17T23:30:00Z"

    coordination_index = _load_json(repo_root / PLAN_COORDINATION_INDEX_PATH)
    assert coordination_index["updated_at"] == "2099-03-17T23:30:00Z"
    assert coordination_index["actionable_task_count"] == 1

    summary_view = (
        repo_root / "plan/initiatives/workspace_delta/summary.md"
    ).read_text(encoding="utf-8")
    assert "`updated_at`: `2099-03-17T23:30:00Z`" in summary_view


def test_plan_workspace_sync_supports_closing_initiatives_with_no_open_tasks(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_epsilon",
            title="Workspace Epsilon",
            updated_at="2026-03-17T17:00:00Z",
        ),
        write=True,
    )
    package_service.approve_packwide(
        "workspace_epsilon",
        "actor.repository_maintainer",
        write=True,
    )

    initiative_root = repo_root / "plan/initiatives/workspace_epsilon/.wt"
    for slug in ("seed_contracts", "validate_gate"):
        task_path = initiative_root / "tasks" / slug / "task.json"
        task_document = _load_json(task_path)
        task_document["status"] = "active"
        task_document["task_status"] = "completed"
        task_document["updated_at"] = "2026-03-17T17:10:00Z"
        task_path.write_text(f"{json.dumps(task_document, indent=2)}\n", encoding="utf-8")

    initiative_path = initiative_root / "initiative.json"
    initiative_document = _load_json(initiative_path)
    initiative_document["lifecycle_stage"] = "closing"
    initiative_document["updated_at"] = "2026-03-17T17:10:00Z"
    initiative_path.write_text(f"{json.dumps(initiative_document, indent=2)}\n", encoding="utf-8")

    sync_result = workspace_service.sync(write=True)

    assert sync_result.wrote is True

    initiative_index = _load_json(repo_root / PLAN_INITIATIVE_INDEX_PATH)
    initiative_entry = next(
        entry
        for entry in initiative_index["entries"]
        if entry["initiative_id"] == "initiative.workspace_epsilon"
    )
    assert initiative_entry["current_phase"] == "closeout"
    assert initiative_entry["open_task_count"] == 0
    assert initiative_entry["next_action"] == "Finalize closeout, evidence, and promotion decisions."
    assert initiative_entry["next_surface_path"] == "plan/initiatives/workspace_epsilon/summary.md"

    coordination_index = _load_json(repo_root / PLAN_COORDINATION_INDEX_PATH)
    assert all(
        task["trace_id"] != "trace.workspace_epsilon"
        for task in coordination_index["actionable_tasks"]
    )


def test_plan_workspace_sync_treats_task_complete_ready_initiatives_as_closeout(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_zeta",
            title="Workspace Zeta",
            updated_at="2026-03-17T17:20:00Z",
        ),
        write=True,
    )
    package_service.approve_packwide(
        "workspace_zeta",
        "actor.repository_maintainer",
        write=True,
    )

    initiative_root = repo_root / "plan/initiatives/workspace_zeta/.wt"
    for slug in ("seed_contracts", "validate_gate"):
        task_path = initiative_root / "tasks" / slug / "task.json"
        task_document = _load_json(task_path)
        task_document["status"] = "active"
        task_document["task_status"] = "completed"
        task_document["updated_at"] = "2026-03-17T17:25:00Z"
        task_path.write_text(f"{json.dumps(task_document, indent=2)}\n", encoding="utf-8")

    sync_result = workspace_service.sync(write=True)

    assert sync_result.wrote is True

    initiative_index = _load_json(repo_root / PLAN_INITIATIVE_INDEX_PATH)
    initiative_entry = next(
        entry
        for entry in initiative_index["entries"]
        if entry["initiative_id"] == "initiative.workspace_zeta"
    )
    assert initiative_entry["initiative_status"] == "active"
    assert initiative_entry["current_phase"] == "closeout"
    assert initiative_entry["open_task_count"] == 0
    assert initiative_entry["next_action"] == "Finalize closeout, evidence, and promotion decisions."
    assert initiative_entry["next_surface_path"] == "plan/initiatives/workspace_zeta/summary.md"


def test_validate_packwide_preserves_closing_lifecycle_while_rebuilding_stale_surfaces(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    package_service = InitiativePackageService(loader)
    workspace_service = PlanWorkspaceService(loader)

    package_service.bootstrap_packwide(
        _bootstrap_params(
            initiative_slug="workspace_zeta",
            title="Workspace Zeta",
            updated_at="2026-03-17T17:20:00Z",
        ),
        write=True,
    )
    package_service.approve_packwide(
        "workspace_zeta",
        "actor.repository_maintainer",
        write=True,
    )
    workspace_service.sync(write=True)

    initiative_root = repo_root / "plan/initiatives/workspace_zeta/.wt"
    for slug in ("seed_contracts", "validate_gate"):
        task_path = initiative_root / "tasks" / slug / "task.json"
        task_document = _load_json(task_path)
        task_document["status"] = "active"
        task_document["task_status"] = "completed"
        task_document["updated_at"] = "2026-03-17T17:25:00Z"
        task_path.write_text(f"{json.dumps(task_document, indent=2)}\n", encoding="utf-8")

    initiative_path = initiative_root / "initiative.json"
    initiative_document = _load_json(initiative_path)
    initiative_document["lifecycle_stage"] = "closing"
    initiative_document["updated_at"] = "2026-03-17T17:25:00Z"
    initiative_path.write_text(f"{json.dumps(initiative_document, indent=2)}\n", encoding="utf-8")

    readiness = package_service.validate_packwide(
        "workspace_zeta",
        write=True,
        require_approved=True,
    )

    assert readiness.passed is False
    assert readiness.lifecycle_stage == "closing"
    assert "stale_derived_surfaces" in readiness.blocking_reasons

    persisted_state = _load_json(initiative_path)
    assert persisted_state["lifecycle_stage"] == "closing"

    workspace_service.sync(write=True)
    restored = package_service.validate_packwide(
        "workspace_zeta",
        write=True,
        require_approved=True,
    )

    assert restored.passed is True
    assert restored.lifecycle_stage == "closing"
