from __future__ import annotations

import importlib
import json
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

from watchtower_plan import integration as plan_integration
from watchtower_plan.cli import (
    closeout as plan_closeout_cli,
)
from watchtower_plan.cli import (
    namespace as plan_namespace_cli,
)
from watchtower_plan.cli import (
    query as plan_query_cli,
)
from watchtower_plan.cli import (
    sync as plan_sync_cli,
)
from watchtower_plan.cli import (
    tasks as plan_tasks_cli,
)
from watchtower_plan.testing.externalized_plan_fixtures import (
    externalized_plan_command_surface_paths,
    materialize_externalized_plan_command_docs,
    materialize_externalized_plan_python,
    materialize_externalized_plan_validation_suite,
)

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_externalized_fixture_python,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.pack_integration import (
    CorePythonWorkspaceRegistration,
    ensure_core_python_workspace_registration,
)
from watchtower_host.cli.introspection import iter_host_command_parser_specs
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


def _patch_live_plan_command_surfaces(monkeypatch, pack_root: Path) -> None:
    paths = externalized_plan_command_surface_paths(pack_root)
    monkeypatch.setattr(
        plan_integration,
        "PACK_INTEGRATION",
        replace(
            plan_integration.PACK_INTEGRATION,
            command_implementation_path=paths["namespace"],
            command_subcommand_implementation_paths=(
                ("bootstrap", paths["handlers"]),
                ("confirm-inputs", paths["handlers"]),
                ("approve", paths["handlers"]),
                ("query", paths["query"]),
                ("sync", paths["sync"]),
                ("closeout", paths["closeout"]),
                ("task", paths["tasks"]),
            ),
        ),
    )
    monkeypatch.setattr(plan_namespace_cli, "IMPLEMENTATION_PATH", paths["namespace"])
    monkeypatch.setattr(plan_namespace_cli, "SUBCOMMAND_IMPLEMENTATION_PATH", paths["handlers"])
    monkeypatch.setattr(plan_query_cli, "IMPLEMENTATION_PATH", paths["query"])
    monkeypatch.setattr(plan_sync_cli, "IMPLEMENTATION_PATH", paths["sync"])
    monkeypatch.setattr(plan_closeout_cli, "IMPLEMENTATION_PATH", paths["closeout"])
    monkeypatch.setattr(plan_tasks_cli, "IMPLEMENTATION_PATH", paths["tasks"])


def test_pack_validate_succeeds_with_externalized_plan_package(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    surfaces = materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
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


def test_pack_bootstrap_registers_scaffolded_pack_without_manual_host_edits(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    materialize_externalized_plan_command_docs(repo_root / "packs" / "plan")
    materialize_externalized_plan_python(repo_root / "packs" / "plan" / "python")
    _patch_live_plan_command_surfaces(monkeypatch, repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    scaffold_result = main(
        [
            "pack",
            "scaffold",
            "--pack-slug",
            "oversight",
            "--pack-root",
            "packs/oversight",
            "--domain-root",
            "reviews",
            "--domain-root",
            "assessments",
            "--format",
            "json",
        ]
    )
    assert scaffold_result == 0
    capsys.readouterr()

    with _temporary_module_prefix_reload("watchtower_plan"):
        with _temporary_module_prefix_reload("watchtower_oversight"):
            bootstrap_result = main(
                [
                    "pack",
                    "bootstrap",
                    "--pack-settings-path",
                    "packs/oversight/.wt/manifests/pack_settings.json",
                    "--write",
                    "--no-sync-workspace",
                    "--format",
                    "json",
                ]
            )
    bootstrap_payload = json.loads(capsys.readouterr().out)

    assert bootstrap_result == 0
    assert bootstrap_payload["validation_passed"] is None

    monkeypatch.syspath_prepend(str(repo_root / "packs" / "oversight" / "python" / "src"))

    with _temporary_module_prefix_reload("watchtower_plan"):
        with _temporary_module_prefix_reload("watchtower_oversight"):
            validate_result = main(
                [
                    "pack",
                    "validate",
                    "--pack-settings-path",
                    "packs/oversight/.wt/manifests/pack_settings.json",
                    "--format",
                    "json",
                ]
            )
            validate_payload = json.loads(capsys.readouterr().out)

    assert validate_result == 0
    assert validate_payload["passed"] is True


def test_pack_validate_fails_when_externalized_plan_manifest_keeps_old_plan_paths(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
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


def test_pack_validate_supports_externalized_second_pack_package(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
        extra_domain_root_names=("artifacts", "targets"),
    )
    materialize_externalized_plan_python(repo_root / "packs" / "plan" / "python")
    materialize_externalized_fixture_python(
        repo_root / "packs" / "oversight" / "python",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        source_package_root=(
            REPO_ROOT
            / "core"
            / "python"
            / "tests"
            / "fixtures"
            / "python"
            / "watchtower_oversight_fixture"
        ),
        description="Synthetic oversight runtime package used to prove hosted-pack portability.",
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(str(repo_root / "packs" / "oversight" / "python" / "src"))
    monkeypatch.syspath_prepend(str(repo_root / "packs" / "plan" / "python" / "src"))

    with _temporary_module_prefix_reload("watchtower_plan"):
        with _temporary_module_prefix_reload("watchtower_oversight_fixture"):
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
            imported_module = importlib.import_module("watchtower_oversight_fixture.integration")

    assert result == 0
    assert payload["passed"] is True
    assert imported_module.__file__ is not None
    assert str(
        (
            repo_root / "packs" / "oversight" / "python" / "src" / "watchtower_oversight_fixture"
        ).resolve()
    ) in str(Path(imported_module.__file__).resolve())


def test_externalized_multi_pack_parser_registers_namespaced_command_docs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
        extra_domain_root_names=("artifacts", "targets"),
    )
    materialize_externalized_plan_python(repo_root / "packs" / "plan" / "python")
    materialize_externalized_fixture_python(
        repo_root / "packs" / "oversight" / "python",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        source_package_root=(
            REPO_ROOT
            / "core"
            / "python"
            / "tests"
            / "fixtures"
            / "python"
            / "watchtower_oversight_fixture"
        ),
        description="Synthetic oversight runtime package used to prove hosted-pack portability.",
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(str(repo_root / "packs" / "oversight" / "python" / "src"))
    monkeypatch.syspath_prepend(str(repo_root / "packs" / "plan" / "python" / "src"))

    with _temporary_module_prefix_reload("watchtower_plan"):
        with _temporary_module_prefix_reload("watchtower_oversight_fixture"):
            specs = {
                spec.command_id: spec
                for spec in iter_host_command_parser_specs(ControlPlaneLoader(repo_root))
            }

    assert specs["command.watchtower_core.plan"].doc_path == (
        "packs/plan/docs/commands/core_python/watchtower_core_plan.md"
    )
    assert specs["command.watchtower_core.oversight"].doc_path == (
        "packs/oversight/docs/commands/core_python/watchtower_core_oversight.md"
    )


def test_pack_scaffold_output_becomes_validation_ready_after_host_wiring(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    stale_repo_root = materialize_validation_repo_subset(tmp_path / "stale")
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "scaffold",
            "--pack-slug",
            "oversight",
            "--pack-root",
            "packs/oversight",
            "--command-namespace",
            "oversight",
            "--domain-root",
            "reviews",
            "--format",
            "json",
        ]
    )
    scaffold_payload = json.loads(capsys.readouterr().out)

    pack_registry_path = repo_root / "core" / "control_plane" / "registries" / "pack_registry.json"
    pack_registry = json.loads(pack_registry_path.read_text(encoding="utf-8"))
    pack_registry["packs"].append(scaffold_payload["pack_registry_entry"])
    pack_registry_path.write_text(f"{json.dumps(pack_registry, indent=2)}\n", encoding="utf-8")
    ensure_core_python_workspace_registration(
        repo_root / "core" / "python" / "pyproject.toml",
        CorePythonWorkspaceRegistration(
            dependency=scaffold_payload["core_python_workspace_registration"]["dependency"],
            uv_source_path=scaffold_payload["core_python_workspace_registration"]["uv_source"][
                "path"
            ],
            editable=scaffold_payload["core_python_workspace_registration"]["uv_source"][
                "editable"
            ],
        ),
    )

    materialize_externalized_fixture_python(
        stale_repo_root / "packs" / "oversight" / "python",
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
        description="Synthetic oversight runtime package used to prove hosted-pack portability.",
    )
    monkeypatch.syspath_prepend(str(stale_repo_root / "packs" / "oversight" / "python" / "src"))

    with _temporary_module_prefix_reload("watchtower_plan"):
        with _temporary_module_prefix_reload("watchtower_oversight"):
            stale_module = importlib.import_module("watchtower_oversight.integration")
            assert stale_module.__file__ is not None
            assert str(
                (
                    stale_repo_root
                    / "packs"
                    / "oversight"
                    / "python"
                    / "src"
                    / "watchtower_oversight"
                ).resolve()
            ) in str(Path(stale_module.__file__).resolve())

            monkeypatch.syspath_prepend(
                str(repo_root / "packs" / "oversight" / "python" / "src")
            )
            result = main(
                [
                    "pack",
                    "validate",
                    "--pack-settings-path",
                    scaffold_payload["pack_settings_path"],
                    "--format",
                    "json",
                ]
            )
            payload = json.loads(capsys.readouterr().out)
            current_module = importlib.import_module("watchtower_oversight.integration")

    assert result == 0
    assert scaffold_payload["status"] == "ok"
    assert payload["command"] == "watchtower-core pack validate"
    assert payload["pack_settings_path"] == "packs/oversight/.wt/manifests/pack_settings.json"
    assert payload["passed"] is True
    assert current_module.__file__ is not None
    assert str(
        (repo_root / "packs" / "oversight" / "python" / "src" / "watchtower_oversight").resolve()
    ) in str(Path(current_module.__file__).resolve())
