"""Reusable helpers for pack-facing extraction-output envelopes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ExtractionOutputEnvelopeArtifact

EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID = (
    "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1"
)


@dataclass(frozen=True, slots=True)
class ExtractionObservationSpec:
    """One observation entry to include in an extraction-output envelope."""

    observation_id: str
    summary: str
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExtractionCandidateKnowledgeSpec:
    """One candidate durable-knowledge entry to include in an extraction envelope."""

    candidate_id: str
    title: str
    summary: str
    knowledge_family: str
    evidence_artifact_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ExtractionOutputEnvelopeWriteResult:
    """Summary of one extraction-output envelope write operation."""

    envelope_id: str
    envelope_relative_path: str
    envelope_output_path: str


class ExtractionOutputEnvelopeHelper:
    """Build, validate, load, and write extraction-output envelopes."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def build_document(
        self,
        *,
        envelope_id: str,
        title: str,
        summary: str,
        status: str,
        pack_id: str,
        work_item_id: str,
        trace_id: str,
        source_note_id: str,
        workflow_run_id: str,
        extraction_method: str,
        created_at: str,
        observations: tuple[ExtractionObservationSpec, ...],
        candidate_knowledge: tuple[ExtractionCandidateKnowledgeSpec, ...],
        artifact_manifest_id: str | None = None,
        notes: str | None = None,
        schema_id: str = EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID,
    ) -> dict[str, object]:
        """Build and validate one extraction-output envelope document."""

        document: dict[str, object] = {
            "$schema": schema_id,
            "id": envelope_id,
            "title": title,
            "summary": summary,
            "status": status,
            "pack_id": pack_id,
            "work_item_id": work_item_id,
            "trace_id": trace_id,
            "source_note_id": source_note_id,
            "workflow_run_id": workflow_run_id,
            "extraction_method": extraction_method,
            "created_at": created_at,
            "observations": [
                {
                    "observation_id": entry.observation_id,
                    "summary": entry.summary,
                    **({"tags": list(entry.tags)} if entry.tags else {}),
                }
                for entry in observations
            ],
            "candidate_knowledge": [
                {
                    "candidate_id": entry.candidate_id,
                    "title": entry.title,
                    "summary": entry.summary,
                    "knowledge_family": entry.knowledge_family,
                    **(
                        {"evidence_artifact_ids": list(entry.evidence_artifact_ids)}
                        if entry.evidence_artifact_ids
                        else {}
                    ),
                    **({"tags": list(entry.tags)} if entry.tags else {}),
                }
                for entry in candidate_knowledge
            ],
            **(
                {"artifact_manifest_id": artifact_manifest_id}
                if artifact_manifest_id is not None
                else {}
            ),
            **({"notes": notes} if notes is not None else {}),
        }
        self._loader.schema_store.validate_instance(document, schema_id=schema_id)
        return document

    def artifact_from_document(
        self,
        document: dict[str, object],
    ) -> ExtractionOutputEnvelopeArtifact:
        """Validate and return one typed extraction-output envelope artifact."""

        self._loader.schema_store.validate_instance(document)
        return ExtractionOutputEnvelopeArtifact.from_document(document)

    def load_artifact(self, relative_path: str) -> ExtractionOutputEnvelopeArtifact:
        """Load one validated extraction-output envelope by repo-relative path."""

        document = self._loader.load_validated_document(relative_path)
        return ExtractionOutputEnvelopeArtifact.from_document(document)

    def write_document(
        self,
        document: dict[str, object],
        *,
        envelope_relative_path: str,
    ) -> ExtractionOutputEnvelopeWriteResult:
        """Write one validated extraction-output envelope to its canonical path."""

        self._loader.schema_store.validate_instance(document)
        output_path = self._loader.artifact_store.write_json_object(
            envelope_relative_path,
            document,
        )
        self._loader.set_validated_document_override(envelope_relative_path, document)
        return ExtractionOutputEnvelopeWriteResult(
            envelope_id=str(document["id"]),
            envelope_relative_path=envelope_relative_path,
            envelope_output_path=str(output_path),
        )

    def write_to_path(
        self,
        document: dict[str, object],
        *,
        destination: Path,
    ) -> Path:
        """Write one validated extraction-output envelope to an explicit path."""

        self._loader.schema_store.validate_instance(document)
        return self._loader.artifact_store.write_json_file(destination, document)


__all__ = [
    "EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID",
    "ExtractionCandidateKnowledgeSpec",
    "ExtractionObservationSpec",
    "ExtractionOutputEnvelopeHelper",
    "ExtractionOutputEnvelopeWriteResult",
]
