from __future__ import annotations

import importlib
import json
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from tests.pack_fixture_support import (
    materialize_externalized_plan_python,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_host.cli.main import main


def _purge_module_prefix(prefix: str) -> None:
    for module_name in tuple(sys.modules):
        if module_name == prefix or module_name.startswith(f"{prefix}."):
            sys.modules.pop(module_name, None)


@contextmanager
def _temporary_module_prefix_reload(prefix: str) -> Iterator[None]:
    original_modules = {
        module_name: module
        for module_name, module in sys.modules.items()
        if module_name == prefix or module_name.startswith(f"{prefix}.")
    }
    _purge_module_prefix(prefix)
    try:
        yield
    finally:
        _purge_module_prefix(prefix)
        sys.modules.update(original_modules)


def test_pack_validate_succeeds_with_externalized_plan_package(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    materialize_externalized_plan_python(repo_root / "packs" / "plan" / "python")
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(str(repo_root / "packs" / "plan" / "python" / "src"))

    with _temporary_module_prefix_reload("watchtower_plan"):
        result = main(
            [
                "pack",
                "validate",
                "--pack-settings-path",
                surfaces["pack_settings_path"],
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        imported_module = importlib.import_module("watchtower_plan.integration")

    assert result == 0
    assert payload["passed"] is True
    assert imported_module.__file__ is not None
    assert str(
        (repo_root / "packs" / "plan" / "python" / "src" / "watchtower_plan").resolve()
    ) in str(Path(imported_module.__file__).resolve())


def test_pack_validate_fails_when_externalized_plan_manifest_keeps_old_plan_paths(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    materialize_externalized_plan_python(repo_root / "packs" / "plan" / "python")

    pack_settings_path = repo_root / surfaces["pack_settings_path"]
    pack_settings = json.loads(pack_settings_path.read_text(encoding="utf-8"))
    pack_settings["workspace_roots"].update(
        {
            "workspace_root": "plan",
            "machine_root": "plan/.wt",
            "docs_root": "plan/docs",
            "workflows_root": "plan/workflows",
            "tracking_root": "plan/tracking",
            "initiatives_root": "plan/initiatives",
            "projects_root": "plan/projects",
            "domain_roots": {
                "initiatives": "plan/initiatives",
                "projects": "plan/projects",
            },
            "overview_path": "plan/plan_overview.md",
        }
    )
    pack_settings_path.write_text(f"{json.dumps(pack_settings, indent=2)}\n", encoding="utf-8")

    runtime_manifest_path = repo_root / surfaces["pack_runtime_manifest_path"]
    runtime_manifest = json.loads(runtime_manifest_path.read_text(encoding="utf-8"))
    runtime_manifest["owned_roots"].update(
        {
            "workspace_root": "plan",
            "machine_root": "plan/.wt",
            "docs_root": "plan/docs",
            "workflows_root": "plan/workflows",
            "tracking_root": "plan/tracking",
            "python_root": "plan/python",
            "initiatives_root": "plan/initiatives",
            "projects_root": "plan/projects",
            "domain_roots": {
                "initiatives": "plan/initiatives",
                "projects": "plan/projects",
            },
        }
    )
    runtime_manifest_path.write_text(
        f"{json.dumps(runtime_manifest, indent=2)}\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(str(repo_root / "packs" / "plan" / "python" / "src"))

    with _temporary_module_prefix_reload("watchtower_plan"):
        result = main(
            [
                "pack",
                "validate",
                "--pack-settings-path",
                surfaces["pack_settings_path"],
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)

    assert result == 1
    assert payload["passed"] is False
    issue_codes = {issue["code"] for issue in payload["issues"]}
    assert "pack_settings_path_not_under_machine_root" in issue_codes
    assert "pack_runtime_manifest_path_not_under_machine_root" in issue_codes
