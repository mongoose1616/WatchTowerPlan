"""Durable validation-evidence builders and write helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from watchtower_core.control_plane.loader import (
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_core.validation.models import ValidationResult

VALIDATION_EVIDENCE_SCHEMA_ID = "urn:watchtower:schema:artifacts:ledgers:validation-evidence:v1"
VALIDATION_EVIDENCE_DIRECTORY = "core/control_plane/ledgers/validation_evidence"


def _timestamp_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return normalized or "item"


def _list_with_unique(existing: list[str], additions: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in [*existing, *additions]:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


@dataclass(frozen=True, slots=True)
class EvidenceWriteResult:
    """Summary of a durable evidence-write operation."""

    evidence_id: str
    evidence_relative_path: str
    trace_id: str
    recorded_at: str
    overall_result: str
    evidence_output_path: str
    traceability_output_path: str


class ValidationEvidenceRecorder:
    """Build and write durable validation evidence plus traceability updates."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def build_document(
        self,
        result: ValidationResult,
        *,
        trace_id: str,
        evidence_id: str | None = None,
        subject_ids: tuple[str, ...] = (),
        acceptance_ids: tuple[str, ...] = (),
        title: str | None = None,
        check_title: str | None = None,
        notes: str | None = None,
        recorded_at: str | None = None,
    ) -> tuple[dict[str, object], str, str]:
        """Build a schema-valid durable evidence document and its canonical path."""
        if Path(result.target_path).is_absolute():
            raise ValueError("Durable evidence requires a repository-local target path.")

        trace_entry = self._loader.load_traceability_index().get(trace_id)
        timestamp = recorded_at or _timestamp_now()
        resolved_evidence_id = evidence_id or self._derive_evidence_id(trace_id, result)
        evidence_relative_path = self._derive_evidence_relative_path(resolved_evidence_id)
        overall_result = "passed" if result.passed else "failed"
        check_id = self._derive_check_id(trace_id, result)
        issue_note = None
        if result.issues:
            issue_note = "; ".join(issue.message for issue in result.issues[:3])

        document: dict[str, object] = {
            "$schema": VALIDATION_EVIDENCE_SCHEMA_ID,
            "id": resolved_evidence_id,
            "title": title or f"Validation Evidence for {result.target_path}",
            "status": "active",
            "trace_id": trace_id,
            "overall_result": overall_result,
            "recorded_at": timestamp,
            "checks": [
                {
                    "check_id": check_id,
                    "title": check_title or f"Validation for {result.target_path}",
                    "result": overall_result,
                    "subject_paths": [result.target_path],
                    "validator_id": result.validator_id,
                    **({"subject_ids": list(subject_ids)} if subject_ids else {}),
                    **({"acceptance_ids": list(acceptance_ids)} if acceptance_ids else {}),
                    **({"notes": issue_note} if issue_note else {}),
                }
            ],
            "related_paths": [result.target_path, evidence_relative_path],
        }

        if trace_entry.prd_ids:
            document["source_prd_ids"] = list(trace_entry.prd_ids)
        if trace_entry.decision_ids:
            document["source_decision_ids"] = list(trace_entry.decision_ids)
        if trace_entry.design_ids:
            document["source_design_ids"] = list(trace_entry.design_ids)
        if trace_entry.plan_ids:
            document["source_plan_ids"] = list(trace_entry.plan_ids)
        if trace_entry.acceptance_contract_ids:
            document["source_acceptance_contract_ids"] = list(
                trace_entry.acceptance_contract_ids
            )
        if notes:
            document["notes"] = notes

        self._loader.schema_store.validate_instance(
            document,
            schema_id=VALIDATION_EVIDENCE_SCHEMA_ID,
        )
        return document, resolved_evidence_id, evidence_relative_path

    def build_updated_traceability_document(
        self,
        *,
        trace_id: str,
        evidence_id: str,
        evidence_relative_path: str,
        validator_id: str,
        subject_path: str,
        updated_at: str,
    ) -> dict[str, object]:
        """Return an updated traceability index document for one evidence artifact."""
        document = self._loader.load_validated_document(TRACEABILITY_INDEX_PATH)
        entries = document.get("entries")
        if not isinstance(entries, list):
            raise ValueError("Traceability index is missing its entries list.")

        updated = False
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("trace_id") != trace_id:
                continue

            existing_evidence_ids = list(entry.get("evidence_ids", []))
            entry["evidence_ids"] = _list_with_unique(existing_evidence_ids, [evidence_id])

            existing_validator_ids = list(entry.get("validator_ids", []))
            entry["validator_ids"] = _list_with_unique(existing_validator_ids, [validator_id])

            existing_related_paths = list(entry.get("related_paths", []))
            entry["related_paths"] = _list_with_unique(
                existing_related_paths,
                [subject_path, evidence_relative_path],
            )
            entry["updated_at"] = updated_at
            updated = True
            break

        if not updated:
            raise ValueError(f"Traceability entry does not exist for trace_id: {trace_id}")

        self._loader.schema_store.validate_instance(document)
        return document

    def write_document(
        self,
        document: dict[str, object],
        *,
        destination: Path,
    ) -> Path:
        """Write a validated JSON document to disk."""
        return self._loader.artifact_store.write_json_file(destination, document)

    def record(
        self,
        result: ValidationResult,
        *,
        trace_id: str,
        evidence_id: str | None = None,
        subject_ids: tuple[str, ...] = (),
        acceptance_ids: tuple[str, ...] = (),
        title: str | None = None,
        check_title: str | None = None,
        notes: str | None = None,
        evidence_output: Path | None = None,
        traceability_output: Path | None = None,
    ) -> EvidenceWriteResult:
        """Write durable evidence plus the synchronized traceability update."""
        document, resolved_evidence_id, evidence_relative_path = self.build_document(
            result,
            trace_id=trace_id,
            evidence_id=evidence_id,
            subject_ids=subject_ids,
            acceptance_ids=acceptance_ids,
            title=title,
            check_title=check_title,
            notes=notes,
        )
        recorded_at = str(document["recorded_at"])
        updated_traceability = self.build_updated_traceability_document(
            trace_id=trace_id,
            evidence_id=resolved_evidence_id,
            evidence_relative_path=evidence_relative_path,
            validator_id=result.validator_id,
            subject_path=result.target_path,
            updated_at=recorded_at,
        )

        if evidence_output is None:
            evidence_path = self._loader.artifact_store.write_json_object(
                evidence_relative_path,
                document,
            )
            self._loader.set_validated_document_override(
                evidence_relative_path,
                document,
            )
        else:
            evidence_path = self.write_document(document, destination=evidence_output)

        if traceability_output is None:
            traceability_path = self._loader.artifact_store.write_json_object(
                TRACEABILITY_INDEX_PATH,
                updated_traceability,
            )
            self._loader.set_validated_document_override(
                TRACEABILITY_INDEX_PATH,
                updated_traceability,
            )
        else:
            traceability_path = self.write_document(
                updated_traceability,
                destination=traceability_output,
            )
        return EvidenceWriteResult(
            evidence_id=resolved_evidence_id,
            evidence_relative_path=evidence_relative_path,
            trace_id=trace_id,
            recorded_at=recorded_at,
            overall_result=str(document["overall_result"]),
            evidence_output_path=str(evidence_path),
            traceability_output_path=str(traceability_path),
        )

    def _derive_evidence_id(self, trace_id: str, result: ValidationResult) -> str:
        trace_suffix = trace_id.removeprefix("trace.")
        target_slug = _slugify(Path(result.target_path).stem)
        validator_slug = _slugify(result.validator_id.rsplit(".", 1)[-1])
        return f"evidence.{trace_suffix}.{target_slug}_{validator_slug}_validation"

    def _derive_check_id(self, trace_id: str, result: ValidationResult) -> str:
        trace_suffix = trace_id.removeprefix("trace.")
        target_slug = _slugify(Path(result.target_path).stem)
        validator_slug = _slugify(result.validator_id.rsplit(".", 1)[-1])
        return f"check.{trace_suffix}.{target_slug}_{validator_slug}"

    def _derive_evidence_relative_path(self, evidence_id: str) -> str:
        stem = evidence_id.removeprefix("evidence.").replace(".", "_")
        return f"{VALIDATION_EVIDENCE_DIRECTORY}/{stem}.v1.json"
