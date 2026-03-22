"""Helpers for governed workflow metadata, companion, and route relationship resolution."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import (
    RouteIndex,
    RouteIndexEntry,
    WorkflowIndex,
    WorkflowIndexEntry,
    WorkflowMetadataDefinition,
    WorkflowMetadataRegistry,
)


@dataclass(frozen=True, slots=True)
class WorkflowCatalogSnapshot:
    """Joined workflow-catalog view for one workflow."""

    workflow: WorkflowIndexEntry
    metadata: WorkflowMetadataDefinition
    companion_workflows: tuple[WorkflowIndexEntry, ...]
    route_bindings: tuple[RouteIndexEntry, ...]
    compatible_workflows: tuple[WorkflowIndexEntry, ...]


class WorkflowCatalogHelper:
    """Resolve workflow metadata, companion workflows, and route bindings together."""

    def __init__(
        self,
        *,
        workflow_index: WorkflowIndex,
        route_index: RouteIndex,
        metadata_registry: WorkflowMetadataRegistry,
    ) -> None:
        self._workflow_index = workflow_index
        self._route_index = route_index
        self._metadata_registry = metadata_registry

    @classmethod
    def from_loader(cls, loader: ControlPlaneLoader) -> WorkflowCatalogHelper:
        """Build one helper from the governed workflow and route surfaces."""

        return cls(
            workflow_index=loader.load_workflow_index(),
            route_index=loader.load_route_index(),
            metadata_registry=loader.load_workflow_metadata_registry(),
        )

    def workflow(self, workflow_id: str) -> WorkflowIndexEntry:
        """Return one workflow-index entry by identifier."""

        return self._workflow_index.get(workflow_id)

    def metadata(self, workflow_id: str) -> WorkflowMetadataDefinition:
        """Return one workflow metadata entry by identifier."""

        return self._metadata_registry.get(workflow_id)

    def companion_workflows(self, workflow_id: str) -> tuple[WorkflowIndexEntry, ...]:
        """Return typed companion workflows declared for one workflow."""

        workflow = self.workflow(workflow_id)
        return tuple(
            self.workflow(companion_id) for companion_id in workflow.companion_workflow_ids
        )

    def routes_for_workflow(self, workflow_id: str) -> tuple[RouteIndexEntry, ...]:
        """Return the routed task types that require one workflow."""

        self.workflow(workflow_id)
        return tuple(
            entry
            for entry in self._route_index.entries
            if workflow_id in entry.required_workflow_ids
        )

    def compatible_workflows(self, workflow_id: str) -> tuple[WorkflowIndexEntry, ...]:
        """Return workflows that share at least one route with the target workflow."""

        route_bindings = self.routes_for_workflow(workflow_id)
        compatible_ids = sorted(
            {
                required_workflow_id
                for route in route_bindings
                for required_workflow_id in route.required_workflow_ids
                if required_workflow_id != workflow_id
            }
        )
        return tuple(self.workflow(candidate_id) for candidate_id in compatible_ids)

    def snapshot(self, workflow_id: str) -> WorkflowCatalogSnapshot:
        """Return one fully joined workflow catalog snapshot."""

        workflow = self.workflow(workflow_id)
        metadata = self.metadata(workflow_id)
        companions = self.companion_workflows(workflow_id)
        route_bindings = self.routes_for_workflow(workflow_id)
        compatible = self.compatible_workflows(workflow_id)
        return WorkflowCatalogSnapshot(
            workflow=workflow,
            metadata=metadata,
            companion_workflows=companions,
            route_bindings=route_bindings,
            compatible_workflows=compatible,
        )


__all__ = ["WorkflowCatalogHelper", "WorkflowCatalogSnapshot"]
