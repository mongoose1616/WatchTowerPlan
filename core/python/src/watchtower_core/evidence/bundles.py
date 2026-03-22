"""Reusable helpers for pack-local evidence bundles."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import EvidenceBundleArtifact

EVIDENCE_BUNDLE_SUBJECT_KIND = "validation_bundle"


@dataclass(frozen=True, slots=True)
class EvidenceBundleEntrySpec:
    """One evidence-bundle entry to include in a bundle document."""

    entry_id: str
    acceptance_label: str
    validation_type: str
    owner: str
    target_phase: str
    expected_output_paths: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EvidenceBundleWriteResult:
    """Summary of one evidence-bundle write operation."""

    evidence_id: str
    evidence_relative_path: str
    evidence_output_path: str


class EvidenceBundleHelper:
    """Build, validate, load, and write pack-local evidence bundles."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def build_document(
        self,
        *,
        evidence_id: str,
        initiative_id: str,
        trace_id: str,
        title: str,
        status: str,
        updated_at: str,
        entries: tuple[EvidenceBundleEntrySpec, ...],
        schema_id: str | None = None,
    ) -> dict[str, object]:
        """Build and validate one evidence-bundle document."""

        resolved_schema_id = self._resolve_schema_id(schema_id)
        document: dict[str, object] = {
            "$schema": resolved_schema_id,
            "id": evidence_id,
            "initiative_id": initiative_id,
            "trace_id": trace_id,
            "title": title,
            "status": status,
            "updated_at": updated_at,
            "entries": [
                {
                    "entry_id": entry.entry_id,
                    "acceptance_label": entry.acceptance_label,
                    "validation_type": entry.validation_type,
                    "owner": entry.owner,
                    "target_phase": entry.target_phase,
                    "expected_output_paths": list(entry.expected_output_paths),
                }
                for entry in entries
            ],
        }
        self._loader.schema_store.validate_instance(document, schema_id=resolved_schema_id)
        return document

    def artifact_from_document(self, document: dict[str, object]) -> EvidenceBundleArtifact:
        """Validate and return one typed evidence-bundle artifact."""

        self._loader.schema_store.validate_instance(document)
        return EvidenceBundleArtifact.from_document(document)

    def load_artifact(self, relative_path: str) -> EvidenceBundleArtifact:
        """Load one validated evidence bundle by repo-relative path."""

        document = self._loader.load_validated_document(relative_path)
        return EvidenceBundleArtifact.from_document(document)

    def write_document(
        self,
        document: dict[str, object],
        *,
        evidence_relative_path: str,
    ) -> EvidenceBundleWriteResult:
        """Write one validated evidence-bundle document to its canonical path."""

        self._loader.schema_store.validate_instance(document)
        output_path = self._loader.artifact_store.write_json_object(
            evidence_relative_path,
            document,
        )
        self._loader.set_validated_document_override(evidence_relative_path, document)
        return EvidenceBundleWriteResult(
            evidence_id=str(document["id"]),
            evidence_relative_path=evidence_relative_path,
            evidence_output_path=str(output_path),
        )

    def write_to_path(
        self,
        document: dict[str, object],
        *,
        destination: Path,
    ) -> Path:
        """Write one validated evidence-bundle document to an explicit filesystem path."""

        self._loader.schema_store.validate_instance(document)
        return self._loader.artifact_store.write_json_file(destination, document)

    def _resolve_schema_id(self, schema_id: str | None) -> str:
        """Return the explicit or active-pack evidence-bundle schema identifier."""

        if schema_id is not None:
            return schema_id

        try:
            return (
                self._loader.load_schema_catalog()
                .get_by_subject_kind(EVIDENCE_BUNDLE_SUBJECT_KIND)
                .schema_id
            )
        except KeyError as exc:
            raise ValueError(
                "Evidence bundles require an active pack schema catalog entry for "
                f"{EVIDENCE_BUNDLE_SUBJECT_KIND!r} or an explicit schema_id."
            ) from exc
        except ValueError as exc:
            raise ValueError(
                "Evidence bundle schema resolution requires exactly one schema catalog "
                f"entry for {EVIDENCE_BUNDLE_SUBJECT_KIND!r}."
            ) from exc


__all__ = [
    "EVIDENCE_BUNDLE_SUBJECT_KIND",
    "EvidenceBundleEntrySpec",
    "EvidenceBundleHelper",
    "EvidenceBundleWriteResult",
]
