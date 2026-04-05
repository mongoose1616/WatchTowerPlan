"""Plan-pack export cleanup for customer-safe staged bundles."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.export.cleanup_helpers import clear_directory_contents, remove_if_exists
from watchtower_core.pack_integration import (
    PackExportCleanupRequest,
    PackExportCleanupResult,
)
from watchtower_plan.projects.workspace import PLAN_PROJECT_INDEX_PATH, ProjectWorkspaceService
from watchtower_plan.sync.all import AllSyncService
from watchtower_plan.workspace.artifacts import PLAN_ARTIFACT_INDEX_PATH
from watchtower_plan.workspace.constants import (
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
)
from watchtower_plan.workspace.service import PlanWorkspaceService

_REPOSITORY_EXPORT_SCOPE = "repository_bundle"
_PLAN_TRACKING_OUTPUTS = (
    "plan/tracking/initiative_tracking.md",
    "plan/tracking/task_tracking.md",
    "plan/tracking/coordination_tracking.md",
)
_PLAN_WORKSPACE_OUTPUTS = (
    PLAN_PROJECT_INDEX_PATH,
    PLAN_ARTIFACT_INDEX_PATH,
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
    PLAN_OVERVIEW_PATH,
)


def scrub_plan_export(request: PackExportCleanupRequest) -> PackExportCleanupResult:
    """Scrub live plan history from one staged export and rebuild safe empty views."""

    output_root = Path(request.output_root).expanduser().resolve()
    scrubbed_paths: set[str] = set()
    changed_paths: set[str] = set()

    roots_to_scrub = [
        request.initiatives_root,
        request.projects_root,
        f"{request.machine_root}/work_items",
    ]
    if request.export_scope != _REPOSITORY_EXPORT_SCOPE:
        roots_to_scrub.append(request.tracking_root)

    for relative_root in roots_to_scrub:
        if not relative_root:
            continue
        scrubbed_paths.update(clear_directory_contents(output_root, relative_root))

    scrubbed_paths.update(remove_if_exists(output_root, request.overview_path))

    indexes_root = output_root / request.machine_root / "indexes"
    if request.export_scope != _REPOSITORY_EXPORT_SCOPE and indexes_root.exists():
        scrubbed_paths.update(
            clear_directory_contents(output_root, f"{request.machine_root}/indexes")
        )

    if request.export_scope != _REPOSITORY_EXPORT_SCOPE:
        return PackExportCleanupResult(
            scrubbed_paths=tuple(sorted(scrubbed_paths)),
            changed_paths=tuple(sorted(changed_paths)),
        )

    loader = ControlPlaneLoader(
        output_root,
        active_pack_settings_path=request.pack_settings_path,
    )
    ProjectWorkspaceService(loader).sync(write=True)
    PlanWorkspaceService(loader).sync(write=True)
    sync_result = AllSyncService(loader).run(write=True)

    changed_paths.update(_PLAN_WORKSPACE_OUTPUTS)
    changed_paths.update(_PLAN_TRACKING_OUTPUTS)
    changed_paths.update(record.relative_output_path for record in sync_result.records)
    return PackExportCleanupResult(
        scrubbed_paths=tuple(sorted(scrubbed_paths)),
        changed_paths=tuple(sorted(changed_paths)),
    )



__all__ = ["scrub_plan_export"]
