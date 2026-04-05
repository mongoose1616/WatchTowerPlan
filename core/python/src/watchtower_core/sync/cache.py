"""Persistent incremental cache helpers for deterministic document sync services."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Literal, Protocol, runtime_checkable

from jsonschema import ValidationError

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_settings_discovery import (
    discover_pack_settings_paths,
)
from watchtower_core.control_plane.schemas import SchemaResolutionError
from watchtower_core.pack_integration.docs import pack_command_docs_root
from watchtower_core.pack_integration.roots import discover_pack_workspace_roots

SYNC_CACHE_FALLBACK_ROOT = "core/python/.cache/watchtower/sync_cache"
SYNC_CACHE_MANIFEST_VERSION = 1
SyncCacheStatus = Literal["disabled", "hit", "miss"]
_REPO_ROOT_SEGMENTS = frozenset({"core", "plan"})


@dataclass(frozen=True, slots=True)
class SyncCacheInputSpec:
    """Declared tracked inputs used to fingerprint one deterministic sync surface."""

    tracked_paths: tuple[str, ...]
    extra_marker_values: tuple[str, ...] = ()


@runtime_checkable
class SyncCacheAwareDocumentService(Protocol):
    """Protocol for document sync services that support persistent incremental caching."""

    def sync_cache_inputs(self) -> SyncCacheInputSpec:
        """Return the tracked repo-relative files or directories for this service."""


@dataclass(frozen=True, slots=True)
class PreparedDocumentSyncCache:
    """Prepared cache state for one document sync execution."""

    cache_status: SyncCacheStatus
    input_file_count: int
    document: dict[str, object] | None
    canonical_output_path: Path
    relative_output_path: str
    service_id: str | None = None
    tracked_paths: tuple[str, ...] = ()
    extra_marker_values: tuple[str, ...] = ()
    manifest_path: Path | None = None
    fingerprint: str | None = None
    input_states: tuple[_TrackedFileState, ...] = ()


@dataclass(frozen=True, slots=True)
class _TrackedFileState:
    """One tracked input file fingerprint reused across sync runs."""

    path: str
    size: int
    mtime_ns: int
    sha256: str


def module_relative_path(repo_root: Path, module_file: str) -> str:
    """Return one repo-relative module path suitable for cache tracking."""

    resolved_module_path = Path(module_file).resolve()
    resolved_repo_root = repo_root.resolve()
    try:
        return resolved_module_path.relative_to(resolved_repo_root).as_posix()
    except ValueError:
        parts = resolved_module_path.parts
        for index in range(1, len(parts)):
            candidate = Path(*parts[index:])
            if (resolved_repo_root / candidate).exists():
                return candidate.as_posix()
        for index, part in enumerate(parts):
            if part not in _REPO_ROOT_SEGMENTS:
                continue
            return Path(*parts[index:]).as_posix()
        raise


def ordered_sync_cache_paths(*groups: str | tuple[str, ...]) -> tuple[str, ...]:
    """Return one stable deduplicated tuple of candidate tracked paths."""

    ordered: list[str] = []
    seen: set[str] = set()
    for group in groups:
        candidates = (group,) if isinstance(group, str) else group
        for candidate in candidates:
            normalized = candidate.strip().rstrip("/")
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            ordered.append(normalized)
    return tuple(ordered)


def discover_pack_sync_cache_paths(
    loader: ControlPlaneLoader,
    *,
    include_command_docs: bool = False,
    include_reference_docs: bool = False,
    include_standard_docs: bool = False,
    include_workflows: bool = False,
    include_python_sources: bool = False,
    include_workspace_sources: bool = False,
    include_tracking: bool = False,
    include_machine_manifests: bool = True,
    include_machine_registries: bool = False,
) -> tuple[str, ...]:
    """Return stable pack-owned roots that can affect deterministic sync outputs."""

    repo_root = loader.repo_root
    tracked_paths: list[str] = [
        "core/control_plane/registries/pack_registry.json",
        *discover_pack_settings_paths(repo_root),
    ]
    for roots in discover_pack_workspace_roots(repo_root, loader=loader):
        if include_machine_manifests:
            tracked_paths.append(f"{roots.machine_root}/manifests")
        if include_machine_registries:
            tracked_paths.append(f"{roots.machine_root}/registries")
        if include_command_docs:
            tracked_paths.append(pack_command_docs_root(docs_root=roots.docs_root))
        if include_reference_docs:
            tracked_paths.append(f"{roots.docs_root}/references")
        if include_standard_docs:
            tracked_paths.append(f"{roots.docs_root}/standards")
        if include_workflows:
            tracked_paths.extend(
                (
                    f"{roots.workflows_root}/ROUTING_TABLE.md",
                    f"{roots.workflows_root}/modules",
                    f"{roots.workflows_root}/roles",
                )
            )
        if include_python_sources:
            tracked_paths.append(f"{roots.workspace_root}/python/src")
        if include_tracking:
            tracked_paths.append(roots.tracking_root)
        if include_workspace_sources:
            if roots.initiatives_root is not None:
                tracked_paths.append(roots.initiatives_root)
            if roots.projects_root is not None:
                tracked_paths.append(roots.projects_root)
            tracked_paths.extend(path for _, path in roots.domain_roots)
    return ordered_sync_cache_paths(tuple(tracked_paths))


def prepare_document_sync_cache(
    loader: ControlPlaneLoader,
    service: object,
    *,
    relative_output_path: str,
) -> PreparedDocumentSyncCache:
    """Prepare cache metadata and load the cached canonical document when available."""

    canonical_output_path = loader.workspace_config.resolve_path(relative_output_path)
    if not isinstance(service, SyncCacheAwareDocumentService):
        return PreparedDocumentSyncCache(
            cache_status="disabled",
            input_file_count=0,
            document=None,
            canonical_output_path=canonical_output_path,
            relative_output_path=relative_output_path,
        )

    spec = service.sync_cache_inputs()
    if not spec.tracked_paths:
        return PreparedDocumentSyncCache(
            cache_status="disabled",
            input_file_count=0,
            document=None,
            canonical_output_path=canonical_output_path,
            relative_output_path=relative_output_path,
        )

    service_id = _service_id(service)
    manifest_path = _manifest_path_for(
        loader, service_id=service_id, relative_output_path=relative_output_path
    )
    manifest = _load_manifest(manifest_path)
    previous_states = _manifest_states_by_path(manifest)
    expanded_paths = _expand_tracked_paths(
        loader,
        tracked_paths=spec.tracked_paths,
        exclude_relative_path=relative_output_path,
    )
    input_states = tuple(
        _tracked_file_state(
            loader.workspace_config.resolve_path(path),
            path=path,
            previous=previous_states.get(path),
        )
        for path in expanded_paths
    )
    fingerprint = _fingerprint_for(
        service_id=service_id,
        relative_output_path=relative_output_path,
        extra_marker_values=spec.extra_marker_values,
        input_states=input_states,
    )
    current_output_hash = (
        _file_sha256(canonical_output_path) if canonical_output_path.exists() else None
    )
    cached_document = _load_cached_document(
        manifest,
        fingerprint=fingerprint,
        current_output_hash=current_output_hash,
        canonical_output_path=canonical_output_path,
    )
    return PreparedDocumentSyncCache(
        cache_status=("hit" if cached_document is not None else "miss"),
        input_file_count=len(input_states),
        document=cached_document,
        canonical_output_path=canonical_output_path,
        relative_output_path=relative_output_path,
        service_id=service_id,
        tracked_paths=spec.tracked_paths,
        extra_marker_values=spec.extra_marker_values,
        manifest_path=manifest_path,
        fingerprint=fingerprint,
        input_states=input_states,
    )


def finalize_document_sync_cache(
    prepared: PreparedDocumentSyncCache,
    *,
    document: dict[str, object],
) -> None:
    """Persist the cache manifest when the canonical output matches the built document."""

    if prepared.cache_status == "disabled":
        return
    if (
        prepared.manifest_path is None
        or prepared.fingerprint is None
        or prepared.service_id is None
    ):
        return
    canonical_output_path = prepared.canonical_output_path
    if not canonical_output_path.exists():
        return
    current_document = _load_json_object(canonical_output_path)
    if current_document != document:
        return

    manifest = {
        "manifest_version": SYNC_CACHE_MANIFEST_VERSION,
        "service_id": prepared.service_id,
        "relative_output_path": prepared.relative_output_path,
        "tracked_paths": list(prepared.tracked_paths),
        "extra_marker_values": list(prepared.extra_marker_values),
        "input_file_count": len(prepared.input_states),
        "fingerprint": prepared.fingerprint,
        "output_hash": _file_sha256(canonical_output_path),
        "input_files": [
            {
                "path": state.path,
                "size": state.size,
                "mtime_ns": state.mtime_ns,
                "sha256": state.sha256,
            }
            for state in prepared.input_states
        ],
    }
    prepared.manifest_path.parent.mkdir(parents=True, exist_ok=True)
    prepared.manifest_path.write_text(f"{json.dumps(manifest, indent=2)}\n", encoding="utf-8")


def validate_prepared_document_sync_cache(
    loader: ControlPlaneLoader,
    prepared: PreparedDocumentSyncCache | None,
) -> PreparedDocumentSyncCache | None:
    """Downgrade cached hits to misses when the cached canonical document no longer validates."""

    if prepared is None or prepared.document is None:
        return prepared
    try:
        loader.schema_store.validate_instance(prepared.document)
    except (SchemaResolutionError, ValidationError):
        return replace(prepared, cache_status="miss", document=None)
    return prepared


def resolve_sync_cache_root(loader: ControlPlaneLoader) -> Path:
    """Return the runtime cache root for reusable deterministic sync surfaces."""

    try:
        pack_settings_path = loader.active_pack_settings_path or loader.default_pack_settings_path()
        pack_settings = loader.load_pack_settings(pack_settings_path)
        machine_root = pack_settings.workspace_roots.machine_root.rstrip("/")
        if machine_root and machine_root != "core/control_plane":
            return loader.workspace_config.resolve_path(machine_root) / "runtime" / "sync_cache"
    except Exception:
        pass
    return loader.workspace_config.resolve_path(SYNC_CACHE_FALLBACK_ROOT)


def _service_id(service: object) -> str:
    service_type = type(service)
    return f"{service_type.__module__}.{service_type.__qualname__}"


def _manifest_path_for(
    loader: ControlPlaneLoader,
    *,
    service_id: str,
    relative_output_path: str,
) -> Path:
    digest = hashlib.sha256(f"{service_id}::{relative_output_path}".encode()).hexdigest()
    return resolve_sync_cache_root(loader) / f"{digest}.json"


def _load_manifest(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    document = _load_json_object(path)
    if document is None:
        return None
    if document.get("manifest_version") != SYNC_CACHE_MANIFEST_VERSION:
        return None
    return document


def _manifest_states_by_path(manifest: dict[str, Any] | None) -> dict[str, _TrackedFileState]:
    if manifest is None:
        return {}
    entries = manifest.get("input_files")
    if not isinstance(entries, list):
        return {}
    states: dict[str, _TrackedFileState] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        path = entry.get("path")
        size = entry.get("size")
        mtime_ns = entry.get("mtime_ns")
        sha256 = entry.get("sha256")
        if not isinstance(path, str) or not isinstance(size, int) or not isinstance(mtime_ns, int):
            continue
        if not isinstance(sha256, str) or not sha256:
            continue
        states[path] = _TrackedFileState(path=path, size=size, mtime_ns=mtime_ns, sha256=sha256)
    return states


def _expand_tracked_paths(
    loader: ControlPlaneLoader,
    *,
    tracked_paths: tuple[str, ...],
    exclude_relative_path: str,
) -> tuple[str, ...]:
    expanded: list[str] = []
    seen: set[str] = set()
    for tracked_path in tracked_paths:
        resolved_path = loader.workspace_config.resolve_path(tracked_path)
        if not resolved_path.exists():
            continue
        if resolved_path.is_file():
            logical_path = loader.workspace_config.logical_path_for(resolved_path)
            _append_tracked_path(
                expanded,
                seen,
                logical_path=logical_path,
                exclude_relative_path=exclude_relative_path,
            )
            continue
        for candidate in sorted(path for path in resolved_path.rglob("*") if path.is_file()):
            logical_path = loader.workspace_config.logical_path_for(candidate)
            _append_tracked_path(
                expanded,
                seen,
                logical_path=logical_path,
                exclude_relative_path=exclude_relative_path,
            )
    return tuple(expanded)


def _append_tracked_path(
    expanded: list[str],
    seen: set[str],
    *,
    logical_path: str,
    exclude_relative_path: str,
) -> None:
    if logical_path == exclude_relative_path:
        return
    if _ignored_runtime_cache_input(logical_path):
        return
    if logical_path in seen:
        return
    seen.add(logical_path)
    expanded.append(logical_path)


def _ignored_runtime_cache_input(logical_path: str) -> bool:
    normalized = logical_path.rstrip("/")
    marker = f"/{normalized}"
    return (
        normalized.startswith("core/python/.cache/")
        or "/.wt/runtime/" in marker
        or "/__pycache__/" in marker
        or "/.pytest_cache/" in marker
        or "/.mypy_cache/" in marker
        or "/.ruff_cache/" in marker
        or normalized.endswith((".pyc", ".pyo", ".pyd"))
    )


def _tracked_file_state(
    resolved_path: Path,
    *,
    path: str,
    previous: _TrackedFileState | None,
) -> _TrackedFileState:
    stat = resolved_path.stat()
    if (
        previous is not None
        and previous.size == stat.st_size
        and previous.mtime_ns == stat.st_mtime_ns
    ):
        return _TrackedFileState(
            path=path,
            size=previous.size,
            mtime_ns=previous.mtime_ns,
            sha256=previous.sha256,
        )
    return _TrackedFileState(
        path=path,
        size=stat.st_size,
        mtime_ns=stat.st_mtime_ns,
        sha256=_file_sha256(resolved_path),
    )


def _fingerprint_for(
    *,
    service_id: str,
    relative_output_path: str,
    extra_marker_values: tuple[str, ...],
    input_states: tuple[_TrackedFileState, ...],
) -> str:
    digest = hashlib.sha256()
    digest.update(service_id.encode("utf-8"))
    digest.update(b"\n")
    digest.update(relative_output_path.encode("utf-8"))
    for marker in extra_marker_values:
        digest.update(b"\n")
        digest.update(marker.encode("utf-8"))
    for state in input_states:
        digest.update(b"\n")
        digest.update(state.path.encode("utf-8"))
        digest.update(b":")
        digest.update(state.sha256.encode("utf-8"))
    return digest.hexdigest()


def _load_cached_document(
    manifest: dict[str, Any] | None,
    *,
    fingerprint: str,
    current_output_hash: str | None,
    canonical_output_path: Path,
) -> dict[str, object] | None:
    if manifest is None:
        return None
    if manifest.get("fingerprint") != fingerprint:
        return None
    if manifest.get("output_hash") != current_output_hash:
        return None
    return _load_json_object(canonical_output_path)


def _load_json_object(path: Path) -> dict[str, object] | None:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(loaded, dict):
        return None
    return loaded


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


__all__ = [
    "discover_pack_sync_cache_paths",
    "ordered_sync_cache_paths",
    "PreparedDocumentSyncCache",
    "SYNC_CACHE_FALLBACK_ROOT",
    "SYNC_CACHE_MANIFEST_VERSION",
    "SyncCacheAwareDocumentService",
    "SyncCacheInputSpec",
    "SyncCacheStatus",
    "finalize_document_sync_cache",
    "module_relative_path",
    "prepare_document_sync_cache",
    "resolve_sync_cache_root",
    "validate_prepared_document_sync_cache",
]
