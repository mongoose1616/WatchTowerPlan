from __future__ import annotations

from watchtower_plan.query.coordination import (
    CoordinationQueryService,
    CoordinationSearchParams,
)
from watchtower_plan.workspace.service import PlanWorkspaceService

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import CoordinationIndex, InitiativeIndexEntry
from watchtower_core.control_plane.paths import discover_repo_root


def test_plan_workspace_service_reuses_cached_pack_loader(
    monkeypatch,
) -> None:
    loader = ControlPlaneLoader(discover_repo_root())
    service = PlanWorkspaceService(loader)

    def _unexpected_derive(*args, **kwargs):
        raise AssertionError("load_coordination_index should reuse the cached pack loader")

    monkeypatch.setattr(loader, "derive", _unexpected_derive)

    index = service.load_coordination_index()

    assert isinstance(index, CoordinationIndex)
    assert index.artifact_id == "index.coordination"


def test_coordination_query_service_skips_history_service_for_active_queries(
    monkeypatch,
) -> None:
    entry = InitiativeIndexEntry(
        trace_id="trace.example",
        title="Example Initiative",
        summary="Fixture active initiative.",
        artifact_status="active",
        initiative_status="active",
        current_phase="in_progress",
        updated_at="2026-03-22T00:00:00Z",
        open_task_count=1,
        blocked_task_count=0,
        key_surface_path="plan/initiatives/example/plan.md",
        next_action="Continue execution.",
        next_surface_path="plan/initiatives/example/progress.md",
        initiative_id="initiative.example",
        slug="example",
        scope_type="pack_wide",
        primary_owner="repository_maintainer",
        active_owners=("repository_maintainer",),
    )
    index = CoordinationIndex(
        schema_id="urn:watchtower:schema:coordination-index:v1",
        artifact_id="index.coordination",
        title="Coordination Index",
        status="active",
        updated_at="2026-03-22T00:00:00Z",
        coordination_mode="active_work",
        summary="One active initiative remains.",
        recommended_next_action="Continue execution.",
        recommended_surface_path="plan/initiatives/example/plan.md",
        active_initiative_count=1,
        blocked_task_count=0,
        actionable_task_count=1,
        entries=(entry,),
        actionable_tasks=(),
        recent_closed_initiatives=(),
    )

    class FakePlanWorkspaceService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def load_coordination_index(self) -> CoordinationIndex:
            return index

        def search_coordination(
            self,
            _filters: object,
        ) -> tuple[InitiativeIndexEntry, ...]:
            return index.entries

    def _unexpected_initiative_service(_loader: object) -> object:
        raise AssertionError(
            "active coordination queries should not instantiate InitiativeQueryService"
        )

    monkeypatch.setattr(
        "watchtower_plan.query.coordination.PlanWorkspaceService",
        FakePlanWorkspaceService,
    )
    monkeypatch.setattr(
        "watchtower_plan.query.coordination.InitiativeQueryService",
        _unexpected_initiative_service,
    )

    result = CoordinationQueryService(ControlPlaneLoader(discover_repo_root())).search(
        CoordinationSearchParams(initiative_status="active")
    )

    assert result.index is index
    assert result.entries == index.entries
