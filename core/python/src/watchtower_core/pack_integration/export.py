"""Portable staged export helpers for shared core plus selected hosted packs."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import PACK_REGISTRY_PATH, ControlPlaneLoader
from watchtower_core.pack_integration.bootstrap import (
    PackBootstrapRequest,
    bootstrap_hosted_pack,
    rebuild_shared_discovery_surfaces,
)
from watchtower_core.pack_integration.workspace_registration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    CORE_UV_LOCK_RELATIVE_PATH,
    reconcile_core_python_workspace_pyproject,
)
from watchtower_core.sync.foundation_index import FoundationIndexSyncService
from watchtower_core.validation.models import ValidationIssue, ValidationResult
from watchtower_core.validation.pack_contract import PackContractValidationService
from watchtower_core.validation.portability import (
    PortabilityValidationService,
    traceability_entry_requires_nonportable_acceptance_lineage,
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
    scrubbed_paths = _scrub_export_root(output_root)

    changed_paths: set[str] = set()
    workspace_lock_removed = False
    pack_validations: tuple[PackExportValidationSummary, ...] = ()
    pack_validation_note: str | None = None
    export_scope = (
        PACK_BUNDLE_EXPORT_SCOPE if request.pack_only else REPOSITORY_EXPORT_SCOPE
    )
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


def _copytree_ignore(current_root: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in _DEV_DIRECTORY_NAMES or name in _DEV_FILE_NAMES:
            ignored.add(name)
            continue
        if any(name.endswith(suffix) for suffix in _DEV_FILE_SUFFIXES):
            ignored.add(name)
    return ignored


def _scrub_export_root(output_root: Path) -> list[str]:
    scrubbed_paths: list[str] = []
    scrubbed_paths.extend(_scrub_retained_history(output_root))
    scrubbed_paths.extend(_scrub_nonportable_acceptance_lineage(output_root))

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


__all__ = [
    "PACK_BUNDLE_EXPORT_SCOPE",
    "PackExportRequest",
    "PackExportResult",
    "PackExportValidationSummary",
    "REPOSITORY_EXPORT_SCOPE",
    "export_hosted_repository",
]
