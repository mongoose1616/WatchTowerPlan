"""Helpers for governed human-surface placement and compliance checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    HumanSurfacePolicyEntry,
    HumanSurfacePolicyRegistry,
)


@dataclass(frozen=True, slots=True)
class HumanSurfacePolicyIssue:
    """One compliance issue discovered against the human-surface policy registry."""

    issue_code: str
    policy_id: str
    root_path: str
    surface_path: str
    message: str


class HumanSurfacePolicyHelper:
    """Resolve and validate governed human-surface expectations by root."""

    def __init__(self, registry: HumanSurfacePolicyRegistry) -> None:
        self._registry = registry

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> HumanSurfacePolicyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("human_surface_policy_registry")
        if not isinstance(registry, HumanSurfacePolicyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed human_surface_policy_registry."
            )
        return cls(registry)

    def policy_for_root(self, relative_root: str) -> HumanSurfacePolicyEntry:
        """Return the most-specific policy entry for one repository-relative root."""

        normalized_root = _normalize_relative_root(relative_root)
        matches = tuple(
            entry for entry in self._registry.entries if _policy_matches(entry, normalized_root)
        )
        if not matches:
            raise KeyError(normalized_root)
        return sorted(matches, key=_specificity_key, reverse=True)[0]

    def validate_root(
        self,
        repo_root: Path,
        relative_root: str,
    ) -> tuple[HumanSurfacePolicyIssue, ...]:
        """Validate one concrete root against its resolved policy entry."""

        normalized_root = _normalize_relative_root(relative_root)
        policy = self.policy_for_root(normalized_root)
        root_path = repo_root if normalized_root == "." else repo_root / normalized_root
        issues: list[HumanSurfacePolicyIssue] = []

        if not root_path.exists():
            if any(surface.mode == "required" for surface in policy.surfaces):
                issues.append(
                    HumanSurfacePolicyIssue(
                        issue_code="root_missing",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=normalized_root,
                        message=(
                            f"Human-surface policy root is missing: {normalized_root} "
                            f"for {policy.policy_id}."
                        ),
                    )
                )
            return tuple(issues)

        if not root_path.is_dir():
            issues.append(
                HumanSurfacePolicyIssue(
                    issue_code="root_not_directory",
                    policy_id=policy.policy_id,
                    root_path=normalized_root,
                    surface_path=normalized_root,
                    message=(
                        f"Human-surface policy root is not a directory: {normalized_root} "
                        f"for {policy.policy_id}."
                    ),
                )
            )
            return tuple(issues)

        for surface in policy.surfaces:
            target_path = root_path / surface.relative_path
            target_relative_path = _join_relative(normalized_root, surface.relative_path)
            exists = target_path.exists()

            if surface.mode == "required":
                if not exists:
                    issues.append(
                        HumanSurfacePolicyIssue(
                            issue_code="required_surface_missing",
                            policy_id=policy.policy_id,
                            root_path=normalized_root,
                            surface_path=target_relative_path,
                            message=(
                                f"Required human surface is missing: {target_relative_path} "
                                f"for {policy.policy_id}."
                            ),
                        )
                    )
                    continue
                if surface.entity_shape == "file" and not target_path.is_file():
                    issues.append(
                        HumanSurfacePolicyIssue(
                            issue_code="required_surface_shape_mismatch",
                            policy_id=policy.policy_id,
                            root_path=normalized_root,
                            surface_path=target_relative_path,
                            message=(
                                f"Required human surface must be a file: {target_relative_path} "
                                f"for {policy.policy_id}."
                            ),
                        )
                    )
                if surface.entity_shape == "directory" and not target_path.is_dir():
                    issues.append(
                        HumanSurfacePolicyIssue(
                            issue_code="required_surface_shape_mismatch",
                            policy_id=policy.policy_id,
                            root_path=normalized_root,
                            surface_path=target_relative_path,
                            message=(
                                "Required human surface must be a directory: "
                                f"{target_relative_path} for {policy.policy_id}."
                            ),
                        )
                    )
                continue

            if surface.mode == "forbidden" and exists:
                issues.append(
                    HumanSurfacePolicyIssue(
                        issue_code="forbidden_surface_present",
                        policy_id=policy.policy_id,
                        root_path=normalized_root,
                        surface_path=target_relative_path,
                        message=(
                            f"Forbidden human surface is present: {target_relative_path} "
                            f"for {policy.policy_id}."
                        ),
                    )
                )

        return tuple(issues)

    def validate_repository(self, repo_root: Path) -> tuple[HumanSurfacePolicyIssue, ...]:
        """Validate all declared roots against one repository root."""

        issues: list[HumanSurfacePolicyIssue] = []
        for entry in self._registry.entries:
            for relative_root in _roots_for_entry(repo_root, entry):
                issues.extend(self.validate_root(repo_root, relative_root))
        return tuple(issues)


def _normalize_relative_root(relative_root: str) -> str:
    cleaned = relative_root.strip().strip("/")
    if cleaned in {"", "."}:
        return "."
    return cleaned


def _join_relative(root: str, relative_path: str) -> str:
    if root == ".":
        return relative_path
    return f"{root}/{relative_path}"


def _policy_matches(entry: HumanSurfacePolicyEntry, relative_root: str) -> bool:
    if entry.match_mode == "exact":
        return _normalize_relative_root(entry.path_pattern) == relative_root
    return PurePosixPath(relative_root).match(entry.path_pattern)


def _specificity_key(entry: HumanSurfacePolicyEntry) -> tuple[int, int]:
    wildcard_penalty = entry.path_pattern.count("*")
    return (len(entry.path_pattern) - wildcard_penalty, -wildcard_penalty)


def _roots_for_entry(repo_root: Path, entry: HumanSurfacePolicyEntry) -> tuple[str, ...]:
    if entry.match_mode == "exact":
        return (_normalize_relative_root(entry.path_pattern),)
    return tuple(
        sorted(
            _normalize_relative_root(path.relative_to(repo_root).as_posix())
            for path in repo_root.glob(entry.path_pattern)
            if path.is_dir()
        )
    )


__all__ = ["HumanSurfacePolicyHelper", "HumanSurfacePolicyIssue"]
