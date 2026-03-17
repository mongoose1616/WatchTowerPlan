"""Helpers for governed documentation-family resolution and placement checks."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    DocumentationFamilyEntry,
    DocumentationFamilyRegistry,
)


@dataclass(frozen=True, slots=True)
class DocumentationFamilyIssue:
    """One documentation-family issue discovered for a root or family."""

    issue_code: str
    family_id: str
    relative_root: str
    message: str


class DocumentationFamilyHelper:
    """Resolve governed documentation-family behavior from the active pack context."""

    def __init__(self, registry: DocumentationFamilyRegistry) -> None:
        self._registry = registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> DocumentationFamilyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("documentation_family_registry")
        if not isinstance(registry, DocumentationFamilyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed documentation_family_registry."
            )
        return cls(registry)

    def family(self, family_id: str) -> DocumentationFamilyEntry:
        """Return one documentation-family entry by identifier."""

        return self._registry.get(family_id)

    def families_for_root(self, relative_root: str) -> tuple[DocumentationFamilyEntry, ...]:
        """Return active families that allow the given repository-relative root."""

        normalized_root = _normalize_root(relative_root)
        return tuple(
            entry
            for entry in self._registry.entries
            if entry.entry_status == "active" and normalized_root in entry.allowed_roots
        )

    def allowed_in_root(self, family_id: str, relative_root: str) -> bool:
        """Return whether the given family may exist under the given root."""

        normalized_root = _normalize_root(relative_root)
        return normalized_root in self.family(family_id).allowed_roots

    def validate_root(self, family_id: str, relative_root: str) -> tuple[DocumentationFamilyIssue, ...]:
        """Validate one family-root pairing against the registry."""

        normalized_root = _normalize_root(relative_root)
        entry = self.family(family_id)
        issues: list[DocumentationFamilyIssue] = []
        if normalized_root not in entry.allowed_roots:
            issues.append(
                DocumentationFamilyIssue(
                    issue_code="root_not_allowed",
                    family_id=family_id,
                    relative_root=normalized_root,
                    message=(
                        f"Documentation family {family_id} is not allowed under {normalized_root}."
                    ),
                )
            )
        if entry.mirror_group_id and normalized_root not in entry.required_mirror_roots:
            issues.append(
                DocumentationFamilyIssue(
                    issue_code="missing_required_mirror_root",
                    family_id=family_id,
                    relative_root=normalized_root,
                    message=(
                        f"Documentation family {family_id} participates in mirror group "
                        f"{entry.mirror_group_id} but {normalized_root} is not one of the declared required mirror roots."
                    ),
                )
            )
        return tuple(issues)


def _normalize_root(relative_root: str) -> str:
    return relative_root.strip().strip("/")


__all__ = ["DocumentationFamilyHelper", "DocumentationFamilyIssue"]
