"""Portable staged export helpers for shared core plus selected hosted packs."""

from __future__ import annotations

import filecmp
import json
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import PACK_REGISTRY_PATH, ControlPlaneLoader
from watchtower_core.pack_integration.bootstrap import (
    PackBootstrapRequest,
    bootstrap_hosted_pack,
    rebuild_shared_discovery_surfaces,
)
from watchtower_core.pack_integration.runtime import load_active_pack_integration
from watchtower_core.pack_integration.workspace_registration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    CORE_UV_LOCK_RELATIVE_PATH,
    reconcile_core_python_workspace_pyproject,
)
from watchtower_core.sync.foundation_index import FoundationIndexSyncService
from watchtower_core.validation.models import ValidationIssue, ValidationResult
from watchtower_core.validation.pack_contract import PackContractValidationService
from watchtower_core.validation.portability import (
    ENGINEERING_CORE_EXTRACT_SCOPE,
    PortabilityValidationService,
    acceptance_contract_is_shared_core_portable,
    traceability_entry_is_repository_export_portable,
    traceability_entry_is_shared_core_portable,
    traceability_entry_requires_nonportable_acceptance_lineage,
    validation_evidence_artifact_is_shared_core_portable,
)

_PORTABLE_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    ".gitignore",
    "LICENSE",
    "LICENSE.md",
    "LICENSE.txt",
)
_PORTABLE_ROOT_DIRECTORIES = (".github",)
_DEV_DIRECTORY_NAMES = {
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "pip-wheel-metadata",
}
_DEV_FILE_NAMES = {
    ".coverage",
    "coverage.xml",
}
_DEV_FILE_SUFFIXES = (
    ".egg-info",
    ".egg-link",
    ".pyc",
    ".pyo",
    ".whl",
)
_INTERNAL_REFERENCE_SUFFIXES = (
    "_assessment_closeout_reference.md",
    "_comparison_closeout_reference.md",
)
REPOSITORY_EXPORT_SCOPE = "repository_bundle"
PACK_BUNDLE_EXPORT_SCOPE = "pack_bundle"


@dataclass(frozen=True, slots=True)
class PackExportRequest:
    """Parameters for staging one portable shared-core export."""

    output_root: str
    included_pack_slugs: tuple[str, ...] = ()
    overwrite: bool = False
    pack_only: bool = False


@dataclass(frozen=True, slots=True)
class PackExportValidationSummary:
    """Validation status for one included hosted pack."""

    pack_slug: str
    pack_settings_path: str
    passed: bool
    issue_count: int
    issues: tuple[ValidationIssue, ...]


@dataclass(frozen=True, slots=True)
class PackExportResult:
    """Summary of one staged export plus its validation outcomes."""

    output_root: str
    export_scope: str
    included_pack_slugs: tuple[str, ...]
    default_pack_slug: str | None
    copied_paths: tuple[str, ...]
    scrubbed_paths: tuple[str, ...]
    changed_paths: tuple[str, ...]
    workspace_lock_removed: bool
    pack_validations: tuple[PackExportValidationSummary, ...]
    pack_validation_note: str | None
    portability_result: ValidationResult

    @property
    def passed(self) -> bool:
        return self.portability_result.passed and all(
            summary.passed for summary in self.pack_validations
        )


@dataclass(frozen=True, slots=True)
class PackExportCleanupRequest:
    """Inputs passed to one optional pack-owned export cleanup hook."""

    output_root: str
    export_scope: str
    pack_settings_path: str
    pack_slug: str
    command_namespace: str
    workspace_root: str
    machine_root: str
    docs_root: str
    tracking_root: str
    overview_path: str
    initiatives_root: str | None = None
    projects_root: str | None = None


@dataclass(frozen=True, slots=True)
class PackExportCleanupResult:
    """Paths scrubbed or rewritten by one pack-owned export cleanup hook."""

    scrubbed_paths: tuple[str, ...] = ()
    changed_paths: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EngineeringCoreExtractRequest:
    """Parameters for staging one bootstrap-ready engineering core extract."""

    output_root: str
    overwrite: bool = False


@dataclass(frozen=True, slots=True)
class EngineeringCoreApplyRequest:
    """Parameters for applying one staged engineering core extract locally."""

    source_root: str
    write: bool = False


@dataclass(frozen=True, slots=True)
class EngineeringCoreExtractResult:
    """Summary of one staged shared-core extract plus readiness validation."""

    output_root: str
    copied_paths: tuple[str, ...]
    scrubbed_paths: tuple[str, ...]
    changed_paths: tuple[str, ...]
    workspace_lock_removed: bool
    readiness_result: ValidationResult

    @property
    def passed(self) -> bool:
        return self.readiness_result.passed


@dataclass(frozen=True, slots=True)
class EngineeringCoreApplyResult:
    """Summary of applying one staged shared-core extract into a recipient repo."""

    source_root: str
    source_core_root: str
    target_core_root: str
    source_readiness_result: ValidationResult
    changed_paths: tuple[str, ...]
    deleted_paths: tuple[str, ...]
    preserved_paths: tuple[str, ...]
    wrote: bool


def export_hosted_repository(
    repo_root: Path,
    request: PackExportRequest,
) -> PackExportResult:
    """Stage a portability-clean export of shared core or selected pack roots."""

    resolved_repo_root = repo_root.resolve()
    output_root = Path(request.output_root).expanduser().resolve()
    _validate_output_root(repo_root=resolved_repo_root, output_root=output_root)
    normalized_pack_slugs = tuple(dict.fromkeys(request.included_pack_slugs))
    if request.pack_only and not normalized_pack_slugs:
        raise ValueError("Pack-only export requires at least one --include-pack slug.")

    loader = ControlPlaneLoader(resolved_repo_root)
    selected_pack_settings_paths: list[str] = []
    selected_pack_roots: list[str] = []
    for pack_slug in normalized_pack_slugs:
        try:
            registry_entry = loader.load_pack_registry().get_by_pack_slug(pack_slug)
        except KeyError as exc:
            raise ValueError(f"Unknown hosted pack slug for export: {pack_slug}.") from exc
        runtime_manifest = loader.load_pack_runtime_manifest(
            pack_settings_path=registry_entry.pack_settings_path
        )
        selected_pack_settings_paths.append(registry_entry.pack_settings_path)
        selected_pack_roots.append(runtime_manifest.owned_roots.workspace_root)

    _prepare_output_root(output_root=output_root, overwrite=request.overwrite)
    copied_paths = _copy_portable_surfaces(
        repo_root=resolved_repo_root,
        output_root=output_root,
        selected_pack_roots=tuple(selected_pack_roots),
        include_root_material=not request.pack_only,
        include_core=not request.pack_only,
    )
    scrubbed_paths = _scrub_export_root(
        output_root,
        selected_pack_roots=tuple(selected_pack_roots),
    )
    export_scope = (
        PACK_BUNDLE_EXPORT_SCOPE if request.pack_only else REPOSITORY_EXPORT_SCOPE
    )
    cleanup_scrubbed_paths, cleanup_changed_paths = _run_pack_export_cleanup_hooks(
        repo_root=resolved_repo_root,
        output_root=output_root,
        export_scope=export_scope,
        selected_pack_settings_paths=tuple(selected_pack_settings_paths),
    )
    scrubbed_paths.extend(cleanup_scrubbed_paths)

    changed_paths: set[str] = set(cleanup_changed_paths)
    workspace_lock_removed = False
    pack_validations: tuple[PackExportValidationSummary, ...] = ()
    pack_validation_note: str | None = None
    if request.pack_only:
        pack_validation_note = (
            "Pack-only export skips shared-core hosted-pack contract validation because "
            "the staged bundle omits shared core surfaces. Bootstrap the copied pack into "
            "a compatible core repository before running full pack validation there."
        )
    else:
        if selected_pack_settings_paths:
            any_pyproject_change = False
            for index, pack_settings_path in enumerate(selected_pack_settings_paths):
                result = bootstrap_hosted_pack(
                    output_root,
                    PackBootstrapRequest(
                        pack_settings_path=pack_settings_path,
                        write=True,
                        sync_workspace=False,
                        replace_hosted_packs=index == 0,
                    ),
                )
                changed_paths.update(result.changed_paths)
                any_pyproject_change = (
                    any_pyproject_change or result.core_python_pyproject_changed
                )
            if any_pyproject_change:
                workspace_lock_removed = _remove_workspace_lock(output_root, changed_paths)
        else:
            changed_paths.update(_scrub_all_hosted_pack_wiring(output_root))
            workspace_lock_removed = _remove_workspace_lock(output_root, changed_paths)

        rebuild_shared_discovery_surfaces(output_root)
        changed_paths.update(
            {
                "core/control_plane/indexes/commands/command_index.json",
                "core/control_plane/indexes/repository_paths/repository_path_index.json",
                "core/control_plane/indexes/references/reference_index.json",
                "core/control_plane/indexes/standards/standard_index.json",
                "core/control_plane/indexes/workflows/workflow_index.json",
                "core/control_plane/indexes/routes/route_index.json",
            }
        )
        _rebuild_foundation_index(output_root)
        changed_paths.add("core/control_plane/indexes/foundations/foundation_index.json")

        export_loader = ControlPlaneLoader(output_root)
        pack_validations = tuple(
            _validate_exported_pack(
                export_loader,
                pack_slug=pack_slug,
                pack_settings_path=pack_settings_path,
            )
            for pack_slug, pack_settings_path in zip(
                normalized_pack_slugs,
                selected_pack_settings_paths,
                strict=True,
            )
        )
    scrubbed_paths.extend(_scrub_developer_residue(output_root))
    portability_result = PortabilityValidationService().validate(
        output_root,
        included_pack_slugs=normalized_pack_slugs,
        scope=export_scope,
    )
    default_pack_slug = (
        None
        if request.pack_only or not normalized_pack_slugs
        else normalized_pack_slugs[0]
    )
    return PackExportResult(
        output_root=str(output_root),
        export_scope=export_scope,
        included_pack_slugs=normalized_pack_slugs,
        default_pack_slug=default_pack_slug,
        copied_paths=tuple(copied_paths),
        scrubbed_paths=tuple(sorted(set(scrubbed_paths))),
        changed_paths=tuple(sorted(changed_paths)),
        workspace_lock_removed=workspace_lock_removed,
        pack_validations=pack_validations,
        pack_validation_note=pack_validation_note,
        portability_result=portability_result,
    )


def extract_engineering_core(
    repo_root: Path,
    request: EngineeringCoreExtractRequest,
) -> EngineeringCoreExtractResult:
    """Stage a donor-neutral shared-core extract for repository-to-repository reuse."""

    resolved_repo_root = repo_root.resolve()
    output_root = Path(request.output_root).expanduser().resolve()
    _validate_output_root(repo_root=resolved_repo_root, output_root=output_root)
    _prepare_output_root(output_root=output_root, overwrite=request.overwrite)

    copied_paths = _copy_portable_surfaces(
        repo_root=resolved_repo_root,
        output_root=output_root,
        selected_pack_roots=(),
        include_root_material=True,
        include_core=True,
    )
    scrubbed_paths = _scrub_engineering_core_root(output_root)

    changed_paths = _scrub_all_hosted_pack_wiring(output_root)
    workspace_lock_removed = False
    if changed_paths:
        rebuild_shared_discovery_surfaces(output_root)
        changed_paths.update(
            {
                "core/control_plane/indexes/commands/command_index.json",
                "core/control_plane/indexes/repository_paths/repository_path_index.json",
                "core/control_plane/indexes/references/reference_index.json",
                "core/control_plane/indexes/standards/standard_index.json",
                "core/control_plane/indexes/workflows/workflow_index.json",
                "core/control_plane/indexes/routes/route_index.json",
            }
        )
        _rebuild_foundation_index(output_root)
        changed_paths.add("core/control_plane/indexes/foundations/foundation_index.json")
        if CORE_PYPROJECT_RELATIVE_PATH in changed_paths:
            workspace_lock_removed = _remove_workspace_lock(output_root, changed_paths)

    readiness_result = PortabilityValidationService().validate(
        output_root,
        scope=ENGINEERING_CORE_EXTRACT_SCOPE,
    )
    return EngineeringCoreExtractResult(
        output_root=str(output_root),
        copied_paths=tuple(copied_paths),
        scrubbed_paths=tuple(sorted(set(scrubbed_paths))),
        changed_paths=tuple(sorted(changed_paths)),
        workspace_lock_removed=workspace_lock_removed,
        readiness_result=readiness_result,
    )


def apply_engineering_core_extract(
    repo_root: Path,
    request: EngineeringCoreApplyRequest,
) -> EngineeringCoreApplyResult:
    """Apply one staged engineering core extract into the local recipient repo."""

    resolved_repo_root = repo_root.resolve()
    source_root = Path(request.source_root).expanduser().resolve()
    _validate_apply_source_root(repo_root=resolved_repo_root, source_root=source_root)

    source_core_root = source_root / "core"
    if not source_core_root.is_dir():
        raise ValueError(
            "Engineering core apply source is missing the staged core/ directory: "
            f"{source_root}"
        )

    readiness_result = PortabilityValidationService().validate(
        source_root,
        scope=ENGINEERING_CORE_EXTRACT_SCOPE,
    )
    if not readiness_result.passed:
        raise ValueError(
            "Engineering core apply source failed readiness validation: "
            f"{_validation_issue_summary(readiness_result)}"
        )

    target_core_root = resolved_repo_root / "core"
    changed_paths, deleted_paths, preserved_paths = _apply_core_tree(
        source_core_root=source_core_root,
        target_core_root=target_core_root,
        write=request.write,
    )
    return EngineeringCoreApplyResult(
        source_root=str(source_root),
        source_core_root=str(source_core_root),
        target_core_root=str(target_core_root),
        source_readiness_result=readiness_result,
        changed_paths=changed_paths,
        deleted_paths=deleted_paths,
        preserved_paths=preserved_paths,
        wrote=request.write,
    )


def _copy_portable_surfaces(
    *,
    repo_root: Path,
    output_root: Path,
    selected_pack_roots: tuple[str, ...],
    include_root_material: bool,
    include_core: bool,
) -> list[str]:
    copied_paths: list[str] = []
    if include_root_material:
        for relative_path in _PORTABLE_ROOT_FILES:
            source = repo_root / relative_path
            if not source.is_file():
                continue
            destination = output_root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied_paths.append(relative_path)

        for relative_path in _PORTABLE_ROOT_DIRECTORIES:
            source = repo_root / relative_path
            if not source.is_dir():
                continue
            destination = output_root / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination, ignore=_copytree_ignore)
            copied_paths.append(relative_path)

    required_relative_paths = list(selected_pack_roots)
    if include_core:
        required_relative_paths.insert(0, "core")

    for relative_path in required_relative_paths:
        source = repo_root / relative_path
        if not source.exists():
            raise ValueError(
                "Portable export is missing a required source surface: "
                f"{relative_path}."
            )
        destination = output_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, ignore=_copytree_ignore)
        else:
            shutil.copy2(source, destination)
        copied_paths.append(relative_path)
    return copied_paths


def _copy_engineering_core_surface(
    *,
    repo_root: Path,
    output_root: Path,
) -> list[str]:
    source = repo_root / "core"
    if not source.is_dir():
        raise ValueError("Engineering core extract requires a donor core/ directory.")
    destination = output_root / "core"
    shutil.copytree(source, destination, ignore=_copytree_ignore)
    return ["core"]


def _copytree_ignore(current_root: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in _DEV_DIRECTORY_NAMES or name in _DEV_FILE_NAMES:
            ignored.add(name)
            continue
        if any(name.endswith(suffix) for suffix in _DEV_FILE_SUFFIXES):
            ignored.add(name)
    return ignored


def _is_dev_residue_relative_path(relative_path: PurePosixPath) -> bool:
    parts = relative_path.parts
    if any(part in _DEV_DIRECTORY_NAMES for part in parts):
        return True
    if any(any(part.endswith(suffix) for suffix in _DEV_FILE_SUFFIXES) for part in parts):
        return True
    if not parts:
        return False
    name = parts[-1]
    return name in _DEV_FILE_NAMES or any(name.endswith(suffix) for suffix in _DEV_FILE_SUFFIXES)


def _validation_issue_summary(result: ValidationResult) -> str:
    if not result.issues:
        return "validation failed without reported issues."
    return "; ".join(f"{issue.code}: {issue.message}" for issue in result.issues[:5])


def _scrub_export_root(
    output_root: Path,
    *,
    selected_pack_roots: tuple[str, ...],
) -> list[str]:
    scrubbed_paths: list[str] = []
    scrubbed_paths.extend(_scrub_retained_history(output_root))
    scrubbed_paths.extend(_scrub_nonportable_acceptance_lineage(output_root))
    scrubbed_paths.extend(
        _scrub_nonportable_traceability_entries(
            output_root,
            allowed_roots=("core", *selected_pack_roots),
        )
    )

    for candidate in sorted(output_root.rglob("runtime")):
        if not candidate.is_dir() or candidate.parent.name != ".wt":
            continue
        scrubbed_paths.extend(_clear_directory_contents(candidate, output_root))

    for candidate in sorted(output_root.glob("*/python/tests")):
        if candidate.is_dir():
            scrubbed_paths.extend(_clear_directory_contents(candidate, output_root))

    for candidate in sorted(output_root.rglob("python/tests")):
        if candidate.is_dir():
            scrubbed_paths.extend(_clear_directory_contents(candidate, output_root))

    for candidate in sorted(output_root.rglob("testing")):
        if (
            candidate.is_dir()
            and candidate.parent.name.startswith("watchtower_")
            and candidate.parent.parent.name == "src"
        ):
            scrubbed_paths.extend(_clear_directory_contents(candidate, output_root))

    for candidate in sorted(output_root.rglob("project_repository_map.json")):
        if candidate.is_file():
            candidate.unlink()
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())

    for candidate in sorted(output_root.rglob("*")):
        if not candidate.exists():
            continue
        if candidate.is_dir() and candidate.name in _DEV_DIRECTORY_NAMES:
            shutil.rmtree(candidate)
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
            continue
        if not candidate.is_file():
            continue
        if candidate.name in _DEV_FILE_NAMES or any(
            candidate.name.endswith(suffix) for suffix in _DEV_FILE_SUFFIXES
        ):
            candidate.unlink()
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
            continue
        relative_path = candidate.relative_to(output_root).as_posix()
        if (
            "docs/references/" in relative_path
            and candidate.name.endswith(_INTERNAL_REFERENCE_SUFFIXES)
        ):
            candidate.unlink()
            scrubbed_paths.append(relative_path)
    return scrubbed_paths


def _run_pack_export_cleanup_hooks(
    *,
    repo_root: Path,
    output_root: Path,
    export_scope: str,
    selected_pack_settings_paths: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not selected_pack_settings_paths:
        return (), ()

    loader = ControlPlaneLoader(repo_root)
    scrubbed_paths: set[str] = set()
    changed_paths: set[str] = set()
    for pack_settings_path in selected_pack_settings_paths:
        loaded = load_active_pack_integration(loader, pack_settings_path=pack_settings_path)
        if "export_cleanup" not in loaded.integration.declared_capabilities:
            continue
        hook = loaded.integration.export_cleanup
        if hook is None:
            raise ValueError(
                "Pack integration declares export_cleanup but is missing the hook: "
                f"{loaded.runtime_manifest.integration_module}"
            )
        workspace_roots = loaded.pack_settings.workspace_roots
        runtime_roots = loaded.runtime_manifest.owned_roots
        result = hook(
            PackExportCleanupRequest(
                output_root=str(output_root),
                export_scope=export_scope,
                pack_settings_path=pack_settings_path,
                pack_slug=loaded.runtime_manifest.pack_slug,
                command_namespace=loaded.runtime_manifest.command_namespace,
                workspace_root=runtime_roots.workspace_root,
                machine_root=runtime_roots.machine_root,
                docs_root=runtime_roots.docs_root,
                tracking_root=runtime_roots.tracking_root,
                overview_path=workspace_roots.overview_path,
                initiatives_root=workspace_roots.initiatives_root,
                projects_root=workspace_roots.projects_root,
            )
        )
        if not isinstance(result, PackExportCleanupResult):
            raise ValueError(
                "Pack export_cleanup hook must return PackExportCleanupResult: "
                f"{loaded.runtime_manifest.integration_module}"
            )
        scrubbed_paths.update(result.scrubbed_paths)
        changed_paths.update(result.changed_paths)
    return tuple(sorted(scrubbed_paths)), tuple(sorted(changed_paths))


def _apply_core_tree(
    *,
    source_core_root: Path,
    target_core_root: Path,
    write: bool,
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    changed_paths: set[str] = set()
    deleted_paths: set[str] = set()
    preserved_paths: set[str] = set()
    if write:
        target_core_root.mkdir(parents=True, exist_ok=True)
    _sync_applied_core_directory(
        source_directory=source_core_root,
        target_directory=target_core_root,
        relative_root=PurePosixPath(),
        write=write,
        changed_paths=changed_paths,
        deleted_paths=deleted_paths,
        preserved_paths=preserved_paths,
    )
    return (
        tuple(sorted(changed_paths)),
        tuple(sorted(deleted_paths)),
        tuple(sorted(preserved_paths)),
    )


def _sync_applied_core_directory(
    *,
    source_directory: Path,
    target_directory: Path,
    relative_root: PurePosixPath,
    write: bool,
    changed_paths: set[str],
    deleted_paths: set[str],
    preserved_paths: set[str],
) -> None:
    source_names: set[str] = set()
    target_entries = (
        {entry.name: entry for entry in target_directory.iterdir()}
        if target_directory.is_dir()
        else {}
    )

    for source_entry in sorted(source_directory.iterdir(), key=lambda entry: entry.name):
        relative_path = _join_relative_path(relative_root, source_entry.name)
        repo_relative_path = _core_repo_relative_path(relative_path)
        if _is_dev_residue_relative_path(relative_path):
            preserved_paths.add(repo_relative_path)
            continue
        source_names.add(source_entry.name)
        target_entry = target_entries.get(source_entry.name)

        if source_entry.is_dir():
            if target_entry is not None and not target_entry.is_dir():
                deleted_paths.add(repo_relative_path)
                if write:
                    target_entry.unlink()
            if write:
                (target_directory / source_entry.name).mkdir(parents=True, exist_ok=True)
            _sync_applied_core_directory(
                source_directory=source_entry,
                target_directory=target_directory / source_entry.name,
                relative_root=relative_path,
                write=write,
                changed_paths=changed_paths,
                deleted_paths=deleted_paths,
                preserved_paths=preserved_paths,
            )
            continue

        if target_entry is not None and target_entry.is_dir():
            deleted_paths.add(repo_relative_path)
            if write:
                shutil.rmtree(target_entry)
            target_entry = None

        if not (target_entry is not None and target_entry.is_file()):
            changed_paths.add(repo_relative_path)
        elif not filecmp.cmp(source_entry, target_entry, shallow=False):
            changed_paths.add(repo_relative_path)

        if write and repo_relative_path in changed_paths:
            destination = target_directory / source_entry.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_entry, destination)

    for target_entry in sorted(target_entries.values(), key=lambda entry: entry.name):
        relative_path = _join_relative_path(relative_root, target_entry.name)
        repo_relative_path = _core_repo_relative_path(relative_path)
        if _is_dev_residue_relative_path(relative_path):
            preserved_paths.add(repo_relative_path)
            continue
        if target_entry.name in source_names:
            continue
        deleted_paths.add(repo_relative_path)
        if not write:
            continue
        if target_entry.is_dir():
            shutil.rmtree(target_entry)
        else:
            target_entry.unlink()


def _join_relative_path(relative_root: PurePosixPath, name: str) -> PurePosixPath:
    if not relative_root.parts:
        return PurePosixPath(name)
    return relative_root / name


def _core_repo_relative_path(relative_path: PurePosixPath) -> str:
    return PurePosixPath("core", relative_path).as_posix()


def _scrub_engineering_core_root(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    scrubbed_paths.extend(_scrub_nonportable_engineering_history(output_root))
    scrubbed_paths.extend(_scrub_nonportable_engineering_acceptance_lineage(output_root))
    scrubbed_paths.extend(_scrub_internal_assessment_references(output_root))
    scrubbed_paths.extend(_scrub_project_repository_maps(output_root))
    scrubbed_paths.extend(_scrub_developer_residue(output_root))
    return scrubbed_paths


def _scrub_retained_history(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    records_root = output_root / "core" / "control_plane" / "records"
    if not records_root.exists():
        return scrubbed_paths
    for candidate in sorted(records_root.rglob("*")):
        if not candidate.is_file():
            continue
        if candidate.name == "README.md":
            continue
        candidate.unlink()
        scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
    return scrubbed_paths


def _scrub_nonportable_engineering_history(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    records_root = output_root / "core" / "control_plane" / "records"
    if not records_root.exists():
        return scrubbed_paths
    for candidate in sorted(records_root.rglob("*")):
        if not candidate.is_file() or candidate.name == "README.md":
            continue
        relative_path = candidate.relative_to(output_root).as_posix()
        if relative_path.startswith("core/control_plane/records/validation_evidence/"):
            try:
                document = json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                document = None
            if validation_evidence_artifact_is_shared_core_portable(document):
                continue
        candidate.unlink()
        scrubbed_paths.append(relative_path)
    return scrubbed_paths


def _scrub_nonportable_acceptance_lineage(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []

    acceptance_root = output_root / "core" / "control_plane" / "contracts" / "acceptance"
    if acceptance_root.exists():
        for candidate in sorted(acceptance_root.glob("*.json")):
            candidate.unlink()
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())

    traceability_path = (
        output_root / "core" / "control_plane" / "indexes" / "traceability"
        / "traceability_index.json"
    )
    if not traceability_path.exists():
        return scrubbed_paths

    document = json.loads(traceability_path.read_text(encoding="utf-8"))
    entries = document.get("entries")
    if not isinstance(entries, list):
        return scrubbed_paths

    filtered_entries = [
        entry
        for entry in entries
        if not traceability_entry_requires_nonportable_acceptance_lineage(entry)
    ]
    if filtered_entries == entries:
        return scrubbed_paths

    traceability_path.write_text(
        f"{json.dumps({**document, 'entries': filtered_entries}, indent=2)}\n",
        encoding="utf-8",
    )
    scrubbed_paths.append(traceability_path.relative_to(output_root).as_posix())
    return scrubbed_paths


def _scrub_nonportable_traceability_entries(
    output_root: Path,
    *,
    allowed_roots: tuple[str, ...],
) -> list[str]:
    traceability_path = (
        output_root / "core" / "control_plane" / "indexes" / "traceability"
        / "traceability_index.json"
    )
    if not traceability_path.exists():
        return []

    normalized_roots = tuple(
        dict.fromkeys(
            PurePosixPath(root.strip("/")).as_posix()
            for root in allowed_roots
            if isinstance(root, str) and root.strip("/")
        )
    )
    document = json.loads(traceability_path.read_text(encoding="utf-8"))
    entries = document.get("entries")
    if not isinstance(entries, list):
        return []

    filtered_entries = [
        entry
        for entry in entries
        if traceability_entry_is_repository_export_portable(
            entry,
            allowed_roots=normalized_roots,
        )
    ]
    if filtered_entries == entries:
        return []

    traceability_path.write_text(
        f"{json.dumps({**document, 'entries': filtered_entries}, indent=2)}\n",
        encoding="utf-8",
    )
    return [traceability_path.relative_to(output_root).as_posix()]


def _scrub_nonportable_engineering_acceptance_lineage(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []

    acceptance_root = output_root / "core" / "control_plane" / "contracts" / "acceptance"
    if acceptance_root.exists():
        for candidate in sorted(acceptance_root.glob("*.json")):
            try:
                document = json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                document = None
            if acceptance_contract_is_shared_core_portable(document):
                continue
            candidate.unlink()
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())

    traceability_path = (
        output_root / "core" / "control_plane" / "indexes" / "traceability"
        / "traceability_index.json"
    )
    if traceability_path.exists():
        document = json.loads(traceability_path.read_text(encoding="utf-8"))
        entries = document.get("entries")
        if isinstance(entries, list):
            filtered_entries = [
                entry for entry in entries if traceability_entry_is_shared_core_portable(entry)
            ]
            if filtered_entries != entries:
                traceability_path.write_text(
                    f"{json.dumps({**document, 'entries': filtered_entries}, indent=2)}\n",
                    encoding="utf-8",
                )
                scrubbed_paths.append(traceability_path.relative_to(output_root).as_posix())

    return scrubbed_paths


def _scrub_developer_residue(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    for candidate in sorted(output_root.rglob("*")):
        if not candidate.exists():
            continue
        if candidate.is_dir() and candidate.name in _DEV_DIRECTORY_NAMES:
            shutil.rmtree(candidate)
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
            continue
        if not candidate.is_file():
            continue
        if candidate.name in _DEV_FILE_NAMES or any(
            candidate.name.endswith(suffix) for suffix in _DEV_FILE_SUFFIXES
        ):
            candidate.unlink()
            scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
    return scrubbed_paths


def _scrub_project_repository_maps(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    for candidate in sorted(output_root.rglob("project_repository_map.json")):
        if not candidate.is_file():
            continue
        candidate.unlink()
        scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
    return scrubbed_paths


def _scrub_internal_assessment_references(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    for candidate in sorted(output_root.rglob("*.md")):
        if not candidate.is_file():
            continue
        relative_path = candidate.relative_to(output_root).as_posix()
        if "docs/references/" not in relative_path:
            continue
        if not candidate.name.endswith(_INTERNAL_REFERENCE_SUFFIXES):
            continue
        candidate.unlink()
        scrubbed_paths.append(relative_path)
    return scrubbed_paths


def _clear_directory_contents(directory: Path, output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    for candidate in sorted(directory.iterdir()):
        relative_path = candidate.relative_to(output_root).as_posix()
        if candidate.is_dir():
            shutil.rmtree(candidate)
        else:
            candidate.unlink()
        scrubbed_paths.append(relative_path)
    return scrubbed_paths


def _scrub_all_hosted_pack_wiring(output_root: Path) -> set[str]:
    changed_paths: set[str] = set()

    pack_registry_path = output_root / PACK_REGISTRY_PATH
    if pack_registry_path.exists():
        document = json.loads(pack_registry_path.read_text(encoding="utf-8"))
        updated_document = {**document, "packs": []}
        if updated_document != document:
            pack_registry_path.write_text(
                f"{json.dumps(updated_document, indent=2)}\n",
                encoding="utf-8",
            )
            changed_paths.add(PACK_REGISTRY_PATH)

    pyproject_path = output_root / CORE_PYPROJECT_RELATIVE_PATH
    if pyproject_path.exists():
        pyproject_text = pyproject_path.read_text(encoding="utf-8")
        updated_text, changed = reconcile_core_python_workspace_pyproject(pyproject_text)
        if changed:
            pyproject_path.write_text(updated_text, encoding="utf-8")
            changed_paths.add(CORE_PYPROJECT_RELATIVE_PATH)

    return changed_paths


def _remove_workspace_lock(output_root: Path, changed_paths: set[str]) -> bool:
    uv_lock_path = output_root / CORE_UV_LOCK_RELATIVE_PATH
    if not uv_lock_path.exists():
        return False
    uv_lock_path.unlink()
    changed_paths.add(CORE_UV_LOCK_RELATIVE_PATH)
    return True


def _rebuild_foundation_index(output_root: Path) -> None:
    loader = ControlPlaneLoader(output_root)
    service = FoundationIndexSyncService(loader)
    document = service.build_document()
    service.write_document(document)


def _validate_exported_pack(
    loader: ControlPlaneLoader,
    *,
    pack_slug: str,
    pack_settings_path: str,
) -> PackExportValidationSummary:
    result = PackContractValidationService(loader).validate(pack_settings_path)
    return PackExportValidationSummary(
        pack_slug=pack_slug,
        pack_settings_path=pack_settings_path,
        passed=result.passed,
        issue_count=result.issue_count,
        issues=result.issues,
    )


def _prepare_output_root(*, output_root: Path, overwrite: bool) -> None:
    if output_root.exists():
        if not output_root.is_dir():
            raise ValueError(f"Export output path must be a directory: {output_root}")
        if not overwrite:
            raise ValueError(
                "Export output root already exists. Pass --overwrite to replace it: "
                f"{output_root}"
            )
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)


def _validate_output_root(*, repo_root: Path, output_root: Path) -> None:
    if output_root == repo_root or output_root.is_relative_to(repo_root):
        raise ValueError(
            "Export output root must live outside the donor repository root to avoid "
            f"self-copy recursion: {output_root}"
        )


def _validate_apply_source_root(*, repo_root: Path, source_root: Path) -> None:
    if source_root == repo_root or source_root.is_relative_to(repo_root):
        raise ValueError(
            "Engineering core apply source must live outside the recipient repository "
            f"root to avoid self-overwrite: {source_root}"
        )


__all__ = [
    "EngineeringCoreApplyRequest",
    "EngineeringCoreApplyResult",
    "EngineeringCoreExtractRequest",
    "EngineeringCoreExtractResult",
    "PACK_BUNDLE_EXPORT_SCOPE",
    "PackExportRequest",
    "PackExportResult",
    "PackExportValidationSummary",
    "REPOSITORY_EXPORT_SCOPE",
    "apply_engineering_core_extract",
    "extract_engineering_core",
    "export_hosted_repository",
]
