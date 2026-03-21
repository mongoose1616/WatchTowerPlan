from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from shutil import copy2, rmtree

import pytest
from watchtower_plan import integration as plan_integration

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.pack_integration import (
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.pack_integration.runtime import load_pack_validation_runtime
from watchtower_core.validation import (
    PackContractValidationService,
    ValidationSelectionError,
    ValidationSuiteService,
)


def test_pack_contract_validation_passes_for_repo_pack_settings() -> None:
    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is True
    assert result.validator_id == "validator.pack.contract"


def test_pack_contract_validation_fails_when_runtime_manifest_is_missing(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    (repo_root / surfaces["pack_runtime_manifest_path"]).unlink()

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_contract_invalid" for issue in result.issues)


def test_pack_contract_validation_fails_when_pack_command_doc_is_missing(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    (repo_root / surfaces["command_doc_relative_path"]).unlink()

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_command_doc_missing" for issue in result.issues)


def test_pack_contract_validation_fails_when_core_python_workspace_dependency_is_missing(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    pyproject_path = repo_root / "core" / "python" / "pyproject.toml"
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    pyproject_path.write_text(
        pyproject_text.replace('  "watchtower-plan",\n', ""),
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_workspace_dependency_missing" for issue in result.issues)


def test_pack_contract_validation_fails_when_core_python_workspace_source_drifts(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    pyproject_path = repo_root / "core" / "python" / "pyproject.toml"
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    pyproject_path.write_text(
        pyproject_text.replace(
            '../../packs/plan/python',
            '../../packs/plan_clone/python',
        ),
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_workspace_source_path_mismatch" for issue in result.issues)


def test_pack_contract_validation_fails_when_pack_python_root_is_missing(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    rmtree(repo_root / "packs" / "plan" / "python")

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_owned_root_missing" for issue in result.issues)


def test_pack_contract_validation_fails_when_docs_root_is_not_pack_local(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    runtime_manifest_path = repo_root / surfaces["pack_runtime_manifest_path"]
    runtime_manifest = json.loads(runtime_manifest_path.read_text(encoding="utf-8"))
    runtime_manifest["owned_roots"]["docs_root"] = "core/docs"
    runtime_manifest_path.write_text(
        f"{json.dumps(runtime_manifest, indent=2)}\n",
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_owned_root_not_pack_local" for issue in result.issues)


def test_pack_contract_validation_fails_when_named_domain_roots_drift(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    runtime_manifest_path = repo_root / surfaces["pack_runtime_manifest_path"]
    runtime_manifest = json.loads(runtime_manifest_path.read_text(encoding="utf-8"))
    runtime_manifest["owned_roots"]["domain_roots"]["initiatives"] = "packs/plan/traces"
    runtime_manifest_path.write_text(
        f"{json.dumps(runtime_manifest, indent=2)}\n",
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_domain_roots_mismatch" for issue in result.issues)


def test_pack_contract_validation_fails_when_pack_settings_surface_leaves_pack_and_core(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    pack_settings_path = repo_root / surfaces["pack_settings_path"]
    pack_settings = json.loads(pack_settings_path.read_text(encoding="utf-8"))
    relocated_surface = repo_root / "shared" / "schema_catalog.json"
    relocated_surface.parent.mkdir(parents=True, exist_ok=True)
    copy2(
        repo_root / "packs" / "plan" / ".wt" / "registries" / "schema_catalog.json",
        relocated_surface,
    )
    pack_settings["surfaces"][0]["path"] = "shared/schema_catalog.json"
    pack_settings_path.write_text(
        f"{json.dumps(pack_settings, indent=2)}\n",
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_surface_not_pack_or_core_local" for issue in result.issues)


def test_pack_contract_validation_fails_when_reusable_core_imports_pack_runtime(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    illegal_import = repo_root / "core/python/src/watchtower_core/illegal_import.py"
    illegal_import.parent.mkdir(parents=True, exist_ok=True)
    illegal_import.write_text("import watchtower_plan.integration\n", encoding="utf-8")

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_boundary_core_imports_pack" for issue in result.issues)


def test_pack_contract_validation_fails_when_pack_runtime_imports_host_runtime(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    illegal_import = repo_root / "packs/plan/python/src/watchtower_plan/illegal_import.py"
    illegal_import.parent.mkdir(parents=True, exist_ok=True)
    illegal_import.write_text("from watchtower_host.cli import main\n", encoding="utf-8")

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_boundary_pack_imports_host" for issue in result.issues)


def test_pack_contract_validation_fails_when_reusable_core_imports_host_runtime(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    illegal_import = repo_root / "core/python/src/watchtower_core/illegal_host_import.py"
    illegal_import.parent.mkdir(parents=True, exist_ok=True)
    illegal_import.write_text("from watchtower_host.cli import parser\n", encoding="utf-8")

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_boundary_core_imports_host" for issue in result.issues)


def test_pack_contract_validation_fails_when_reusable_core_mutates_sys_path(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    illegal_mutation = repo_root / "core/python/src/watchtower_core/illegal_sys_path.py"
    illegal_mutation.parent.mkdir(parents=True, exist_ok=True)
    illegal_mutation.write_text(
        "\n".join(
            [
                "import sys",
                "",
                "sys.path.insert(0, 'packs/plan/python/src')",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_boundary_core_mutates_sys_path" for issue in result.issues)


def test_pack_contract_validation_fails_when_suite_registry_surface_is_missing(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "plan",
        include_validation_suite_registry=False,
    )
    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert result.issues[0].code == "pack_contract_invalid"
    assert "validation_suite_registry" in result.issues[0].message


def test_validation_suite_service_runs_pack_suite(tmp_path: Path) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )
    result = ValidationSuiteService(loader).run(
        surfaces["suite_id"],
        pack_settings_path=surfaces["pack_settings_path"],
    )

    assert result.passed is True
    assert [summary.step_kind for summary in result.step_summaries] == [
        "pack_contract",
        "artifact",
    ]
    assert surfaces["pack_settings_path"].startswith("packs/plan/.wt/")
    assert (repo_root / "packs" / "plan" / ".wt").is_dir()
    assert not (repo_root / "domain_packs").exists()
    targets = {record.target for record in result.records}
    assert surfaces["pack_settings_path"] in targets
    assert surfaces["artifact_relative_path"] in targets


def test_validation_suite_service_rejects_unknown_suite_id() -> None:
    service = ValidationSuiteService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError, match="Unknown validation suite ID"):
        service.run("suite.missing.validation_baseline")


def test_validation_suite_service_fails_closed_on_invalid_step_validator_id(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "plan",
        suite_step_validator_id="validator.packs.missing",
    )
    loader = ControlPlaneLoader(
        repo_root,
        active_pack_settings_path=surfaces["pack_settings_path"],
    )
    result = ValidationSuiteService(loader).run(
        surfaces["suite_id"],
        pack_settings_path=surfaces["pack_settings_path"],
    )

    assert result.passed is False
    failing_record = next(record for record in result.records if not record.result.passed)
    assert failing_record.step_kind == "artifact"
    assert failing_record.result.issues[0].code == "validation_step_error"
    assert "Unknown validator ID" in failing_record.result.issues[0].message


def test_load_pack_validation_runtime_returns_plan_validation_hooks() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    runtime = load_pack_validation_runtime(loader)

    assert isinstance(runtime, PackValidationRuntime)
    assert callable(runtime.document_semantics_factory)
    assert callable(runtime.suite_target_resolver)


def test_pack_contract_validation_fails_when_validation_provider_returns_invalid_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        validation_provider=lambda: object(),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is False
    assert any(issue.code == "pack_validation_provider_invalid" for issue in result.issues)


def test_pack_contract_validation_fails_when_integration_module_is_not_pack_local(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    runtime_manifest_path = repo_root / surfaces["pack_runtime_manifest_path"]
    runtime_manifest = json.loads(runtime_manifest_path.read_text(encoding="utf-8"))
    runtime_manifest["integration_module"] = "watchtower_host.cli.main"
    runtime_manifest_path.write_text(
        f"{json.dumps(runtime_manifest, indent=2)}\n",
        encoding="utf-8",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(issue.code == "pack_integration_module_not_pack_local" for issue in result.issues)


def test_pack_contract_validation_fails_when_command_namespace_conflicts(
    tmp_path: Path,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    materialize_pack_validation_suite(repo_root / "packs" / "plan")
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="plan",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=False,
        registry_mode="append",
    )

    result = PackContractValidationService(ControlPlaneLoader(repo_root)).validate(
        surfaces["pack_settings_path"]
    )

    assert result.passed is False
    assert any(
        issue.code == "pack_registry_command_namespace_conflict"
        for issue in result.issues
    )


def test_pack_contract_validation_fails_when_query_runtime_returns_invalid_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        query_runtime=lambda: object(),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is False
    assert any(issue.code == "pack_query_runtime_invalid" for issue in result.issues)


def test_pack_contract_validation_fails_when_query_runtime_returns_empty_commands(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        query_runtime=lambda: PackQueryRuntime(commands=()),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is False
    assert any(issue.code == "pack_query_runtime_invalid" for issue in result.issues)


def test_pack_contract_validation_fails_when_sync_targets_returns_invalid_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        sync_targets=lambda: object(),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is False
    assert any(issue.code == "pack_sync_runtime_invalid" for issue in result.issues)


def test_pack_contract_validation_fails_when_sync_targets_returns_empty_targets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bad_descriptor = replace(
        plan_integration.PACK_INTEGRATION,
        sync_targets=lambda: PackSyncRuntime(targets=()),
    )
    monkeypatch.setattr(plan_integration, "PACK_INTEGRATION", bad_descriptor)

    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is False
    assert any(issue.code == "pack_sync_runtime_invalid" for issue in result.issues)
