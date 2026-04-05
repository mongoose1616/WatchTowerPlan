"""Reusable directory cleanup and atomic-write helpers for export pipelines."""

from __future__ import annotations

import contextlib
import os
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from watchtower_core.pack_integration.export import (
    PackExportCleanupRequest,
    PackExportCleanupResult,
)

# ---------------------------------------------------------------------------
# Low-level utilities
# ---------------------------------------------------------------------------


def clear_directory_contents(
    output_root: Path,
    relative_root: str,
    *,
    keep_filenames: frozenset[str] = frozenset(),
) -> tuple[str, ...]:
    """Remove directory children, optionally preserving named files.

    Returns repo-relative POSIX paths of all removed entries.
    """

    root = output_root / relative_root
    if not root.exists() or not root.is_dir():
        return ()

    scrubbed_paths: list[str] = []
    for candidate in sorted(root.iterdir()):
        if keep_filenames and candidate.is_file() and candidate.name in keep_filenames:
            continue
        if candidate.is_dir():
            shutil.rmtree(candidate)
        else:
            candidate.unlink()
        scrubbed_paths.append(candidate.relative_to(output_root).as_posix())
    return tuple(scrubbed_paths)


def remove_if_exists(output_root: Path, relative_path: str) -> tuple[str, ...]:
    """Remove a file or clear a directory at *relative_path* under *output_root*.

    Returns repo-relative POSIX paths of all removed entries.
    """

    candidate = output_root / relative_path
    if not candidate.exists():
        return ()
    if candidate.is_dir():
        return clear_directory_contents(output_root, relative_path)
    candidate.unlink()
    return (candidate.relative_to(output_root).as_posix(),)


def atomic_write_text(path: Path, content: str) -> None:
    """Write *content* to *path* atomically via a temporary file and rename."""

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_path, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp_path)
        raise


# ---------------------------------------------------------------------------
# Config-driven export cleanup
# ---------------------------------------------------------------------------

ExportRebuildCallback = Callable[
    [Path, PackExportCleanupRequest],
    tuple[tuple[str, ...], tuple[str, ...]],
]
"""Callback ``(output_root, request) -> (scrubbed_paths, changed_paths)``."""


@dataclass(frozen=True, slots=True)
class ScrubSpec:
    """One directory or file to scrub during export cleanup."""

    relative_root: str
    keep_filenames: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True, slots=True)
class PackExportCleanupConfig:
    """Declarative configuration for a pack's export cleanup pipeline.

    *scrub_specs* lists directories whose contents should be removed.
    *remove_paths* lists individual files or directories to remove entirely.
    *rebuild_callback* is an optional pack-specific hook called after scrubbing
    to rebuild derived surfaces; it returns ``(scrubbed_paths, changed_paths)``
    that are merged into the result.
    """

    scrub_specs: tuple[ScrubSpec, ...] = ()
    remove_paths: tuple[str, ...] = ()
    rebuild_callback: ExportRebuildCallback | None = None


def run_export_cleanup(
    config: PackExportCleanupConfig,
    request: PackExportCleanupRequest,
) -> PackExportCleanupResult:
    """Execute a pack export cleanup pipeline from declarative configuration."""

    output_root = Path(request.output_root).expanduser().resolve()
    scrubbed_paths: set[str] = set()
    changed_paths: set[str] = set()

    for spec in config.scrub_specs:
        scrubbed_paths.update(
            clear_directory_contents(
                output_root,
                spec.relative_root,
                keep_filenames=spec.keep_filenames,
            )
        )

    for relative_path in config.remove_paths:
        scrubbed_paths.update(remove_if_exists(output_root, relative_path))

    if config.rebuild_callback is not None:
        extra_scrubbed, extra_changed = config.rebuild_callback(output_root, request)
        scrubbed_paths.update(extra_scrubbed)
        changed_paths.update(extra_changed)

    return PackExportCleanupResult(
        scrubbed_paths=tuple(sorted(scrubbed_paths)),
        changed_paths=tuple(sorted(changed_paths)),
    )
