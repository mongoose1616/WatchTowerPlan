from __future__ import annotations

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_python_workspace_tooling_contract_publishes_stricter_reusable_core_rules() -> None:
    pyproject = tomllib.loads(
        (REPO_ROOT / "core/python/pyproject.toml").read_text(encoding="utf-8")
    )

    mypy_config = pyproject["tool"]["mypy"]
    assert mypy_config["warn_redundant_casts"] is True
    assert mypy_config["warn_unused_ignores"] is True

    mypy_overrides = pyproject["tool"]["mypy"]["overrides"]
    strict_override = next(
        override
        for override in mypy_overrides
        if "watchtower_core.control_plane" in override["module"]
    )

    assert strict_override["check_untyped_defs"] is True
    assert strict_override["disallow_incomplete_defs"] is True
    assert strict_override["strict_equality"] is True
    assert {
        "watchtower_core.adapters",
        "watchtower_core.control_plane",
        "watchtower_core.documentation",
        "watchtower_core.validation",
        "watchtower_core.query",
        "watchtower_core.sync",
        "watchtower_core.rebuild",
        "watchtower_core.routing",
        "watchtower_core.workflow_execution",
        "watchtower_core.evidence",
        "watchtower_core.utils",
    }.issubset({module_name.removesuffix(".*") for module_name in strict_override["module"]})

    ruff_select = pyproject["tool"]["ruff"]["lint"]["select"]
    assert "C4" in ruff_select
