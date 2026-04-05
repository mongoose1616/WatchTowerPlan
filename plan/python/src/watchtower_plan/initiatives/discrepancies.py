"""Discrepancy, event, and authorization helpers for live initiative packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.actors import ActorRegistryHelper
from watchtower_core.control_plane.discrepancy import (
    DiscrepancyDescriptor,
    DiscrepancyHelper,
    DiscrepancyIssue,
)
from watchtower_core.control_plane.event_stream import (
    EventStreamDescriptor,
    EventStreamHelper,
    EventStreamWriteRequest,
)
from watchtower_core.control_plane.human_surface_policy import HumanSurfacePolicyHelper
from watchtower_plan.initiatives.locations import (
    InitiativeLocation,
    InitiativeLocationManager,
)
from watchtower_plan.projects import ProjectWorkspaceService
from watchtower_plan.workspace.constants import PLAN_PACK_SETTINGS_PATH
from watchtower_plan.workspace.service import PlanWorkspaceService


class InitiativeDiscrepancyCoordinator:
    """Manage initiative-local discrepancies, events, and maintainer checks."""

    def __init__(
        self,
        context: InitiativeLocationManager,
    ) -> None:
        self._context = context

    def authored_input_drift_issues(
        self,
        *,
        location: InitiativeLocation,
        initiative_document: dict[str, Any],
    ) -> tuple[DiscrepancyIssue, ...]:
        issues: list[DiscrepancyIssue] = []
        for record in initiative_document["authored_inputs"]:
            relative_path = str(record["path"])
            current_digest = self._context.sha256_for_relative_path(relative_path)
            if current_digest != record["sha256"]:
                issues.append(
                    DiscrepancyIssue(
                        record_slug=f"{record['doc_kind']}_drift",
                        category="authored_input_drift",
                        source_paths=(relative_path,),
                        summary=(
                            f"Authored input drift detected for {relative_path}; "
                            "machine confirmation is required."
                        ),
                        discrepancy_id=(
                            f"discrepancy.{location.discrepancy_namespace}.{record['doc_kind']}_drift"
                        ),
                    )
                )
        return tuple(issues)

    def stale_derived_surface_issues(
        self,
        location: InitiativeLocation,
    ) -> tuple[DiscrepancyIssue, ...]:
        return PlanWorkspaceService(
            self._context.fresh_loader()
        ).expected_surface_issues(location.initiative_root_relative)

    def project_surface_issues(
        self,
        location: InitiativeLocation,
    ) -> tuple[DiscrepancyIssue, ...]:
        if location.project_slug is None:
            return ()
        fresh_loader = self._context.fresh_loader()
        return tuple(
            DiscrepancyIssue(
                record_slug=f"{Path(issue.relative_path).stem}_project_drift",
                category=issue.category,
                source_paths=(issue.relative_path,),
                summary=issue.message,
                discrepancy_id=(
                    f"discrepancy.{location.discrepancy_namespace}.{Path(issue.relative_path).stem}_project_drift"
                ),
            )
            for issue in ProjectWorkspaceService(fresh_loader).expected_surface_issues(
                location.project_slug
            )
        )

    def machine_root_policy_issues(
        self, location: InitiativeLocation
    ) -> tuple[str, ...]:
        helper = HumanSurfacePolicyHelper.from_loader(
            self._context.pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        machine_root = self._context.initiative_path(location, ".wt")
        return tuple(
            issue.message
            for issue in helper.validate_root(
                self._context.pack_loader().repo_root,
                machine_root,
            )
        )

    def blocking_deferred_item_issues(
        self, location: InitiativeLocation
    ) -> tuple[str, ...]:
        deferred_dir = (
            self._context.pack_loader().repo_root
            / self._context.initiative_path(
                location,
                ".wt/deferred",
            )
        )
        if not deferred_dir.exists():
            return ()
        issues: list[str] = []
        for path in sorted(deferred_dir.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            if document["status"] == "open" and document["blocks_ready_for_execution"]:
                issues.append(
                    f"Blocking deferred item {document['deferred_item_id']} remains open."
                )
        return tuple(issues)

    def open_discrepancy_documents(
        self,
        location: InitiativeLocation,
    ) -> tuple[tuple[str, dict[str, Any]], ...]:
        return self._discrepancy_helper().open_records(
            DiscrepancyDescriptor(
                relative_dir=self._context.initiative_path(
                    location, ".wt/discrepancies"
                ),
                initiative_id=str(
                    self._context.load_json(
                        self._context.initiative_path(location, ".wt/initiative.json")
                    )["initiative_id"]
                ),
            )
        )

    def sync_managed_discrepancies(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        discrepancy_issues: tuple[DiscrepancyIssue, ...],
        updated_at: str,
    ) -> None:
        self._discrepancy_helper().sync_records(
            DiscrepancyDescriptor(
                relative_dir=self._context.initiative_path(
                    location, ".wt/discrepancies"
                ),
                initiative_id=initiative_id,
            ),
            issues=discrepancy_issues,
            updated_at=updated_at,
            managed_categories=(
                "authored_input_drift",
                "stale_rendered_surface",
                "stale_aggregate_index",
            ),
        )

    def append_initiative_event(
        self,
        *,
        location: InitiativeLocation,
        initiative_id: str,
        trace_id: str,
        event_type: str,
        summary: str,
        actor_id: str,
        recorded_at: str,
    ) -> None:
        initiative_slug = location.initiative_slug
        descriptor = EventStreamDescriptor.initiative(
            relative_dir=self._context.initiative_path(location, ".wt/events"),
            event_id_prefix=f"event.{initiative_slug}",
            initiative_id=initiative_id,
            trace_id=trace_id,
        )
        self._event_stream_helper().append_event(
            descriptor,
            EventStreamWriteRequest(
                event_type=event_type,
                actor_id=actor_id,
                recorded_at=recorded_at,
                summary=summary,
                payload={},
            ),
        )

    def assert_default_authorized_maintainer(self, actor_id: str) -> None:
        helper = ActorRegistryHelper.from_loader(
            self._context.pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        try:
            helper.require_actor(
                actor_id,
                allowed_types=("user",),
                allowed_roles=("owner",),
                allowed_scopes=("repository",),
            )
        except ValueError as exc:
            raise ValueError(
                "Only default human repository maintainers may approve this initiative package."
            ) from exc

    def event_stream_helper(self) -> EventStreamHelper:
        return self._event_stream_helper()

    def _event_stream_helper(self) -> EventStreamHelper:
        return EventStreamHelper.from_loader(
            self._context.pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def _discrepancy_helper(self) -> DiscrepancyHelper:
        return DiscrepancyHelper.from_loader(
            self._context.pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )


__all__ = ["InitiativeDiscrepancyCoordinator"]
