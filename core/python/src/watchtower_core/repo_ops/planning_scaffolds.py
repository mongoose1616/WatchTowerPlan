"""Template-aligned planning scaffold helpers."""

from __future__ import annotations

from watchtower_core.adapters import render_front_matter
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.front_matter_paths import normalize_governed_applies_to_values
from watchtower_core.repo_ops.planning_bootstrap_support import (
    build_acceptance_contract_artifact,
    build_bootstrap_identifiers,
    build_bootstrap_scaffold_params,
    build_bootstrap_task_create_params,
    build_validation_evidence_artifact,
    refresh_bootstrap_document_surfaces,
    refresh_planning_surfaces,
)
from watchtower_core.repo_ops.planning_scaffold_models import (
    AcceptanceContractResult,
    PlanBootstrapParams,
    PlanBootstrapResult,
    PlanScaffoldParams,
    ScaffoldDocumentResult,
    ValidationEvidenceResult,
)
from watchtower_core.repo_ops.planning_scaffold_rendering import render_document_content
from watchtower_core.repo_ops.planning_scaffold_specs import render_sections
from watchtower_core.repo_ops.planning_scaffold_support import (
    PLAN_KIND_CHOICES,
    RenderedDocument,
    compact_front_matter,
    default_authority_for_kind,
    default_status_for_kind,
    ensure_available_path,
    id_label_for_kind,
    normalize_list,
    normalize_plan_kind,
    normalize_required_string,
    ordered_front_matter,
    scaffold_directory_for_kind,
    scaffold_schema_for_kind,
    scaffold_type_for_kind,
    slugify_file_stem,
    status_label_for_kind,
    validate_rendered_document,
)
from watchtower_core.repo_ops.sync.coordination import CoordinationSyncService
from watchtower_core.repo_ops.task_lifecycle import (
    TaskCreateParams,
    TaskLifecycleService,
    TaskMutationResult,
)
from watchtower_core.utils import utc_timestamp_now

__all__ = [
    "PLAN_KIND_CHOICES",
    "PlanBootstrapParams",
    "PlanBootstrapResult",
    "PlanScaffoldParams",
    "PlanningScaffoldService",
    "ScaffoldDocumentResult",
]


class PlanningScaffoldService:
    """Render compact planning scaffolds aligned with current repository templates."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def scaffold(self, params: PlanScaffoldParams, *, write: bool) -> ScaffoldDocumentResult:
        rendered = self._render_scaffold(params)
        if write:
            self._write_rendered_document(rendered)
            refresh_planning_surfaces(self._loader, kind=rendered.kind)
            if self._trace_participates_in_coordination(rendered.trace_id):
                CoordinationSyncService(self._loader).run(write=True)
        return _scaffold_result_from_rendered(rendered, wrote=write)

    def bootstrap(self, params: PlanBootstrapParams, *, write: bool) -> PlanBootstrapResult:
        updated_at = params.updated_at or utc_timestamp_now()
        identifiers = build_bootstrap_identifiers(params)
        rendered_documents = tuple(
            self._render_scaffold(scaffold_params)
            for scaffold_params in build_bootstrap_scaffold_params(
                params,
                identifiers,
                updated_at=updated_at,
            )
        )
        bootstrap_task_params = build_bootstrap_task_create_params(
            params,
            identifiers,
            updated_at=updated_at,
            related_ids=tuple(document.document_id for document in rendered_documents)
            + (identifiers.contract_id,),
        )
        preview_task_result = self._bootstrap_task_result(bootstrap_task_params, write=False)
        acceptance_contract_document, acceptance_contract_preview = (
            build_acceptance_contract_artifact(
                self._loader,
                params,
                identifiers,
                updated_at=updated_at,
                rendered_documents=rendered_documents,
                task_doc_path=preview_task_result.doc_path,
            )
        )
        validation_evidence_document, validation_evidence_preview = (
            build_validation_evidence_artifact(
                self._loader,
                params,
                identifiers,
                updated_at=updated_at,
                rendered_documents=rendered_documents,
                task_doc_path=preview_task_result.doc_path,
                contract_doc_path=acceptance_contract_preview.doc_path,
            )
        )

        task_result = preview_task_result
        if write:
            for rendered in rendered_documents:
                self._write_rendered_document(rendered)
            refresh_bootstrap_document_surfaces(
                self._loader,
                include_decision=params.include_decision,
            )
            self._write_json_artifact(
                acceptance_contract_preview.doc_path,
                acceptance_contract_document,
            )
            task_result = self._bootstrap_task_result(bootstrap_task_params, write=True)
            self._write_json_artifact(
                validation_evidence_preview.doc_path,
                validation_evidence_document,
            )
            CoordinationSyncService(self._loader).run(write=True)

        return PlanBootstrapResult(
            documents=tuple(
                _scaffold_result_from_rendered(rendered, wrote=write)
                for rendered in rendered_documents
            ),
            acceptance_contract=_acceptance_contract_result_from_preview(
                acceptance_contract_preview,
                wrote=write,
            ),
            validation_evidence=_validation_evidence_result_from_preview(
                validation_evidence_preview,
                wrote=write,
            ),
            task_result=TaskMutationResult(
                task_id=task_result.task_id,
                title=task_result.title,
                summary=task_result.summary,
                trace_id=task_result.trace_id,
                task_status=task_result.task_status,
                task_kind=task_result.task_kind,
                priority=task_result.priority,
                owner=task_result.owner,
                updated_at=task_result.updated_at,
                doc_path=task_result.doc_path,
                previous_doc_path=task_result.previous_doc_path,
                moved=task_result.moved,
                changed=task_result.changed,
                wrote=write,
                coordination_refreshed=write,
                closeout_recommended=task_result.closeout_recommended,
            ),
            wrote=write,
            sync_refreshed=write,
        )

    def _render_scaffold(self, params: PlanScaffoldParams) -> RenderedDocument:
        kind = normalize_plan_kind(params.kind)
        updated_at = params.updated_at or utc_timestamp_now()
        applies_to = normalize_governed_applies_to_values(
            params.applies_to,
            origin=f"{kind} scaffold applies_to",
            repo_root=self._loader.repo_root,
        )
        front_matter = compact_front_matter(
            {
                "trace_id": normalize_required_string(params.trace_id, label="trace_id"),
                "id": normalize_required_string(params.document_id, label="document_id"),
                "title": normalize_required_string(params.title, label="title"),
                "summary": normalize_required_string(params.summary, label="summary"),
                "type": scaffold_type_for_kind(kind),
                "status": normalize_required_string(
                    params.status or default_status_for_kind(kind),
                    label="status",
                ),
                "owner": normalize_required_string(params.owner, label="owner"),
                "updated_at": updated_at,
                "audience": "shared",
                "authority": default_authority_for_kind(kind),
                "applies_to": applies_to,
                "aliases": normalize_list(params.aliases),
            }
        )
        doc_path = (
            f"{scaffold_directory_for_kind(kind)}/"
            f"{slugify_file_stem(params.file_stem or params.title)}.md"
        )
        ensure_available_path(self._loader, doc_path)
        sections = render_sections(kind, front_matter, params)
        content = render_document_content(front_matter["title"], sections)
        rendered = RenderedDocument(
            kind=kind,
            document_id=str(front_matter["id"]),
            trace_id=str(front_matter["trace_id"]),
            title=str(front_matter["title"]),
            summary=str(front_matter["summary"]),
            status=str(front_matter["status"]),
            schema_id=scaffold_schema_for_kind(kind),
            id_label=id_label_for_kind(kind),
            status_label=status_label_for_kind(kind),
            doc_path=doc_path,
            front_matter=front_matter,
            sections=sections,
            content=content,
        )
        validate_rendered_document(self._loader, rendered)
        return rendered

    def _bootstrap_task_result(
        self,
        task_params: TaskCreateParams,
        *,
        write: bool,
    ) -> TaskMutationResult:
        return TaskLifecycleService(self._loader).create(task_params, write=write)

    def _write_rendered_document(self, rendered: RenderedDocument) -> None:
        path = self._loader.repo_root / rendered.doc_path
        path.parent.mkdir(parents=True, exist_ok=True)
        rendered_front_matter = render_front_matter(ordered_front_matter(rendered.front_matter))
        path.write_text(
            f"---\n{rendered_front_matter}\n---\n\n{rendered.content}",
            encoding="utf-8",
        )

    def _write_json_artifact(
        self,
        relative_path: str,
        document: dict[str, object],
    ) -> None:
        self._loader.artifact_store.write_json_object(relative_path, document)

    def _trace_participates_in_coordination(self, trace_id: str) -> bool:
        try:
            self._loader.load_traceability_index().get(trace_id)
            return True
        except KeyError:
            return any(
                entry.trace_id == trace_id for entry in self._loader.load_task_index().entries
            )


def _scaffold_result_from_rendered(
    rendered: RenderedDocument,
    *,
    wrote: bool,
) -> ScaffoldDocumentResult:
    return ScaffoldDocumentResult(
        kind=rendered.kind,
        document_id=rendered.document_id,
        trace_id=rendered.trace_id,
        title=rendered.title,
        summary=rendered.summary,
        status=rendered.status,
        doc_path=rendered.doc_path,
        content=rendered.content,
        wrote=wrote,
    )


def _acceptance_contract_result_from_preview(
    preview: AcceptanceContractResult,
    *,
    wrote: bool,
) -> AcceptanceContractResult:
    return AcceptanceContractResult(
        contract_id=preview.contract_id,
        trace_id=preview.trace_id,
        source_prd_id=preview.source_prd_id,
        title=preview.title,
        doc_path=preview.doc_path,
        content=preview.content,
        wrote=wrote,
    )


def _validation_evidence_result_from_preview(
    preview: ValidationEvidenceResult,
    *,
    wrote: bool,
) -> ValidationEvidenceResult:
    return ValidationEvidenceResult(
        evidence_id=preview.evidence_id,
        trace_id=preview.trace_id,
        title=preview.title,
        overall_result=preview.overall_result,
        doc_path=preview.doc_path,
        content=preview.content,
        wrote=wrote,
    )
