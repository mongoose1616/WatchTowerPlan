"""Helpers for governed template-catalog resolution and template-path validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import TemplateCatalog, TemplateCatalogEntry


@dataclass(frozen=True, slots=True)
class TemplateCatalogIssue:
    """One template-catalog issue discovered against a repository root."""

    issue_code: str
    template_id: str
    relative_path: str
    message: str


class TemplateCatalogHelper:
    """Resolve governed template metadata from the active pack context."""

    def __init__(self, catalog: TemplateCatalog) -> None:
        self._catalog = catalog

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> TemplateCatalogHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("template_catalog")
        if not isinstance(registry, TemplateCatalog):
            raise ValueError(
                "Active pack settings do not declare a typed template_catalog."
            )
        return cls(registry)

    def template(self, template_id: str) -> TemplateCatalogEntry:
        """Return one template entry by identifier."""

        return self._catalog.get(template_id)

    def templates_for_family(self, family_id: str) -> tuple[TemplateCatalogEntry, ...]:
        """Return active templates bound to one documentation family."""

        return tuple(
            entry
            for entry in self._catalog.entries
            if entry.entry_status == "active" and entry.family_id == family_id
        )

    def templates_for_surface(self, surface_id: str) -> tuple[TemplateCatalogEntry, ...]:
        """Return active templates bound to one rendered or authored surface id."""

        return tuple(
            entry
            for entry in self._catalog.entries
            if entry.entry_status == "active" and entry.surface_id == surface_id
        )

    def template_path(self, repo_root: Path, template_id: str) -> Path:
        """Return the resolved filesystem path for one template entry."""

        return repo_root / self.template(template_id).template_path

    def validate_paths(self, repo_root: Path) -> tuple[TemplateCatalogIssue, ...]:
        """Validate that every active template entry points to a real file."""

        issues: list[TemplateCatalogIssue] = []
        for entry in self._catalog.entries:
            if entry.entry_status != "active":
                continue
            candidate = repo_root / entry.template_path
            if not candidate.exists():
                issues.append(
                    TemplateCatalogIssue(
                        issue_code="template_missing",
                        template_id=entry.template_id,
                        relative_path=entry.template_path,
                        message=f"Template path is missing: {entry.template_path}.",
                    )
                )
                continue
            if not candidate.is_file():
                issues.append(
                    TemplateCatalogIssue(
                        issue_code="template_not_file",
                        template_id=entry.template_id,
                        relative_path=entry.template_path,
                        message=f"Template path is not a file: {entry.template_path}.",
                    )
                )
        return tuple(issues)


__all__ = ["TemplateCatalogHelper", "TemplateCatalogIssue"]
