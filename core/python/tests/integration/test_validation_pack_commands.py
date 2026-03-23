from __future__ import annotations

import json
from pathlib import Path
from shutil import copy2, copytree

import pytest

from tests.pack_fixture_support import REPO_ROOT, materialize_pack_validation_suite
from watchtower_host.cli.main import main


def _copy_validation_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    copy2(
        REPO_ROOT / "core" / "python" / "pyproject.toml",
        repo_root / "core" / "python" / "pyproject.toml",
    )
    return repo_root


def test_validate_suite_runs_synthetic_pack_fixture_via_cli_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            surfaces["suite_id"],
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate suite"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["suite_id"] == surfaces["suite_id"]
    targets = {record["target"] for record in payload["records"]}
    assert surfaces["pack_settings_path"] in targets
    assert surfaces["artifact_relative_path"] in targets


def test_validate_suite_runs_first_party_root_pack_fixture_via_cli_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "oversight",
        pack_id="pack.oversight",
        pack_slug="oversight",
        command_namespace="oversight",
        python_distribution="watchtower-oversight-fixture",
        python_package="watchtower_oversight_fixture",
        integration_module="watchtower_oversight_fixture.integration",
        default_repo_pack=True,
    )
    monkeypatch.chdir(repo_root / "core" / "python")
    monkeypatch.syspath_prepend(
        str(REPO_ROOT / "core" / "python" / "tests" / "fixtures" / "python")
    )

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            surfaces["suite_id"],
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate suite"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["suite_id"] == "suite.oversight.validation_baseline"
    targets = {record["target"] for record in payload["records"]}
    assert surfaces["pack_settings_path"] in targets
    assert surfaces["artifact_relative_path"] in targets


def test_validate_suite_fails_closed_on_invalid_schema_reference_via_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "plan",
        validator_schema_ids=("urn:watchtower:schema:interfaces:packs:missing:v1",),
    )
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            surfaces["suite_id"],
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
    failing_record = next(record for record in payload["records"] if not record["passed"])
    assert failing_record["step_kind"] == "artifact"
    assert failing_record["issues"][0]["code"] == "validation_step_error"
    assert "Unknown schema ID" in failing_record["issues"][0]["message"]


def test_validate_suite_fails_closed_on_invalid_validator_reference_via_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(
        repo_root / "packs" / "plan",
        suite_step_validator_id="validator.packs.missing",
    )
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            surfaces["suite_id"],
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
    failing_record = next(record for record in payload["records"] if not record["passed"])
    assert failing_record["issues"][0]["code"] == "validation_step_error"
    assert "Unknown validator ID" in failing_record["issues"][0]["message"]


def test_validate_suite_rejects_unknown_suite_id_via_cli(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            surfaces["suite_id"].replace(".validation_baseline", ".missing"),
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--format",
            "json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 1
    assert payload["status"] == "error"
    assert "Unknown validation suite ID" in payload["message"]
