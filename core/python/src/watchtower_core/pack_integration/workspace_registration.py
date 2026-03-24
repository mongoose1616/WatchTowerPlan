"""Shared core-python workspace registration helpers for hosted packs."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

CORE_PYPROJECT_RELATIVE_PATH = "core/python/pyproject.toml"
CORE_UV_LOCK_RELATIVE_PATH = "core/python/uv.lock"
_CORE_PYTHON_ROOT = Path("core/python")


@dataclass(frozen=True, slots=True)
class CorePythonWorkspaceRegistration:
    """One hosted-pack dependency registration for the shared Python workspace."""

    dependency: str
    uv_source_path: str
    editable: bool = True


@dataclass(frozen=True, slots=True)
class CorePythonWorkspaceState:
    """Parsed dependency and uv-source state from one shared workspace pyproject."""

    dev_dependencies: tuple[str, ...]
    uv_sources: tuple[tuple[str, str, bool], ...]

    def uv_source_map(self) -> dict[str, dict[str, object]]:
        """Return the uv sources as a mutable mapping."""

        return {
            name: {"path": path, "editable": editable} for name, path, editable in self.uv_sources
        }


def core_python_workspace_registration(
    repo_root: Path,
    *,
    python_root: str,
    python_distribution: str,
) -> CorePythonWorkspaceRegistration:
    """Return the shared workspace registration for one hosted pack python root."""

    core_python_root = repo_root / _CORE_PYTHON_ROOT
    source_path = PurePosixPath(
        os.path.relpath(repo_root / python_root, core_python_root)
    ).as_posix()
    return CorePythonWorkspaceRegistration(
        dependency=python_distribution,
        uv_source_path=source_path,
        editable=True,
    )


def load_core_python_workspace_state(pyproject_path: Path) -> CorePythonWorkspaceState:
    """Load the shared workspace dependency state from one pyproject file."""

    return parse_core_python_workspace_state(pyproject_path.read_text(encoding="utf-8"))


def parse_core_python_workspace_state(pyproject_text: str) -> CorePythonWorkspaceState:
    """Parse the shared workspace dependency state from pyproject text."""

    document = tomllib.loads(pyproject_text)
    dev_dependencies = tuple(document["project"]["optional-dependencies"]["dev"])
    uv_sources_document = document["tool"]["uv"]["sources"]
    uv_sources = tuple(
        sorted(
            (
                str(name),
                str(source_document["path"]),
                bool(source_document.get("editable", False)),
            )
            for name, source_document in uv_sources_document.items()
        )
    )
    return CorePythonWorkspaceState(
        dev_dependencies=dev_dependencies,
        uv_sources=uv_sources,
    )


def render_core_python_workspace_pyproject(
    pyproject_text: str,
    registration: CorePythonWorkspaceRegistration,
    *,
    retained_dependencies: tuple[str, ...] | None = None,
) -> tuple[str, bool]:
    """Return updated pyproject text with the hosted-pack registration applied."""

    state = parse_core_python_workspace_state(pyproject_text)
    if retained_dependencies is None:
        dev_dependencies = tuple(
            sorted(
                {*(state.dev_dependencies), registration.dependency},
                key=str.casefold,
            )
        )
        uv_sources = state.uv_source_map()
    else:
        retained = set(retained_dependencies)
        retained.add(registration.dependency)

        pack_dependency_names = {
            name
            for name, path, _editable in state.uv_sources
            if name.startswith("watchtower-") and path.startswith("..")
        }

        dev_dependencies = tuple(
            sorted(
                {
                    dependency
                    for dependency in state.dev_dependencies
                    if dependency not in pack_dependency_names or dependency in retained
                }
                | retained,
                key=str.casefold,
            )
        )
        uv_sources = {
            name: source
            for name, source in state.uv_source_map().items()
            if name not in pack_dependency_names or name in retained
        }
    uv_sources[registration.dependency] = {
        "path": registration.uv_source_path,
        "editable": registration.editable,
    }
    updated_text = _rewrite_dev_dependencies(pyproject_text, dev_dependencies)
    updated_text = _rewrite_uv_sources(updated_text, uv_sources)
    return updated_text, updated_text != pyproject_text


def reconcile_core_python_workspace_pyproject(
    pyproject_text: str,
    *,
    retained_registrations: tuple[CorePythonWorkspaceRegistration, ...] = (),
) -> tuple[str, bool]:
    """Return pyproject text with hosted-pack wiring reconciled to one exact set."""

    state = parse_core_python_workspace_state(pyproject_text)
    retained_map = {
        registration.dependency: {
            "path": registration.uv_source_path,
            "editable": registration.editable,
        }
        for registration in retained_registrations
    }
    pack_dependency_names = {
        name
        for name, path, _editable in state.uv_sources
        if name.startswith("watchtower-") and path.startswith("..")
    }
    dev_dependencies = tuple(
        sorted(
            {
                dependency
                for dependency in state.dev_dependencies
                if dependency not in pack_dependency_names
            }
            | set(retained_map),
            key=str.casefold,
        )
    )
    uv_sources = {
        name: source
        for name, source in state.uv_source_map().items()
        if name not in pack_dependency_names
    }
    uv_sources.update(retained_map)
    updated_text = _rewrite_dev_dependencies(pyproject_text, dev_dependencies)
    updated_text = _rewrite_uv_sources(updated_text, uv_sources)
    return updated_text, updated_text != pyproject_text


def ensure_core_python_workspace_registration(
    pyproject_path: Path,
    registration: CorePythonWorkspaceRegistration,
) -> bool:
    """Persist one hosted-pack workspace registration into the shared pyproject."""

    current_text = pyproject_path.read_text(encoding="utf-8")
    updated_text, changed = render_core_python_workspace_pyproject(
        current_text,
        registration,
    )
    if changed:
        pyproject_path.write_text(updated_text, encoding="utf-8")
    return changed


def _rewrite_dev_dependencies(pyproject_text: str, dependencies: tuple[str, ...]) -> str:
    lines = pyproject_text.splitlines()
    section_start = _find_section_start(lines, "[project.optional-dependencies]")
    dev_start = _find_line(
        lines,
        "dev = [",
        start=section_start + 1,
        end=_find_section_end(lines, section_start),
    )
    dev_end = _find_line(lines, "]", start=dev_start + 1)
    replacement = [
        "dev = [",
        *[f'  "{dependency}",' for dependency in dependencies],
        "]",
    ]
    new_lines = [*lines[:dev_start], *replacement, *lines[dev_end + 1 :]]
    return _join_lines_like_original(pyproject_text, new_lines)


def _rewrite_uv_sources(
    pyproject_text: str,
    uv_sources: dict[str, dict[str, object]],
) -> str:
    lines = pyproject_text.splitlines()
    section_start = _find_section_start(lines, "[tool.uv.sources]")
    section_end = _find_section_end(lines, section_start)
    replacement = [
        "[tool.uv.sources]",
        *[
            (
                f'{name} = {{ path = "{source["path"]}", '
                f"editable = {str(bool(source.get('editable', False))).lower()} }}"
            )
            for name, source in sorted(uv_sources.items(), key=lambda item: item[0].casefold())
        ],
    ]
    new_lines = [*lines[:section_start], *replacement, *lines[section_end:]]
    return _join_lines_like_original(pyproject_text, new_lines)


def _find_section_start(lines: list[str], header: str) -> int:
    for index, line in enumerate(lines):
        if line == header:
            return index
    raise ValueError(f"Missing required pyproject section: {header}")


def _find_section_end(lines: list[str], section_start: int) -> int:
    for index in range(section_start + 1, len(lines)):
        if lines[index].startswith("[") and lines[index].endswith("]"):
            return index
    return len(lines)


def _find_line(lines: list[str], needle: str, *, start: int, end: int | None = None) -> int:
    stop = len(lines) if end is None else end
    for index in range(start, stop):
        if lines[index] == needle:
            return index
    raise ValueError(f"Missing required pyproject line: {needle}")


def _join_lines_like_original(original_text: str, lines: list[str]) -> str:
    return "\n".join(lines) + ("\n" if original_text.endswith("\n") else "")


__all__ = [
    "CORE_PYPROJECT_RELATIVE_PATH",
    "CORE_UV_LOCK_RELATIVE_PATH",
    "CorePythonWorkspaceRegistration",
    "CorePythonWorkspaceState",
    "core_python_workspace_registration",
    "ensure_core_python_workspace_registration",
    "load_core_python_workspace_state",
    "parse_core_python_workspace_state",
    "reconcile_core_python_workspace_pyproject",
    "render_core_python_workspace_pyproject",
]
