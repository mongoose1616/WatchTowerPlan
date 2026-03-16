"""Repo-local filename policy validation for governed control-plane JSON files."""

from __future__ import annotations

import re
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation.common import resolve_target_path
from watchtower_core.validation.models import ValidationIssue, ValidationResult

CONTROL_PLANE_PREFIX = "core/control_plane/"
SCHEMA_PREFIX = "core/control_plane/schemas/"
EXAMPLE_PREFIX = "core/control_plane/examples/"
VERSION_TOKEN_PATTERN = re.compile(r"\.v[0-9]+(?=(?:\.[a-z0-9_]+)?\.json$)")


class GovernedFilenameValidationService:
    """Validate repo-local filename policy for governed control-plane JSON files."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def iter_targets(self) -> tuple[str, ...]:
        """Return every governed JSON file under the control-plane tree."""
        root = self._loader.workspace_config.control_plane_root
        return tuple(
            self._loader.workspace_config.logical_path_for(path)
            for path in sorted(root.rglob("*.json"))
        )

    def validate(self, path: str | Path) -> ValidationResult:
        """Validate one governed JSON file against the filename policy."""
        resolved_path, target_path, relative_target_path = resolve_target_path(self._loader, path)
        issues = tuple(self._iter_issues(resolved_path, relative_target_path))
        return ValidationResult(
            validator_id="validator.repo.governed_filename_policy",
            target_path=relative_target_path or target_path,
            engine="repo_policy",
            schema_ids=(),
            passed=not issues,
            issues=issues,
        )

    def _iter_issues(
        self,
        path: Path,
        relative_target_path: str | None,
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        basename = path.name

        if relative_target_path is None or not relative_target_path.startswith(
            CONTROL_PLANE_PREFIX
        ):
            return issues

        if VERSION_TOKEN_PATTERN.search(basename) is not None:
            issues.append(
                ValidationIssue(
                    code="governed_filename_version_token_forbidden",
                    message=(
                        "Governed filenames must not embed major-version tokens such "
                        "as `.v1`; keep compatibility signaling inside artifact content."
                    ),
                    location=basename,
                )
            )

        if relative_target_path.startswith(SCHEMA_PREFIX) and not basename.endswith(".schema.json"):
            issues.append(
                ValidationIssue(
                    code="schema_filename_suffix_invalid",
                    message="Published schema filenames must end with `.schema.json`.",
                    location=basename,
                )
            )

        if relative_target_path.startswith(EXAMPLE_PREFIX) and not basename.endswith(
            ".example.json"
        ):
            issues.append(
                ValidationIssue(
                    code="example_filename_suffix_invalid",
                    message="Published example filenames must end with `.example.json`.",
                    location=basename,
                )
            )

        return issues
