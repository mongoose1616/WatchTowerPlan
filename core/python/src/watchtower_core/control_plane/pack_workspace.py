"""Typed helpers for pack-declared workspace roots and path construction."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import PackSettings
from watchtower_core.control_plane.path_ids import PlanInitiativeLocation, PlanPathIdHelper


@dataclass(frozen=True, slots=True)
class PackWorkspacePaths:
    """Resolved repository-relative workspace roots for one active pack."""

    pack_id: str
    pack_settings_path: str
    workspace_root: str
    machine_root: str
    docs_root: str
    workflows_root: str
    tracking_root: str
    initiatives_root: str
    projects_root: str
    overview_path: str
    default_validation_suite_id: str

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> PackWorkspacePaths:
        """Build one workspace helper from pack settings resolved through the loader."""

        effective_pack_settings_path = loader.effective_pack_settings_path(pack_settings_path)
        effective_loader = (
            loader
            if loader.active_pack_settings_path == effective_pack_settings_path
            else loader.derive(active_pack_settings_path=effective_pack_settings_path)
        )
        pack_settings = effective_loader.load_pack_settings(effective_pack_settings_path)
        return cls.from_pack_settings(
            pack_settings,
            pack_settings_path=effective_pack_settings_path,
        )

    @classmethod
    def from_pack_settings(
        cls,
        pack_settings: PackSettings,
        *,
        pack_settings_path: str,
    ) -> PackWorkspacePaths:
        """Build one workspace helper from one typed pack-settings document."""

        roots = pack_settings.workspace_roots
        return cls(
            pack_id=pack_settings.pack_id,
            pack_settings_path=pack_settings_path,
            workspace_root=roots.workspace_root,
            machine_root=roots.machine_root,
            docs_root=roots.docs_root,
            workflows_root=roots.workflows_root,
            tracking_root=roots.tracking_root,
            initiatives_root=roots.initiatives_root,
            projects_root=roots.projects_root,
            overview_path=roots.overview_path,
            default_validation_suite_id=pack_settings.default_validation_suite_id,
        )

    def packwide_initiative_location(
        self,
        *,
        trace_id: str | None = None,
        initiative_slug: str | None = None,
    ) -> PlanInitiativeLocation:
        """Return the canonical pack-wide initiative location for this workspace."""

        slug = self._resolve_initiative_slug(trace_id=trace_id, initiative_slug=initiative_slug)
        return PlanInitiativeLocation(
            initiative_slug=slug,
            initiative_root_relative=self.join(self.initiatives_root, slug),
            scope_type="pack_wide",
        )

    def project_scoped_initiative_location(
        self,
        project_slug: str,
        *,
        trace_id: str | None = None,
        initiative_slug: str | None = None,
    ) -> PlanInitiativeLocation:
        """Return the canonical project-scoped initiative location for this workspace."""

        normalized_project_slug = PlanPathIdHelper.normalize_slug(
            project_slug,
            label="project_slug",
        )
        slug = self._resolve_initiative_slug(trace_id=trace_id, initiative_slug=initiative_slug)
        return PlanInitiativeLocation(
            initiative_slug=slug,
            initiative_root_relative=self.join(
                self.project_initiatives_root_relative(normalized_project_slug),
                slug,
            ),
            scope_type="project_scoped",
            project_slug=normalized_project_slug,
            project_id=PlanPathIdHelper.canonical_project_id(normalized_project_slug),
        )

    def project_root_relative(self, project_slug: str) -> str:
        """Return the canonical relative root for one project container."""

        normalized = PlanPathIdHelper.normalize_slug(project_slug, label="project_slug")
        return self.join(self.projects_root, normalized)

    def project_machine_root_relative(self, project_slug: str) -> str:
        """Return the canonical machine root for one project container."""

        return self.join(self.project_root_relative(project_slug), ".wt")

    def project_initiatives_root_relative(self, project_slug: str) -> str:
        """Return the canonical initiatives root for one project container."""

        return self.join(self.project_root_relative(project_slug), "initiatives")

    def machine_path(self, suffix: str) -> str:
        """Return one repository-relative path beneath the pack machine root."""

        return self.join(self.machine_root, suffix)

    def index_path(self, filename: str) -> str:
        """Return one repository-relative path beneath the pack index root."""

        return self.machine_path(f"indexes/{filename}")

    def registry_path(self, filename: str) -> str:
        """Return one repository-relative path beneath the pack registry root."""

        return self.machine_path(f"registries/{filename}")

    def tracking_path(self, filename: str) -> str:
        """Return one repository-relative path beneath the pack tracking root."""

        return self.join(self.tracking_root, filename)

    def docs_path(self, suffix: str) -> str:
        """Return one repository-relative path beneath the pack docs root."""

        return self.join(self.docs_root, suffix)

    def workflows_path(self, suffix: str) -> str:
        """Return one repository-relative path beneath the pack workflows root."""

        return self.join(self.workflows_root, suffix)

    @staticmethod
    def join(root: str, suffix: str) -> str:
        """Join one repository-relative root with a relative suffix."""

        return PlanPathIdHelper.join_relative(root, suffix)

    def _resolve_initiative_slug(
        self,
        *,
        trace_id: str | None,
        initiative_slug: str | None,
    ) -> str:
        if trace_id is None and initiative_slug is None:
            raise ValueError("trace_id or initiative_slug is required.")
        return PlanPathIdHelper.initiative_slug(
            trace_id=trace_id or f"trace.{initiative_slug}",
            initiative_slug=initiative_slug,
        )


__all__ = ["PackWorkspacePaths"]
