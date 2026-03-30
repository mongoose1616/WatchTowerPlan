from __future__ import annotations

import importlib
import json
import sys
import tomllib
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path

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
from watchtower_core.pack_integration import PackQueryRuntime
from watchtower_host.cli.introspection import iter_host_command_parser_specs
from watchtower_host.cli.main import main
from watchtower_host.cli.registry import load_command_group_specs, load_pack_command_group_spec


def _materialize_unbootstrapped_oversight_root_pack(repo_root: Path) -> dict[str, str]:
    surfaces = materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        register_with_host_registry=False,
        register_with_core_python_workspace=False,
    )
    materialize_externalized_fixture_python(
        repo_root / "oversight" / "python",
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
    return surfaces


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


def _current_plan_integration_module():
    return importlib.import_module("watchtower_plan.integration")


def _patch_live_plan_command_surfaces(monkeypatch, pack_root: Path) -> None:
    plan_integration = _current_plan_integration_module()
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


def test_pack_list_supports_json_output(capsys) -> None:
    result = main(["pack", "list", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack list"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 1
    assert any(entry["pack_slug"] == "plan" for entry in payload["results"])


def test_pack_describe_supports_json_output(capsys) -> None:
    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack describe"
    assert payload["pack"]["pack_slug"] == "plan"
    assert payload["runtime_manifest"]["integration_module"] == "watchtower_plan.integration"
    assert "query_runtime" in payload["runtime_manifest"]["declared_capabilities"]
    assert payload["runtime_manifest"]["owned_roots"]["domain_roots"] == {
        "initiatives": "plan/initiatives",
        "projects": "plan/projects",
    }
    assert "coordination" in payload["integration"]["query_runtime_commands"]
    assert payload["integration"]["query_runtime_error"] is None
    assert "all" in payload["integration"]["sync_runtime_targets"]
    assert payload["integration"]["sync_runtime_error"] is None


def test_pack_validate_supports_json_output(capsys) -> None:
    result = main(["pack", "validate", "--pack", "plan", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack validate"
    assert payload["pack"] == "plan"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.pack.contract"


def test_pack_describe_reports_unknown_pack_as_json_error(capsys) -> None:
    result = main(["pack", "describe", "--pack", "missing", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core pack describe"
    assert payload["status"] == "error"
    assert "Unknown pack slug: missing." in payload["message"]


def test_pack_describe_reports_runtime_hook_errors_without_masking_import_success(
    capsys,
    monkeypatch,
) -> None:
    plan_integration = _current_plan_integration_module()
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        query_runtime=lambda: PackQueryRuntime(commands=()),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["integration"]["importable"] is True
    assert payload["integration"]["error"] is None
    assert payload["integration"]["query_runtime_commands"] is None
    assert "non-empty command names" in payload["integration"]["query_runtime_error"]
    assert "all" in payload["integration"]["sync_runtime_targets"]


def test_pack_commands_support_second_pack_fixture(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
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
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(
        str(REPO_ROOT / "core" / "python" / "tests" / "fixtures" / "python")
    )

    result = main(["pack", "describe", "--pack", "oversight", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["pack"]["pack_slug"] == "oversight"
    assert (
        payload["runtime_manifest"]["integration_module"]
        == "watchtower_oversight_fixture.integration"
    )
    assert payload["integration"]["query_runtime_commands"] == ["assessments", "reviews"]
    assert payload["integration"]["sync_runtime_targets"] == ["all"]


def test_pack_commands_support_root_pack_fixture(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_externalized_plan_validation_suite(repo_root / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["pack"]["pack_settings_path"] == surfaces["pack_settings_path"]
    assert payload["runtime_manifest"]["owned_roots"]["workspace_root"] == "plan"
    assert payload["integration"]["importable"] is True


def test_pack_validate_supports_second_pack_fixture(
    tmp_path: Path,
    monkeypatch,
    capsys,
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
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(
        str(REPO_ROOT / "core" / "python" / "tests" / "fixtures" / "python")
    )

    result = main(["pack", "validate", "--pack", "oversight", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack validate"
    assert payload["pack"] == "oversight"
    assert payload["passed"] is True


def test_pack_commands_still_work_when_another_registered_pack_is_broken(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    oversight_surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
    )
    oversight_manifest_path = repo_root / oversight_surfaces["pack_runtime_manifest_path"]
    oversight_manifest = json.loads(oversight_manifest_path.read_text(encoding="utf-8"))
    oversight_manifest["integration_module"] = "watchtower_oversight_fixture.missing_integration"
    oversight_manifest_path.write_text(
        f"{json.dumps(oversight_manifest, indent=2)}\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["pack", "list", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["status"] == "ok"
    assert {entry["pack_slug"] for entry in payload["results"]} == {"plan", "oversight"}

    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["pack"]["pack_slug"] == "plan"
    assert payload["integration"]["importable"] is True

    result = main(["pack", "validate", "--pack", "plan", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["pack"] == "plan"
    assert payload["passed"] is True


def test_pack_list_discovers_unbootstrapped_root_pack_in_copied_core_repo(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["pack", "list", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert {entry["pack_slug"] for entry in payload["results"]} == {"oversight"}
    assert payload["results"][0]["default_repo_pack"] is True


def test_pack_describe_discovers_unbootstrapped_root_pack_in_copied_core_repo(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["pack", "describe", "--pack", "oversight", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["pack"]["pack_slug"] == "oversight"
    assert payload["pack"]["pack_settings_path"] == surfaces["pack_settings_path"]
    assert payload["integration"]["importable"] is True
    assert payload["integration"]["query_runtime_commands"] == ["assessments", "reviews"]


def test_pack_describe_reports_stale_authored_registry_entry_as_structured_error(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["pack", "describe", "--pack", "plan", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert result == 1
    assert payload["command"] == "watchtower-core pack describe"
    assert payload["status"] == "error"
    assert "Hosted-pack registry entry for 'plan' is unusable" in payload["message"]


def test_pack_validate_reports_unbootstrapped_root_pack_as_structured_failure(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(["pack", "validate", "--pack", "oversight", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    issue_codes = {issue["code"] for issue in payload["issues"]}
    assert result == 1
    assert payload["pack"] == "oversight"
    assert payload["passed"] is False
    assert "pack_registry_entry_missing" in issue_codes
    assert "pack_workspace_dependency_missing" in issue_codes
    assert "pack_workspace_source_missing" in issue_codes


def test_pack_validate_reports_missing_pack_command_doc_via_cli(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    (repo_root / surfaces["command_doc_relative_path"]).unlink()
    monkeypatch.chdir(repo_root / "core" / "python")

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
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert any(issue["code"] == "pack_command_doc_missing" for issue in payload["issues"])


def test_pack_scaffold_supports_json_output(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "scaffold",
            "--pack-slug",
            "oversight",
            "--pack-root",
            "oversight",
            "--command-namespace",
            "oversight",
            "--domain-root",
            "reviews",
            "--domain-root",
            "assessments",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack scaffold"
    assert payload["pack_slug"] == "oversight"
    assert payload["command_namespace"] == "oversight"
    assert payload["pack_settings_path"] == "oversight/.wt/manifests/pack_settings.json"
    assert (
        payload["pack_runtime_manifest_path"]
        == "oversight/.wt/manifests/pack_runtime_manifest.json"
    )
    assert payload["pack_registry_entry"]["pack_slug"] == "oversight"
    assert payload["core_python_workspace_registration"]["dependency"] == "watchtower-oversight"
    assert (
        payload["core_python_workspace_registration"]["uv_source"]["path"]
        == "../../oversight/python"
    )
    created_paths = set(payload["created_paths"])
    assert "oversight/.wt/manifests/pack_settings.json" in created_paths
    assert "oversight/.wt/registries/schema_catalog.json" in created_paths
    assert "oversight/.wt/registries/workflow_metadata_registry.json" in created_paths
    assert "oversight/python/pyproject.toml" in created_paths
    assert "oversight/docs/commands/core_python/watchtower_core_oversight.md" in created_paths
    assert "oversight/reviews/README.md" in created_paths
    assert "oversight/assessments/README.md" in created_paths


def test_pack_bootstrap_supports_json_dry_run(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    scaffold_result = main(
        [
            "pack",
            "scaffold",
            "--pack-slug",
            "oversight",
            "--pack-root",
            "oversight",
            "--format",
            "json",
        ]
    )
    assert scaffold_result == 0
    capsys.readouterr()

    result = main(
        [
            "pack",
            "bootstrap",
            "--pack-settings-path",
            "oversight/.wt/manifests/pack_settings.json",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core pack bootstrap"
    assert payload["pack_slug"] == "oversight"
    assert payload["wrote"] is False
    assert payload["pack_registry_changed"] is True
    assert payload["core_python_pyproject_changed"] is True
    assert payload["workspace_sync_ran"] is False
    assert payload["workspace_sync_required"] is True
    assert payload["validation_passed"] is None
    assert "core/control_plane/registries/pack_registry.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/commands/command_index.json" in payload["changed_paths"]
    assert (
        "core/control_plane/indexes/repository_paths/repository_path_index.json"
        in payload["changed_paths"]
    )
    assert "core/control_plane/indexes/references/reference_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/standards/standard_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/workflows/workflow_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/routes/route_index.json" in payload["changed_paths"]
    assert "core/python/pyproject.toml" in payload["changed_paths"]

    registry = json.loads(
        (repo_root / "core" / "control_plane" / "registries" / "pack_registry.json").read_text(
            encoding="utf-8"
        )
    )
    assert all(entry["pack_slug"] != "oversight" for entry in registry["packs"])


def test_pack_bootstrap_write_updates_registry_and_workspace(
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
            "oversight",
            "--domain-root",
            "reviews",
            "--format",
            "json",
        ]
    )
    assert scaffold_result == 0
    capsys.readouterr()

    with _temporary_module_prefix_reload("watchtower_oversight"):
        result = main(
            [
                "pack",
                "bootstrap",
                "--pack-settings-path",
                "oversight/.wt/manifests/pack_settings.json",
                "--write",
                "--no-sync-workspace",
                "--format",
                "json",
            ]
        )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["wrote"] is True
    assert payload["pack_slug"] == "oversight"
    assert payload["validation_passed"] is None
    assert payload["workspace_sync_ran"] is False
    assert payload["workspace_sync_required"] is True
    assert payload["core_python_workspace_registration"]["dependency"] == "watchtower-oversight"
    assert (
        payload["core_python_workspace_registration"]["uv_source"]["path"]
        == "../../oversight/python"
    )
    assert payload["next_steps"] == [
        (
            "Run `uv sync` in core/python before using the hosted pack from a clean shell "
            "or environment."
        ),
        (
            "Run watchtower-core pack validate --pack-settings-path "
            "oversight/.wt/manifests/pack_settings.json --format json after the "
            "workspace sync completes."
        ),
    ]
    assert "core/control_plane/indexes/commands/command_index.json" in payload["changed_paths"]
    assert (
        "core/control_plane/indexes/repository_paths/repository_path_index.json"
        in payload["changed_paths"]
    )
    assert "core/control_plane/indexes/references/reference_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/standards/standard_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/workflows/workflow_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/routes/route_index.json" in payload["changed_paths"]

    registry = json.loads(
        (repo_root / "core" / "control_plane" / "registries" / "pack_registry.json").read_text(
            encoding="utf-8"
        )
    )
    assert any(entry["pack_slug"] == "oversight" for entry in registry["packs"])

    pyproject = tomllib.loads(
        (repo_root / "core" / "python" / "pyproject.toml").read_text(encoding="utf-8")
    )
    assert "watchtower-oversight" in pyproject["project"]["optional-dependencies"]["dev"]
    assert "watchtower-plan" in pyproject["project"]["optional-dependencies"]["dev"]
    assert pyproject["tool"]["uv"]["sources"]["watchtower-oversight"] == {
        "path": "../../oversight/python",
        "editable": True,
    }
    assert pyproject["tool"]["uv"]["sources"]["watchtower-plan"] == {
        "path": "../../packs/plan/python",
        "editable": True,
    }


def test_pack_bootstrap_reconciles_copied_core_registry_and_command_discovery(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(
        tmp_path,
        include_shared_discovery_sources=True,
    )
    surfaces = _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    with _temporary_module_prefix_reload("watchtower_oversight_fixture"):
        result = main(
            [
                "pack",
                "bootstrap",
                "--pack-settings-path",
                surfaces["pack_settings_path"],
                "--write",
                "--no-sync-workspace",
                "--format",
                "json",
            ]
        )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["pack_slug"] == "oversight"
    assert payload["wrote"] is True
    assert payload["pack_registry_changed"] is True
    assert payload["core_python_pyproject_changed"] is True
    assert payload["workspace_sync_required"] is True
    assert "core/control_plane/indexes/commands/command_index.json" in payload["changed_paths"]
    assert (
        "core/control_plane/indexes/repository_paths/repository_path_index.json"
        in payload["changed_paths"]
    )
    assert "core/control_plane/indexes/references/reference_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/standards/standard_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/workflows/workflow_index.json" in payload["changed_paths"]
    assert "core/control_plane/indexes/routes/route_index.json" in payload["changed_paths"]

    registry = json.loads(
        (repo_root / "core" / "control_plane" / "registries" / "pack_registry.json").read_text(
            encoding="utf-8"
        )
    )
    assert [entry["pack_slug"] for entry in registry["packs"]] == ["oversight"]
    assert registry["packs"][0]["default_repo_pack"] is True

    command_index = json.loads(
        (
            repo_root / "core" / "control_plane" / "indexes" / "commands" / "command_index.json"
        ).read_text(encoding="utf-8")
    )
    commands = {entry["command"] for entry in command_index["entries"]}
    assert "watchtower-core oversight" in commands
    assert all(not command.startswith("watchtower-core plan") for command in commands)

    repository_path_index = json.loads(
        (
            repo_root
            / "core"
            / "control_plane"
            / "indexes"
            / "repository_paths"
            / "repository_path_index.json"
        ).read_text(encoding="utf-8")
    )
    indexed_paths = {entry["path"] for entry in repository_path_index["entries"]}
    assert all(not path.startswith("plan/") for path in indexed_paths)

    reference_index = json.loads(
        (
            repo_root / "core" / "control_plane" / "indexes" / "references" / "reference_index.json"
        ).read_text(encoding="utf-8")
    )
    assert all(
        not path.startswith("plan/")
        for entry in reference_index["entries"]
        for path in (
            list(entry.get("cited_by_paths", [])) + list(entry.get("applied_by_paths", []))
        )
    )

    standard_index = json.loads(
        (
            repo_root / "core" / "control_plane" / "indexes" / "standards" / "standard_index.json"
        ).read_text(encoding="utf-8")
    )
    assert all(
        not path.startswith("plan/")
        for entry in standard_index["entries"]
        for path in (
            list(entry.get("operationalization_paths", []))
            + list(entry.get("related_paths", []))
            + list(entry.get("applied_reference_paths", []))
        )
    )

    workflow_index = json.loads(
        (
            repo_root / "core" / "control_plane" / "indexes" / "workflows" / "workflow_index.json"
        ).read_text(encoding="utf-8")
    )
    assert all(not entry["doc_path"].startswith("plan/") for entry in workflow_index["entries"])
    assert all(
        not path.startswith("plan/")
        for entry in workflow_index["entries"]
        for path in (
            list(entry.get("related_paths", []))
            + list(entry.get("reference_doc_paths", []))
            + list(entry.get("internal_reference_paths", []))
        )
    )

    route_index = json.loads(
        (
            repo_root / "core" / "control_plane" / "indexes" / "routes" / "route_index.json"
        ).read_text(encoding="utf-8")
    )
    assert all(
        not path.startswith("plan/")
        for entry in route_index["entries"]
        for path in entry.get("required_workflow_paths", [])
    )

    query_result = main(["query", "commands", "--query", "oversight", "--format", "json"])

    query_payload = json.loads(capsys.readouterr().out)
    assert query_result == 0
    assert query_payload["result_count"] >= 1
    assert any(
        entry["command"] == "watchtower-core oversight"
        for entry in query_payload["results"]
    )


def test_pack_scaffold_rejects_registry_collisions(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "pack",
            "scaffold",
            "--pack-slug",
            "plan",
            "--pack-root",
            "packs/plan_clone",
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 1
    assert payload["command"] == "watchtower-core pack scaffold"
    assert payload["status"] == "error"
    assert "Hosted pack already exists in pack_registry: plan" in payload["message"]


def test_host_command_registry_loads_second_pack_namespace(
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
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(
        str(REPO_ROOT / "core" / "python" / "tests" / "fixtures" / "python")
    )

    specs = load_command_group_specs(include_pack_namespaces=True)

    assert any(spec.name == "plan" for spec in specs)
    assert any(spec.name == "oversight" for spec in specs)


def test_host_command_registry_discovers_unbootstrapped_root_pack_namespace(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    specs = load_command_group_specs(
        loader=ControlPlaneLoader(repo_root),
        include_pack_namespaces=True,
    )

    assert all(spec.name != "plan" for spec in specs)
    assert any(spec.name == "oversight" for spec in specs)


def test_selected_pack_namespace_loading_isolated_from_broken_other_pack(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    oversight_surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
    )
    oversight_manifest_path = repo_root / oversight_surfaces["pack_runtime_manifest_path"]
    oversight_manifest = json.loads(oversight_manifest_path.read_text(encoding="utf-8"))
    oversight_manifest["integration_module"] = "watchtower_oversight_fixture.missing_integration"
    oversight_manifest_path.write_text(
        f"{json.dumps(oversight_manifest, indent=2)}\n",
        encoding="utf-8",
    )
    loader = ControlPlaneLoader(repo_root)

    plan_spec = load_pack_command_group_spec(
        "plan",
        loader=loader,
        tolerate_import_errors=True,
    )
    oversight_spec = load_pack_command_group_spec(
        "oversight",
        loader=loader,
        tolerate_import_errors=True,
    )

    assert plan_spec is not None
    assert plan_spec.name == "plan"
    assert plan_spec.notes is None
    assert oversight_spec is not None
    assert oversight_spec.name == "oversight"
    assert oversight_spec.notes is not None


def test_introspection_marks_broken_pack_namespace_unavailable(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_externalized_plan_validation_suite(repo_root / "packs" / "plan")
    oversight_surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
    )
    oversight_manifest_path = repo_root / oversight_surfaces["pack_runtime_manifest_path"]
    oversight_manifest = json.loads(oversight_manifest_path.read_text(encoding="utf-8"))
    oversight_manifest["integration_module"] = "watchtower_oversight_fixture.missing_integration"
    oversight_manifest_path.write_text(
        f"{json.dumps(oversight_manifest, indent=2)}\n",
        encoding="utf-8",
    )

    specs = {
        spec.command_id: spec
        for spec in iter_host_command_parser_specs(ControlPlaneLoader(repo_root))
    }

    assert specs["command.watchtower_core.plan"].notes is None
    assert specs["command.watchtower_core.oversight"].doc_path == (
        "packs/oversight/docs/commands/core_python/watchtower_core_oversight.md"
    )
    assert "unavailable" in (specs["command.watchtower_core.oversight"].notes or "")


def test_parser_specs_route_pack_commands_to_owned_doc_roots(
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
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(
        str(REPO_ROOT / "core" / "python" / "tests" / "fixtures" / "python")
    )

    specs = {
        spec.command_id: spec
        for spec in iter_host_command_parser_specs(ControlPlaneLoader(repo_root))
    }

    assert (
        specs["command.watchtower_core.plan"].doc_path
        == "packs/plan/docs/commands/core_python/watchtower_core_plan.md"
    )
    assert (
        specs["command.watchtower_core.oversight"].doc_path
        == "packs/oversight/docs/commands/core_python/watchtower_core_oversight.md"
    )
