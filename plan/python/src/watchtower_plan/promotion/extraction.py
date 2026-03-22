"""Promotion candidate resolution and extraction-envelope helpers."""

# ruff: noqa: E501

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane import (
    ExtractionCandidateKnowledgeSpec,
    ExtractionObservationSpec,
    ExtractionOutputEnvelopeHelper,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ExtractionOutputEnvelopeArtifact
from watchtower_plan.promotion.rendering import (
    extract_markdown_summary,
    extract_markdown_title,
    guidance_summary,
    guidance_title,
    readable_source_artifact_kind,
)
from watchtower_plan.promotion.targets import (
    default_mirror_target_paths,
    default_target_path,
    guidance_id_for_target_path,
    source_artifact_kind_for_path,
)

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


@dataclass(frozen=True, slots=True)
class ResolvedPromotionCandidate:
    source_path: str
    source_artifact_kind: str
    target_family: str
    target_path: str
    guidance_id: str
    review_path: str
    provenance_expectation: str
    mirror_update_mode: str
    mirror_target_paths: tuple[str, ...]
    template_path: Path
    source_title: str | None = None
    source_summary: str | None = None


class GuidancePromotionExtractionHelper:
    """Resolve initiative-local promotion candidates and build extraction envelopes."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        pack_loader: ControlPlaneLoader,
        policy_helper: Any,
        documentation_helper: Any,
        template_helper: Any,
        pack_settings: Any,
    ) -> None:
        self._loader = loader
        self._pack_loader = pack_loader
        self._policy_helper = policy_helper
        self._documentation_helper = documentation_helper
        self._template_helper = template_helper
        self._pack_settings = pack_settings
        self._extraction_helper = ExtractionOutputEnvelopeHelper(pack_loader)

    def load_promotion_inputs(
        self,
        *,
        initiative_root: Path,
        promotion_record_filename: str,
    ) -> tuple[dict[str, Any], dict[str, Any], str]:
        state_relative_path = (initiative_root / ".wt/initiative.json").as_posix()
        promotion_relative_path = (
            initiative_root / ".wt/promotions" / promotion_record_filename
        ).as_posix()
        initiative_document = load_json(self._loader.repo_root / state_relative_path)
        promotion_document = load_json(self._loader.repo_root / promotion_relative_path)
        return initiative_document, promotion_document, promotion_relative_path

    def resolve_candidates(
        self,
        *,
        initiative_document: dict[str, Any],
        promotion_document: dict[str, Any],
    ) -> tuple[ResolvedPromotionCandidate, ...]:
        resolved: list[ResolvedPromotionCandidate] = []
        initiative_slug = str(initiative_document["slug"])
        for candidate in promotion_document["candidates"]:
            source_path = str(candidate["candidate_path"])
            source_artifact_kind = str(
                candidate.get("source_artifact_kind")
                or source_artifact_kind_for_path(source_path)
            )
            target_family = str(candidate["target_family"])
            policy = self._policy_helper.resolve(
                source_artifact_kind=source_artifact_kind,
                target_family=target_family,
            )
            family = self._documentation_helper.family(target_family)
            if policy.target_root not in family.allowed_roots:
                raise ValueError(
                    f"Promotion policy {policy.policy_id} targets disallowed root {policy.target_root}."
                )
            target_path = str(
                candidate.get("target_path")
                or default_target_path(
                    initiative_slug=initiative_slug,
                    source_path=source_path,
                    target_family=target_family,
                    target_root=policy.target_root,
                )
            )
            if not target_path.startswith(f"{policy.target_root}/"):
                raise ValueError(
                    f"Promotion target path {target_path} must live under policy root {policy.target_root}."
                )
            mirror_target_paths = tuple(
                candidate.get("mirror_target_paths")
                or default_mirror_target_paths(
                    target_path=target_path,
                    target_root=policy.target_root,
                    mirror_roots=policy.mirror_roots,
                )
            )
            if policy.mirror_update_mode == "none" and mirror_target_paths:
                raise ValueError(
                    f"Promotion candidate {source_path} declares mirror targets without a mirror policy."
                )
            if policy.mirror_update_mode != "none" and not mirror_target_paths:
                raise ValueError(
                    f"Promotion candidate {source_path} requires mirror target paths."
                )
            template = self._template_helper.template(
                template_id_by_family(target_family)
            )
            source_file = self._loader.repo_root / source_path
            resolved.append(
                ResolvedPromotionCandidate(
                    source_path=source_path,
                    source_artifact_kind=source_artifact_kind,
                    target_family=target_family,
                    target_path=target_path,
                    guidance_id=guidance_id_for_target_path(target_family, target_path),
                    review_path=str(
                        candidate.get("review_path") or policy.required_review_path
                    ),
                    provenance_expectation=str(
                        candidate.get("provenance_expectation")
                        or "Promotions must cite the source initiative id, trace id, and evidence bundle id."
                    ),
                    mirror_update_mode=policy.mirror_update_mode,
                    mirror_target_paths=mirror_target_paths,
                    template_path=self._loader.repo_root / template.template_path,
                    source_title=extract_markdown_title(source_file),
                    source_summary=extract_markdown_summary(source_file),
                )
            )
        return tuple(resolved)

    def build_extraction_envelopes(
        self,
        *,
        initiative_document: dict[str, Any],
        promotion_document: dict[str, Any],
        candidates: tuple[ResolvedPromotionCandidate, ...],
        updated_at: str,
    ) -> tuple[ExtractionOutputEnvelopeArtifact, ...]:
        initiative_slug = str(initiative_document["slug"])
        initiative_title = str(initiative_document["title"])
        initiative_summary = str(initiative_document["summary"])
        evidence_ids = tuple(
            str(value) for value in initiative_document.get("evidence_ids", ())
        )
        extraction_envelopes: list[ExtractionOutputEnvelopeArtifact] = []
        for candidate in candidates:
            source_label = (
                candidate.source_title
                or readable_source_artifact_kind(candidate.source_artifact_kind).title()
            )
            source_summary_line = candidate.source_summary or initiative_summary
            document = self._extraction_helper.build_document(
                envelope_id=extraction_envelope_id(
                    initiative_slug, candidate.source_path
                ),
                title=f"Extraction Envelope: {source_label}",
                summary=(
                    f"Structured extraction output for {candidate.source_path} before "
                    f"promotion into the {candidate.target_family} family. {source_summary_line}"
                ),
                status="active",
                pack_id=self._pack_settings.pack_id,
                work_item_id=str(promotion_document["id"]),
                trace_id=str(initiative_document["trace_id"]),
                source_note_id=source_note_id(initiative_slug, candidate.source_path),
                workflow_run_id=workflow_run_id(initiative_slug),
                extraction_method="governed_guidance_promotion",
                created_at=updated_at,
                observations=(
                    ExtractionObservationSpec(
                        observation_id=observation_id(
                            initiative_slug, candidate.source_path
                        ),
                        summary=(
                            f"{candidate.source_path} is eligible for governed promotion into "
                            f"{candidate.target_family} at {candidate.target_path}."
                        ),
                        tags=(candidate.source_artifact_kind, candidate.target_family),
                    ),
                ),
                candidate_knowledge=(
                    ExtractionCandidateKnowledgeSpec(
                        candidate_id=knowledge_candidate_id(
                            initiative_slug, candidate.source_path
                        ),
                        title=guidance_title(
                            initiative_title=initiative_title,
                            target_family=candidate.target_family,
                            source_artifact_kind=candidate.source_artifact_kind,
                            source_title=candidate.source_title,
                        ),
                        summary=guidance_summary(
                            initiative_title=initiative_title,
                            initiative_summary=initiative_summary,
                            target_family=candidate.target_family,
                            source_artifact_kind=candidate.source_artifact_kind,
                            source_summary=candidate.source_summary,
                        ),
                        knowledge_family=candidate.target_family,
                        evidence_artifact_ids=evidence_ids,
                        tags=(
                            "promoted_guidance",
                            candidate.source_artifact_kind,
                            candidate.target_family,
                        ),
                    ),
                ),
                notes=(
                    f"Promotion record {promotion_document['id']} keeps the review path "
                    f"{candidate.review_path} and target path {candidate.target_path} authoritative."
                ),
            )
            extraction_envelopes.append(
                self._extraction_helper.artifact_from_document(document)
            )
        return tuple(extraction_envelopes)


def template_id_by_family(target_family: str) -> str:
    try:
        return {
            "foundation": "template.plan.guidance.foundation",
            "standard": "template.plan.guidance.standard",
            "reference": "template.plan.guidance.reference",
            "decision_record": "template.plan.guidance.decision_record",
            "pattern": "template.plan.guidance.pattern",
        }[target_family]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported promotion target family: {target_family}"
        ) from exc


def extraction_envelope_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"envelope.{initiative_slug}.{stem}"


def knowledge_candidate_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"candidate.{initiative_slug}.{stem}"


def observation_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"observation.{initiative_slug}.{stem}"


def source_note_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"note.{initiative_slug}.{stem}"


def workflow_run_id(initiative_slug: str) -> str:
    return f"run.{initiative_slug}.guidance_promotion"


def plan_pack_loader(loader: ControlPlaneLoader) -> ControlPlaneLoader:
    if loader.active_pack_settings_path == PLAN_PACK_SETTINGS_PATH:
        return loader
    return loader.derive(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)


def load_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    return document
