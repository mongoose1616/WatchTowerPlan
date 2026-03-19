"""Repo-specific query helpers for live plan evidence bundles."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.plan_workspace import (
    PlanEvidenceIndexEntry,
    PlanWorkspaceService,
)
from watchtower_core.repo_ops.plan_workspace import (
    PlanEvidenceSearchParams as WorkspacePlanEvidenceSearchParams,
)
from watchtower_core.repo_ops.query.common import DataclassSearchAdapter


@dataclass(frozen=True, slots=True)
class PlanEvidenceSearchParams:
    """Filter and ranking inputs for live plan evidence lookup."""

    query: str | None = None
    initiative_id: str | None = None
    project_id: str | None = None
    trace_id: str | None = None
    status: str | None = None
    owner: str | None = None
    target_phase: str | None = None
    validation_type: str | None = None
    acceptance_label: str | None = None
    limit: int | None = None


class PlanEvidenceQueryService(
    DataclassSearchAdapter[
        PlanEvidenceSearchParams,
        WorkspacePlanEvidenceSearchParams,
        PlanEvidenceIndexEntry,
    ]
):
    """Search the live plan evidence index."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        plan_workspace = PlanWorkspaceService(loader)
        super().__init__(
            target_type=WorkspacePlanEvidenceSearchParams,
            search=plan_workspace.search_evidence,
        )
