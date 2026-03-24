"""Hosted-pack bootstrap helpers for shared registry and workspace installation."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import (
    PACK_REGISTRY_PATH,
    ControlPlaneLoader,
)
from watchtower_core.pack_integration.runtime_registry import load_pack_registry_runtime_view
from watchtower_core.pack_integration.workspace_registration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    CORE_UV_LOCK_RELATIVE_PATH,
    CorePythonWorkspaceRegistration,
    core_python_workspace_registration,
    render_core_python_workspace_pyproject,
)

COMMAND_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/commands/command_index.json"
REPOSITORY_PATH_INDEX_ARTIFACT_PATH = (
    "core/control_plane/indexes/repository_paths/repository_path_index.json"
)
REFERENCE_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/references/reference_index.json"
STANDARD_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/standards/standard_index.json"
WORKFLOW_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/workflows/workflow_index.json"
ROUTE_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/routes/route_index.json"
SHARED_DISCOVERY_ARTIFACT_PATHS = (
    COMMAND_INDEX_ARTIFACT_PATH,
    REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
    REFERENCE_INDEX_ARTIFACT_PATH,
    STANDARD_INDEX_ARTIFACT_PATH,
    WORKFLOW_INDEX_ARTIFACT_PATH,
    ROUTE_INDEX_ARTIFACT_PATH,
)


@dataclass(frozen=True, slots=True)
class PackBootstrapRequest:
    """Parameters for registering one hosted pack into the shared workspace."""

    pack_settings_path: str
    write: bool = False
    sync_workspace: bool = True
    replace_hosted_packs: bool = False


@dataclass(frozen=True, slots=True)
class PackBootstrapResult:
    """Summary of one hosted-pack bootstrap operation."""

    pack_slug: str
    pack_settings_path: str
    pack_runtime_manifest_path: str
    replace_hosted_packs: bool
    scrubbed_pack_slugs: tuple[str, ...]
    pack_registry_entry: dict[str, object]
    core_python_workspace_registration: CorePythonWorkspaceRegistration
    pack_registry_changed: bool
    core_python_pyproject_changed: bool
    workspace_sync_ran: bool
    workspace_sync_required: bool
    validation_passed: bool | None
    changed_paths: tuple[str, ...]
    wrote: bool


def bootstrap_hosted_pack(
    repo_root: Path,
    request: PackBootstrapRequest,
) -> PackBootstrapResult:
    """Register one hosted pack and optionally sync the shared Python workspace."""

    loader = ControlPlaneLoader(repo_root)
    pack_settings_path = _validate_relative_path(request.pack_settings_path)
    pack_settings = loader.load_pack_settings(pack_settings_path)
    runtime_manifest = loader.load_pack_runtime_manifest(pack_settings_path=pack_settings_path)
    pack_runtime_manifest_path = loader.pack_runtime_manifest_path(pack_settings_path)

    _preflight_integration_module_source(
        repo_root=repo_root,
        integration_module=runtime_manifest.integration_module,
        python_root=runtime_manifest.owned_roots.python_root,
    )

    pack_registry_entry = _build_pack_registry_entry(
        loader=loader,
        pack_settings_path=pack_settings_path,
        pack_runtime_manifest_path=pack_runtime_manifest_path,
        pack_id=pack_settings.pack_id,
        pack_slug=runtime_manifest.pack_slug,
        command_namespace=runtime_manifest.command_namespace,
        python_distribution=runtime_manifest.python_distribution,
        python_package=runtime_manifest.python_package,
    )
    registration = core_python_workspace_registration(
        repo_root,
        python_root=runtime_manifest.owned_roots.python_root,
        python_distribution=runtime_manifest.python_distribution,
    )
    runtime_view = load_pack_registry_runtime_view(loader)
    invalid_pack_settings_paths = {
        entry.pack_settings_path for entry in runtime_view.invalid_entries
    }

    pack_registry_path = repo_root / PACK_REGISTRY_PATH
    pyproject_path = repo_root / CORE_PYPROJECT_RELATIVE_PATH
    uv_lock_path = repo_root / CORE_UV_LOCK_RELATIVE_PATH
    shared_discovery_paths = tuple(
        repo_root / relative_path for relative_path in SHARED_DISCOVERY_ARTIFACT_PATHS
    )

    registry_document = json.loads(pack_registry_path.read_text(encoding="utf-8"))
    updated_registry_document, pack_registry_changed = _updated_pack_registry_document(
        registry_document,
        pack_registry_entry,
        invalid_pack_settings_paths=invalid_pack_settings_paths,
        replace_hosted_packs=request.replace_hosted_packs,
    )
    scrubbed_pack_slugs = _scrubbed_pack_slugs(
        registry_document=registry_document,
        updated_registry_document=updated_registry_document,
        candidate_entry=pack_registry_entry,
    )
    retained_workspace_dependencies = _retained_workspace_dependencies(
        updated_registry_document,
    )
    current_pyproject_text = pyproject_path.read_text(encoding="utf-8")
    updated_pyproject_text, core_python_pyproject_changed = render_core_python_workspace_pyproject(
        current_pyproject_text,
        registration,
        retained_dependencies=retained_workspace_dependencies,
    )

    changed_paths = []
    if pack_registry_changed:
        changed_paths.append(PACK_REGISTRY_PATH)
        changed_paths.extend(SHARED_DISCOVERY_ARTIFACT_PATHS)
    if core_python_pyproject_changed:
        changed_paths.append(CORE_PYPROJECT_RELATIVE_PATH)
    if request.sync_workspace and request.write and core_python_pyproject_changed:
        changed_paths.append(CORE_UV_LOCK_RELATIVE_PATH)

    if not request.write:
        return PackBootstrapResult(
            pack_slug=runtime_manifest.pack_slug,
            pack_settings_path=pack_settings_path,
            pack_runtime_manifest_path=pack_runtime_manifest_path,
            replace_hosted_packs=request.replace_hosted_packs,
            scrubbed_pack_slugs=scrubbed_pack_slugs,
            pack_registry_entry=pack_registry_entry,
            core_python_workspace_registration=registration,
            pack_registry_changed=pack_registry_changed,
            core_python_pyproject_changed=core_python_pyproject_changed,
            workspace_sync_ran=False,
            workspace_sync_required=request.sync_workspace and core_python_pyproject_changed,
            validation_passed=None,
            changed_paths=tuple(changed_paths),
            wrote=False,
        )

    original_registry_text = pack_registry_path.read_text(encoding="utf-8")
    original_pyproject_text = current_pyproject_text
    original_workspace_file_texts = _snapshot_optional_texts(
        (uv_lock_path, *shared_discovery_paths)
    )
    workspace_sync_ran = False
    validation_passed: bool | None = None

    try:
        if pack_registry_changed:
            pack_registry_path.write_text(
                f"{json.dumps(updated_registry_document, indent=2)}\n",
                encoding="utf-8",
            )
        if core_python_pyproject_changed:
            pyproject_path.write_text(updated_pyproject_text, encoding="utf-8")
        if pack_registry_changed:
            _rebuild_shared_discovery_surfaces(repo_root)
        if request.sync_workspace and core_python_pyproject_changed:
            _run_workspace_sync(repo_root)
            workspace_sync_ran = True
        if workspace_sync_ran or not core_python_pyproject_changed:
            validation_passed = _validate_bootstrapped_pack(
                repo_root=repo_root,
                pack_settings_path=pack_settings_path,
            )
    except Exception:
        _restore_workspace_files(
            pack_registry_path=pack_registry_path,
            original_registry_text=original_registry_text,
            pyproject_path=pyproject_path,
            original_pyproject_text=original_pyproject_text,
            original_workspace_file_texts=original_workspace_file_texts,
        )
        if workspace_sync_ran:
            _best_effort_workspace_resync(repo_root)
        raise

    return PackBootstrapResult(
        pack_slug=runtime_manifest.pack_slug,
        pack_settings_path=pack_settings_path,
        pack_runtime_manifest_path=pack_runtime_manifest_path,
        replace_hosted_packs=request.replace_hosted_packs,
        scrubbed_pack_slugs=scrubbed_pack_slugs,
        pack_registry_entry=pack_registry_entry,
        core_python_workspace_registration=registration,
        pack_registry_changed=pack_registry_changed,
        core_python_pyproject_changed=core_python_pyproject_changed,
        workspace_sync_ran=workspace_sync_ran,
        workspace_sync_required=not workspace_sync_ran and core_python_pyproject_changed,
        validation_passed=validation_passed,
        changed_paths=tuple(changed_paths),
        wrote=True,
    )


def _build_pack_registry_entry(
    *,
    loader: ControlPlaneLoader,
    pack_settings_path: str,
    pack_runtime_manifest_path: str,
    pack_id: str,
    pack_slug: str,
    command_namespace: str,
    python_distribution: str,
    python_package: str,
) -> dict[str, object]:
    try:
        existing_entry = loader.load_pack_registry().get_by_pack_id(pack_id)
    except KeyError:
        existing_entry = None
    return {
        "pack_id": pack_id,
        "pack_slug": pack_slug,
        "command_namespace": command_namespace,
        "pack_settings_path": pack_settings_path,
        "pack_runtime_manifest_path": pack_runtime_manifest_path,
        "python_distribution": python_distribution,
        "python_package": python_package,
        "default_repo_pack": existing_entry.default_repo_pack if existing_entry else False,
        "notes": (
            existing_entry.notes
            if existing_entry is not None and existing_entry.notes is not None
            else (
                f"The {pack_slug} pack is registered for shared host composition and "
                "workspace installation."
            )
        ),
    }


def _updated_pack_registry_document(
    registry_document: dict[str, object],
    candidate_entry: dict[str, object],
    *,
    invalid_pack_settings_paths: set[str],
    replace_hosted_packs: bool = False,
) -> tuple[dict[str, object], bool]:
    raw_packs = registry_document.get("packs")
    if not isinstance(raw_packs, list):
        raise ValueError("Pack registry document is missing its packs list.")
    packs = tuple(entry for entry in raw_packs if isinstance(entry, dict))
    updated_packs: list[dict[str, object]] = []
    matched_existing = False
    changed = False

    for entry in packs:
        if _matches_same_pack(entry, candidate_entry):
            merged_entry = {
                **candidate_entry,
                "default_repo_pack": bool(entry.get("default_repo_pack", False)),
                "notes": entry.get("notes") or candidate_entry["notes"],
            }
            updated_packs.append(merged_entry)
            matched_existing = True
            if merged_entry != entry:
                changed = True
            continue
        if entry.get("pack_settings_path") in invalid_pack_settings_paths:
            changed = True
            continue
        if replace_hosted_packs:
            changed = True
            continue
        _raise_conflict_if_present(entry, candidate_entry)
        updated_packs.append(entry)

    if not matched_existing:
        updated_packs.append(candidate_entry)
        changed = True

    normalized_packs = updated_packs
    if replace_hosted_packs or not any(
        bool(entry.get("default_repo_pack", False)) for entry in updated_packs
    ):
        normalized_packs = [
            {
                **entry,
                "default_repo_pack": _matches_same_pack(entry, candidate_entry),
            }
            for entry in updated_packs
        ]
    if normalized_packs != updated_packs:
        changed = True
        updated_packs = normalized_packs

    sorted_packs = sorted(
        updated_packs,
        key=lambda entry: (
            not bool(entry.get("default_repo_pack", False)),
            str(entry["pack_slug"]).casefold(),
        ),
    )
    updated_document = {**registry_document, "packs": sorted_packs}
    return updated_document, changed


def _scrubbed_pack_slugs(
    *,
    registry_document: dict[str, object],
    updated_registry_document: dict[str, object],
    candidate_entry: dict[str, object],
) -> tuple[str, ...]:
    original_packs = registry_document.get("packs")
    updated_packs = updated_registry_document.get("packs")
    if not isinstance(original_packs, list) or not isinstance(updated_packs, list):
        return ()

    updated_keys = {
        (
            entry.get("pack_id"),
            entry.get("pack_slug"),
            entry.get("pack_settings_path"),
            entry.get("pack_runtime_manifest_path"),
        )
        for entry in updated_packs
        if isinstance(entry, dict)
    }
    scrubbed: list[str] = []
    for entry in original_packs:
        if not isinstance(entry, dict):
            continue
        entry_key = (
            entry.get("pack_id"),
            entry.get("pack_slug"),
            entry.get("pack_settings_path"),
            entry.get("pack_runtime_manifest_path"),
        )
        if entry_key in updated_keys or _matches_same_pack(entry, candidate_entry):
            continue
        scrubbed.append(
            str(entry.get("pack_slug", entry.get("pack_id", "<unknown-pack>")))
        )
    return tuple(scrubbed)


def _retained_workspace_dependencies(
    registry_document: dict[str, object],
) -> tuple[str, ...]:
    raw_packs = registry_document.get("packs")
    if not isinstance(raw_packs, list):
        raise ValueError("Pack registry document is missing its packs list.")
    return tuple(
        sorted(
            {
                str(entry["python_distribution"])
                for entry in raw_packs
                if isinstance(entry, dict) and isinstance(entry.get("python_distribution"), str)
            },
            key=str.casefold,
        )
    )


def _matches_same_pack(
    existing_entry: dict[str, object],
    candidate_entry: dict[str, object],
) -> bool:
    return any(
        existing_entry.get(key) == candidate_entry[key]
        for key in (
            "pack_id",
            "pack_slug",
            "pack_settings_path",
            "pack_runtime_manifest_path",
        )
    )


def _raise_conflict_if_present(
    existing_entry: dict[str, object],
    candidate_entry: dict[str, object],
) -> None:
    for field_name in ("command_namespace", "python_distribution", "python_package"):
        if existing_entry.get(field_name) == candidate_entry[field_name]:
            raise ValueError(
                "Hosted-pack bootstrap would conflict with an existing registry entry: "
                f"{field_name}={candidate_entry[field_name]!r} is already owned by "
                f"{existing_entry.get('pack_slug', existing_entry.get('pack_id'))}."
            )


def _validate_bootstrapped_pack(
    *,
    repo_root: Path,
    pack_settings_path: str,
) -> bool:
    from watchtower_core.validation.pack_contract import PackContractValidationService

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        pack_settings_path
    )
    if result.passed:
        return True
    issue_summary = "; ".join(f"{issue.code}: {issue.message}" for issue in result.issues[:5])
    raise ValueError(
        "Hosted-pack bootstrap failed validation after applying shared workspace wiring: "
        f"{issue_summary}"
    )


def _preflight_integration_module_source(
    *,
    repo_root: Path,
    integration_module: str,
    python_root: str,
) -> None:
    python_source_root = repo_root / python_root / "src"
    module_parts = integration_module.split(".")
    module_file = python_source_root.joinpath(*module_parts).with_suffix(".py")
    package_init = python_source_root.joinpath(*module_parts, "__init__.py")
    if module_file.is_file() or package_init.is_file():
        return
    raise ValueError(
        "Hosted-pack bootstrap preflight could not resolve the integration module beneath "
        "the declared pack python root: "
        f"{integration_module} under {python_root}/src"
    )


def _run_workspace_sync(repo_root: Path) -> None:
    core_python_root = repo_root / "core" / "python"
    completed = subprocess.run(
        ["uv", "sync"],
        cwd=core_python_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode == 0:
        return
    stderr = completed.stderr.strip()
    stdout = completed.stdout.strip()
    detail = stderr or stdout or "uv sync failed without output."
    raise ValueError(f"Hosted-pack bootstrap could not sync the shared workspace: {detail}")


def _best_effort_workspace_resync(repo_root: Path) -> None:
    try:
        _run_workspace_sync(repo_root)
    except Exception:
        return


def _restore_workspace_files(
    *,
    pack_registry_path: Path,
    original_registry_text: str,
    pyproject_path: Path,
    original_pyproject_text: str,
    original_workspace_file_texts: dict[Path, str | None],
) -> None:
    pack_registry_path.write_text(original_registry_text, encoding="utf-8")
    pyproject_path.write_text(original_pyproject_text, encoding="utf-8")
    for path, original_text in original_workspace_file_texts.items():
        if original_text is None:
            if path.exists():
                path.unlink()
            continue
        path.write_text(original_text, encoding="utf-8")


def _rebuild_shared_discovery_surfaces(repo_root: Path) -> None:
    from watchtower_core.sync.reference_index import ReferenceIndexSyncService
    from watchtower_core.sync.repository_paths import RepositoryPathIndexSyncService
    from watchtower_core.sync.route_index import RouteIndexSyncService
    from watchtower_core.sync.standard_index import StandardIndexSyncService
    from watchtower_core.sync.workflow_index import WorkflowIndexSyncService

    command_index_module = import_module("watchtower_host.cli.command_index")
    command_index_service_class = command_index_module.CommandIndexSyncService
    loader = ControlPlaneLoader(repo_root)
    command_index_service = command_index_service_class(loader)
    command_index_document = command_index_service.build_document()
    command_index_service.write_document(command_index_document)

    repository_path_service = RepositoryPathIndexSyncService(loader)
    repository_path_document = repository_path_service.build_document()
    repository_path_service.write_document(repository_path_document)

    reference_index_service = ReferenceIndexSyncService(loader)
    reference_index_document = reference_index_service.build_document()
    reference_index_service.write_document(reference_index_document)

    standard_index_service = StandardIndexSyncService(loader)
    standard_index_document = standard_index_service.build_document()
    standard_index_service.write_document(standard_index_document)

    workflow_index_service = WorkflowIndexSyncService(loader)
    workflow_index_document = workflow_index_service.build_document()
    workflow_index_service.write_document(workflow_index_document)

    route_index_service = RouteIndexSyncService(loader)
    route_index_document = route_index_service.build_document()
    route_index_service.write_document(route_index_document)


def _snapshot_optional_texts(paths: tuple[Path, ...]) -> dict[Path, str | None]:
    return {
        path: (path.read_text(encoding="utf-8") if path.exists() else None) for path in paths
    }


def _validate_relative_path(relative_path: str) -> str:
    candidate = PurePosixPath(relative_path.strip())
    if not relative_path.strip():
        raise ValueError("pack_settings_path is required.")
    if candidate.is_absolute() or any(part == ".." for part in candidate.parts):
        raise ValueError("pack_settings_path must stay repository-relative and portable.")
    return candidate.as_posix()


__all__ = [
    "PackBootstrapRequest",
    "PackBootstrapResult",
    "bootstrap_hosted_pack",
]
