from __future__ import annotations

import importlib
import sys
from pathlib import Path

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_externalized_fixture_python,
    materialize_validation_repo_subset,
)
from watchtower_core.pack_integration.importing import import_pack_integration_module


def _purge_module_prefix(prefix: str) -> None:
    for module_name in tuple(sys.modules):
        if module_name == prefix or module_name.startswith(f"{prefix}."):
            sys.modules.pop(module_name, None)


def test_import_pack_integration_module_reloads_stale_pack_module_from_current_repo_root(
    tmp_path: Path,
    monkeypatch,
) -> None:
    stale_repo = materialize_validation_repo_subset(tmp_path / "stale")
    current_repo = materialize_validation_repo_subset(tmp_path / "current")

    for repo_root in (stale_repo, current_repo):
        materialize_externalized_fixture_python(
            repo_root / "oversight" / "python",
            python_distribution="watchtower-oversight",
            python_package="watchtower_oversight",
            source_package_root=(
                REPO_ROOT
                / "core"
                / "python"
                / "tests"
                / "fixtures"
                / "python"
                / "watchtower_oversight_fixture"
            ),
            description=(
                "Synthetic oversight runtime package used to prove copied-core discovery."
            ),
        )

    monkeypatch.syspath_prepend(str(stale_repo / "oversight" / "python" / "src"))
    _purge_module_prefix("watchtower_oversight")
    try:
        stale_module, stale_source = import_pack_integration_module(
            repo_root=stale_repo,
            integration_module="watchtower_oversight.integration",
            python_package="watchtower_oversight",
            python_root="oversight/python",
        )
        assert stale_source == "workspace"
        assert stale_module.__file__ is not None
        assert str(
            (stale_repo / "oversight" / "python" / "src" / "watchtower_oversight").resolve()
        ) in str(Path(stale_module.__file__).resolve())

        monkeypatch.syspath_prepend(str(current_repo / "oversight" / "python" / "src"))
        current_module, current_source = import_pack_integration_module(
            repo_root=current_repo,
            integration_module="watchtower_oversight.integration",
            python_package="watchtower_oversight",
            python_root="oversight/python",
        )

        assert current_source == "pack_python_root"
        assert current_module.__file__ is not None
        assert str(
            (current_repo / "oversight" / "python" / "src" / "watchtower_oversight").resolve()
        ) in str(Path(current_module.__file__).resolve())
        assert importlib.import_module("watchtower_oversight.integration") is current_module
    finally:
        _purge_module_prefix("watchtower_oversight")
