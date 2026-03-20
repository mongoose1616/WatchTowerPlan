from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.pack_integration import PackQueryRuntime
from watchtower_host.cli.introspection import iter_command_parser_specs
from watchtower_host.cli.parser import build_parser
from watchtower_host.cli.registry import load_command_group_specs
from watchtower_host.cli.main import main
from watchtower_plan import integration as plan_integration


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
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "packs" / "plan")
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
    assert payload["runtime_manifest"]["integration_module"] == "watchtower_oversight_fixture.integration"
    assert payload["integration"]["query_runtime_commands"] == ["assessments", "reviews"]
    assert payload["integration"]["sync_runtime_targets"] == ["oversight-index", "review-index"]


def test_pack_validate_supports_second_pack_fixture(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "packs" / "plan")
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


def test_pack_validate_reports_missing_pack_command_doc_via_cli(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
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


def test_host_command_registry_loads_second_pack_namespace(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "packs" / "plan")
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

    specs = load_command_group_specs()

    assert any(spec.name == "plan" for spec in specs)
    assert any(spec.name == "oversight" for spec in specs)


def test_parser_specs_route_pack_commands_to_owned_doc_roots(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "packs" / "plan")
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

    specs = {spec.command_id: spec for spec in iter_command_parser_specs(build_parser())}

    assert (
        specs["command.watchtower_core.plan"].doc_path
        == "packs/plan/docs/commands/core_python/watchtower_core_plan.md"
    )
    assert (
        specs["command.watchtower_core.oversight"].doc_path
        == "packs/oversight/docs/commands/core_python/watchtower_core_oversight.md"
    )
