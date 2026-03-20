from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.pack_fixture_support import REPO_ROOT, materialize_pack_validation_suite
from watchtower_host.cli.main import main


def _copy_validation_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def test_validate_suite_runs_plan_domain_pack_fixture_via_cli_json(
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
    assert payload["suite_id"] == "suite.plan.validation_baseline"
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
            "suite.plan.missing",
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
