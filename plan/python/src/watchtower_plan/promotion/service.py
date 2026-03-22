"""Governed initiative-to-guidance promotion helpers for the live plan workspace."""

from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import (
    DocumentationFamilyHelper,
    PromotionPolicyHelper,
    TemplateCatalogHelper,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import ExtractionOutputEnvelopeArtifact
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_plan.promotion.extraction import (
    GuidancePromotionExtractionHelper,
    plan_pack_loader,
)
from watchtower_plan.promotion.models import (
    GuidancePromotionOutput,
    GuidancePromotionResult,
)
from watchtower_plan.promotion.rendering import render_guidance_document

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"
PROMOTION_RECORD_FILENAME = "guidance_promotion_record.bootstrap.json"


class GuidancePromotionService:
    """Promote approved initiative-local outputs into durable plan guidance roots."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._pack_loader = plan_pack_loader(loader)
        self._workspace_paths = PackWorkspacePaths.from_loader(
            self._pack_loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
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
        self._pack_settings = self._pack_loader.load_pack_settings()
        self._extraction = GuidancePromotionExtractionHelper(
            loader,
            pack_loader=self._pack_loader,
            policy_helper=self._policy_helper,
            documentation_helper=self._documentation_helper,
            template_helper=self._template_helper,
            pack_settings=self._pack_settings,
        )

    def extract_packwide(
        self,
        initiative_slug: str,
        *,
        promotion_record_filename: str = PROMOTION_RECORD_FILENAME,
        updated_at: str | None = None,
    ) -> tuple[ExtractionOutputEnvelopeArtifact, ...]:
        """Build validated extraction envelopes for one pack-wide initiative."""

        return self._extract(
            initiative_root=Path(self._workspace_paths.initiatives_root)
            / initiative_slug,
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
            initiative_root=Path(
                self._workspace_paths.project_initiatives_root_relative(project_slug)
            )
            / initiative_slug,
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
            initiative_root=Path(self._workspace_paths.initiatives_root)
            / initiative_slug,
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
            initiative_root=Path(
                self._workspace_paths.project_initiatives_root_relative(project_slug)
            )
            / initiative_slug,
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
        ) = self._extraction.load_promotion_inputs(
            initiative_root=initiative_root,
            promotion_record_filename=promotion_record_filename,
        )
        resolved_candidates = self._extraction.resolve_candidates(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
        )
        extraction_envelopes = self._extraction.build_extraction_envelopes(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
            candidates=resolved_candidates,
            updated_at=updated_at,
        )

        outputs: list[GuidancePromotionOutput] = []
        rendered_documents: list[tuple[str, str]] = []
        updated_candidates: list[dict[str, object]] = []

        for candidate in resolved_candidates:
            rendered = render_guidance_document(
                initiative_document=initiative_document,
                promotion_document=promotion_document,
                source_path=candidate.source_path,
                source_artifact_kind=candidate.source_artifact_kind,
                target_family=candidate.target_family,
                target_path=candidate.target_path,
                mirror_target_paths=candidate.mirror_target_paths,
                template_path=candidate.template_path,
                updated_at=updated_at,
                source_title=candidate.source_title,
                source_summary=candidate.source_summary,
                documentation_helper=self._documentation_helper,
                pack_loader=self._pack_loader,
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
                {str(candidate["review_path"]) for candidate in updated_candidates}
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
        initiative_document, promotion_document, _ = (
            self._extraction.load_promotion_inputs(
                initiative_root=initiative_root,
                promotion_record_filename=promotion_record_filename,
            )
        )
        resolved_candidates = self._extraction.resolve_candidates(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
        )
        return self._extraction.build_extraction_envelopes(
            initiative_document=initiative_document,
            promotion_document=promotion_document,
            candidates=resolved_candidates,
            updated_at=updated_at,
        )


__all__ = [
    "GuidancePromotionOutput",
    "GuidancePromotionResult",
    "GuidancePromotionService",
    "PROMOTION_RECORD_FILENAME",
    "PLAN_PACK_SETTINGS_PATH",
]
