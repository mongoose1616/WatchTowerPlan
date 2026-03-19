"""WatchTowerPlan-specific validation target enumeration."""

from __future__ import annotations

from collections.abc import Callable

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ValidationSuiteStepDefinition
from watchtower_core.plan_runtime.planning_documents import iter_markdown_documents
from watchtower_core.plan_runtime.sync.foundation_index import (
    FOUNDATION_DOC_ROOT,
    FOUNDATION_EXCLUDED_NAMES,
)
from watchtower_core.plan_runtime.sync.reference_index import (
    REFERENCE_DOC_ROOT,
    REFERENCE_EXCLUDED_NAMES,
)
from watchtower_core.plan_runtime.sync.standard_index import STANDARD_DOC_ROOT, STANDARD_EXCLUDED_NAMES
from watchtower_core.plan_runtime.sync.workflow_index import WORKFLOW_DOC_ROOTS, WORKFLOW_EXCLUDED_NAMES
from watchtower_core.validation.context import PackValidationContext

WATCHTOWER_PLAN_VALIDATION_SUITE_ID = "suite.watchtower_plan.validation_baseline"
_WATCHTOWER_PLAN_PACK_ID = "pack.watchtower_plan"
_STEP_TARGET_BUILDERS: dict[str, Callable[[ControlPlaneLoader], tuple[str, ...]]] = {}


def resolve_watchtower_plan_suite_targets(
    context: PackValidationContext,
    step: ValidationSuiteStepDefinition,
) -> tuple[str, ...] | None:
    """Return repo-native target lists for the WatchTowerPlan validation baseline."""

    if context.pack_settings.pack_id != _WATCHTOWER_PLAN_PACK_ID:
        return None
    builder = _STEP_TARGET_BUILDERS.get(step.step_id)
    if builder is None:
        return None
    return builder(context.loader)


def front_matter_targets(loader: ControlPlaneLoader) -> tuple[str, ...]:
    """Return repo-native front-matter validation targets."""

    repo_root = loader.repo_root
    standards_root = repo_root / STANDARD_DOC_ROOT
    standards = tuple(
        path.relative_to(repo_root).as_posix()
        for path in sorted(standards_root.rglob("*.md"))
        if path.name not in STANDARD_EXCLUDED_NAMES
    )
    return (
        *iter_markdown_documents(
            repo_root,
            REFERENCE_DOC_ROOT,
            excluded_names=REFERENCE_EXCLUDED_NAMES,
        ),
        *iter_markdown_documents(
            repo_root,
            FOUNDATION_DOC_ROOT,
            excluded_names=FOUNDATION_EXCLUDED_NAMES,
        ),
        *standards,
    )


def document_semantics_targets(loader: ControlPlaneLoader) -> tuple[str, ...]:
    """Return repo-native document-semantics validation targets."""

    repo_root = loader.repo_root
    standards_root = repo_root / STANDARD_DOC_ROOT
    standards = tuple(
        path.relative_to(repo_root).as_posix()
        for path in sorted(standards_root.rglob("*.md"))
        if path.name not in STANDARD_EXCLUDED_NAMES
    )
    workflows = tuple(
        path.relative_to(repo_root).as_posix()
        for workflow_root in WORKFLOW_DOC_ROOTS
        for path in sorted((repo_root / workflow_root).glob("*.md"))
        if path.name not in WORKFLOW_EXCLUDED_NAMES
    )
    return (
        *iter_markdown_documents(
            repo_root,
            REFERENCE_DOC_ROOT,
            excluded_names=REFERENCE_EXCLUDED_NAMES,
        ),
        *iter_markdown_documents(
            repo_root,
            FOUNDATION_DOC_ROOT,
            excluded_names=FOUNDATION_EXCLUDED_NAMES,
        ),
        *standards,
        *workflows,
    )


def artifact_targets(loader: ControlPlaneLoader) -> tuple[str, ...]:
    """Return repo-native schema-backed artifact validation targets."""

    registry = loader.load_validator_registry()
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
            for relative_path in _artifact_paths_for_pattern(loader, pattern):
                if relative_path in seen:
                    continue
                seen.add(relative_path)
                ordered_paths.append(relative_path)
    return tuple(ordered_paths)


def _artifact_paths_for_pattern(
    loader: ControlPlaneLoader,
    pattern: str,
) -> tuple[str, ...]:
    if pattern.endswith("/**"):
        relative_root = pattern.removesuffix("/**")
        return tuple(
            loader.workspace_config.logical_path_for(path)
            for path in sorted(loader.resolve_path(relative_root).glob("*.json"))
        )
    if pattern.endswith(".json"):
        path = loader.resolve_path(pattern)
        if path.exists():
            return (pattern,)
        return ()
    return ()
_STEP_TARGET_BUILDERS = {
    "step.watchtower_plan.front_matter": front_matter_targets,
    "step.watchtower_plan.document_semantics": document_semantics_targets,
    "step.watchtower_plan.artifacts": artifact_targets,
}

__all__ = [
    "WATCHTOWER_PLAN_VALIDATION_SUITE_ID",
    "artifact_targets",
    "document_semantics_targets",
    "front_matter_targets",
    "resolve_watchtower_plan_suite_targets",
]
