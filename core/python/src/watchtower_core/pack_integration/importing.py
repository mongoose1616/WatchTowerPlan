"""Helpers for importing hosted-pack integrations during runtime composition."""

from __future__ import annotations

import sys
from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType


def import_pack_integration_module(
    *,
    repo_root: Path,
    integration_module: str,
    python_package: str,
    python_root: str,
) -> tuple[ModuleType, str]:
    """Import one pack integration module with a bounded bootstrap fallback.

    The preferred path remains the shared `core/python` workspace registration.
    When a consuming repository has copied `core/` and the hosted pack exists
    locally but has not yet been bootstrapped into `core/python/pyproject.toml`,
    fall back to the declared `<python_root>/src` path for this one import.
    """

    try:
        return import_module(integration_module), "workspace"
    except ModuleNotFoundError as exc:
        if not _matches_pack_module_lookup(exc, python_package):
            raise
        return (
            _import_module_from_pack_root(
                repo_root=repo_root,
                integration_module=integration_module,
                python_package=python_package,
                python_root=python_root,
            ),
            "pack_python_root",
        )


def _matches_pack_module_lookup(exc: ModuleNotFoundError, python_package: str) -> bool:
    missing_name = getattr(exc, "name", None)
    if not isinstance(missing_name, str):
        return False
    return missing_name == python_package or missing_name.startswith(f"{python_package}.")


def _import_module_from_pack_root(
    *,
    repo_root: Path,
    integration_module: str,
    python_package: str,
    python_root: str,
) -> ModuleType:
    source_root = repo_root / python_root / "src"
    if not source_root.is_dir():
        raise ModuleNotFoundError(name=python_package)
    if integration_module != python_package and not integration_module.startswith(
        f"{python_package}."
    ):
        raise ModuleNotFoundError(name=integration_module)
    _ensure_parent_packages_loaded(source_root=source_root, module_name=integration_module)
    module_path, submodule_search_locations = _resolve_module_source_path(
        source_root=source_root,
        module_name=integration_module,
    )
    return _load_module_from_source(
        module_name=integration_module,
        source_path=module_path,
        submodule_search_locations=submodule_search_locations,
    )


def _ensure_parent_packages_loaded(*, source_root: Path, module_name: str) -> None:
    package_parts = module_name.split(".")[:-1]
    current_path = source_root
    current_name_parts: list[str] = []
    for part in package_parts:
        current_name_parts.append(part)
        current_path = current_path / part
        init_path = current_path / "__init__.py"
        if not init_path.is_file():
            raise ModuleNotFoundError(name=".".join(current_name_parts))
        _load_module_from_source(
            module_name=".".join(current_name_parts),
            source_path=init_path,
            submodule_search_locations=[str(current_path)],
        )


def _resolve_module_source_path(
    *,
    source_root: Path,
    module_name: str,
) -> tuple[Path, list[str] | None]:
    module_root = source_root.joinpath(*module_name.split("."))
    package_init = module_root / "__init__.py"
    if package_init.is_file():
        return package_init, [str(module_root)]
    module_path = module_root.with_suffix(".py")
    if module_path.is_file():
        return module_path, None
    raise ModuleNotFoundError(name=module_name)


def _load_module_from_source(
    *,
    module_name: str,
    source_path: Path,
    submodule_search_locations: list[str] | None,
) -> ModuleType:
    cached = sys.modules.get(module_name)
    if cached is not None:
        return cached
    spec = spec_from_file_location(
        module_name,
        source_path,
        submodule_search_locations=submodule_search_locations,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create module spec for {module_name}: {source_path}")
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


__all__ = ["import_pack_integration_module"]
