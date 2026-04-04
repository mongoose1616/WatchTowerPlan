"""Hosted-pack bootstrap helpers for shared registry and workspace installation."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import (
    PACK_REGISTRY_PATH,
    ControlPlaneLoader,
)
from watchtower_core.pack_integration.runtime import load_pack_sync_runtime
from watchtower_core.pack_integration.runtime_registry import load_pack_registry_runtime_view
from watchtower_core.pack_integration.workspace_registration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    CORE_UV_LOCK_RELATIVE_PATH,
    CorePythonWorkspaceRegistration,
    core_python_workspace_registration,
    render_core_python_workspace_pyproject,
)
from watchtower_core.sync.cache import (
    finalize_document_sync_cache,
    prepare_document_sync_cache,
    validate_prepared_document_sync_cache,
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
    sync_extras: tuple[str, ...] = ()
    replace_hosted_packs: bool = False
    enable_runtime_cache: bool = True


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
    workspace_sync_extras: tuple[str, ...]
    pack_sync_targets: tuple[str, ...]
    pack_sync_ran: bool
    pack_sync_required: bool
    validation_passed: bool | None
    changed_paths: tuple[str, ...]
    wrote: bool


@dataclass(frozen=True, slots=True)
class PackLocalSyncAllResult:
    """Parsed result from one pack-local `sync all` invocation."""

    relative_output_paths: tuple[str, ...]


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
    pack_sync_runtime = load_pack_sync_runtime(loader, pack_settings_path=pack_settings_path)
    pack_sync_targets = tuple(dict.fromkeys(pack_sync_runtime.targets))
    pack_sync_declares_all = "all" in pack_sync_targets

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
    effective_pack_registry_entry = _effective_pack_registry_entry(
        updated_registry_document,
        candidate_entry=pack_registry_entry,
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
            pack_registry_entry=effective_pack_registry_entry,
            core_python_workspace_registration=registration,
            pack_registry_changed=pack_registry_changed,
            core_python_pyproject_changed=core_python_pyproject_changed,
            workspace_sync_ran=False,
            workspace_sync_required=request.sync_workspace and core_python_pyproject_changed,
            workspace_sync_extras=tuple(dict.fromkeys(request.sync_extras)),
            pack_sync_targets=pack_sync_targets,
            pack_sync_ran=False,
            pack_sync_required=False,
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
    pack_sync_ran = False
    pack_sync_required = False
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
            rebuild_shared_discovery_surfaces(
                repo_root,
                enable_runtime_cache=request.enable_runtime_cache,
            )
        if request.sync_workspace and core_python_pyproject_changed:
            _run_workspace_sync(
                repo_root,
                extras=tuple(dict.fromkeys(request.sync_extras)),
            )
            workspace_sync_ran = True
        can_run_pack_sync = pack_sync_declares_all and (
            workspace_sync_ran or not core_python_pyproject_changed
        )
        if can_run_pack_sync:
            pack_sync_preview = _run_pack_local_sync_all(
                repo_root=repo_root,
                command_namespace=runtime_manifest.command_namespace,
                write=False,
            )
            pack_sync_paths = tuple(
                repo_root / relative_path
                for relative_path in pack_sync_preview.relative_output_paths
            )
            original_workspace_file_texts.update(_snapshot_optional_texts(pack_sync_paths))
            pack_sync_result = _run_pack_local_sync_all(
                repo_root=repo_root,
                command_namespace=runtime_manifest.command_namespace,
                write=True,
            )
            pack_sync_ran = True
            changed_paths.extend(pack_sync_result.relative_output_paths)
        elif (
            pack_sync_declares_all and core_python_pyproject_changed and not request.sync_workspace
        ):
            pack_sync_required = True
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
            _best_effort_workspace_resync(
                repo_root,
                extras=tuple(dict.fromkeys(request.sync_extras)),
            )
        raise

    return PackBootstrapResult(
        pack_slug=runtime_manifest.pack_slug,
        pack_settings_path=pack_settings_path,
        pack_runtime_manifest_path=pack_runtime_manifest_path,
        replace_hosted_packs=request.replace_hosted_packs,
        scrubbed_pack_slugs=scrubbed_pack_slugs,
        pack_registry_entry=effective_pack_registry_entry,
        core_python_workspace_registration=registration,
        pack_registry_changed=pack_registry_changed,
        core_python_pyproject_changed=core_python_pyproject_changed,
        workspace_sync_ran=workspace_sync_ran,
        workspace_sync_required=not workspace_sync_ran and core_python_pyproject_changed,
        workspace_sync_extras=tuple(dict.fromkeys(request.sync_extras)),
        pack_sync_targets=pack_sync_targets,
        pack_sync_ran=pack_sync_ran,
        pack_sync_required=pack_sync_required,
        validation_passed=validation_passed,
        changed_paths=tuple(dict.fromkeys(changed_paths)),
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
        scrubbed.append(str(entry.get("pack_slug", entry.get("pack_id", "<unknown-pack>"))))
    return tuple(scrubbed)


def _effective_pack_registry_entry(
    registry_document: dict[str, object],
    *,
    candidate_entry: dict[str, object],
) -> dict[str, object]:
    raw_packs = registry_document.get("packs")
    if not isinstance(raw_packs, list):
        return dict(candidate_entry)
    for entry in raw_packs:
        if not isinstance(entry, dict):
            continue
        if _matches_same_pack(entry, candidate_entry):
            return dict(entry)
    return dict(candidate_entry)


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
        candidate_entry.get(key) is not None and existing_entry.get(key) == candidate_entry.get(key)
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
    issue_summary_items = [f"{issue.code}: {issue.message}" for issue in result.issues[:5]]
    remaining_issue_count = len(result.issues) - len(issue_summary_items)
    if remaining_issue_count > 0:
        issue_summary_items.append(f"... and {remaining_issue_count} more")
    issue_summary = "; ".join(issue_summary_items)
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


def _run_workspace_sync(repo_root: Path, *, extras: tuple[str, ...] = ()) -> None:
    core_python_root = repo_root / "core" / "python"
    uv_executable = _resolve_uv_executable()
    command = [uv_executable, "sync"]
    for extra in dict.fromkeys(extras):
        command.extend(("--extra", extra))
    completed = subprocess.run(
        command,
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


def _resolve_uv_executable() -> str:
    candidate = shutil.which("uv")
    if candidate is not None:
        return candidate
    interpreter_sibling = Path(sys.executable).resolve().with_name("uv")
    if interpreter_sibling.is_file():
        return str(interpreter_sibling)
    raise ValueError(
        "Hosted-pack bootstrap could not find the `uv` executable needed for shared "
        "workspace sync. Install `uv` or rerun with --no-sync-workspace."
    )


def _run_pack_local_sync_all(
    *,
    repo_root: Path,
    command_namespace: str,
    write: bool,
) -> PackLocalSyncAllResult:
    command = [
        sys.executable,
        "-m",
        "watchtower_host.cli.main",
        command_namespace,
        "sync",
        "all",
    ]
    if write:
        command.append("--write")
    command.extend(("--format", "json"))
    env = dict(os.environ)
    env["WATCHTOWER_TELEMETRY"] = "off"
    completed = subprocess.run(
        command,
        cwd=repo_root / "core" / "python",
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    if completed.returncode != 0:
        detail = _cli_command_error_detail(completed)
        raise ValueError(
            f"Hosted-pack bootstrap could not run the pack-local sync-all command: {detail}"
        )
    stdout = completed.stdout.strip()
    if not stdout:
        return PackLocalSyncAllResult(relative_output_paths=())
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Hosted-pack bootstrap received non-JSON output from the pack-local "
            f"sync-all command: {exc}"
        ) from exc
    if payload.get("status") != "ok":
        raise ValueError(
            "Hosted-pack bootstrap received an error payload from the pack-local "
            f"sync-all command: {payload!r}"
        )
    raw_results = payload.get("results")
    if not isinstance(raw_results, list):
        return PackLocalSyncAllResult(relative_output_paths=())
    relative_output_paths: list[str] = []
    for entry in raw_results:
        if not isinstance(entry, dict):
            continue
        relative_output_path = entry.get("relative_output_path")
        if not isinstance(relative_output_path, str) or not relative_output_path:
            continue
        relative_output_paths.append(relative_output_path)
    return PackLocalSyncAllResult(relative_output_paths=tuple(dict.fromkeys(relative_output_paths)))


def _cli_command_error_detail(completed: subprocess.CompletedProcess[str]) -> str:
    stdout = completed.stdout.strip()
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            pass
        else:
            message = payload.get("message")
            if isinstance(message, str) and message:
                return message
    stderr = completed.stderr.strip()
    if stderr:
        return stderr
    if stdout:
        return stdout
    return "command failed without output."


def _best_effort_workspace_resync(
    repo_root: Path,
    *,
    extras: tuple[str, ...] = (),
) -> None:
    try:
        _run_workspace_sync(repo_root, extras=extras)
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


def _rebuild_document_sync_surface(
    loader: ControlPlaneLoader,
    service: object,
    *,
    relative_output_path: str,
    enable_runtime_cache: bool,
) -> None:
    prepared_cache = (
        prepare_document_sync_cache(
            loader,
            service,
            relative_output_path=relative_output_path,
        )
        if enable_runtime_cache
        else None
    )
    prepared_cache = validate_prepared_document_sync_cache(loader, prepared_cache)
    document = (
        prepared_cache.document if prepared_cache is not None else None
    ) or service.build_document()
    loader.schema_store.validate_instance(document)
    if prepared_cache is None or prepared_cache.cache_status != "hit":
        service.write_document(document)
    if prepared_cache is not None:
        finalize_document_sync_cache(prepared_cache, document=document)


def rebuild_shared_discovery_surfaces(
    repo_root: Path,
    *,
    enable_runtime_cache: bool = True,
) -> None:
    from watchtower_core.sync.reference_index import ReferenceIndexSyncService
    from watchtower_core.sync.repository_paths import RepositoryPathIndexSyncService
    from watchtower_core.sync.route_index import RouteIndexSyncService
    from watchtower_core.sync.standard_index import StandardIndexSyncService
    from watchtower_core.sync.workflow_index import WorkflowIndexSyncService

    command_index_module = import_module("watchtower_host.cli.command_index")
    command_index_service_class = command_index_module.CommandIndexSyncService
    loader = ControlPlaneLoader(repo_root)
    command_index_service = command_index_service_class(loader)
    _rebuild_document_sync_surface(
        loader,
        command_index_service,
        relative_output_path=COMMAND_INDEX_ARTIFACT_PATH,
        enable_runtime_cache=enable_runtime_cache,
    )

    repository_path_service = RepositoryPathIndexSyncService(loader)
    _rebuild_document_sync_surface(
        loader,
        repository_path_service,
        relative_output_path=REPOSITORY_PATH_INDEX_ARTIFACT_PATH,
        enable_runtime_cache=enable_runtime_cache,
    )

    reference_index_service = ReferenceIndexSyncService(loader)
    _rebuild_document_sync_surface(
        loader,
        reference_index_service,
        relative_output_path=REFERENCE_INDEX_ARTIFACT_PATH,
        enable_runtime_cache=enable_runtime_cache,
    )

    standard_index_service = StandardIndexSyncService(loader)
    _rebuild_document_sync_surface(
        loader,
        standard_index_service,
        relative_output_path=STANDARD_INDEX_ARTIFACT_PATH,
        enable_runtime_cache=enable_runtime_cache,
    )

    workflow_index_service = WorkflowIndexSyncService(loader)
    _rebuild_document_sync_surface(
        loader,
        workflow_index_service,
        relative_output_path=WORKFLOW_INDEX_ARTIFACT_PATH,
        enable_runtime_cache=enable_runtime_cache,
    )

    route_index_service = RouteIndexSyncService(loader)
    _rebuild_document_sync_surface(
        loader,
        route_index_service,
        relative_output_path=ROUTE_INDEX_ARTIFACT_PATH,
        enable_runtime_cache=enable_runtime_cache,
    )


def _snapshot_optional_texts(paths: tuple[Path, ...]) -> dict[Path, str | None]:
    return {path: (path.read_text(encoding="utf-8") if path.exists() else None) for path in paths}


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
    "rebuild_shared_discovery_surfaces",
]
