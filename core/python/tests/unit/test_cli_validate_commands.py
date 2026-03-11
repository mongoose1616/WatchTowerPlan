from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.cli.main import main


def test_validate_front_matter_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "docs/standards/metadata/front_matter_standard.md",
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


def test_validate_front_matter_can_record_evidence_to_temp_outputs(
    tmp_path: Path, capsys
) -> None:
    evidence_output = tmp_path / "validation_evidence.v1.json"
    traceability_output = tmp_path / "traceability_index.v1.json"

    result = main(
        [
            "validate",
            "front-matter",
            "--path",
            "docs/standards/metadata/front_matter_standard.md",
            "--record-evidence",
            "--trace-id",
            "trace.core_python_foundation",
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
    assert payload["evidence"]["trace_id"] == "trace.core_python_foundation"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_document_semantics_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "document-semantics",
            "--path",
            "workflows/modules/code_validation.md",
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
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
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
    schema_path = tmp_path / "schemas" / "external_note.v1.schema.json"
    artifact_path = tmp_path / "artifacts" / "external_note.v1.json"
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
    artifact_path = tmp_path / "artifacts" / "external_note.v1.json"
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


def test_validate_artifact_can_record_evidence_to_temp_outputs(
    tmp_path: Path, capsys
) -> None:
    evidence_output = tmp_path / "validation_evidence.v1.json"
    traceability_output = tmp_path / "traceability_index.v1.json"

    result = main(
        [
            "validate",
            "artifact",
            "--path",
            "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json",
            "--record-evidence",
            "--trace-id",
            "trace.core_python_foundation",
            "--acceptance-id",
            "ac.core_python_foundation.001",
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
    assert payload["evidence"]["trace_id"] == "trace.core_python_foundation"
    assert evidence_output.exists()
    assert traceability_output.exists()


def test_validate_acceptance_supports_json_output(capsys) -> None:
    result = main(
        [
            "validate",
            "acceptance",
            "--trace-id",
            "trace.core_python_foundation",
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
    assert payload["included_families"] == ["front_matter", "document_semantics", "artifacts"]
    assert any(summary["family"] == "front_matter" for summary in payload["family_summaries"])
    assert any(
        summary["family"] == "document_semantics" for summary in payload["family_summaries"]
    )
    assert any(summary["family"] == "artifacts" for summary in payload["family_summaries"])


def test_validate_all_supports_json_output(capsys) -> None:
    result = main(["validate", "all", "--format", "json"])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core validate all"
    assert payload["status"] == "ok"
    assert payload["passed"] is True
    assert payload["failed_count"] == 0
    acceptance_summary = next(
        summary for summary in payload["family_summaries"] if summary["family"] == "acceptance"
    )
    assert acceptance_summary["failed_count"] == 0
