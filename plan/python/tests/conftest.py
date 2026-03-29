from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path
from types import ModuleType

import pytest

from watchtower_core.pack_integration.importing import import_pack_integration_module

_WATCHTOWER_PLAN_PREFIX = "watchtower_plan"
_PLAN_TESTS_ROOT = Path(__file__).resolve().parent
_REPO_ROOT = _PLAN_TESTS_ROOT.parents[2]


def _restore_workspace_watchtower_plan_modules() -> None:
    import_pack_integration_module(
        repo_root=_REPO_ROOT,
        integration_module="watchtower_plan.integration",
        python_package=_WATCHTOWER_PLAN_PREFIX,
        python_root="plan/python",
    )


def _active_watchtower_plan_modules() -> dict[str, ModuleType]:
    return {
        name: module
        for name, module in sys.modules.items()
        if isinstance(module, ModuleType)
        and (name == _WATCHTOWER_PLAN_PREFIX or name.startswith(f"{_WATCHTOWER_PLAN_PREFIX}."))
    }


def _ensure_watchtower_plan_module(module_name: str) -> ModuleType | None:
    module = sys.modules.get(module_name)
    if isinstance(module, ModuleType):
        return module
    if module_name == _WATCHTOWER_PLAN_PREFIX or module_name.startswith(
        f"{_WATCHTOWER_PLAN_PREFIX}."
    ):
        imported = import_module(module_name)
        if isinstance(imported, ModuleType):
            return imported
    return None


def _refresh_plan_test_globals() -> None:
    active_modules = _active_watchtower_plan_modules()
    if not active_modules:
        return

    for module in tuple(sys.modules.values()):
        if not isinstance(module, ModuleType):
            continue
        module_file = getattr(module, "__file__", None)
        if not isinstance(module_file, str):
            continue
        try:
            Path(module_file).resolve().relative_to(_PLAN_TESTS_ROOT)
        except ValueError:
            continue

        for global_name, value in tuple(vars(module).items()):
            if isinstance(value, ModuleType):
                replacement = active_modules.get(value.__name__) or _ensure_watchtower_plan_module(
                    value.__name__
                )
                if replacement is not None and replacement is not value:
                    setattr(module, global_name, replacement)
                continue

            origin_module_name = getattr(value, "__module__", None)
            origin_attr_name = getattr(value, "__name__", None)
            if (
                not isinstance(origin_module_name, str)
                or not origin_module_name.startswith(f"{_WATCHTOWER_PLAN_PREFIX}.")
                or not isinstance(origin_attr_name, str)
            ):
                continue

            origin_module = active_modules.get(origin_module_name)
            if origin_module is None:
                origin_module = _ensure_watchtower_plan_module(origin_module_name)
            if origin_module is None or not hasattr(origin_module, origin_attr_name):
                continue
            replacement = getattr(origin_module, origin_attr_name)
            if replacement is not value:
                setattr(module, global_name, replacement)


@pytest.fixture(autouse=True)
def _refresh_plan_imported_globals() -> None:
    _restore_workspace_watchtower_plan_modules()
    _refresh_plan_test_globals()
    yield
    _restore_workspace_watchtower_plan_modules()
    _refresh_plan_test_globals()
