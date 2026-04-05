"""Initiative-package orchestration façade for pack-wide and project-scoped plan work."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.initiatives.bootstrap import InitiativeBootstrapCoordinator
from watchtower_plan.initiatives.closeout import InitiativeCloseoutCoordinator
from watchtower_plan.initiatives.discrepancies import InitiativeDiscrepancyCoordinator
from watchtower_plan.initiatives.locations import InitiativeLocation, InitiativeLocationManager
from watchtower_plan.initiatives.models import (
    DeferredItemSpec,
    InitiativeBootstrapParams,
    InitiativePackageResult,
    InitiativeReadinessResult,
    InitiativeTaskSpec,
    InitiativeTerminalCloseoutResult,
)
from watchtower_plan.initiatives.readiness import InitiativeReadinessCoordinator


class InitiativePackageService:
    """Manage pack-wide and project-scoped initiative packages in the live plan workspace."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._context = InitiativeLocationManager(loader)
        self._discrepancies = InitiativeDiscrepancyCoordinator(self._context)
        self._readiness = InitiativeReadinessCoordinator(
            self._context, self._discrepancies
        )
        self._bootstrap = InitiativeBootstrapCoordinator(
            self._context,
            self._discrepancies,
            self._readiness,
        )
        self._closeout = InitiativeCloseoutCoordinator(
            self._context,
            self._discrepancies,
            self._readiness,
        )

    def bootstrap_packwide(
        self,
        params: InitiativeBootstrapParams,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Create one pack-wide initiative package and stage it for review."""

        return self._bootstrap.bootstrap_initiative(
            self._context.packwide_location(params),
            params,
            write=write,
        )

    def bootstrap_project_scoped(
        self,
        project_slug: str,
        params: InitiativeBootstrapParams,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Create one project-scoped initiative package beneath a bootstrapped project."""

        return self._bootstrap.bootstrap_initiative(
            self._context.project_scoped_location(project_slug, params),
            params,
            write=write,
        )

    def validate_packwide(
        self,
        initiative_slug: str,
        *,
        write: bool,
        require_approved: bool = False,
    ) -> InitiativeReadinessResult:
        """Validate one pack-wide initiative package and refresh its gate state."""

        return self._readiness.validate_initiative(
            self._context.packwide_location_for_slug(initiative_slug),
            write=write,
            require_approved=require_approved,
        )

    def validate_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        *,
        write: bool,
        require_approved: bool = False,
    ) -> InitiativeReadinessResult:
        """Validate one project-scoped initiative package and refresh its gate state."""

        return self._readiness.validate_initiative(
            self._context.project_scoped_location_for_slug(
                project_slug, initiative_slug
            ),
            write=write,
            require_approved=require_approved,
        )

    def confirm_authored_inputs(
        self,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Confirm edited authored inputs into machine state."""

        return self._readiness.confirm_authored_inputs(
            self._context.packwide_location_for_slug(initiative_slug),
            approver_actor_id,
            write=write,
        )

    def confirm_project_scoped_inputs(
        self,
        project_slug: str,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Confirm edited authored inputs for one project-scoped initiative package."""

        return self._readiness.confirm_authored_inputs(
            self._context.project_scoped_location_for_slug(
                project_slug, initiative_slug
            ),
            approver_actor_id,
            write=write,
        )

    def approve_packwide(
        self,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Approve one validated pack-wide initiative into ready_for_execution."""

        return self._readiness.approve_initiative(
            self._context.packwide_location_for_slug(initiative_slug),
            approver_actor_id,
            write=write,
        )

    def approve_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        approver_actor_id: str,
        *,
        write: bool,
    ) -> InitiativePackageResult:
        """Approve one validated project-scoped initiative into ready_for_execution."""

        return self._readiness.approve_initiative(
            self._context.project_scoped_location_for_slug(
                project_slug, initiative_slug
            ),
            approver_actor_id,
            write=write,
        )

    def close_packwide(
        self,
        initiative_slug: str,
        *,
        initiative_status: str,
        closure_reason: str,
        write: bool,
        closed_at: str | None = None,
        superseded_by_trace_id: str | None = None,
    ) -> InitiativeTerminalCloseoutResult:
        """Close a pack-wide initiative into a terminal lifecycle state."""

        return self._closeout.close_initiative(
            self._context.packwide_location_for_slug(initiative_slug),
            initiative_status=initiative_status,
            closure_reason=closure_reason,
            write=write,
            closed_at=closed_at,
            superseded_by_trace_id=superseded_by_trace_id,
        )

    def close_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        *,
        initiative_status: str,
        closure_reason: str,
        write: bool,
        closed_at: str | None = None,
        superseded_by_trace_id: str | None = None,
    ) -> InitiativeTerminalCloseoutResult:
        """Close a project-scoped initiative into a terminal lifecycle state."""

        return self._closeout.close_initiative(
            self._context.project_scoped_location_for_slug(
                project_slug, initiative_slug
            ),
            initiative_status=initiative_status,
            closure_reason=closure_reason,
            write=write,
            closed_at=closed_at,
            superseded_by_trace_id=superseded_by_trace_id,
        )

    def _packwide_location(self, params: InitiativeBootstrapParams) -> InitiativeLocation:
        return self._context.packwide_location(params)

    def _packwide_location_for_slug(self, initiative_slug: str) -> InitiativeLocation:
        return self._context.packwide_location_for_slug(initiative_slug)

    def _project_scoped_location(
        self,
        project_slug: str,
        params: InitiativeBootstrapParams,
    ) -> InitiativeLocation:
        return self._context.project_scoped_location(project_slug, params)

    def _project_scoped_location_for_slug(
        self,
        project_slug: str,
        initiative_slug: str,
    ) -> InitiativeLocation:
        return self._context.project_scoped_location_for_slug(
            project_slug, initiative_slug
        )

    def _sync_derived_surfaces(self, location: InitiativeLocation) -> None:
        self._context.sync_derived_surfaces(location)


__all__ = [
    "DeferredItemSpec",
    "InitiativeBootstrapParams",
    "InitiativePackageResult",
    "InitiativePackageService",
    "InitiativeReadinessResult",
    "InitiativeTaskSpec",
    "InitiativeTerminalCloseoutResult",
]
