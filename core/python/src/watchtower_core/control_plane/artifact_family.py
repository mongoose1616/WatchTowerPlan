"""Helpers for governed artifact-family resolution and placement checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import ArtifactFamilyEntry, ArtifactFamilyRegistry


@dataclass(frozen=True, slots=True)
class ArtifactFamilyIssue:
    """One artifact-family issue discovered against a repository-relative path."""

    issue_code: str
    relative_path: str
    message: str


class ArtifactFamilyHelper:
    """Resolve governed artifact-family behavior from the active pack context."""

    def __init__(self, registry: ArtifactFamilyRegistry) -> None:
        self._registry = registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> ArtifactFamilyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("artifact_family_registry")
        if not isinstance(registry, ArtifactFamilyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed artifact_family_registry."
            )
        return cls(registry)

    def family(self, family_id: str) -> ArtifactFamilyEntry:
        """Return one artifact-family entry by identifier."""

        return self._registry.get(family_id)

    def family_for_path(self, relative_path: str) -> ArtifactFamilyEntry:
        """Return the most-specific artifact family for one repository-relative path."""

        normalized_path = _normalize_relative_path(relative_path)
        matches = self.families_for_path(normalized_path)
        if not matches:
            raise KeyError(normalized_path)
        return matches[0]

    def families_for_path(self, relative_path: str) -> tuple[ArtifactFamilyEntry, ...]:
        """Return all matching artifact-family entries for one repository-relative path."""

        normalized_path = _normalize_relative_path(relative_path)
        matches = tuple(
            entry
            for entry in self._registry.entries
            if any(_pattern_matches(pattern, normalized_path) for pattern in entry.placement_roots)
        )
        return tuple(sorted(matches, key=_specificity_key, reverse=True))

    def placement_allowed(self, family_id: str, relative_path: str) -> bool:
        """Return whether one relative path is allowed for the given artifact family."""

        normalized_path = _normalize_relative_path(relative_path)
        entry = self.family(family_id)
        return any(_pattern_matches(pattern, normalized_path) for pattern in entry.placement_roots)

    def validate_relative_path(self, relative_path: str) -> tuple[ArtifactFamilyIssue, ...]:
        """Validate that one repository-relative path resolves to at least one family."""

        normalized_path = _normalize_relative_path(relative_path)
        if self.families_for_path(normalized_path):
            return ()
        return (
            ArtifactFamilyIssue(
                issue_code="unclassified_artifact_path",
                relative_path=normalized_path,
                message=f"No artifact family covers repository path {normalized_path}.",
            ),
        )


def _normalize_relative_path(relative_path: str) -> str:
    return relative_path.strip().strip("/")


def _pattern_matches(pattern: str, relative_path: str) -> bool:
    return PurePosixPath(relative_path).match(pattern)


def _specificity_key(entry: ArtifactFamilyEntry) -> tuple[int, int]:
    best_length = max((len(pattern) for pattern in entry.placement_roots), default=0)
    wildcard_penalty = sum(pattern.count("*") for pattern in entry.placement_roots)
    return (best_length - wildcard_penalty, -wildcard_penalty)


__all__ = ["ArtifactFamilyHelper", "ArtifactFamilyIssue"]
