"""Generic pack-validation target enumeration helpers."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ValidationSuiteStepDefinition
from watchtower_core.validation.common import artifact_pattern_match_score
from watchtower_core.validation.context import PackValidationContext

_STEP_TARGET_BUILDERS: dict[
    str,
    Callable[[PackValidationContext], tuple[str, ...]],
] = {}
_EXCLUDED_MARKDOWN_TARGET_NAMES = {"README.md", "AGENTS.md"}


def resolve_pack_validation_suite_targets(
    context: PackValidationContext,
    step: ValidationSuiteStepDefinition,
) -> tuple[str, ...] | None:
    """Return target lists for one pack-declared validation suite step."""

    builder = _STEP_TARGET_BUILDERS.get(step.step_kind)
    if builder is None:
        return None
    return builder(context)


def front_matter_targets(context: PackValidationContext) -> tuple[str, ...]:
    """Return Markdown front-matter validation targets for the active pack."""

    return _targets_for_validators(
        context.loader,
        engine="json_schema",
        artifact_kind="documentation_front_matter",
        default_extension=".md",
        exclude_workflow_targets=True,
    )


def document_semantics_targets(context: PackValidationContext) -> tuple[str, ...]:
    """Return document-semantics validation targets for the active pack."""

    return _targets_for_validators(
        context.loader,
        engine="python",
        artifact_kind="documentation_semantics",
        default_extension=".md",
    )


def artifact_targets(context: PackValidationContext) -> tuple[str, ...]:
    """Return schema-backed artifact validation targets for the active pack."""

    registry = context.validator_registry
    ordered_paths: list[str] = []
    seen: set[str] = set()
    for validator in registry.validators:
        if validator.status != "active":
            continue
        if validator.engine != "json_schema":
            continue
        if validator.artifact_kind == "documentation_front_matter":
            continue
        for pattern in validator.applies_to:
            for relative_path in _paths_for_pattern(
                context.loader,
                pattern,
                default_extension=".json",
            ):
                if artifact_pattern_match_score(relative_path, pattern) is None:
                    continue
                if relative_path in seen:
                    continue
                seen.add(relative_path)
                ordered_paths.append(relative_path)
    return tuple(ordered_paths)


def _paths_for_pattern(
    loader: ControlPlaneLoader,
    pattern: str,
    *,
    default_extension: str,
) -> tuple[str, ...]:
    if pattern.endswith("/**"):
        suffix = Path(pattern.removesuffix("/**")).suffix.casefold()
        extension = suffix or default_extension
        relative_root = pattern.removesuffix("/**")
        root = loader.resolve_path(relative_root)
        if not root.exists():
            return ()
        return tuple(
            loader.workspace_config.logical_path_for(path)
            for path in sorted(root.rglob(f"*{extension}"))
            if path.is_file()
        )
    if any(token in pattern for token in "*?[]"):
        candidate_paths = sorted(loader.repo_root.glob(pattern))
        return tuple(
            loader.workspace_config.logical_path_for(path)
            for path in candidate_paths
            if path.is_file() and (not default_extension or path.suffix == default_extension)
        )
    if pattern.endswith(".json") or pattern.endswith(".md"):
        path = loader.resolve_path(pattern)
        if path.exists():
            return (pattern,)
        return ()
    return ()


def _targets_for_validators(
    loader: ControlPlaneLoader,
    *,
    engine: str,
    artifact_kind: str,
    default_extension: str,
    exclude_workflow_targets: bool = False,
) -> tuple[str, ...]:
    ordered_paths: list[str] = []
    seen: set[str] = set()
    for validator in loader.load_validator_registry().validators:
        if validator.status != "active":
            continue
        if validator.engine != engine:
            continue
        if validator.artifact_kind != artifact_kind:
            continue
        for pattern in validator.applies_to:
            for relative_path in _paths_for_pattern(
                loader,
                pattern,
                default_extension=default_extension,
            ):
                if not _include_validation_target(
                    relative_path,
                    exclude_workflow_targets=exclude_workflow_targets,
                ):
                    continue
                if relative_path in seen:
                    continue
                seen.add(relative_path)
                ordered_paths.append(relative_path)
    return tuple(ordered_paths)


def _include_validation_target(
    relative_path: str,
    *,
    exclude_workflow_targets: bool = False,
) -> bool:
    path = Path(relative_path)
    if path.name in _EXCLUDED_MARKDOWN_TARGET_NAMES:
        return False
    if "workflows" in path.parts and "modules" not in path.parts:
        return False
    if exclude_workflow_targets and "workflows" in path.parts:
        return False
    return True


_STEP_TARGET_BUILDERS = {
    "front_matter": front_matter_targets,
    "document_semantics": document_semantics_targets,
    "artifact": artifact_targets,
}


__all__ = [
    "artifact_targets",
    "document_semantics_targets",
    "front_matter_targets",
    "resolve_pack_validation_suite_targets",
]
