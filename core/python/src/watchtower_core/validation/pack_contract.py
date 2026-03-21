"""Pack-contract validation services."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.errors import ControlPlaneError
from watchtower_core.control_plane.loader import (
    PACK_REGISTRY_PATH,
    PACK_SETTINGS_PATH,
    ControlPlaneLoader,
)
from watchtower_core.pack_integration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    REQUIRED_PACK_CAPABILITIES,
    SUPPORTED_PACK_CAPABILITIES,
    PackIntegration,
    core_python_workspace_registration,
    load_core_python_workspace_state,
    pack_command_entry_doc_path,
)
from watchtower_core.pack_integration.runtime import (
    validate_pack_query_runtime,
    validate_pack_sync_runtime,
    validate_pack_validation_runtime,
)
from watchtower_core.validation.context import PackValidationContext
from watchtower_core.validation.models import ValidationIssue, ValidationResult

PACK_CONTRACT_VALIDATOR_ID = "validator.pack.contract"
CORE_PACKAGE_RELATIVE_PATH = Path("core/python/src/watchtower_core")
HOST_PACKAGE_RELATIVE_PATH = Path("core/python/src/watchtower_host")


class PackContractValidationService:
    """Validate that a pack publishes the governed surfaces core expects."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, pack_settings_path: str = PACK_SETTINGS_PATH) -> ValidationResult:
        """Validate one pack settings surface and its declared validation context."""

        issues: list[ValidationIssue] = []
        try:
            context = PackValidationContext.from_loader(
                self._loader,
                pack_settings_path=pack_settings_path,
            )
            pack_registry = context.loader.load_pack_registry()
            registry_entry = pack_registry.get_by_pack_id(context.pack_settings.pack_id)
            runtime_manifest = context.loader.load_pack_runtime_manifest(
                pack_settings_path=context.pack_settings_path
            )
        except (ControlPlaneError, ValueError) as exc:
            return ValidationResult(
                validator_id=PACK_CONTRACT_VALIDATOR_ID,
                target_path=pack_settings_path,
                engine="python",
                schema_ids=(),
                passed=False,
                issues=(
                    ValidationIssue(
                        code="pack_contract_invalid",
                        message=str(exc),
                        location=pack_settings_path,
                    ),
                ),
            )

        if registry_entry.pack_settings_path != context.pack_settings_path:
            issues.append(
                ValidationIssue(
                    code="pack_registry_settings_path_mismatch",
                    message=(
                        "Pack registry entry does not match the active pack settings path: "
                        f"{registry_entry.pack_settings_path} != {context.pack_settings_path}"
                    ),
                    location=context.pack_settings_path,
                )
            )
        effective_runtime_manifest_path = context.loader.pack_runtime_manifest_path(
            context.pack_settings_path
        )
        if registry_entry.pack_runtime_manifest_path != effective_runtime_manifest_path:
            issues.append(
                ValidationIssue(
                    code="pack_registry_runtime_manifest_path_mismatch",
                    message=(
                        "Pack registry entry does not match the active runtime manifest path: "
                        f"{registry_entry.pack_runtime_manifest_path} "
                        f"!= {effective_runtime_manifest_path}"
                    ),
                    location=effective_runtime_manifest_path,
                )
            )

        issues.extend(
            _matching_field_issues(
                pack_id=context.pack_settings.pack_id,
                registry_pack_id=registry_entry.pack_id,
                manifest_pack_id=runtime_manifest.pack_id,
                pack_slug=registry_entry.pack_slug,
                manifest_pack_slug=runtime_manifest.pack_slug,
                command_namespace=registry_entry.command_namespace,
                manifest_command_namespace=runtime_manifest.command_namespace,
                python_distribution=registry_entry.python_distribution,
                manifest_python_distribution=runtime_manifest.python_distribution,
                python_package=registry_entry.python_package,
                manifest_python_package=runtime_manifest.python_package,
            )
        )
        issues.extend(_registry_collision_issues(pack_registry, registry_entry))
        issues.extend(_manifest_path_issues(context, runtime_manifest))
        issues.extend(_owned_root_issues(context, runtime_manifest))
        issues.extend(_surface_path_issues(context))
        issues.extend(_command_doc_issues(context, runtime_manifest))
        issues.extend(_core_python_workspace_issues(context, runtime_manifest))
        issues.extend(_validation_suite_issues(context, runtime_manifest))
        issues.extend(_integration_issues(runtime_manifest))
        issues.extend(_dependency_boundary_issues(context, runtime_manifest))

        return ValidationResult(
            validator_id=PACK_CONTRACT_VALIDATOR_ID,
            target_path=pack_settings_path,
            engine="python",
            schema_ids=(),
            passed=not issues,
            issues=tuple(issues),
        )


def _matching_field_issues(
    *,
    pack_id: str,
    registry_pack_id: str,
    manifest_pack_id: str,
    pack_slug: str,
    manifest_pack_slug: str,
    command_namespace: str,
    manifest_command_namespace: str,
    python_distribution: str,
    manifest_python_distribution: str,
    python_package: str,
    manifest_python_package: str,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for field_name, left, right in (
        ("pack_id", pack_id, registry_pack_id),
        ("pack_id", pack_id, manifest_pack_id),
        ("pack_slug", pack_slug, manifest_pack_slug),
        ("command_namespace", command_namespace, manifest_command_namespace),
        ("python_distribution", python_distribution, manifest_python_distribution),
        ("python_package", python_package, manifest_python_package),
    ):
        if left == right:
            continue
        issues.append(
            ValidationIssue(
                code=f"pack_contract_{field_name}_mismatch",
                message=f"Pack contract field mismatch for {field_name}: {left} != {right}",
            )
        )
    return tuple(issues)


def _registry_collision_issues(
    pack_registry,
    registry_entry,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    conflicting_entries = tuple(
        entry
        for entry in pack_registry.packs
        if entry.command_namespace == registry_entry.command_namespace
    )
    if len(conflicting_entries) > 1:
        conflicting_pack_slugs = ", ".join(
            sorted(entry.pack_slug for entry in conflicting_entries)
        )
        issues.append(
            ValidationIssue(
                code="pack_registry_command_namespace_conflict",
                message=(
                    "Hosted-pack command namespaces must be unique across the pack registry: "
                    f"{registry_entry.command_namespace} is shared by {conflicting_pack_slugs}"
                ),
                location=PACK_REGISTRY_PATH,
            )
        )
    return tuple(issues)


def _owned_root_issues(
    context: PackValidationContext,
    runtime_manifest,
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
            _expected_python_root(workspace_roots.workspace_root),
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
            _owned_root_location_issues(
                workspace_root=owned_roots.workspace_root,
                field_name=field_name,
                relative_path=actual,
                repo_root=context.loader.repo_root,
            )
        )
    expected_domain_roots, expected_domain_root_issues = _merged_domain_roots(
        initiatives_root=workspace_roots.initiatives_root,
        projects_root=workspace_roots.projects_root,
        domain_roots=workspace_roots.domain_root_map(),
        location=context.pack_settings_path,
    )
    actual_domain_roots, actual_domain_root_issues = _merged_domain_roots(
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
            _owned_root_location_issues(
                workspace_root=owned_roots.workspace_root,
                field_name=f"domain_roots.{root_name}",
                relative_path=relative_path,
                repo_root=context.loader.repo_root,
            )
        )
    return tuple(issues)


def _command_doc_issues(
    context: PackValidationContext,
    runtime_manifest,
) -> tuple[ValidationIssue, ...]:
    command_doc_path = pack_command_entry_doc_path(
        command_namespace=runtime_manifest.command_namespace,
        docs_root=runtime_manifest.owned_roots.docs_root,
    )
    if context.loader.resolve_path(command_doc_path).is_file():
        return ()
    return (
        ValidationIssue(
            code="pack_command_doc_missing",
            message=(
                "Pack contract is missing the pack-owned namespace command page: "
                f"{command_doc_path}"
            ),
            location=command_doc_path,
        ),
    )


def _core_python_workspace_issues(
    context: PackValidationContext,
    runtime_manifest,
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


def _expected_python_root(workspace_root: str) -> str:
    return f"{workspace_root}/python"


def _expected_manifest_path(machine_root: str, filename: str) -> str:
    return f"{machine_root}/manifests/{filename}"


def _manifest_path_issues(
    context: PackValidationContext,
    runtime_manifest,
) -> tuple[ValidationIssue, ...]:
    expected_pack_settings_path = _expected_manifest_path(
        context.workspace_roots.machine_root,
        "pack_settings.json",
    )
    expected_runtime_manifest_path = _expected_manifest_path(
        runtime_manifest.owned_roots.machine_root,
        "pack_runtime_manifest.json",
    )
    issues: list[ValidationIssue] = []
    if context.pack_settings_path != expected_pack_settings_path:
        issues.append(
            ValidationIssue(
                code="pack_settings_path_not_under_machine_root",
                message=(
                    "Pack settings must live directly under the declared machine-root "
                    f"manifest directory: {context.pack_settings_path} != "
                    f"{expected_pack_settings_path}"
                ),
                location=context.pack_settings_path,
            )
        )
    actual_runtime_manifest_path = context.loader.pack_runtime_manifest_path(
        context.pack_settings_path
    )
    if actual_runtime_manifest_path != expected_runtime_manifest_path:
        issues.append(
            ValidationIssue(
                code="pack_runtime_manifest_path_not_under_machine_root",
                message=(
                    "Pack runtime manifest must live directly under the declared "
                    f"machine-root manifest directory: {actual_runtime_manifest_path} "
                    f"!= {expected_runtime_manifest_path}"
                ),
                location=actual_runtime_manifest_path,
            )
        )
    return tuple(issues)


def _owned_root_location_issues(
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
        _repo_relative_path_issues(
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


def _surface_path_issues(
    context: PackValidationContext,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    workspace_root = context.workspace_roots.workspace_root
    for declaration in context.pack_settings.surfaces:
        issues.extend(
            _repo_relative_path_issues(
                declaration.path,
                code="pack_surface_path_not_repo_relative",
                message_prefix=(
                    "Pack settings surfaces must stay repository-relative and portable"
                ),
            )
        )
        if declaration.path.startswith("core/control_plane/"):
            continue
        if declaration.path == workspace_root or declaration.path.startswith(
            f"{workspace_root}/"
        ):
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


def _validation_suite_issues(
    context: PackValidationContext,
    runtime_manifest,
) -> tuple[ValidationIssue, ...]:
    available_suite_ids = {
        suite.suite_id for suite in context.validation_suite_registry.suites
    }
    issues: list[ValidationIssue] = []
    for suite_id in runtime_manifest.required_validation_suite_ids:
        if suite_id in available_suite_ids:
            continue
        issues.append(
            ValidationIssue(
                code="pack_required_validation_suite_missing",
                message=(
                    "Pack runtime manifest declares a missing validation suite: "
                    f"{suite_id}"
                ),
                location=context.pack_settings_path,
            )
        )
    return tuple(issues)


def _integration_issues(runtime_manifest) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    if runtime_manifest.integration_module != runtime_manifest.python_package and not (
        runtime_manifest.integration_module.startswith(f"{runtime_manifest.python_package}.")
    ):
        issues.append(
            ValidationIssue(
                code="pack_integration_module_not_pack_local",
                message=(
                    "Pack runtime manifest integration_module must stay inside the "
                    "declared pack python package."
                ),
                location=runtime_manifest.integration_module,
            )
        )
    unsupported_capabilities = set(runtime_manifest.declared_capabilities).difference(
        SUPPORTED_PACK_CAPABILITIES
    )
    if unsupported_capabilities:
        issues.append(
            ValidationIssue(
                code="pack_capability_unsupported",
                message=(
                    "Pack runtime manifest declares unsupported capabilities: "
                    + ", ".join(sorted(unsupported_capabilities))
                ),
            )
        )
        return tuple(issues)

    missing_required_capabilities = set(REQUIRED_PACK_CAPABILITIES).difference(
        runtime_manifest.declared_capabilities
    )
    if missing_required_capabilities:
        issues.append(
            ValidationIssue(
                code="pack_required_capability_missing",
                message=(
                    "Pack runtime manifest is missing required capabilities: "
                    + ", ".join(sorted(missing_required_capabilities))
                ),
            )
        )
    try:
        module = importlib.import_module(runtime_manifest.integration_module)
    except ModuleNotFoundError:
        return (
            *issues,
            ValidationIssue(
                code="pack_integration_module_missing",
                message=(
                    "Pack runtime manifest integration module is not importable: "
                    f"{runtime_manifest.integration_module}"
                ),
                location=runtime_manifest.integration_module,
            ),
        )

    descriptor = getattr(module, "PACK_INTEGRATION", None)
    if not isinstance(descriptor, PackIntegration):
        return (
            *issues,
            ValidationIssue(
                code="pack_integration_descriptor_missing",
                message=(
                    "Pack integration module must export PACK_INTEGRATION as a "
                    "watchtower_core.pack_integration.PackIntegration instance."
                ),
                location=runtime_manifest.integration_module,
            ),
        )

    for field_name, expected, actual in (
        ("pack_id", runtime_manifest.pack_id, descriptor.pack_id),
        ("pack_slug", runtime_manifest.pack_slug, descriptor.pack_slug),
        ("command_namespace", runtime_manifest.command_namespace, descriptor.command_namespace),
        ("python_package", runtime_manifest.python_package, descriptor.python_package),
    ):
        if expected == actual:
            continue
        issues.append(
            ValidationIssue(
                code=f"pack_integration_{field_name}_mismatch",
                message=(
                    "Pack integration descriptor mismatch for "
                    f"{field_name}: {expected} != {actual}"
                ),
                location=runtime_manifest.integration_module,
            )
        )

    descriptor_capabilities = set(descriptor.declared_capabilities)
    manifest_capabilities = set(runtime_manifest.declared_capabilities)
    if descriptor_capabilities != manifest_capabilities:
        issues.append(
            ValidationIssue(
                code="pack_integration_capability_mismatch",
                message=(
                    "Pack integration descriptor capabilities do not match the runtime manifest."
                ),
                location=runtime_manifest.integration_module,
            )
        )

    for capability in runtime_manifest.declared_capabilities:
        hook = descriptor.hook_for_capability(capability)
        if hook is None:
            issues.append(
                ValidationIssue(
                    code="pack_integration_hook_missing",
                    message=f"Pack integration descriptor is missing the {capability} hook.",
                    location=runtime_manifest.integration_module,
                )
            )
            continue
        if capability == "validation_provider":
            issues.extend(
                _runtime_hook_issues(
                    hook=hook,
                    integration_module=runtime_manifest.integration_module,
                    validator=validate_pack_validation_runtime,
                    error_code="pack_validation_provider_error",
                    invalid_code="pack_validation_provider_invalid",
                    invalid_message=(
                        "Pack validation_provider hook must return "
                        "watchtower_core.pack_integration.PackValidationRuntime."
                    ),
                )
            )
            continue
        if capability == "query_runtime":
            issues.extend(
                _runtime_hook_issues(
                    hook=hook,
                    integration_module=runtime_manifest.integration_module,
                    validator=validate_pack_query_runtime,
                    error_code="pack_query_runtime_error",
                    invalid_code="pack_query_runtime_invalid",
                    invalid_message=(
                        "Pack query_runtime hook must return "
                        "watchtower_core.pack_integration.PackQueryRuntime."
                    ),
                )
            )
            continue
        if capability == "sync_targets":
            issues.extend(
                _runtime_hook_issues(
                    hook=hook,
                    integration_module=runtime_manifest.integration_module,
                    validator=validate_pack_sync_runtime,
                    error_code="pack_sync_runtime_error",
                    invalid_code="pack_sync_runtime_invalid",
                    invalid_message=(
                        "Pack sync_targets hook must return "
                        "watchtower_core.pack_integration.PackSyncRuntime."
                    ),
                )
            )
            continue

    return tuple(issues)


def _runtime_hook_issues(
    *,
    hook,
    integration_module: str,
    validator,
    error_code: str,
    invalid_code: str,
    invalid_message: str,
) -> tuple[ValidationIssue, ...]:
    try:
        runtime = hook()
    except Exception as exc:  # pragma: no cover - fail-closed guard
        return (
            ValidationIssue(
                code=error_code,
                message=f"Pack integration hook raised an error: {exc}",
                location=integration_module,
            ),
        )
    try:
        validator(runtime, integration_module=integration_module)
        return ()
    except ValueError:
        pass
    return (
        ValidationIssue(
            code=invalid_code,
            message=invalid_message,
            location=integration_module,
        ),
    )


def _dependency_boundary_issues(
    context: PackValidationContext,
    runtime_manifest,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    repo_root = context.loader.repo_root
    core_package_root = repo_root / CORE_PACKAGE_RELATIVE_PATH
    pack_package_root = (
        repo_root
        / runtime_manifest.owned_roots.python_root
        / "src"
        / Path(*runtime_manifest.python_package.split("."))
    )
    if core_package_root.is_dir():
        issues.extend(
            _forbidden_import_issues(
                package_root=core_package_root,
                forbidden_prefixes=(runtime_manifest.python_package,),
                code="pack_boundary_core_imports_pack",
                message_prefix="Reusable core may not import pack runtime modules",
            )
        )
        issues.extend(
            _forbidden_import_issues(
                package_root=core_package_root,
                forbidden_prefixes=("watchtower_host",),
                code="pack_boundary_core_imports_host",
                message_prefix="Reusable core may not import host composition modules",
                exempt_path_suffixes=("watchtower_core/cli/main.py",),
            )
        )
        issues.extend(_sys_path_mutation_issues(core_package_root))
    if pack_package_root.is_dir():
        issues.extend(
            _forbidden_import_issues(
                package_root=pack_package_root,
                forbidden_prefixes=("watchtower_host",),
                code="pack_boundary_pack_imports_host",
                message_prefix="Pack runtime may not import host composition modules",
            )
        )
    return tuple(issues)


def _forbidden_import_issues(
    *,
    package_root: Path,
    forbidden_prefixes: tuple[str, ...],
    code: str,
    message_prefix: str,
    exempt_path_suffixes: tuple[str, ...] = (),
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for path in sorted(package_root.rglob("*.py")):
        if any(path.as_posix().endswith(suffix) for suffix in exempt_path_suffixes):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            issues.append(
                ValidationIssue(
                    code="pack_boundary_scan_failed",
                    message=f"Could not parse Python module during boundary scan: {exc}",
                    location=path.as_posix(),
                )
            )
            continue
        for module_name in _iter_import_modules(tree):
            if not _module_matches_forbidden_prefix(
                module_name=module_name,
                forbidden_prefixes=forbidden_prefixes,
            ):
                continue
            issues.append(
                ValidationIssue(
                    code=code,
                    message=f"{message_prefix}: {module_name}",
                    location=path.as_posix(),
                )
            )
    return tuple(issues)


def _sys_path_mutation_issues(package_root: Path) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for path in sorted(package_root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            issues.append(
                ValidationIssue(
                    code="pack_boundary_scan_failed",
                    message=f"Could not parse Python module during boundary scan: {exc}",
                    location=path.as_posix(),
                )
            )
            continue
        if not _tree_mutates_sys_path(tree):
            continue
        issues.append(
            ValidationIssue(
                code="pack_boundary_core_mutates_sys_path",
                message=(
                    "Reusable core may not mutate sys.path while validating or composing "
                    "pack runtime."
                ),
                location=path.as_posix(),
            )
        )
    return tuple(issues)


def _tree_mutates_sys_path(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if func.attr not in {"append", "extend", "insert", "pop", "remove"}:
            continue
        if isinstance(func.value, ast.Attribute) and func.value.attr == "path":
            if isinstance(func.value.value, ast.Name) and func.value.value.id == "sys":
                return True
    return False


def _iter_import_modules(tree: ast.AST) -> tuple[str, ...]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules.append(node.module)
    return tuple(modules)


def _module_matches_forbidden_prefix(
    *,
    module_name: str,
    forbidden_prefixes: tuple[str, ...],
) -> bool:
    return any(
        module_name == prefix or module_name.startswith(f"{prefix}.")
        for prefix in forbidden_prefixes
    )


def _merged_domain_roots(
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


def _repo_relative_path_issues(
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
