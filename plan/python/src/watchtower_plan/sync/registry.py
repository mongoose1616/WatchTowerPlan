"""Canonical registry for deterministic repo-local sync targets."""

from __future__ import annotations

from typing import Literal

from watchtower_core.sync.command_index import (
    COMMAND_INDEX_ARTIFACT_PATH,
    CommandIndexSyncService,
)
from watchtower_core.sync.foundation_index import (
    FOUNDATION_INDEX_ARTIFACT_PATH,
    FoundationIndexSyncService,
)
from watchtower_core.sync.reference_index import (
    REFERENCE_INDEX_ARTIFACT_PATH,
    ReferenceIndexSyncService,
)
from watchtower_plan.sync.coordination_index import (
    COORDINATION_INDEX_ARTIFACT_PATH,
    CoordinationIndexSyncService,
)
from watchtower_plan.sync.coordination_tracking import (
    COORDINATION_TRACKING_DOCUMENT_PATH,
    CoordinationTrackingSyncService,
)
from watchtower_plan.sync.initiative_index import (
    INITIATIVE_INDEX_ARTIFACT_PATH,
    InitiativeIndexSyncService,
)
from watchtower_plan.sync.initiative_tracking import (
    INITIATIVE_TRACKING_DOCUMENT_PATH,
    InitiativeTrackingSyncService,
)
from watchtower_core.sync.repository_paths import (
    REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
    RepositoryPathIndexSyncService,
)
from watchtower_core.sync.route_index import (
    ROUTE_INDEX_ARTIFACT_PATH,
    RouteIndexSyncService,
)
from watchtower_core.sync.standard_index import (
    STANDARD_INDEX_ARTIFACT_PATH,
    StandardIndexSyncService,
)
from watchtower_core.sync.workflow_index import (
    WORKFLOW_INDEX_ARTIFACT_PATH,
    WorkflowIndexSyncService,
)
from watchtower_plan.sync.review_index import (
    REVIEW_INDEX_ARTIFACT_PATH,
    ReviewIndexSyncService,
)
from watchtower_plan.sync.task_index import TASK_INDEX_ARTIFACT_PATH, TaskIndexSyncService
from watchtower_plan.sync.task_tracking import (
    TASK_TRACKING_DOCUMENT_PATH,
    TaskTrackingSyncService,
)
from watchtower_plan.sync.traceability import (
    TRACEABILITY_INDEX_ARTIFACT_PATH,
    TraceabilityIndexSyncService,
)
from watchtower_core.sync.harness import SyncTargetMode, SyncTargetSpec

SyncTargetGroup = Literal["coordination"]
COORDINATION_SYNC_GROUP: SyncTargetGroup = "coordination"


SYNC_TARGET_SPECS: tuple[SyncTargetSpec, ...] = (
    SyncTargetSpec(
        target="command-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=COMMAND_INDEX_ARTIFACT_PATH,
        service_factory=CommandIndexSyncService,
    ),
    SyncTargetSpec(
        target="foundation-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=FOUNDATION_INDEX_ARTIFACT_PATH,
        service_factory=FoundationIndexSyncService,
    ),
    SyncTargetSpec(
        target="reference-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=REFERENCE_INDEX_ARTIFACT_PATH,
        service_factory=ReferenceIndexSyncService,
    ),
    SyncTargetSpec(
        target="route-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=ROUTE_INDEX_ARTIFACT_PATH,
        service_factory=RouteIndexSyncService,
    ),
    SyncTargetSpec(
        target="standard-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=STANDARD_INDEX_ARTIFACT_PATH,
        service_factory=StandardIndexSyncService,
    ),
    SyncTargetSpec(
        target="workflow-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=WORKFLOW_INDEX_ARTIFACT_PATH,
        service_factory=WorkflowIndexSyncService,
    ),
    SyncTargetSpec(
        target="task-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=TASK_INDEX_ARTIFACT_PATH,
        service_factory=TaskIndexSyncService,
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="review-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=REVIEW_INDEX_ARTIFACT_PATH,
        service_factory=ReviewIndexSyncService,
    ),
    SyncTargetSpec(
        target="traceability-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=TRACEABILITY_INDEX_ARTIFACT_PATH,
        service_factory=TraceabilityIndexSyncService,
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="initiative-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=INITIATIVE_INDEX_ARTIFACT_PATH,
        service_factory=InitiativeIndexSyncService,
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="coordination-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=COORDINATION_INDEX_ARTIFACT_PATH,
        service_factory=CoordinationIndexSyncService,
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="task-tracking",
        mode="tracking",
        artifact_kind="tracker",
        relative_output_path=TASK_TRACKING_DOCUMENT_PATH,
        service_factory=TaskTrackingSyncService,
        record_count_attr="task_count",
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="initiative-tracking",
        mode="tracking",
        artifact_kind="tracker",
        relative_output_path=INITIATIVE_TRACKING_DOCUMENT_PATH,
        service_factory=InitiativeTrackingSyncService,
        record_count_attr="initiative_count",
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="coordination-tracking",
        mode="tracking",
        artifact_kind="tracker",
        relative_output_path=COORDINATION_TRACKING_DOCUMENT_PATH,
        service_factory=CoordinationTrackingSyncService,
        record_count_attr="coordination_entry_count",
        groups=(COORDINATION_SYNC_GROUP,),
    ),
    SyncTargetSpec(
        target="repository-paths",
        mode="document",
        artifact_kind="index",
        relative_output_path=REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
        service_factory=RepositoryPathIndexSyncService,
    ),
)


def sync_target_specs_for_group(group: SyncTargetGroup) -> tuple[SyncTargetSpec, ...]:
    """Return sync targets that belong to one explicit orchestration group."""
    return tuple(spec for spec in SYNC_TARGET_SPECS if group in spec.groups)


__all__ = [
    "COORDINATION_SYNC_GROUP",
    "SYNC_TARGET_SPECS",
    "SyncTargetGroup",
    "SyncTargetMode",
    "SyncTargetSpec",
    "sync_target_specs_for_group",
]
