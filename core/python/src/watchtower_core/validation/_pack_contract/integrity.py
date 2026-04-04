"""Shared registry-integrity and validator-coverage checks for pack validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from watchtower_core.pack_integration.runtime_registry import load_pack_registry_runtime_view
from watchtower_core.validation.common import artifact_pattern_match_score
from watchtower_core.validation.models import ValidationIssue


def pack_registry_integrity_issues(loader: Any) -> tuple[ValidationIssue, ...]:
    """Return issues for authored shared pack-registry entries that do not resolve."""

    runtime_view = load_pack_registry_runtime_view(loader)
    issues: list[ValidationIssue] = [
        ValidationIssue(
            code="pack_registry_entry_unresolvable",
            message=message,
            location=entry.pack_settings_path,
        )
        for entry, message in runtime_view.invalid_entry_details
    ]

    repo_root: Path = loader.repo_root
    pack_registry = loader.load_pack_registry()
    for entry in pack_registry.packs:
        settings_file = repo_root / entry.pack_settings_path
        if not settings_file.exists():
            issues.append(
                ValidationIssue(
                    code="phantom_pack_entry",
                    message=(
                        f"Pack registry entry {entry.pack_slug!r} declares "
                        f"pack_settings_path={entry.pack_settings_path!r} "
                        "but the file does not exist on disk."
                    ),
                    location=entry.pack_settings_path,
                )
            )
        manifest_path = entry.pack_runtime_manifest_path
        if manifest_path and not (repo_root / manifest_path).exists():
            issues.append(
                ValidationIssue(
                    code="phantom_pack_entry",
                    message=(
                        f"Pack registry entry {entry.pack_slug!r} declares "
                        f"pack_runtime_manifest_path={manifest_path!r} "
                        "but the file does not exist on disk."
                    ),
                    location=manifest_path,
                )
            )
    return tuple(issues)


def validator_coverage_issues(context: Any) -> tuple[ValidationIssue, ...]:
    """Return issues for governed JSON artifacts that no active validator claims."""

    validator_registry = context.validator_registry
    artifact_validators = tuple(
        validator
        for validator in validator_registry.validators
        if validator.status == "active"
        and validator.engine == "json_schema"
        and validator.artifact_kind != "documentation_front_matter"
    )
    if not artifact_validators:
        return (
            ValidationIssue(
                code="validator_coverage_missing",
                message="Active validation context does not declare any schema-backed validators.",
                location=context.pack_settings_path,
            ),
        )

    uncovered_paths = tuple(
        relative_path
        for relative_path in _governed_artifact_candidate_paths(context)
        if not any(
            artifact_pattern_match_score(relative_path, pattern) is not None
            for validator in artifact_validators
            for pattern in validator.applies_to
        )
    )
    if not uncovered_paths:
        return ()

    issues: list[ValidationIssue] = []
    for relative_path in uncovered_paths:
        issues.append(
            ValidationIssue(
                code="validator_coverage_missing",
                message=(
                    "No active schema-backed validator claims this governed artifact path. "
                    "Add or restore a validator-registry applies_to pattern that covers "
                    f"{relative_path}."
                ),
                location=relative_path,
            )
        )
    return tuple(issues)


def _governed_artifact_candidate_paths(context: Any) -> tuple[str, ...]:
    loader = context.loader
    workspace_roots = context.workspace_roots
    repo_root = loader.repo_root
    machine_root = workspace_roots.machine_root
    candidate_roots = ["core/control_plane"]
    if machine_root != "core/control_plane":
        candidate_roots.append(machine_root)

    ordered_paths: list[str] = []
    seen_paths: set[str] = set()
    for relative_root in candidate_roots:
        root = repo_root / relative_root
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.json")):
            relative_path = path.relative_to(repo_root).as_posix()
            if relative_path in seen_paths:
                continue
            if _exclude_from_coverage(relative_path, machine_root=machine_root):
                continue
            seen_paths.add(relative_path)
            ordered_paths.append(relative_path)
    return tuple(ordered_paths)


def _exclude_from_coverage(relative_path: str, *, machine_root: str) -> bool:
    path = Path(relative_path)
    if path.name.endswith(".schema.json"):
        return True
    if "/examples/" in relative_path:
        return True
    if machine_root != "core/control_plane" and relative_path.startswith(f"{machine_root}/"):
        for suffix in ("indexes/", "manifests/", "runtime/", "schemas/"):
            if relative_path.startswith(f"{machine_root}/{suffix}"):
                return True
        for filename in ("schema_catalog.json", "validator_registry.json"):
            if relative_path.endswith(f"/{filename}"):
                return True
    return False


__all__ = [
    "pack_registry_integrity_issues",
    "validator_coverage_issues",
]
