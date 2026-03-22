from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import (
    ControlPlaneLoader,
    ExtractionCandidateKnowledgeSpec,
    ExtractionObservationSpec,
    ExtractionOutputEnvelopeHelper,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_extraction_output_helper_builds_schema_valid_document() -> None:
    helper = ExtractionOutputEnvelopeHelper(ControlPlaneLoader(REPO_ROOT))

    document = helper.build_document(
        envelope_id="envelope.plan_example.design_record",
        title="Extraction Envelope: Design Record",
        summary="Structured extraction output before promotion into decision_record guidance.",
        status="active",
        pack_id="pack.plan",
        work_item_id="promotion.plan_example.bootstrap_shell",
        trace_id="trace.plan_example",
        source_note_id="note.plan_example.design_record",
        workflow_run_id="run.plan_example.guidance_promotion",
        extraction_method="governed_guidance_promotion",
        created_at="2026-03-18T02:10:00Z",
        observations=(
            ExtractionObservationSpec(
                observation_id="observation.plan_example.design_record",
                summary="The design record is eligible for governed promotion.",
                tags=("design_record", "decision_record"),
            ),
        ),
        candidate_knowledge=(
            ExtractionCandidateKnowledgeSpec(
                candidate_id="candidate.plan_example.design_record",
                title="Plan Example Decision Record: Design Record",
                summary=(
                    "Promoted decision record extracted from the design record for Plan Example."
                ),
                knowledge_family="decision_record",
                evidence_artifact_ids=("evidence.plan_example.bootstrap_validation_bundle",),
                tags=("promoted_guidance", "design_record", "decision_record"),
            ),
        ),
        notes="Promotion record promotion.plan_example.bootstrap_shell remains authoritative.",
    )

    artifact = helper.artifact_from_document(document)

    assert artifact.artifact_id == "envelope.plan_example.design_record"
    assert artifact.observation_count == 1
    assert artifact.knowledge_count == 1
    assert artifact.knowledge_families == ("decision_record",)
    assert artifact.evidence_artifact_ids == ("evidence.plan_example.bootstrap_validation_bundle",)
