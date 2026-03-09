from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.evidence import ValidationEvidenceRecorder
from watchtower_core.validation import FrontMatterValidationService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_validation_evidence_recorder_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    result = FrontMatterValidationService(loader).validate(
        "docs/standards/metadata/front_matter_standard.md"
    )
    recorder = ValidationEvidenceRecorder(loader)

    document, evidence_id, evidence_relative_path = recorder.build_document(
        result,
        trace_id="trace.core_python_foundation",
        subject_ids=("std.metadata.front_matter",),
    )

    loader.schema_store.validate_instance(document)
    assert evidence_id.startswith("evidence.core_python_foundation.")
    assert evidence_relative_path.startswith("core/control_plane/ledgers/validation_evidence/")
    assert document["overall_result"] == "passed"


def test_validation_evidence_recorder_builds_updated_traceability_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    result = FrontMatterValidationService(loader).validate(
        "docs/standards/metadata/front_matter_standard.md"
    )
    recorder = ValidationEvidenceRecorder(loader)
    document, evidence_id, evidence_relative_path = recorder.build_document(
        result,
        trace_id="trace.core_python_foundation",
    )

    updated_traceability = recorder.build_updated_traceability_document(
        trace_id="trace.core_python_foundation",
        evidence_id=evidence_id,
        evidence_relative_path=evidence_relative_path,
        validator_id=result.validator_id,
        subject_path=result.target_path,
        updated_at=str(document["recorded_at"]),
    )

    loader.schema_store.validate_instance(updated_traceability)
    entry = next(
        item
        for item in updated_traceability["entries"]
        if item["trace_id"] == "trace.core_python_foundation"
    )
    assert evidence_id in entry["evidence_ids"]
    assert result.validator_id in entry["validator_ids"]
    assert evidence_relative_path in entry["related_paths"]


def test_validation_evidence_recorder_writes_temp_outputs(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    result = FrontMatterValidationService(loader).validate(
        "docs/standards/metadata/front_matter_standard.md"
    )
    recorder = ValidationEvidenceRecorder(loader)
    evidence_output = tmp_path / "evidence.v1.json"
    traceability_output = tmp_path / "traceability_index.v1.json"

    write_result = recorder.record(
        result,
        trace_id="trace.core_python_foundation",
        evidence_output=evidence_output,
        traceability_output=traceability_output,
    )

    assert evidence_output.exists()
    assert traceability_output.exists()

    written_evidence = json.loads(evidence_output.read_text(encoding="utf-8"))
    written_traceability = json.loads(traceability_output.read_text(encoding="utf-8"))
    assert written_evidence["id"] == write_result.evidence_id
    trace_entry = next(
        item
        for item in written_traceability["entries"]
        if item["trace_id"] == "trace.core_python_foundation"
    )
    assert write_result.evidence_id in trace_entry["evidence_ids"]
