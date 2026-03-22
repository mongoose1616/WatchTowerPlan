"""Workspace, root-placement, and validation-suite checks for pack contracts."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

from watchtower_core.pack_integration.workspace_registration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    core_python_workspace_registration,
    load_core_python_workspace_state,
)
from watchtower_core.validation._pack_contract.manifest import expected_python_root
from watchtower_core.validation.models import ValidationIssue


def owned_root_issues(
    context: Any,
    runtime_manifest: Any,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    workspace_roots = context.workspace_roots
    owned_roots = runtime_manifest.owned_roots
    for field_name, expected, actual in (
        ("workspace_root", workspace_roots.workspace_root, owned_roots.workspace_root),
        ("machine_root", workspace_roots.machine_root, owned_roots.machine_root),
        ("docs_root", workspace_roots.docs_root, owned_roots.docs_root),
        ("workflows_root", workspace_roots.workflows_root, owned_roots.workflows_root),
        ("tracking_root", workspace_roots.tracking_root, owned_roots.tracking_root),
        (
            "python_root",
            expected_python_root(workspace_roots.workspace_root),
            owned_roots.python_root,
        ),
        ("initiatives_root", workspace_roots.initiatives_root, owned_roots.initiatives_root),
        ("projects_root", workspace_roots.projects_root, owned_roots.projects_root),
    ):
        if expected != actual:
            issues.append(
                ValidationIssue(
                    code=f"pack_owned_roots_{field_name}_mismatch",
                    message=(
                        f"Pack owned_roots field mismatch for {field_name}: {expected} != {actual}"
                    ),
                    location=actual,
                )
            )
        issues.extend(
            owned_root_location_issues(
                workspace_root=owned_roots.workspace_root,
                field_name=field_name,
                relative_path=actual,
                repo_root=context.loader.repo_root,
            )
        )
    expected_domain_roots, expected_domain_root_issues = merged_domain_roots(
        initiatives_root=workspace_roots.initiatives_root,
        projects_root=workspace_roots.projects_root,
        domain_roots=workspace_roots.domain_root_map(),
        location=context.pack_settings_path,
    )
    actual_domain_roots, actual_domain_root_issues = merged_domain_roots(
        initiatives_root=owned_roots.initiatives_root,
        projects_root=owned_roots.projects_root,
        domain_roots=owned_roots.domain_root_map(),
        location=context.loader.pack_runtime_manifest_path(context.pack_settings_path),
    )
    issues.extend(expected_domain_root_issues)
    issues.extend(actual_domain_root_issues)
    if expected_domain_roots != actual_domain_roots:
        issues.append(
            ValidationIssue(
                code="pack_domain_roots_mismatch",
                message=(
                    "Pack named domain roots must match between pack settings and the "
                    f"runtime manifest: {expected_domain_roots} != {actual_domain_roots}"
                ),
                location=context.pack_settings_path,
            )
        )
    for root_name, relative_path in actual_domain_roots.items():
        issues.extend(
            owned_root_location_issues(
                workspace_root=owned_roots.workspace_root,
                field_name=f"domain_roots.{root_name}",
                relative_path=relative_path,
                repo_root=context.loader.repo_root,
            )
        )
    return tuple(issues)


def core_python_workspace_issues(
    context: Any,
    runtime_manifest: Any,
) -> tuple[ValidationIssue, ...]:
    pyproject_path = context.loader.repo_root / CORE_PYPROJECT_RELATIVE_PATH
    if not pyproject_path.is_file():
        return (
            ValidationIssue(
                code="pack_core_python_pyproject_missing",
                message=(
                    "Hosted-pack validation requires the shared core/python/pyproject.toml "
                    "workspace file."
                ),
                location=CORE_PYPROJECT_RELATIVE_PATH,
            ),
        )
    try:
        workspace_state = load_core_python_workspace_state(pyproject_path)
    except Exception as exc:  # pragma: no cover - fail-closed config guard
        return (
            ValidationIssue(
                code="pack_core_python_pyproject_invalid",
                message=f"Could not parse shared core/python/pyproject.toml: {exc}",
                location=CORE_PYPROJECT_RELATIVE_PATH,
            ),
        )

    registration = core_python_workspace_registration(
        context.loader.repo_root,
        python_root=runtime_manifest.owned_roots.python_root,
        python_distribution=runtime_manifest.python_distribution,
    )
    issues: list[ValidationIssue] = []
    if registration.dependency not in set(workspace_state.dev_dependencies):
        issues.append(
            ValidationIssue(
                code="pack_workspace_dependency_missing",
                message=(
                    "Shared core/python optional dev dependencies are missing the hosted-pack "
                    f"distribution: {registration.dependency}"
                ),
                location=CORE_PYPROJECT_RELATIVE_PATH,
            )
        )
    uv_source = workspace_state.uv_source_map().get(registration.dependency)
    if uv_source is None:
        issues.append(
            ValidationIssue(
                code="pack_workspace_source_missing",
                message=(
                    "Shared core/python uv sources are missing the hosted-pack path source: "
                    f"{registration.dependency}"
                ),
                location=CORE_PYPROJECT_RELATIVE_PATH,
            )
        )
        return tuple(issues)
    if uv_source.get("path") != registration.uv_source_path:
        issues.append(
            ValidationIssue(
                code="pack_workspace_source_path_mismatch",
                message=(
                    "Shared core/python uv source path does not match the hosted-pack python "
                    f"root: {uv_source.get('path')} != {registration.uv_source_path}"
                ),
                location=CORE_PYPROJECT_RELATIVE_PATH,
            )
        )
    if bool(uv_source.get("editable", False)) is not registration.editable:
        issues.append(
            ValidationIssue(
                code="pack_workspace_source_editable_mismatch",
                message=(
                    "Shared core/python uv source editable flag must match the hosted-pack "
                    f"registration for {registration.dependency}."
                ),
                location=CORE_PYPROJECT_RELATIVE_PATH,
            )
        )
    return tuple(issues)


def owned_root_location_issues(
    *,
    workspace_root: str,
    field_name: str,
    relative_path: str | None,
    repo_root: Path,
) -> tuple[ValidationIssue, ...]:
    if not relative_path:
        return ()
    issues: list[ValidationIssue] = []
    issues.extend(
        repo_relative_path_issues(
            relative_path,
            code="pack_owned_root_not_repo_relative",
            message_prefix="Pack owned root must stay repository-relative and portable",
        )
    )
    if relative_path != workspace_root and not relative_path.startswith(f"{workspace_root}/"):
        issues.append(
            ValidationIssue(
                code="pack_owned_root_not_pack_local",
                message=(
                    "Pack owned root must stay under the pack workspace root: "
                    f"{field_name} -> {relative_path}"
                ),
                location=relative_path,
            )
        )
    if not (repo_root / relative_path).exists():
        issues.append(
            ValidationIssue(
                code="pack_owned_root_missing",
                message=f"Pack owned root is missing from the repository: {relative_path}",
                location=relative_path,
            )
        )
    return tuple(issues)


def surface_path_issues(
    context: Any,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    workspace_root = context.workspace_roots.workspace_root
    for declaration in context.pack_settings.surfaces:
        issues.extend(
            repo_relative_path_issues(
                declaration.path,
                code="pack_surface_path_not_repo_relative",
                message_prefix=(
                    "Pack settings surfaces must stay repository-relative and portable"
                ),
            )
        )
        if declaration.path.startswith("core/control_plane/"):
            continue
        if declaration.path == workspace_root or declaration.path.startswith(f"{workspace_root}/"):
            continue
        issues.append(
            ValidationIssue(
                code="pack_surface_not_pack_or_core_local",
                message=(
                    "Pack settings may only reference shared core control-plane surfaces "
                    f"or pack-local paths: {declaration.surface_name} -> {declaration.path}"
                ),
                location=declaration.path,
            )
        )
    return tuple(issues)


def validation_suite_issues(
    context: Any,
    runtime_manifest: Any,
) -> tuple[ValidationIssue, ...]:
    available_suite_ids = {suite.suite_id for suite in context.validation_suite_registry.suites}
    issues: list[ValidationIssue] = []
    for suite_id in runtime_manifest.required_validation_suite_ids:
        if suite_id in available_suite_ids:
            continue
        issues.append(
            ValidationIssue(
                code="pack_required_validation_suite_missing",
                message=(f"Pack runtime manifest declares a missing validation suite: {suite_id}"),
                location=context.pack_settings_path,
            )
        )
    return tuple(issues)


def merged_domain_roots(
    *,
    initiatives_root: str | None,
    projects_root: str | None,
    domain_roots: dict[str, str],
    location: str,
) -> tuple[dict[str, str], tuple[ValidationIssue, ...]]:
    merged = dict(domain_roots)
    issues: list[ValidationIssue] = []
    for legacy_name, legacy_value in (
        ("initiatives", initiatives_root),
        ("projects", projects_root),
    ):
        if legacy_value is None:
            continue
        existing = merged.get(legacy_name)
        if existing is not None and existing != legacy_value:
            issues.append(
                ValidationIssue(
                    code="pack_domain_root_legacy_mismatch",
                    message=(
                        "Legacy domain-root fields must match the named domain_roots map: "
                        f"{legacy_name} -> {existing} != {legacy_value}"
                    ),
                    location=location,
                )
            )
            continue
        merged[legacy_name] = legacy_value
    return merged, tuple(issues)


def repo_relative_path_issues(
    relative_path: str,
    *,
    code: str,
    message_prefix: str,
) -> tuple[ValidationIssue, ...]:
    path = PurePosixPath(relative_path)
    issues: list[ValidationIssue] = []
    if path.is_absolute():
        issues.append(
            ValidationIssue(
                code=code,
                message=f"{message_prefix}: absolute paths are not allowed ({relative_path})",
                location=relative_path,
            )
        )
    if ".." in path.parts:
        issues.append(
            ValidationIssue(
                code=code,
                message=f"{message_prefix}: parent traversal is not allowed ({relative_path})",
                location=relative_path,
            )
        )
    return tuple(issues)
