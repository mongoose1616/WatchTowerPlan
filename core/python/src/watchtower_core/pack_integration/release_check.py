"""Local release-gate orchestration over validation, schema checks, and export."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.pack_integration.export import (
    PackExportRequest,
    PackExportResult,
    export_hosted_repository,
)
from watchtower_core.pack_integration.runtime import load_pack_validation_runtime
from watchtower_core.validation.all import ValidationAllResult, ValidationAllService
from watchtower_core.validation.models import ValidationResult
from watchtower_core.validation.schema_definition import SchemaDefinitionValidationService


@dataclass(frozen=True, slots=True)
class GitWorktreeEntry:
    """One git worktree status entry."""

    raw_status: str
    path: str
    original_path: str | None = None

    @property
    def tracked(self) -> bool:
        """Return True when the entry reflects a tracked-file change."""

        return self.raw_status != "??"


@dataclass(frozen=True, slots=True)
class GitWorktreeStatus:
    """Summary of the current git worktree state when available."""

    available: bool
    clean: bool | None
    repo_root: str
    git_root: str | None
    entries: tuple[GitWorktreeEntry, ...]
    message: str | None = None

    @property
    def dirty(self) -> bool:
        """Return True when the worktree has any tracked or untracked changes."""

        return bool(self.entries)

    @property
    def tracked_change_count(self) -> int:
        """Return the number of tracked worktree entries."""

        return sum(1 for entry in self.entries if entry.tracked)

    @property
    def untracked_change_count(self) -> int:
        """Return the number of untracked worktree entries."""

        return sum(1 for entry in self.entries if not entry.tracked)


@dataclass(frozen=True, slots=True)
class ReleaseSchemaValidationSummary:
    """One schema-definition validation executed as part of release gating."""

    schema_path: str
    auto_detected: bool
    result: ValidationResult


@dataclass(frozen=True, slots=True)
class ReleaseCheckRequest:
    """Parameters for one local release-gate run."""

    output_root: str
    included_pack_slugs: tuple[str, ...] = ()
    overwrite: bool = False
    pack_only: bool = False
    allow_dirty: bool = False
    schema_paths: tuple[str, ...] = ()
    pack_settings_path: str = PACK_SETTINGS_PATH


@dataclass(frozen=True, slots=True)
class ReleaseCheckResult:
    """Summary of one local release-gate run."""

    output_root: str
    included_pack_slugs: tuple[str, ...]
    export_scope: str
    allow_dirty: bool
    worktree: GitWorktreeStatus
    dirty_worktree_blocked: bool
    requested_schema_paths: tuple[str, ...]
    auto_detected_schema_paths: tuple[str, ...]
    schema_validations: tuple[ReleaseSchemaValidationSummary, ...]
    validation_all_result: ValidationAllResult | None
    export_result: PackExportResult | None
    pack_settings_path: str

    @property
    def passed(self) -> bool:
        """Return True when the release gate completed successfully."""

        if self.dirty_worktree_blocked:
            return False
        if self.validation_all_result is None or not self.validation_all_result.passed:
            return False
        if any(not summary.result.passed for summary in self.schema_validations):
            return False
        if self.export_result is None or not self.export_result.passed:
            return False
        return True


def run_release_check(
    repo_root: Path,
    request: ReleaseCheckRequest,
) -> ReleaseCheckResult:
    """Run the local release gate against the donor repository root."""

    resolved_repo_root = repo_root.resolve()
    normalized_pack_slugs = tuple(dict.fromkeys(request.included_pack_slugs))
    worktree = inspect_git_worktree(resolved_repo_root)
    dirty_blocked = bool(worktree.available and worktree.dirty and not request.allow_dirty)
    requested_schema_paths = tuple(
        dict.fromkeys(
            _normalize_schema_path(resolved_repo_root, schema_path)
            for schema_path in request.schema_paths
        )
    )
    auto_detected_schema_paths = tuple(
        dict.fromkeys(
            entry.path
            for entry in worktree.entries
            if entry.path.endswith(".schema.json")
            and (resolved_repo_root / entry.path).is_file()
        )
    )
    if dirty_blocked:
        return ReleaseCheckResult(
            output_root=str(Path(request.output_root).expanduser().resolve()),
            included_pack_slugs=normalized_pack_slugs,
            export_scope="pack_bundle" if request.pack_only else "repository_bundle",
            allow_dirty=request.allow_dirty,
            worktree=worktree,
            dirty_worktree_blocked=True,
            requested_schema_paths=requested_schema_paths,
            auto_detected_schema_paths=auto_detected_schema_paths,
            schema_validations=(),
            validation_all_result=None,
            export_result=None,
            pack_settings_path=request.pack_settings_path,
        )

    active_pack_settings_path = (
        None if request.pack_settings_path == PACK_SETTINGS_PATH else request.pack_settings_path
    )
    loader = ControlPlaneLoader(
        resolved_repo_root,
        active_pack_settings_path=active_pack_settings_path,
    )
    validation_runtime = load_pack_validation_runtime(
        loader,
        pack_settings_path=request.pack_settings_path,
    )
    suite_id = loader.load_pack_settings(request.pack_settings_path).default_validation_suite_id
    validation_all_result = ValidationAllService(
        loader,
        suite_id=suite_id,
        pack_settings_path=request.pack_settings_path,
        document_semantics_factory=validation_runtime.document_semantics_factory,
        suite_target_resolver=validation_runtime.suite_target_resolver,
    ).run()

    schema_service = SchemaDefinitionValidationService(loader)
    auto_detected_set = set(auto_detected_schema_paths)
    selected_schema_paths = tuple(
        dict.fromkeys((*requested_schema_paths, *auto_detected_schema_paths))
    )
    schema_validations = tuple(
        ReleaseSchemaValidationSummary(
            schema_path=schema_path,
            auto_detected=schema_path in auto_detected_set,
            result=schema_service.validate(schema_path),
        )
        for schema_path in selected_schema_paths
    )

    export_result = export_hosted_repository(
        resolved_repo_root,
        PackExportRequest(
            output_root=request.output_root,
            included_pack_slugs=normalized_pack_slugs,
            overwrite=bool(request.overwrite),
            pack_only=bool(request.pack_only),
        ),
    )
    return ReleaseCheckResult(
        output_root=export_result.output_root,
        included_pack_slugs=export_result.included_pack_slugs,
        export_scope=export_result.export_scope,
        allow_dirty=request.allow_dirty,
        worktree=worktree,
        dirty_worktree_blocked=False,
        requested_schema_paths=requested_schema_paths,
        auto_detected_schema_paths=auto_detected_schema_paths,
        schema_validations=schema_validations,
        validation_all_result=validation_all_result,
        export_result=export_result,
        pack_settings_path=request.pack_settings_path,
    )


def inspect_git_worktree(repo_root: Path) -> GitWorktreeStatus:
    """Return git worktree status when the repository root is inside a git worktree."""

    resolved_repo_root = repo_root.resolve()
    git_root = _git_toplevel(resolved_repo_root)
    if git_root is None:
        return GitWorktreeStatus(
            available=False,
            clean=None,
            repo_root=str(resolved_repo_root),
            git_root=None,
            entries=(),
            message="Git metadata is not available for the current repository root.",
        )

    status = subprocess.run(
        [
            "git",
            "-C",
            str(resolved_repo_root),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if status.returncode != 0:
        return GitWorktreeStatus(
            available=False,
            clean=None,
            repo_root=str(resolved_repo_root),
            git_root=str(git_root),
            entries=(),
            message=status.stderr.strip() or "Unable to inspect git worktree state.",
        )

    entries = tuple(
        entry
        for line in status.stdout.splitlines()
        if (entry := _parse_git_status_line(line)) is not None
    )
    return GitWorktreeStatus(
        available=True,
        clean=not entries,
        repo_root=str(resolved_repo_root),
        git_root=str(git_root),
        entries=entries,
    )


def _git_toplevel(repo_root: Path) -> Path | None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None
    if completed.returncode != 0:
        return None
    candidate = completed.stdout.strip()
    if not candidate:
        return None
    return Path(candidate).resolve()


def _parse_git_status_line(line: str) -> GitWorktreeEntry | None:
    stripped = line.rstrip()
    if len(stripped) < 4:
        return None
    raw_status = stripped[:2]
    path_text = stripped[3:]
    original_path = None
    if " -> " in path_text:
        original_path, path_text = path_text.split(" -> ", 1)
    return GitWorktreeEntry(
        raw_status=raw_status,
        path=Path(path_text).as_posix(),
        original_path=Path(original_path).as_posix() if original_path else None,
    )


def _normalize_schema_path(repo_root: Path, schema_path: str) -> str:
    candidate = Path(schema_path).expanduser()
    if not candidate.is_absolute():
        return candidate.as_posix()
    resolved = candidate.resolve()
    try:
        return resolved.relative_to(repo_root).as_posix()
    except ValueError:
        return str(resolved)


__all__ = [
    "GitWorktreeEntry",
    "GitWorktreeStatus",
    "ReleaseCheckRequest",
    "ReleaseCheckResult",
    "ReleaseSchemaValidationSummary",
    "inspect_git_worktree",
    "run_release_check",
]
