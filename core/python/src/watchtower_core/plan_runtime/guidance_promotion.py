"""Governed initiative-to-guidance promotion helpers for the live plan workspace."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.adapters.front_matter import render_front_matter
from watchtower_core.control_plane import (
    DocumentationFamilyHelper,
    ExtractionCandidateKnowledgeSpec,
    ExtractionObservationSpec,
    ExtractionOutputEnvelopeHelper,
    PromotionPolicyHelper,
    TemplateCatalogHelper,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ExtractionOutputEnvelopeArtifact
from watchtower_core.utils.timestamps import utc_timestamp_now

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"
PROMOTION_RECORD_FILENAME = "guidance_promotion_record.bootstrap.json"

_SOURCE_ARTIFACT_KIND_BY_FILENAME = {
    "initiative_brief.md": "initiative_brief",
    "design_record.md": "design_record",
    "implementation_slice.md": "implementation_slice",
    "decision_notes.md": "decision_notes",
}
_DEFAULT_TARGET_FAMILY_BY_SOURCE_KIND = {
    "initiative_brief": "reference",
    "design_record": "decision_record",
    "implementation_slice": "pattern",
    "decision_notes": "standard",
}
_AUTHORITY_BY_FAMILY = {
    "reference": "reference",
    "decision_record": "authoritative",
    "pattern": "authoritative",
    "standard": "authoritative",
    "foundation": "authoritative",
}
_TEMPLATE_ID_BY_FAMILY = {
    "foundation": "template.plan.guidance.foundation",
    "standard": "template.plan.guidance.standard",
    "reference": "template.plan.guidance.reference",
    "decision_record": "template.plan.guidance.decision_record",
    "pattern": "template.plan.guidance.pattern",
}
_GUIDANCE_ID_PREFIX_BY_FAMILY = {
    "decision_record": "decision",
}


@dataclass(frozen=True, slots=True)
class GuidancePromotionOutput:
    """One promoted guidance output emitted from an initiative-local candidate."""

    source_path: str
    source_artifact_kind: str
    target_family: str
    target_path: str
    guidance_id: str
    mirror_target_paths: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class GuidancePromotionResult:
    """Promotion result for one initiative-local promotion record."""

    promotion_id: str
    initiative_id: str
    trace_id: str
    status: str
    updated_at: str
    wrote: bool
    outputs: tuple[GuidancePromotionOutput, ...]
    extraction_envelopes: tuple[ExtractionOutputEnvelopeArtifact, ...] = ()


@dataclass(frozen=True, slots=True)
class _ResolvedPromotionCandidate:
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


class GuidancePromotionService:
    """Promote approved initiative-local outputs into durable plan guidance roots."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._pack_loader = _plan_pack_loader(loader)
        self._policy_helper = PromotionPolicyHelper.from_loader(
            self._pack_loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._documentation_helper = DocumentationFamilyHelper.from_loader(
            self._pack_loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._template_helper = TemplateCatalogHelper.from_loader(
            self._pack_loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._extraction_helper = ExtractionOutputEnvelopeHelper(self._pack_loader)
        self._pack_settings = self._pack_loader.load_pack_settings()

    def extract_packwide(
        self,
        initiative_slug: str,
        *,
        promotion_record_filename: str = PROMOTION_RECORD_FILENAME,
        updated_at: str | None = None,
    ) -> tuple[ExtractionOutputEnvelopeArtifact, ...]:
        """Build validated extraction envelopes for one pack-wide initiative."""

        return self._extract(
            initiative_root=Path("plan/initiatives") / initiative_slug,
            promotion_record_filename=promotion_record_filename,
            updated_at=updated_at or utc_timestamp_now(),
        )

    def extract_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        *,
        promotion_record_filename: str = PROMOTION_RECORD_FILENAME,
        updated_at: str | None = None,
    ) -> tuple[ExtractionOutputEnvelopeArtifact, ...]:
        """Build validated extraction envelopes for one project-scoped initiative."""

        return self._extract(
            initiative_root=Path("plan/projects") / project_slug / "initiatives" / initiative_slug,
            promotion_record_filename=promotion_record_filename,
            updated_at=updated_at or utc_timestamp_now(),
        )

    def promote_packwide(
        self,
        initiative_slug: str,
        *,
        promotion_record_filename: str = PROMOTION_RECORD_FILENAME,
        approver_ref: str = "actor.repository_maintainer",
        updated_at: str | None = None,
        write: bool = False,
    ) -> GuidancePromotionResult:
        """Promote durable outputs for one pack-wide initiative."""

        return self._promote(
            initiative_root=Path("plan/initiatives") / initiative_slug,
            promotion_record_filename=promotion_record_filename,
            approver_ref=approver_ref,
            updated_at=updated_at or utc_timestamp_now(),
            write=write,
        )

    def promote_project_scoped(
        self,
        project_slug: str,
        initiative_slug: str,
        *,
        promotion_record_filename: str = PROMOTION_RECORD_FILENAME,
        approver_ref: str = "actor.repository_maintainer",
        updated_at: str | None = None,
        write: bool = False,
    ) -> GuidancePromotionResult:
        """Promote durable outputs for one project-scoped initiative."""

        return self._promote(
            initiative_root=Path("plan/projects") / project_slug / "initiatives" / initiative_slug,
            promotion_record_filename=promotion_record_filename,
            approver_ref=approver_ref,
            updated_at=updated_at or utc_timestamp_now(),
            write=write,
        )

    def _promote(
        self,
        *,
        initiative_root: Path,
        promotion_record_filename: str,
        approver_ref: str,
        updated_at: str,
        write: bool,
    ) -> GuidancePromotionResult:
        (
            initiative_document,
            promotion_document,
            promotion_relative_path,
        ) = self._load_promotion_inputs(
            initiative_root=initiative_root,
            promotion_record_filename=promotion_record_filename,
        )
        resolved_candidates = self._resolve_candidates(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
        )
        extraction_envelopes = self._build_extraction_envelopes(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
            candidates=resolved_candidates,
            updated_at=updated_at,
        )

        outputs: list[GuidancePromotionOutput] = []
        rendered_documents: list[tuple[str, str]] = []
        updated_candidates: list[dict[str, Any]] = []

        for candidate in resolved_candidates:
            rendered = self._render_guidance_document(
                initiative_document=initiative_document,
                promotion_document=promotion_document,
                source_path=candidate.source_path,
                source_artifact_kind=candidate.source_artifact_kind,
                target_family=candidate.target_family,
                target_path=candidate.target_path,
                template_path=candidate.template_path,
                updated_at=updated_at,
                source_title=candidate.source_title,
                source_summary=candidate.source_summary,
            )
            rendered_documents.append((candidate.target_path, rendered))
            for mirror_target_path in candidate.mirror_target_paths:
                rendered_documents.append((mirror_target_path, rendered))

            outputs.append(
                GuidancePromotionOutput(
                    source_path=candidate.source_path,
                    source_artifact_kind=candidate.source_artifact_kind,
                    target_family=candidate.target_family,
                    target_path=candidate.target_path,
                    guidance_id=candidate.guidance_id,
                    mirror_target_paths=candidate.mirror_target_paths,
                )
            )
            updated_candidates.append(
                {
                    "candidate_path": candidate.source_path,
                    "source_artifact_kind": candidate.source_artifact_kind,
                    "target_family": candidate.target_family,
                    "target_path": candidate.target_path,
                    "review_path": candidate.review_path,
                    "provenance_expectation": candidate.provenance_expectation,
                    "mirror_update_mode": candidate.mirror_update_mode,
                    "mirror_target_paths": list(candidate.mirror_target_paths),
                }
            )

        updated_promotion = {
            "$schema": promotion_document["$schema"],
            "id": promotion_document["id"],
            "initiative_id": initiative_document["initiative_id"],
            "trace_id": initiative_document["trace_id"],
            "title": promotion_document["title"],
            "status": "promoted",
            "approval_state": "approved",
            "approver_refs": [approver_ref],
            "review_refs": sorted(
                {
                    str(candidate["review_path"])
                    for candidate in updated_candidates
                }
            ),
            "evidence_refs": list(initiative_document.get("evidence_ids", ())),
            "updated_at": updated_at,
            "candidates": updated_candidates,
        }
        self._pack_loader.schema_store.validate_instance(updated_promotion)

        if write:
            for relative_path, rendered in rendered_documents:
                destination = self._loader.repo_root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(rendered, encoding="utf-8")
            self._loader.artifact_store.write_json_object(
                promotion_relative_path,
                updated_promotion,
            )

        return GuidancePromotionResult(
            promotion_id=str(updated_promotion["id"]),
            initiative_id=str(updated_promotion["initiative_id"]),
            trace_id=str(updated_promotion["trace_id"]),
            status=str(updated_promotion["status"]),
            updated_at=updated_at,
            wrote=write,
            outputs=tuple(outputs),
            extraction_envelopes=extraction_envelopes,
        )

    def _extract(
        self,
        *,
        initiative_root: Path,
        promotion_record_filename: str,
        updated_at: str,
    ) -> tuple[ExtractionOutputEnvelopeArtifact, ...]:
        initiative_document, promotion_document, _ = self._load_promotion_inputs(
            initiative_root=initiative_root,
            promotion_record_filename=promotion_record_filename,
        )
        resolved_candidates = self._resolve_candidates(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
        )
        return self._build_extraction_envelopes(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
            candidates=resolved_candidates,
            updated_at=updated_at,
        )

    def _load_promotion_inputs(
        self,
        *,
        initiative_root: Path,
        promotion_record_filename: str,
    ) -> tuple[dict[str, Any], dict[str, Any], str]:
        state_relative_path = (initiative_root / ".wt/initiative.json").as_posix()
        promotion_relative_path = (initiative_root / ".wt/promotions" / promotion_record_filename).as_posix()
        initiative_document = _load_json(self._loader.repo_root / state_relative_path)
        promotion_document = _load_json(self._loader.repo_root / promotion_relative_path)
        return initiative_document, promotion_document, promotion_relative_path

    def _resolve_candidates(
        self,
        *,
        initiative_document: dict[str, Any],
        promotion_document: dict[str, Any],
    ) -> tuple[_ResolvedPromotionCandidate, ...]:
        resolved: list[_ResolvedPromotionCandidate] = []
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
            if target_family not in _TEMPLATE_ID_BY_FAMILY:
                raise ValueError(f"Unsupported promotion target family: {target_family}")
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
            template = self._template_helper.template(_TEMPLATE_ID_BY_FAMILY[target_family])
            source_file = self._loader.repo_root / source_path
            resolved.append(
                _ResolvedPromotionCandidate(
                    source_path=source_path,
                    source_artifact_kind=source_artifact_kind,
                    target_family=target_family,
                    target_path=target_path,
                    guidance_id=guidance_id_for_target_path(target_family, target_path),
                    review_path=str(candidate.get("review_path") or policy.required_review_path),
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

    def _build_extraction_envelopes(
        self,
        *,
        initiative_document: dict[str, Any],
        promotion_document: dict[str, Any],
        candidates: tuple[_ResolvedPromotionCandidate, ...],
        updated_at: str,
    ) -> tuple[ExtractionOutputEnvelopeArtifact, ...]:
        initiative_slug = str(initiative_document["slug"])
        initiative_title = str(initiative_document["title"])
        initiative_summary = str(initiative_document["summary"])
        evidence_ids = tuple(str(value) for value in initiative_document.get("evidence_ids", ()))
        extraction_envelopes: list[ExtractionOutputEnvelopeArtifact] = []
        for candidate in candidates:
            source_label = candidate.source_title or readable_source_artifact_kind(
                candidate.source_artifact_kind
            ).title()
            source_summary_line = candidate.source_summary or initiative_summary
            document = self._extraction_helper.build_document(
                envelope_id=_extraction_envelope_id(initiative_slug, candidate.source_path),
                title=f"Extraction Envelope: {source_label}",
                summary=(
                    f"Structured extraction output for {candidate.source_path} before "
                    f"promotion into the {candidate.target_family} family. {source_summary_line}"
                ),
                status="active",
                pack_id=self._pack_settings.pack_id,
                work_item_id=str(promotion_document["id"]),
                trace_id=str(initiative_document["trace_id"]),
                source_note_id=_source_note_id(initiative_slug, candidate.source_path),
                workflow_run_id=_workflow_run_id(initiative_slug),
                extraction_method="governed_guidance_promotion",
                created_at=updated_at,
                observations=(
                    ExtractionObservationSpec(
                        observation_id=_observation_id(initiative_slug, candidate.source_path),
                        summary=(
                            f"{candidate.source_path} is eligible for governed promotion into "
                            f"{candidate.target_family} at {candidate.target_path}."
                        ),
                        tags=(candidate.source_artifact_kind, candidate.target_family),
                    ),
                ),
                candidate_knowledge=(
                    ExtractionCandidateKnowledgeSpec(
                        candidate_id=_knowledge_candidate_id(initiative_slug, candidate.source_path),
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

    def _render_guidance_document(
        self,
        *,
        initiative_document: dict[str, Any],
        promotion_document: dict[str, Any],
        source_path: str,
        source_artifact_kind: str,
        target_family: str,
        target_path: str,
        template_path: Path,
        updated_at: str,
        source_title: str | None,
        source_summary: str | None,
    ) -> str:
        front_matter = build_guidance_front_matter(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
            source_path=source_path,
            source_artifact_kind=source_artifact_kind,
            target_family=target_family,
            target_path=target_path,
            updated_at=updated_at,
            source_title=source_title,
            source_summary=source_summary,
        )
        family = self._documentation_helper.family(target_family)
        self._pack_loader.schema_store.validate_instance(
            front_matter,
            schema_id=family.front_matter_schema_id,
        )
        body = render_guidance_body(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
            source_path=source_path,
            source_artifact_kind=source_artifact_kind,
            source_title=source_title,
            source_summary=source_summary,
            target_family=target_family,
            target_path=target_path,
            template_path=template_path,
        )
        return f"---\n{render_front_matter(front_matter)}\n---\n\n{body}"


def source_artifact_kind_for_path(source_path: str) -> str:
    """Resolve the initiative-local source artifact kind for one authored input path."""

    filename = Path(source_path).name
    try:
        return _SOURCE_ARTIFACT_KIND_BY_FILENAME[filename]
    except KeyError as exc:
        raise ValueError(f"Unsupported promotion source artifact: {source_path}") from exc


def default_target_family_for_source_kind(source_artifact_kind: str) -> str:
    """Return the default target family for one source artifact kind."""

    try:
        return _DEFAULT_TARGET_FAMILY_BY_SOURCE_KIND[source_artifact_kind]
    except KeyError as exc:
        raise ValueError(
            f"No default target family exists for source artifact kind {source_artifact_kind}."
        ) from exc


def default_target_path(
    *,
    initiative_slug: str,
    source_path: str,
    target_root: str,
) -> str:
    """Return the default target path for one promoted guidance output."""

    source_stem = Path(source_path).stem
    filename = f"{initiative_slug}_{source_stem}.md"
    return f"{target_root}/{filename}"


def default_mirror_target_paths(
    *,
    target_path: str,
    target_root: str,
    mirror_roots: tuple[str, ...],
) -> tuple[str, ...]:
    """Return deterministic mirror targets for one promoted guidance output."""

    relative_suffix = target_path.removeprefix(f"{target_root}/")
    return tuple(f"{root}/{relative_suffix}" for root in mirror_roots if root != target_root)


def guidance_id_for_target_path(target_family: str, target_path: str) -> str:
    """Return the default guidance identifier for one promoted target path."""

    stem = Path(target_path).stem
    prefix = _GUIDANCE_ID_PREFIX_BY_FAMILY.get(target_family, target_family)
    return f"{prefix}.{stem}"


def guidance_trace_id_for_target_path(target_path: str) -> str:
    """Return the durable trace identifier for one promoted guidance target."""

    stem = Path(target_path).stem
    normalized_stem = re.sub(r"[^a-z0-9]+", "_", stem.casefold()).strip("_") or "guidance"
    return f"trace.guidance.{normalized_stem}"


def build_guidance_front_matter(
    *,
    initiative_document: dict[str, Any],
    promotion_document: dict[str, Any],
    source_path: str,
    source_artifact_kind: str,
    target_family: str,
    target_path: str,
    updated_at: str,
    source_title: str | None,
    source_summary: str | None,
) -> dict[str, Any]:
    """Build front matter for one promoted guidance document."""

    initiative_title = str(initiative_document["title"])
    _ = source_path
    _ = promotion_document
    title = guidance_title(
        initiative_title=initiative_title,
        target_family=target_family,
        source_artifact_kind=source_artifact_kind,
        source_title=source_title,
    )
    summary = guidance_summary(
        initiative_title=initiative_title,
        initiative_summary=str(initiative_document["summary"]),
        target_family=target_family,
        source_artifact_kind=source_artifact_kind,
        source_summary=source_summary,
    )
    front_matter: dict[str, Any] = {
        "trace_id": guidance_trace_id_for_target_path(target_path),
        "id": guidance_id_for_target_path(target_family, target_path),
        "title": title,
        "summary": summary,
        "type": target_family,
        "status": "active",
        "owner": str(initiative_document["owner"]),
        "updated_at": updated_at,
        "audience": "shared",
        "authority": _AUTHORITY_BY_FAMILY[target_family],
        "applies_to": [
            target_path,
            "core/python/src/watchtower_core/plan_runtime/guidance_promotion.py",
            "plan/.wt/registries/promotion_policy_registry.json",
            "plan/.wt/indexes/guidance_index.json",
            "plan/.wt/indexes/promotion_index.json",
        ],
    }
    if target_family == "reference":
        front_matter["tags"] = [
            "promoted_guidance",
            target_family,
            "guidance_promotion",
            source_artifact_kind,
        ]
    return front_matter


def render_guidance_body(
    *,
    initiative_document: dict[str, Any],
    promotion_document: dict[str, Any],
    source_path: str,
    source_artifact_kind: str,
    source_title: str | None,
    source_summary: str | None,
    target_family: str,
    target_path: str,
    template_path: Path,
) -> str:
    """Render the markdown body for one promoted guidance output."""

    _ = template_path
    _ = promotion_document
    source_label = source_title or readable_source_artifact_kind(source_artifact_kind)
    source_summary_line = source_summary or str(initiative_document["summary"])
    if target_family == "reference":
        return (
            "# Subject Summary\n\n"
            f"This reference captures the durable operating model for governed guidance promotion. "
            f"{source_summary_line}\n\n"
            "## Usage Guidance\n\n"
            "- Use this reference when implementing or reviewing promotion of initiative-local inputs into `plan/docs/**`.\n"
            "- Treat `plan/.wt/registries/promotion_policy_registry.json`, `plan/.wt/indexes/guidance_index.json`, and `plan/.wt/indexes/promotion_index.json` as the machine companions for this document.\n\n"
            "## Boundaries\n\n"
            "- Durable guidance belongs in `plan/docs/**`.\n"
            "- Live execution state, closeout artifacts, and evidence bundles remain under initiative-local `plan/**` roots.\n\n"
            "## Related Surfaces\n\n"
            f"- `{target_path}`\n"
            "- `core/python/src/watchtower_core/plan_runtime/guidance_promotion.py`\n"
            "- `plan/.wt/indexes/guidance_index.json`\n"
            "- `plan/.wt/indexes/promotion_index.json`\n\n"
            "## Notes\n\n"
            "- Keep this document durable; initiative-local authored inputs are temporary proof surfaces, not long-term guidance roots.\n"
        )
    if target_family == "decision_record":
        return (
            "# Context\n\n"
            "This decision defines how validated initiative-local outputs become durable plan guidance. "
            f"{source_summary_line}\n\n"
            "## Decision\n\n"
            "- Durable guidance must be promoted through governed policy, family, and template contracts rather than being copied ad hoc from live initiative inputs.\n"
            "- Machine-readable promotion and guidance indexes must preserve provenance without forcing durable docs to retain live initiative package references.\n\n"
            "## Consequences\n\n"
            "- Promotion output stays aligned with machine-readable policy and indexing surfaces.\n"
            "- Durable guidance can move out of initiative-local planning state without blocking purge of closed initiative packages.\n"
            "- Future closeout and retention flows can treat promoted docs as authority and initiative artifacts as temporary state.\n\n"
            "## Current Status or Supersession Notes\n\n"
            "- Active as durable guidance under `plan/docs/**`.\n"
            "- Promotion policy and promotion-index records carry the machine-readable provenance for this guidance family.\n"
        )
    if target_family == "pattern":
        return (
            "# Scenario\n\n"
            "Use this pattern when one initiative-local authored input needs to become durable shared guidance without turning `plan/docs/` into a second live workspace. "
            f"{source_summary_line}\n\n"
            "## Recommended Structure\n\n"
            "- Resolve the promotion policy from source artifact kind and target family.\n"
            "- Write the durable document under the governed target root with valid front matter and template headings.\n"
            "- Rebuild the guidance and promotion indexes in the same change.\n\n"
            "## Boundaries or Constraints\n\n"
            "- Promotion is not a substitute for live initiative state or rendered plan views.\n"
            "- Mirrored foundations must update all required roots in the same change set.\n\n"
            "## Usage Notes\n\n"
            f"- Use this pattern for `{source_label}` promotion into durable guidance families.\n"
            "- Keep durable guidance self-contained and rely on machine indexes for provenance.\n\n"
            "## Illustrative Example\n\n"
            f"- Promote a validated initiative-local `{source_artifact_kind.replace('_', ' ')}` into `{target_path}` and keep the guidance and promotion indexes synchronized with the result.\n"
        )
    if target_family == "standard":
        return (
            "# Purpose\n\n"
            "This standard captures the rule-bearing obligations for durable guidance promotion. "
            f"{source_summary_line}\n\n"
            "## Applicability\n\n"
            "- Applies when initiative-local outputs are promoted into `plan/docs/**` guidance roots.\n"
            "- Applies to both pack-wide and project-scoped initiatives when promotion records exist.\n\n"
            "## Required or Prohibited Rules\n\n"
            "- Require one governed promotion record with source, evidence, approval, and target-path metadata.\n"
            "- Require target roots and mirror behavior to match the active promotion policy registry.\n"
            "- Do not promote durable guidance directly into `plan/docs/**` without a recorded initiative-local promotion artifact.\n\n"
            "## Enforcement or Validation Implications\n\n"
            "- Promotion records and promoted docs must pass schema-backed validation.\n"
            "- Guidance and promotion indexes must rebuild cleanly after promotion.\n\n"
            "## Examples\n\n"
            "- `plan/initiatives/example/implementation_slice.md` -> `plan/docs/patterns/example_implementation_slice.md`\n\n"
            "## Notes\n\n"
            "- Durable guidance should stand on its own after the source initiative package is closed and purged.\n"
            "- Promotion indexes carry machine-readable provenance for the guidance family.\n"
        )
    if target_family == "foundation":
        return (
            "# Purpose or Context\n\n"
            "This foundation captures the durable boundary for promotion-authority separation. "
            f"{source_summary_line}\n\n"
            "## Scope Boundary\n\n"
            "- In scope: governed extraction of durable guidance out of live initiative state.\n"
            "- Out of scope: treating live initiative folders as long-term guidance roots.\n\n"
            "## Guiding Principles or Rules\n\n"
            "- Durable guidance promotion is policy-governed and traceable.\n"
            "- Mirrored foundations must remain byte-identical across required roots.\n\n"
            "## Implications for Behavior\n\n"
            "- Operators and agents can rely on promoted guidance as a durable surface without treating initiative-local authored inputs as permanent docs.\n\n"
            "## Related Surfaces\n\n"
            f"- `{target_path}`\n"
            "- `core/python/src/watchtower_core/plan_runtime/guidance_promotion.py`\n"
            "- `plan/.wt/registries/promotion_policy_registry.json`\n\n"
            "## Notes\n\n"
            "- Promotion and guidance indexes retain the machine-readable provenance for these mirrored foundations.\n"
        )
    raise ValueError(f"Unsupported promotion target family: {target_family}")


def extract_markdown_title(path: Path) -> str | None:
    """Extract the first markdown H1 title from one source document."""

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip() or None
    return None


def extract_markdown_summary(path: Path) -> str | None:
    """Extract the first short summary line from a `## Summary` section when present."""

    lines = path.read_text(encoding="utf-8").splitlines()
    summary_started = False
    collected: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == "## Summary":
            summary_started = True
            continue
        if summary_started and stripped.startswith("#"):
            break
        if summary_started and stripped:
            collected.append(stripped)
    if not collected:
        return None
    return " ".join(collected)


def readable_source_artifact_kind(source_artifact_kind: str) -> str:
    """Return a human-readable label for one source artifact kind."""

    return source_artifact_kind.replace("_", " ")


def guidance_title(
    *,
    initiative_title: str,
    target_family: str,
    source_artifact_kind: str,
    source_title: str | None,
) -> str:
    """Build a durable guidance title for one promoted output."""

    _ = initiative_title
    family_label = target_family.replace("_", " ").title()
    source_label = source_title or readable_source_artifact_kind(source_artifact_kind).title()
    return f"Guidance Promotion {family_label}: {source_label}"


def guidance_summary(
    *,
    initiative_title: str,
    initiative_summary: str,
    target_family: str,
    source_artifact_kind: str,
    source_summary: str | None,
) -> str:
    """Build a one-line summary for one promoted output."""

    _ = initiative_title
    fragment = source_summary or initiative_summary
    compact = re.sub(r"\s+", " ", fragment).strip()
    family_label = target_family.replace("_", " ")
    return f"Durable {family_label} for governed guidance promotion. {compact}"


def _extraction_envelope_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"envelope.{initiative_slug}.{stem}"


def _knowledge_candidate_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"candidate.{initiative_slug}.{stem}"


def _observation_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"observation.{initiative_slug}.{stem}"


def _source_note_id(initiative_slug: str, source_path: str) -> str:
    stem = Path(source_path).stem
    return f"note.{initiative_slug}.{stem}"


def _workflow_run_id(initiative_slug: str) -> str:
    return f"run.{initiative_slug}.guidance_promotion"


def _plan_pack_loader(loader: ControlPlaneLoader) -> ControlPlaneLoader:
    if loader.active_pack_settings_path == PLAN_PACK_SETTINGS_PATH:
        return loader
    return loader.derive(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "GuidancePromotionOutput",
    "GuidancePromotionResult",
    "GuidancePromotionService",
    "PROMOTION_RECORD_FILENAME",
    "PLAN_PACK_SETTINGS_PATH",
    "build_guidance_front_matter",
    "default_mirror_target_paths",
    "default_target_family_for_source_kind",
    "default_target_path",
    "guidance_id_for_target_path",
    "source_artifact_kind_for_path",
]
