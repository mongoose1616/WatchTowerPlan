from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.discrepancy import (
    DiscrepancyDescriptor,
    DiscrepancyHelper,
    DiscrepancyIssue,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.workspace import WorkspaceConfig

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "plan", repo_root / "plan")
    return repo_root


def _build_loader(repo_root: Path) -> ControlPlaneLoader:
    return ControlPlaneLoader(
        workspace_config=WorkspaceConfig(
            repo_root=repo_root,
            control_plane_root=repo_root / "core" / "control_plane",
            python_workspace_root=repo_root / "core" / "python",
        )
    )


def test_discrepancy_helper_syncs_and_resolves_managed_records(tmp_path: Path) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = _build_loader(repo_root)
    helper = DiscrepancyHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    descriptor = DiscrepancyDescriptor(
        relative_dir="plan/initiatives/unit_discrepancy/.wt/discrepancies",
        initiative_id="initiative.unit_discrepancy",
    )
    issue = DiscrepancyIssue(
        discrepancy_id="discrepancy.unit_discrepancy.plan_surface_drift",
        record_slug="plan_surface_drift",
        category="stale_rendered_surface",
        summary="Rendered surface drift detected for the unit initiative plan.",
        source_paths=("plan/initiatives/unit_discrepancy/plan.md",),
    )

    helper.sync_records(
        descriptor,
        issues=(issue,),
        updated_at="2026-03-17T23:20:00Z",
        managed_categories=("stale_rendered_surface",),
    )

    open_records = helper.open_records(descriptor)
    assert len(open_records) == 1
    relative_path, document = open_records[0]
    assert relative_path.endswith("plan_surface_drift.json")
    assert document["status"] == "open"
    assert document["category"] == "stale_rendered_surface"

    helper.sync_records(
        descriptor,
        issues=(),
        updated_at="2026-03-17T23:21:00Z",
        managed_categories=("stale_rendered_surface",),
    )

    assert helper.open_records(descriptor) == ()
    resolved_document = json.loads((repo_root / relative_path).read_text(encoding="utf-8"))
    assert resolved_document["status"] == "resolved"
    assert resolved_document["updated_at"] == "2026-03-17T23:21:00Z"


def test_discrepancy_helper_preserves_detected_at_when_refreshing_open_record(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = _build_loader(repo_root)
    helper = DiscrepancyHelper.from_loader(
        loader,
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )
    descriptor = DiscrepancyDescriptor(
        relative_dir="plan/initiatives/unit_discrepancy/.wt/discrepancies",
        initiative_id="initiative.unit_discrepancy",
    )

    helper.sync_records(
        descriptor,
        issues=(
            DiscrepancyIssue(
                discrepancy_id="discrepancy.unit_discrepancy.plan_surface_drift",
                record_slug="plan_surface_drift",
                category="stale_rendered_surface",
                summary="Rendered surface drift detected for the unit initiative plan.",
                source_paths=("plan/initiatives/unit_discrepancy/plan.md",),
            ),
        ),
        updated_at="2026-03-17T23:30:00Z",
        managed_categories=("stale_rendered_surface",),
    )
    helper.sync_records(
        descriptor,
        issues=(
            DiscrepancyIssue(
                discrepancy_id="discrepancy.unit_discrepancy.plan_surface_drift",
                record_slug="plan_surface_drift",
                category="stale_rendered_surface",
                summary="Rendered surface drift is still present after refresh.",
                source_paths=("plan/initiatives/unit_discrepancy/plan.md",),
            ),
        ),
        updated_at="2026-03-17T23:31:00Z",
        managed_categories=("stale_rendered_surface",),
    )

    _, document = helper.open_records(descriptor)[0]
    assert document["detected_at"] == "2026-03-17T23:30:00Z"
    assert document["updated_at"] == "2026-03-17T23:31:00Z"
    assert document["summary"] == "Rendered surface drift is still present after refresh."
