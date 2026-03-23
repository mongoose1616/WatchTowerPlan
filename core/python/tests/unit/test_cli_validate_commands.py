from __future__ import annotations

import json
from pathlib import Path

from tests.pack_fixture_support import (
    REPO_ROOT,
    materialize_externalized_fixture_python,
    materialize_pack_validation_suite,
    materialize_validation_repo_subset,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_host.cli.main import main


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


def test_validate_front_matter_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "core/docs/standards/metadata/front_matter_standard.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate front-matter"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.standard_front_matter"


def test_validate_front_matter_reports_validation_failure(tmp_path: Path, capsys) -> None:
    document_path = tmp_path / "missing_front_matter.md"
    document_path.write_text("# Missing front matter\n", encoding="utf-8")

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            str(document_path),
            "--validator-id",
            "validator.documentation.standard_front_matter",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate front-matter"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["code"] == "front_matter_missing"


def test_validate_front_matter_can_record_evidence_to_temp_outputs(tmp_path: Path, capsys) -> None:
    evidence_output = tmp_path / "validation_evidence.json"
    traceability_output = tmp_path / "traceability_index.json"

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "core/docs/standards/metadata/front_matter_standard.md",
            "--record-evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--subject-id",
            "std.metadata.front_matter",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.governed_acceptance_example"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_document_semantics_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "document-semantics",
            "--path",
            "core/workflows/modules/code_validation.md",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate document-semantics"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.documentation.workflow_semantics"


def test_validate_artifact_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.control_plane.acceptance_contract"


def test_validate_artifact_reports_parse_failure(tmp_path: Path, capsys) -> None:
    document_path = tmp_path / "invalid.json"
    document_path.write_text("{ invalid json", encoding="utf-8")

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(document_path),
            "--validator-id",
            "validator.control_plane.acceptance_contract",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["code"] == "json_parse_invalid"


def test_validate_artifact_supports_external_schema_id_and_supplemental_schema_path(
    tmp_path: Path,
    capsys,
    json_writer,
) -> None:
    schema_path = tmp_path / "schemas" / "external_note.schema.json"
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    schema_id = "urn:watchtower:schema:external:cli-pack-note:v1"
    json_writer(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "CLI Pack Note",
            "description": "External pack note schema loaded through CLI options.",
            "type": "object",
            "properties": {"kind": {"const": "cli_pack_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )
    json_writer(artifact_path, {"kind": "cli_pack_note"})

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(artifact_path),
            "--schema-id",
            schema_id,
            "--supplemental-schema-path",
            str(schema_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == f"schema:{schema_id}"
    assert payload["schema_ids"] == [schema_id]


def test_validate_artifact_reports_invalid_supplemental_schema_path(
    tmp_path: Path,
    capsys,
    json_writer,
) -> None:
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    missing_schema_path = tmp_path / "schemas" / "missing"
    json_writer(artifact_path, {"kind": "cli_pack_note"})

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            str(artifact_path),
            "--schema-id",
            "urn:watchtower:schema:external:cli-pack-note:v1",
            "--supplemental-schema-path",
            str(missing_schema_path),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "error"
    assert "Supplemental schema path does not exist" in payload["message"]


def test_validate_artifact_can_record_evidence_to_temp_outputs(tmp_path: Path, capsys) -> None:
    evidence_output = tmp_path / "validation_evidence.json"
    traceability_output = tmp_path / "traceability_index.json"

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json",
            "--record-evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--acceptance-id",
            "ac.governed_acceptance_example.001",
            "--evidence-output",
            str(evidence_output),
            "--traceability-output",
            str(traceability_output),
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["passed"] is True
    assert payload["evidence"]["trace_id"] == "trace.governed_acceptance_example"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_acceptance_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "acceptance",
            "--trace-id",
            "trace.governed_acceptance_example",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate acceptance"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == "validator.trace.acceptance_reconciliation"


def test_validate_all_supports_json_output_when_acceptance_is_skipped(capsys) -> None:
    result = main(["validate", "all", "--skip-acceptance", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["failed_count"] == 0
    assert payload["included_families"] == [
        "pack_contract",
        "front_matter",
        "document_semantics",
        "artifacts",
    ]
    assert any(summary["family"] == "pack_contract" for summary in payload["family_summaries"])
    assert any(summary["family"] == "front_matter" for summary in payload["family_summaries"])
    assert any(summary["family"] == "document_semantics" for summary in payload["family_summaries"])
    assert any(summary["family"] == "artifacts" for summary in payload["family_summaries"])


def test_validate_all_supports_json_output(capsys) -> None:
    result = main(["validate", "all", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"


def test_validate_all_reports_unbootstrapped_root_pack_without_crashing(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    _materialize_unbootstrapped_oversight_root_pack(repo_root)
    monkeypatch.chdir(repo_root / "core" / "python")

    result = main(
        [
            "validate",
            "all",
            "--skip-front-matter",
            "--skip-document-semantics",
            "--skip-artifacts",
            "--skip-acceptance",
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["passed"] is False
    assert payload["included_families"] == ["pack_contract"]
    assert payload["failed_count"] == 1
    assert payload["results"][0]["family"] == "pack_contract"
    issue_codes = {issue["code"] for issue in payload["results"][0]["issues"]}
    assert "pack_registry_entry_missing" in issue_codes
    assert "pack_workspace_dependency_missing" in issue_codes
    assert "pack_workspace_source_missing" in issue_codes


def test_validate_suite_supports_json_output(capsys) -> None:
    suite_id = ControlPlaneLoader(REPO_ROOT).load_pack_settings().default_validation_suite_id

    result = main(
        [
            "validate",
            "suite",
            "--suite-id",
            suite_id,
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate suite"
    assert payload["status"] == "ok"
    assert payload["suite_id"] == suite_id
    assert payload["passed"] is True
    assert any(summary["step_kind"] == "front_matter" for summary in payload["step_summaries"])
    assert any(
        summary["step_kind"] == "document_semantics" for summary in payload["step_summaries"]
    )
    assert any(summary["step_kind"] == "artifact" for summary in payload["step_summaries"])


def test_validate_artifact_uses_pack_settings_path_to_select_pack_registry(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    repo_root = materialize_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_suite(repo_root / "packs" / "plan")
    monkeypatch.chdir(repo_root / "core" / "python")
    result = main(
        [
            "validate",
            "artifact",
            "--path",
            surfaces["artifact_relative_path"],
            "--pack-settings-path",
            surfaces["pack_settings_path"],
            "--format",
            "json",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate artifact"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["validator_id"] == surfaces["validator_id"]
