"""Cleanup helpers for runtime telemetry sinks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.telemetry.runtime import current_session, resolve_telemetry_root


@dataclass(frozen=True, slots=True)
class TelemetryDeleteRequest:
    """Inputs for one telemetry-delete operation."""

    pack_settings_path: str | None = None
    telemetry_root: Path | None = None
    older_than_days: int | None = None
    before: str | None = None
    delete_all: bool = False
    write: bool = False


@dataclass(frozen=True, slots=True)
class TelemetryDeleteResult:
    """Outputs for one telemetry-delete operation."""

    telemetry_root: Path
    pack_settings_path: str | None
    machine_root: str | None
    selection_mode: Literal["all", "before", "older_than_days"]
    cutoff_utc: str | None
    write: bool
    active_session_output_path: str | None
    matched_file_count: int
    matched_directory_count: int
    matched_bytes: int
    deleted_file_count: int
    deleted_directory_count: int
    deleted_bytes: int
    matched_file_paths: tuple[str, ...]
    pruned_directory_paths: tuple[str, ...]


class TelemetryCleanupService:
    """Delete retained runtime telemetry files under one resolved telemetry root."""

    def __init__(self, loader: ControlPlaneLoader | None = None) -> None:
        self._loader = loader or ControlPlaneLoader()

    def delete(self, request: TelemetryDeleteRequest) -> TelemetryDeleteResult:
        selection_mode, cutoff = _validate_delete_request(request)
        telemetry_root, pack_settings_path, machine_root = _resolve_telemetry_root_for_delete(
            self._loader,
            request,
        )
        active_output_path = _active_session_output_path()
        if not telemetry_root.exists():
            return TelemetryDeleteResult(
                telemetry_root=telemetry_root,
                pack_settings_path=pack_settings_path,
                machine_root=machine_root,
                selection_mode=selection_mode,
                cutoff_utc=_format_timestamp(cutoff) if cutoff is not None else None,
                write=request.write,
                active_session_output_path=_display_path(self._loader.repo_root, active_output_path)
                if active_output_path is not None
                else None,
                matched_file_count=0,
                matched_directory_count=0,
                matched_bytes=0,
                deleted_file_count=0,
                deleted_directory_count=0,
                deleted_bytes=0,
                matched_file_paths=(),
                pruned_directory_paths=(),
            )

        telemetry_files = tuple(
            sorted(path for path in telemetry_root.rglob("*.jsonl") if path.is_file())
        )
        matched_files = tuple(
            path
            for path in telemetry_files
            if _matches_delete_filter(
                path,
                selection_mode=selection_mode,
                cutoff=cutoff,
                active_output_path=active_output_path,
            )
        )
        pruned_directories = _directories_pruned_by_delete(
            telemetry_root,
            telemetry_files=telemetry_files,
            matched_files=matched_files,
        )
        matched_bytes = sum(path.stat().st_size for path in matched_files if path.exists())

        deleted_files: list[Path] = []
        deleted_bytes = 0
        deleted_directories: list[Path] = []
        if request.write:
            for path in matched_files:
                if not path.exists():
                    continue
                size = path.stat().st_size
                path.unlink()
                deleted_files.append(path)
                deleted_bytes += size
            for path in pruned_directories:
                if not path.exists():
                    continue
                path.rmdir()
                deleted_directories.append(path)

        return TelemetryDeleteResult(
            telemetry_root=telemetry_root,
            pack_settings_path=pack_settings_path,
            machine_root=machine_root,
            selection_mode=selection_mode,
            cutoff_utc=_format_timestamp(cutoff) if cutoff is not None else None,
            write=request.write,
            active_session_output_path=_display_path(self._loader.repo_root, active_output_path)
            if active_output_path is not None
            else None,
            matched_file_count=len(matched_files),
            matched_directory_count=len(pruned_directories),
            matched_bytes=matched_bytes,
            deleted_file_count=len(deleted_files),
            deleted_directory_count=len(deleted_directories),
            deleted_bytes=deleted_bytes,
            matched_file_paths=tuple(
                _display_path(self._loader.repo_root, path) for path in matched_files
            ),
            pruned_directory_paths=tuple(
                _display_path(self._loader.repo_root, path) for path in pruned_directories
            ),
        )


def _validate_delete_request(
    request: TelemetryDeleteRequest,
) -> tuple[Literal["all", "before", "older_than_days"], datetime | None]:
    if request.telemetry_root is not None and request.pack_settings_path is not None:
        raise ValueError(
            "telemetry delete accepts either --telemetry-root or --pack-settings-path, not both."
        )
    active_modes = sum(
        (
            1 if request.delete_all else 0,
            1 if request.before and request.before.strip() else 0,
            1 if request.older_than_days is not None else 0,
        )
    )
    if active_modes != 1:
        raise ValueError(
            "telemetry delete requires exactly one of --all, --before, or --older-than-days."
        )
    if request.older_than_days is not None:
        if request.older_than_days < 0:
            raise ValueError("--older-than-days must be >= 0.")
        return ("older_than_days", datetime.now(UTC) - timedelta(days=request.older_than_days))
    if request.before and request.before.strip():
        return ("before", _parse_before_value(request.before))
    return ("all", None)


def _resolve_telemetry_root_for_delete(
    loader: ControlPlaneLoader,
    request: TelemetryDeleteRequest,
) -> tuple[Path, str | None, str | None]:
    if request.telemetry_root is not None:
        candidate = request.telemetry_root.resolve()
        if candidate.name != "telemetry":
            raise ValueError(
                "--telemetry-root must point at the telemetry root directory named `telemetry`."
            )
        if candidate.exists() and not candidate.is_dir():
            raise ValueError(f"Telemetry root is not a directory: {candidate}")
        return (candidate, None, None)
    return resolve_telemetry_root(loader, pack_settings_path=request.pack_settings_path)


def _parse_before_value(value: str) -> datetime:
    normalized = value.strip()
    if not normalized:
        raise ValueError("--before requires a non-empty ISO timestamp or YYYY-MM-DD date.")
    if len(normalized) == 10 and normalized.count("-") == 2:
        try:
            return datetime.fromisoformat(normalized).replace(tzinfo=UTC)
        except ValueError as exc:
            raise ValueError("--before must be an ISO timestamp or YYYY-MM-DD date.") from exc
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("--before must be an ISO timestamp or YYYY-MM-DD date.") from exc
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _active_session_output_path() -> Path | None:
    session = current_session()
    if session is None or session.output_path is None:
        return None
    return session.output_path.resolve()


def _matches_delete_filter(
    path: Path,
    *,
    selection_mode: Literal["all", "before", "older_than_days"],
    cutoff: datetime | None,
    active_output_path: Path | None,
) -> bool:
    resolved_path = path.resolve()
    if active_output_path is not None and resolved_path == active_output_path:
        return False
    if selection_mode == "all":
        return True
    if cutoff is None:
        raise ValueError("cutoff is required when selection_mode is not 'all'")
    modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    return modified_at < cutoff


def _directories_pruned_by_delete(
    telemetry_root: Path,
    *,
    telemetry_files: tuple[Path, ...],
    matched_files: tuple[Path, ...],
) -> tuple[Path, ...]:
    removed_files = {path.resolve() for path in matched_files}
    directories = sorted(
        (
            path
            for path in telemetry_root.rglob("*")
            if path.is_dir() and path.resolve() != telemetry_root.resolve()
        ),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    removed_directories: set[Path] = set()
    retained: list[Path] = []
    for directory in directories:
        if _directory_would_be_empty(
            directory,
            removed_files=removed_files,
            removed_directories=removed_directories,
        ):
            removed_directories.add(directory.resolve())
            retained.append(directory)
    return tuple(retained)


def _directory_would_be_empty(
    directory: Path,
    *,
    removed_files: set[Path],
    removed_directories: set[Path],
) -> bool:
    for child in directory.iterdir():
        resolved_child = child.resolve()
        if resolved_child in removed_files or resolved_child in removed_directories:
            continue
        return False
    return True


def _display_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _format_timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


__all__ = [
    "TelemetryCleanupService",
    "TelemetryDeleteRequest",
    "TelemetryDeleteResult",
]
