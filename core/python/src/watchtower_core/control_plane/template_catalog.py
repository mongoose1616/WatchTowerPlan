"""Helpers for governed template-catalog resolution and template-path validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from jsonschema import ValidationError

from watchtower_core.control_plane.errors import SchemaResolutionError
from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import TemplateCatalog, TemplateCatalogEntry
from watchtower_core.control_plane.schemas import SchemaStore


@dataclass(frozen=True, slots=True)
class TemplateCatalogIssue:
    """One template-catalog issue discovered against a repository root."""

    issue_code: str
    template_id: str
    relative_path: str
    message: str


class TemplateCatalogHelper:
    """Resolve governed template metadata from the active pack context."""

    def __init__(
        self,
        catalog: TemplateCatalog,
        *,
        schema_store: SchemaStore | None = None,
    ) -> None:
        self._catalog = catalog
        self._schema_store = schema_store

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> TemplateCatalogHelper:
        """Build one helper from the active pack context."""

        effective_pack_settings_path = (
            loader.active_pack_settings_path
            if pack_settings_path == PACK_SETTINGS_PATH and loader.active_pack_settings_path
            else pack_settings_path
        )
        effective_loader = (
            loader
            if loader.active_pack_settings_path == effective_pack_settings_path
            else ControlPlaneLoader(
                workspace_config=loader.workspace_config,
                artifact_source=loader.artifact_source,
                artifact_store=loader.artifact_store,
                active_pack_settings_path=effective_pack_settings_path,
            )
        )
        context = effective_loader.load_pack_context(effective_pack_settings_path)
        registry = context.registries.get("template_catalog")
        if not isinstance(registry, TemplateCatalog):
            raise ValueError(
                "Active pack settings do not declare a typed template_catalog."
            )
        return cls(registry, schema_store=effective_loader.schema_store)

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

    def validate_contracts(self, repo_root: Path) -> tuple[TemplateCatalogIssue, ...]:
        """Validate template paths plus any referenced section-spec schema contracts."""

        issues = list(self.validate_paths(repo_root))
        if self._schema_store is None:
            return tuple(issues)

        for entry in self._catalog.entries:
            if entry.entry_status != "active":
                continue
            if entry.section_spec_schema_id is None:
                continue

            try:
                self._schema_store.load_schema(entry.section_spec_schema_id)
            except SchemaResolutionError as exc:
                issues.append(
                    TemplateCatalogIssue(
                        issue_code="section_spec_missing",
                        template_id=entry.template_id,
                        relative_path=entry.template_path,
                        message=str(exc),
                    )
                )
                continue

            candidate = repo_root / entry.template_path
            if not candidate.is_file():
                continue

            contract = {
                "template_id": entry.template_id,
                "required_section_ids": list(entry.required_section_ids),
                "optional_section_ids": list(entry.optional_section_ids),
                "section_order": list(entry.section_order),
                "template_heading_ids": list(_normalized_heading_ids(entry, candidate)),
            }
            if entry.required_rendered_surface_ids:
                contract["required_rendered_surface_ids"] = list(
                    entry.required_rendered_surface_ids
                )

            try:
                self._schema_store.validate_instance(
                    contract,
                    schema_id=entry.section_spec_schema_id,
                )
            except (SchemaResolutionError, ValidationError) as exc:
                issues.append(
                    TemplateCatalogIssue(
                        issue_code="section_spec_mismatch",
                        template_id=entry.template_id,
                        relative_path=entry.template_path,
                        message=str(exc),
                    )
                )

        return tuple(issues)


_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(?P<title>.+?)\s*$")


def _normalized_heading_ids(
    entry: TemplateCatalogEntry,
    template_path: Path,
) -> tuple[str, ...]:
    heading_ids = _extract_heading_ids(template_path)
    expected_ids = set(entry.required_section_ids) | set(entry.optional_section_ids)
    if heading_ids and heading_ids[0] not in expected_ids:
        return tuple(heading_ids[1:])
    return heading_ids


def _extract_heading_ids(template_path: Path) -> tuple[str, ...]:
    markdown = template_path.read_text(encoding="utf-8")
    lines = markdown.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                lines = lines[index + 1 :]
                break

    heading_ids: list[str] = []
    for line in lines:
        match = _HEADING_PATTERN.match(line)
        if not match:
            continue
        title = match.group("title")
        heading_id = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
        if heading_id:
            heading_ids.append(heading_id)
    return tuple(heading_ids)


__all__ = ["TemplateCatalogHelper", "TemplateCatalogIssue"]
