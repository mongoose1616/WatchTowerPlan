"""Helpers for governed project-root surface policy resolution and compliance checks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    ProjectSurfacePolicyEntry,
    ProjectSurfacePolicyRegistry,
    ProjectSurfacePolicySurfaceDefinition,
)


@dataclass(frozen=True, slots=True)
class ProjectSurfacePolicyIssue:
    """One compliance issue discovered against the project-surface policy registry."""

    issue_code: str
    policy_id: str
    root_path: str
    surface_path: str
    message: str


class ProjectSurfacePolicyHelper:
    """Resolve and validate governed project-root surface expectations."""

    def __init__(self, registry: ProjectSurfacePolicyRegistry) -> None:
        self._registry = registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> ProjectSurfacePolicyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("project_surface_policy_registry")
        if not isinstance(registry, ProjectSurfacePolicyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed project_surface_policy_registry."
            )
        return cls(registry)

    def policy_for_root(self, relative_root: str) -> ProjectSurfacePolicyEntry:
        """Return the most-specific policy entry for one repository-relative project root."""

        normalized_root = _normalize_relative_root(relative_root)
        matches = tuple(
            entry for entry in self._registry.entries if _policy_matches(entry, normalized_root)
        )
        if not matches:
            raise KeyError(normalized_root)
        return sorted(matches, key=_specificity_key, reverse=True)[0]

    def surfaces_for_root(
        self,
        relative_root: str,
        *,
        surface_kind: str | None = None,
    ) -> tuple[ProjectSurfacePolicySurfaceDefinition, ...]:
        """Return declared surfaces for one project root, optionally filtered by kind."""

        policy = self.policy_for_root(relative_root)
        if surface_kind is None:
            return policy.surfaces
        return tuple(surface for surface in policy.surfaces if surface.surface_kind == surface_kind)

    def required_relative_paths(
        self,
        relative_root: str,
        *,
        surface_kind: str | None = None,
    ) -> tuple[str, ...]:
        """Return required surface paths for one project root."""

        normalized_root = _normalize_relative_root(relative_root)
        return tuple(
            _join_relative(normalized_root, surface.relative_path)
            for surface in self.surfaces_for_root(normalized_root, surface_kind=surface_kind)
            if surface.mode == "required"
        )

    def validate_root(
        self,
        repo_root: Path,
        relative_root: str,
        *,
        surface_kinds: tuple[str, ...] | None = None,
    ) -> tuple[ProjectSurfacePolicyIssue, ...]:
        """Validate one project root against the resolved policy entry."""

        normalized_root = _normalize_relative_root(relative_root)
        policy = self.policy_for_root(normalized_root)
        root_path = repo_root / normalized_root
        issues: list[ProjectSurfacePolicyIssue] = []

        candidate_surfaces = policy.surfaces
        if surface_kinds is not None:
            candidate_surfaces = tuple(
                surface for surface in candidate_surfaces if surface.surface_kind in surface_kinds
            )

        if not root_path.exists():
            if any(surface.mode == "required" for surface in candidate_surfaces):
                issues.append(
                    ProjectSurfacePolicyIssue(
                        issue_code="root_missing",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=normalized_root,
                        message=(
                            f"Project-surface policy root is missing: {normalized_root} "
                            f"for {policy.policy_id}."
                        ),
                    )
                )
            return tuple(issues)

        if not root_path.is_dir():
            issues.append(
                ProjectSurfacePolicyIssue(
                    issue_code="root_not_directory",
                    policy_id=policy.policy_id,
                    root_path=normalized_root,
                    surface_path=normalized_root,
                    message=(
                        f"Project-surface policy root is not a directory: {normalized_root} "
                        f"for {policy.policy_id}."
                    ),
                )
            )
            return tuple(issues)

        for surface in candidate_surfaces:
            target_path = root_path / surface.relative_path
            target_relative_path = _join_relative(normalized_root, surface.relative_path)
            exists = target_path.exists()

            if surface.mode == "required" and not exists:
                issues.append(
                    ProjectSurfacePolicyIssue(
                        issue_code="required_surface_missing",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=target_relative_path,
                        message=(
                            f"Required project surface is missing: {target_relative_path} "
                            f"for {policy.policy_id}."
                        ),
                    )
                )
                continue

            if surface.mode == "forbidden" and exists:
                issues.append(
                    ProjectSurfacePolicyIssue(
                        issue_code="forbidden_surface_present",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=target_relative_path,
                        message=(
                            f"Forbidden project surface is present: {target_relative_path} "
                            f"for {policy.policy_id}."
                        ),
                    )
                )
                continue

            if not exists:
                continue

            if surface.entity_shape == "file" and not target_path.is_file():
                issues.append(
                    ProjectSurfacePolicyIssue(
                        issue_code="required_surface_shape_mismatch",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=target_relative_path,
                        message=(
                            f"Required project surface must be a file: {target_relative_path} "
                            f"for {policy.policy_id}."
                        ),
                    )
                )
                continue
            if surface.entity_shape == "directory" and not target_path.is_dir():
                issues.append(
                    ProjectSurfacePolicyIssue(
                        issue_code="required_surface_shape_mismatch",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=target_relative_path,
                        message=(
                            "Required project surface must be a directory: "
                            f"{target_relative_path} for {policy.policy_id}."
                        ),
                    )
                )
                continue

            if surface.required_metadata_fields and target_path.suffix == ".json":
                document = json.loads(target_path.read_text(encoding="utf-8"))
                missing_fields = tuple(
                    field for field in surface.required_metadata_fields if field not in document
                )
                if missing_fields:
                    issues.append(
                        ProjectSurfacePolicyIssue(
                            issue_code="required_metadata_missing",
                            policy_id=policy.policy_id,
                            root_path=normalized_root,
                            surface_path=target_relative_path,
                            message=(
                                "Required metadata fields are missing from project surface "
                                f"{target_relative_path}: {', '.join(missing_fields)}."
                            ),
                        )
                    )

        return tuple(issues)


def _normalize_relative_root(relative_root: str) -> str:
    return relative_root.strip().strip("/")


def _join_relative(root: str, relative_path: str) -> str:
    return f"{root}/{relative_path}"


def _policy_matches(entry: ProjectSurfacePolicyEntry, relative_root: str) -> bool:
    if entry.match_mode == "exact":
        return entry.path_pattern == relative_root
    return PurePosixPath(relative_root).match(entry.path_pattern)


def _specificity_key(entry: ProjectSurfacePolicyEntry) -> tuple[int, int]:
    wildcard_penalty = entry.path_pattern.count("*")
    return (len(entry.path_pattern) - wildcard_penalty, -wildcard_penalty)


__all__ = ["ProjectSurfacePolicyHelper", "ProjectSurfacePolicyIssue"]
