"""Hosted-pack bootstrap helpers for shared registry and workspace installation."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from watchtower_core.control_plane.loader import (
    PACK_REGISTRY_PATH,
    ControlPlaneLoader,
)
from watchtower_core.pack_integration.workspace_registration import (
    CORE_PYPROJECT_RELATIVE_PATH,
    CORE_UV_LOCK_RELATIVE_PATH,
    CorePythonWorkspaceRegistration,
    core_python_workspace_registration,
    render_core_python_workspace_pyproject,
)


@dataclass(frozen=True, slots=True)
class PackBootstrapRequest:
    """Parameters for registering one hosted pack into the shared workspace."""

    pack_settings_path: str
    write: bool = False
    sync_workspace: bool = True


@dataclass(frozen=True, slots=True)
class PackBootstrapResult:
    """Summary of one hosted-pack bootstrap operation."""

    pack_slug: str
    pack_settings_path: str
    pack_runtime_manifest_path: str
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

    pack_registry_path = repo_root / PACK_REGISTRY_PATH
    pyproject_path = repo_root / CORE_PYPROJECT_RELATIVE_PATH
    uv_lock_path = repo_root / CORE_UV_LOCK_RELATIVE_PATH

    registry_document = json.loads(pack_registry_path.read_text(encoding="utf-8"))
    updated_registry_document, pack_registry_changed = _updated_pack_registry_document(
        registry_document,
        pack_registry_entry,
    )
    current_pyproject_text = pyproject_path.read_text(encoding="utf-8")
    updated_pyproject_text, core_python_pyproject_changed = render_core_python_workspace_pyproject(
        current_pyproject_text,
        registration,
    )

    changed_paths = []
    if pack_registry_changed:
        changed_paths.append(PACK_REGISTRY_PATH)
    if core_python_pyproject_changed:
        changed_paths.append(CORE_PYPROJECT_RELATIVE_PATH)
    if (
        request.sync_workspace
        and request.write
        and (pack_registry_changed or core_python_pyproject_changed)
    ):
        changed_paths.append(CORE_UV_LOCK_RELATIVE_PATH)

    if not request.write:
        return PackBootstrapResult(
            pack_slug=runtime_manifest.pack_slug,
            pack_settings_path=pack_settings_path,
            pack_runtime_manifest_path=pack_runtime_manifest_path,
            pack_registry_entry=pack_registry_entry,
            core_python_workspace_registration=registration,
            pack_registry_changed=pack_registry_changed,
            core_python_pyproject_changed=core_python_pyproject_changed,
            workspace_sync_ran=False,
            workspace_sync_required=(
                request.sync_workspace and (pack_registry_changed or core_python_pyproject_changed)
            ),
            validation_passed=None,
            changed_paths=tuple(changed_paths),
            wrote=False,
        )

    original_registry_text = pack_registry_path.read_text(encoding="utf-8")
    original_pyproject_text = current_pyproject_text
    original_uv_lock_text = (
        uv_lock_path.read_text(encoding="utf-8") if uv_lock_path.exists() else None
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
        if request.sync_workspace and (pack_registry_changed or core_python_pyproject_changed):
            _run_workspace_sync(repo_root)
            workspace_sync_ran = True
        if workspace_sync_ran or not (pack_registry_changed or core_python_pyproject_changed):
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
            uv_lock_path=uv_lock_path,
            original_uv_lock_text=original_uv_lock_text,
        )
        if workspace_sync_ran:
            _best_effort_workspace_resync(repo_root)
        raise

    return PackBootstrapResult(
        pack_slug=runtime_manifest.pack_slug,
        pack_settings_path=pack_settings_path,
        pack_runtime_manifest_path=pack_runtime_manifest_path,
        pack_registry_entry=pack_registry_entry,
        core_python_workspace_registration=registration,
        pack_registry_changed=pack_registry_changed,
        core_python_pyproject_changed=core_python_pyproject_changed,
        workspace_sync_ran=workspace_sync_ran,
        workspace_sync_required=(
            not workspace_sync_ran and (pack_registry_changed or core_python_pyproject_changed)
        ),
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
        _raise_conflict_if_present(entry, candidate_entry)
        updated_packs.append(entry)

    if not matched_existing:
        updated_packs.append(candidate_entry)
        changed = True

    sorted_packs = sorted(
        updated_packs,
        key=lambda entry: (
            not bool(entry.get("default_repo_pack", False)),
            str(entry["pack_slug"]).casefold(),
        ),
    )
    updated_document = {**registry_document, "packs": sorted_packs}
    return updated_document, changed


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
    uv_lock_path: Path,
    original_uv_lock_text: str | None,
) -> None:
    pack_registry_path.write_text(original_registry_text, encoding="utf-8")
    pyproject_path.write_text(original_pyproject_text, encoding="utf-8")
    if original_uv_lock_text is None:
        if uv_lock_path.exists():
            uv_lock_path.unlink()
        return
    uv_lock_path.write_text(original_uv_lock_text, encoding="utf-8")


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
