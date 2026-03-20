from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.pack_integration import PackValidationRuntime
from watchtower_core.pack_integration.runtime import load_pack_validation_runtime
from watchtower_core.validation import (
    PackContractValidationService,
    ValidationSelectionError,
    ValidationSuiteService,
)
from watchtower_plan import integration as plan_integration


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
