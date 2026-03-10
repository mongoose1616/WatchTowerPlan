"""Canonical registry for deterministic sync targets."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.command_index import (
    COMMAND_INDEX_ARTIFACT_PATH,
    CommandIndexSyncService,
)
from watchtower_core.repo_ops.sync.coordination_index import (
    COORDINATION_INDEX_ARTIFACT_PATH,
    CoordinationIndexSyncService,
)
from watchtower_core.repo_ops.sync.coordination_tracking import (
    COORDINATION_TRACKING_DOCUMENT_PATH,
    CoordinationTrackingSyncService,
)
from watchtower_core.repo_ops.sync.decision_index import (
    DECISION_INDEX_ARTIFACT_PATH,
    DecisionIndexSyncService,
)
from watchtower_core.repo_ops.sync.decision_tracking import (
    DECISION_TRACKING_DOCUMENT_PATH,
    DecisionTrackingSyncService,
)
from watchtower_core.repo_ops.sync.design_document_index import (
    DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH,
    DesignDocumentIndexSyncService,
)
from watchtower_core.repo_ops.sync.design_tracking import (
    DESIGN_TRACKING_DOCUMENT_PATH,
    DesignTrackingSyncService,
)
from watchtower_core.repo_ops.sync.foundation_index import (
    FOUNDATION_INDEX_ARTIFACT_PATH,
    FoundationIndexSyncService,
)
from watchtower_core.repo_ops.sync.initiative_index import (
    INITIATIVE_INDEX_ARTIFACT_PATH,
    InitiativeIndexSyncService,
)
from watchtower_core.repo_ops.sync.initiative_tracking import (
    INITIATIVE_TRACKING_DOCUMENT_PATH,
    InitiativeTrackingSyncService,
)
from watchtower_core.repo_ops.sync.prd_index import PRD_INDEX_ARTIFACT_PATH, PrdIndexSyncService
from watchtower_core.repo_ops.sync.prd_tracking import (
    PRD_TRACKING_DOCUMENT_PATH,
    PrdTrackingSyncService,
)
from watchtower_core.repo_ops.sync.reference_index import (
    REFERENCE_INDEX_ARTIFACT_PATH,
    ReferenceIndexSyncService,
)
from watchtower_core.repo_ops.sync.repository_paths import (
    REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
    RepositoryPathIndexSyncService,
)
from watchtower_core.repo_ops.sync.route_index import (
    ROUTE_INDEX_ARTIFACT_PATH,
    RouteIndexSyncService,
)
from watchtower_core.repo_ops.sync.standard_index import (
    STANDARD_INDEX_ARTIFACT_PATH,
    StandardIndexSyncService,
)
from watchtower_core.repo_ops.sync.task_index import TASK_INDEX_ARTIFACT_PATH, TaskIndexSyncService
from watchtower_core.repo_ops.sync.task_tracking import (
    TASK_TRACKING_DOCUMENT_PATH,
    TaskTrackingSyncService,
)
from watchtower_core.repo_ops.sync.traceability import (
    TRACEABILITY_INDEX_ARTIFACT_PATH,
    TraceabilityIndexSyncService,
)
from watchtower_core.repo_ops.sync.workflow_index import (
    WORKFLOW_INDEX_ARTIFACT_PATH,
    WorkflowIndexSyncService,
)

SyncServiceFactory = Callable[[ControlPlaneLoader], object]
SyncTargetMode = Literal["document", "tracking"]
SyncTargetGroup = Literal["coordination"]
COORDINATION_SYNC_GROUP: SyncTargetGroup = "coordination"


@dataclass(frozen=True, slots=True)
class SyncTargetSpec:
    """One deterministic sync target included in aggregate orchestration."""

    target: str
    mode: SyncTargetMode
    artifact_kind: str
    relative_output_path: str
    service_factory: SyncServiceFactory
    record_count_attr: str | None = None
    groups: tuple[SyncTargetGroup, ...] = ()


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
        target="prd-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=PRD_INDEX_ARTIFACT_PATH,
        service_factory=PrdIndexSyncService,
    ),
    SyncTargetSpec(
        target="decision-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=DECISION_INDEX_ARTIFACT_PATH,
        service_factory=DecisionIndexSyncService,
    ),
    SyncTargetSpec(
        target="design-document-index",
        mode="document",
        artifact_kind="index",
        relative_output_path=DESIGN_DOCUMENT_INDEX_ARTIFACT_PATH,
        service_factory=DesignDocumentIndexSyncService,
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
        target="prd-tracking",
        mode="tracking",
        artifact_kind="tracker",
        relative_output_path=PRD_TRACKING_DOCUMENT_PATH,
        service_factory=PrdTrackingSyncService,
        record_count_attr="prd_count",
    ),
    SyncTargetSpec(
        target="decision-tracking",
        mode="tracking",
        artifact_kind="tracker",
        relative_output_path=DECISION_TRACKING_DOCUMENT_PATH,
        service_factory=DecisionTrackingSyncService,
        record_count_attr="decision_count",
    ),
    SyncTargetSpec(
        target="design-tracking",
        mode="tracking",
        artifact_kind="tracker",
        relative_output_path=DESIGN_TRACKING_DOCUMENT_PATH,
        service_factory=DesignTrackingSyncService,
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
