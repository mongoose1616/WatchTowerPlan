from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from tests.pack_fixture_support import REPO_ROOT, materialize_pack_validation_suite
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import (
    PackContractValidationService,
    ValidationSelectionError,
    ValidationSuiteService,
)


def test_pack_contract_validation_passes_for_repo_pack_settings() -> None:
    result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate()

    assert result.passed is True
    assert result.validator_id == "validator.pack.contract"


def test_pack_contract_validation_fails_when_suite_registry_surface_is_missing() -> None:
    domain_packs_root = REPO_ROOT / "domain_packs"
    domain_packs_root.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(dir=domain_packs_root) as tmp_dir:
        surfaces = materialize_pack_validation_suite(
            Path(tmp_dir),
            include_validation_suite_registry=False,
        )
        result = PackContractValidationService(ControlPlaneLoader(REPO_ROOT)).validate(
            surfaces["pack_settings_path"]
        )

    assert result.passed is False
    assert result.issues[0].code == "pack_contract_invalid"
    assert "validation_suite_registry" in result.issues[0].message


def test_validation_suite_service_runs_pack_suite() -> None:
    domain_packs_root = REPO_ROOT / "domain_packs"
    domain_packs_root.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(dir=domain_packs_root) as tmp_dir:
        surfaces = materialize_pack_validation_suite(Path(tmp_dir))
        loader = ControlPlaneLoader(
            REPO_ROOT,
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
    assert {record.target for record in result.records} == {
        surfaces["pack_settings_path"],
        surfaces["artifact_relative_path"],
    }


def test_validation_suite_service_rejects_unknown_suite_id() -> None:
    service = ValidationSuiteService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError, match="Unknown validation suite ID"):
        service.run("suite.missing.validation_baseline")


def test_validation_suite_service_fails_closed_on_invalid_step_validator_id() -> None:
    domain_packs_root = REPO_ROOT / "domain_packs"
    domain_packs_root.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory(dir=domain_packs_root) as tmp_dir:
        surfaces = materialize_pack_validation_suite(
            Path(tmp_dir),
            suite_step_validator_id="validator.domain_packs.missing",
        )
        loader = ControlPlaneLoader(
            REPO_ROOT,
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
