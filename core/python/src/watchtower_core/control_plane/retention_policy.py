"""Helpers for governed retention-policy resolution and coverage checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.models import RetentionPolicyEntry, RetentionPolicyRegistry


@dataclass(frozen=True, slots=True)
class RetentionPolicyIssue:
    """One retention-policy issue discovered against repository state."""

    issue_code: str
    root_path: str
    message: str


class RetentionPolicyHelper:
    """Resolve and validate governed retention-policy rules by repository path."""

    def __init__(
        self,
        registry: RetentionPolicyRegistry,
        workspace_paths: PackWorkspacePaths,
    ) -> None:
        self._registry = registry
        self._workspace_paths = workspace_paths

    @classmethod
    def from_loader(
        cls,
        loader: ControlPlaneLoader,
        *,
        pack_settings_path: str = PACK_SETTINGS_PATH,
    ) -> RetentionPolicyHelper:
        """Build one helper from the active pack context."""

        context = loader.load_pack_context(pack_settings_path)
        registry = context.registries.get("retention_policy_registry")
        if not isinstance(registry, RetentionPolicyRegistry):
            raise ValueError(
                "Active pack settings do not declare a typed retention_policy_registry."
            )
        return cls(
            registry,
            PackWorkspacePaths.from_loader(loader, pack_settings_path=pack_settings_path),
        )

    def policy_for_path(self, relative_path: str) -> RetentionPolicyEntry:
        """Return the most-specific policy entry for one repository-relative path."""

        normalized_path = _normalize_relative_path(relative_path)
        matches = tuple(
            entry for entry in self._registry.entries if _policy_matches(entry, normalized_path)
        )
        if not matches:
            raise KeyError(normalized_path)
        return sorted(matches, key=_specificity_key, reverse=True)[0]

    def current_disposition(self, relative_path: str) -> str:
        """Return the current retention disposition for one repository-relative path."""

        return self.policy_for_path(relative_path).current_disposition

    def clean_endstate_disposition(self, relative_path: str) -> str:
        """Return the clean-endstate retention disposition for one repository-relative path."""

        return self.policy_for_path(relative_path).clean_endstate_disposition

    def validate_repository(self, repo_root: Path) -> tuple[RetentionPolicyIssue, ...]:
        """Validate that all currently relevant roots resolve to a retention policy."""

        issues: list[RetentionPolicyIssue] = []
        for relative_root in self._relevant_roots(repo_root):
            try:
                self.policy_for_path(relative_root)
            except KeyError:
                issues.append(
                    RetentionPolicyIssue(
                        issue_code="unclassified_root",
                        root_path=relative_root,
                        message=(
                            "No retention policy covers repository path "
                            f"{relative_root}."
                        ),
                    )
                )
        return tuple(issues)

    def _relevant_roots(self, repo_root: Path) -> tuple[str, ...]:
        roots: set[str] = {
            self._workspace_paths.machine_root,
            self._workspace_paths.docs_root,
            "core/control_plane/ledgers/purges",
        }
        initiatives_root = repo_root / self._workspace_paths.initiatives_root
        if initiatives_root.exists():
            roots.update(
                path.relative_to(repo_root).as_posix()
                for path in initiatives_root.glob("*")
                if path.is_dir()
            )
        projects_root = repo_root / self._workspace_paths.projects_root
        if projects_root.exists():
            roots.update(
                path.relative_to(repo_root).as_posix()
                for path in projects_root.glob("*/initiatives/*")
                if path.is_dir()
            )
        return tuple(sorted(roots))


def _normalize_relative_path(relative_path: str) -> str:
    cleaned = relative_path.strip().strip("/")
    if cleaned in {"", "."}:
        return "."
    return cleaned


def _policy_matches(entry: RetentionPolicyEntry, relative_path: str) -> bool:
    normalized_pattern = _normalize_relative_path(entry.path_pattern)
    if entry.match_mode == "exact":
        if normalized_pattern == ".":
            return True
        return relative_path == normalized_pattern or relative_path.startswith(
            f"{normalized_pattern}/"
        )
    candidate = PurePosixPath(relative_path)
    while True:
        if candidate.match(entry.path_pattern):
            return True
        if candidate.parent == candidate:
            return False
        candidate = candidate.parent


def _specificity_key(entry: RetentionPolicyEntry) -> tuple[int, int]:
    wildcard_penalty = entry.path_pattern.count("*")
    return (len(entry.path_pattern) - wildcard_penalty, -wildcard_penalty)


__all__ = ["RetentionPolicyHelper", "RetentionPolicyIssue"]
