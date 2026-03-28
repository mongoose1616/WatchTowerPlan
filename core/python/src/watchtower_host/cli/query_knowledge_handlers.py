"""Runtime handlers for knowledge-oriented query commands."""

from __future__ import annotations

import argparse

from watchtower_core.cli.query_presenters import (
    authority_entry_payload,
    print_authority_entry,
    print_template_catalog_entry,
    template_catalog_entry_payload,
)
from watchtower_core.cli.handler_common import (
    _emit_collection_query_results,
    _print_reference_usage_summary,
)
from watchtower_core.control_plane.loader import CORE_PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.control_plane.models import (
    FoundationIndexEntry,
    ReferenceIndexEntry,
    StandardIndexEntry,
    WorkflowIndexEntry,
)
from watchtower_core.query import (
    AuthorityMapQueryService,
    AuthorityMapSearchParams,
    FoundationQueryService,
    FoundationSearchParams,
    ReferenceQueryService,
    ReferenceSearchParams,
    StandardQueryService,
    StandardSearchParams,
    TemplateCatalogQueryService,
    TemplateCatalogSearchParams,
    WorkflowQueryService,
    WorkflowSearchParams,
)


def _run_query_authority(args: argparse.Namespace) -> int:
    service = AuthorityMapQueryService(
        ControlPlaneLoader(),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )
    entries = service.search(
        AuthorityMapSearchParams(
            query=args.query,
            question_id=args.question_id,
            domain=args.domain,
            artifact_kind=args.artifact_kind,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query authority",
        entries=entries,
        noun="authority",
        empty_message="No authority-map entries matched the requested filters.",
        payload_results_factory=lambda: [authority_entry_payload(entry) for entry in entries],
        render_entry=print_authority_entry,
    )


def _run_query_foundations(args: argparse.Namespace) -> int:
    service = FoundationQueryService(ControlPlaneLoader())
    entries = service.search(
        FoundationSearchParams(
            query=args.query,
            foundation_id=args.foundation_id,
            audience=args.audience,
            authority=args.authority,
            tag=args.tag,
            related_path=args.related_path,
            reference_path=args.reference_path,
            cited_by_path=args.cited_by_path,
            applied_by_path=args.applied_by_path,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query foundations",
        entries=entries,
        noun="foundation",
        empty_message="No foundation entries matched the requested filters.",
        payload_results_factory=lambda: [_foundation_entry_payload(entry) for entry in entries],
        render_entry=_print_foundation_entry,
    )


def _run_query_workflows(args: argparse.Namespace) -> int:
    service = WorkflowQueryService(ControlPlaneLoader())
    entries = service.search(
        WorkflowSearchParams(
            query=args.query,
            workflow_id=args.workflow_id,
            workflow_kind=args.workflow_kind,
            phase_type=args.phase_type,
            task_family=args.task_family,
            trigger_tag=args.trigger_tag,
            related_path=args.related_path,
            reference_path=args.reference_path,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query workflows",
        entries=entries,
        noun="workflow",
        empty_message="No workflow entries matched the requested filters.",
        payload_results_factory=lambda: [_workflow_entry_payload(entry) for entry in entries],
        render_entry=_print_workflow_entry,
    )


def _run_query_references(args: argparse.Namespace) -> int:
    service = ReferenceQueryService(ControlPlaneLoader())
    entries = service.search(
        ReferenceSearchParams(
            query=args.query,
            reference_id=args.reference_id,
            repository_status=args.repository_status,
            tag=args.tag,
            related_path=args.related_path,
            upstream_url=args.upstream_url,
            cited_by_path=args.cited_by_path,
            applied_by_path=args.applied_by_path,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query references",
        entries=entries,
        noun="reference",
        empty_message="No reference entries matched the requested filters.",
        payload_results_factory=lambda: [_reference_entry_payload(entry) for entry in entries],
        render_entry=_print_reference_entry,
    )


def _run_query_standards(args: argparse.Namespace) -> int:
    service = StandardQueryService(ControlPlaneLoader())
    entries = service.search(
        StandardSearchParams(
            query=args.query,
            standard_id=args.standard_id,
            category=args.category,
            owner=args.owner,
            tag=args.tag,
            applies_to=args.applies_to,
            related_path=args.related_path,
            reference_path=args.reference_path,
            operationalization_mode=args.operationalization_mode,
            operationalization_path=args.operationalization_path,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query standards",
        entries=entries,
        noun="standard",
        empty_message="No standard entries matched the requested filters.",
        payload_results_factory=lambda: [_standard_entry_payload(entry) for entry in entries],
        render_entry=_print_standard_entry,
    )


def _run_query_templates(args: argparse.Namespace) -> int:
    service = TemplateCatalogQueryService(
        ControlPlaneLoader(),
        pack_settings_path=CORE_PACK_SETTINGS_PATH,
    )
    entries = service.search(
        TemplateCatalogSearchParams(
            query=args.query,
            template_id=args.template_id,
            family_id=args.family_id,
            surface_id=args.surface_id,
            authorship_mode=args.authorship_mode,
            llm_guidance_mode=args.llm_guidance_mode,
            allowed_root=args.allowed_root,
            required_section_id=args.required_section_id,
            required_rendered_surface_id=args.required_rendered_surface_id,
            limit=args.limit,
        )
    )
    return _emit_collection_query_results(
        args,
        command_name="watchtower-core query templates",
        entries=entries,
        noun="template",
        empty_message="No template-catalog entries matched the requested filters.",
        payload_results_factory=lambda: [template_catalog_entry_payload(entry) for entry in entries],
        render_entry=print_template_catalog_entry,
    )


def _foundation_entry_payload(entry: FoundationIndexEntry) -> dict[str, object]:
    return {
        "foundation_id": entry.foundation_id,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "audience": entry.audience,
        "authority": entry.authority,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
        "uses_internal_references": entry.uses_internal_references,
        "uses_external_references": entry.uses_external_references,
        "related_paths": list(entry.related_paths),
        "reference_doc_paths": list(entry.reference_doc_paths),
        "internal_reference_paths": list(entry.internal_reference_paths),
        "external_reference_urls": list(entry.external_reference_urls),
        "cited_by_paths": list(entry.cited_by_paths),
        "applied_by_paths": list(entry.applied_by_paths),
        "aliases": list(entry.aliases),
        "tags": list(entry.tags),
    }


def _print_foundation_entry(entry: FoundationIndexEntry) -> None:
    print(f"- {entry.foundation_id} [{entry.authority}, {entry.audience}]")
    print(f"  {entry.title}")
    print(f"  {entry.summary}")
    print(
        f"  Usage: cited_by={len(entry.cited_by_paths)}, applied_by={len(entry.applied_by_paths)}"
    )


def _workflow_entry_payload(entry: WorkflowIndexEntry) -> dict[str, object]:
    return {
        "workflow_id": entry.workflow_id,
        "workflow_kind": entry.workflow_kind,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "doc_path": entry.doc_path,
        "phase_type": entry.phase_type,
        "task_family": entry.task_family,
        "uses_internal_references": entry.uses_internal_references,
        "uses_external_references": entry.uses_external_references,
        "primary_risks": list(entry.primary_risks),
        "trigger_tags": list(entry.trigger_tags),
        "companion_workflow_ids": list(entry.companion_workflow_ids),
        "composes_module_paths": list(entry.composes_module_paths),
        "related_paths": list(entry.related_paths),
        "reference_doc_paths": list(entry.reference_doc_paths),
        "internal_reference_paths": list(entry.internal_reference_paths),
        "external_reference_urls": list(entry.external_reference_urls),
        "aliases": list(entry.aliases),
        "tags": list(entry.tags),
    }


def _print_workflow_entry(entry: WorkflowIndexEntry) -> None:
    _print_reference_usage_summary(
        header=(
            f"- {entry.workflow_id} "
            f"[{entry.workflow_kind}, {entry.status}, {entry.phase_type}, {entry.task_family}]"
        ),
        title=entry.title,
        summary=entry.summary,
        uses_internal_references=entry.uses_internal_references,
        uses_external_references=entry.uses_external_references,
    )


def _reference_entry_payload(entry: ReferenceIndexEntry) -> dict[str, object]:
    return {
        "reference_id": entry.reference_id,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
        "repository_status": entry.repository_status,
        "uses_internal_references": entry.uses_internal_references,
        "uses_external_references": entry.uses_external_references,
        "canonical_upstream_urls": list(entry.canonical_upstream_urls),
        "cited_by_paths": list(entry.cited_by_paths),
        "applied_by_paths": list(entry.applied_by_paths),
        "related_paths": list(entry.related_paths),
        "aliases": list(entry.aliases),
        "tags": list(entry.tags),
    }


def _print_reference_entry(entry: ReferenceIndexEntry) -> None:
    _print_reference_usage_summary(
        header=f"- {entry.reference_id} [{entry.status}, {entry.repository_status}]",
        title=entry.title,
        summary=entry.summary,
        uses_internal_references=entry.uses_internal_references,
        uses_external_references=entry.uses_external_references,
    )
    if entry.applied_by_paths:
        print(f"  Applied by {len(entry.applied_by_paths)} doc(s).")
    elif entry.cited_by_paths:
        print(f"  Cited by {len(entry.cited_by_paths)} doc(s).")


def _standard_entry_payload(entry: StandardIndexEntry) -> dict[str, object]:
    return {
        "standard_id": entry.standard_id,
        "category": entry.category,
        "title": entry.title,
        "summary": entry.summary,
        "status": entry.status,
        "owner": entry.owner,
        "doc_path": entry.doc_path,
        "updated_at": entry.updated_at,
        "uses_internal_references": entry.uses_internal_references,
        "uses_external_references": entry.uses_external_references,
        "applies_to": list(entry.applies_to),
        "related_paths": list(entry.related_paths),
        "reference_doc_paths": list(entry.reference_doc_paths),
        "internal_reference_paths": list(entry.internal_reference_paths),
        "applied_reference_paths": list(entry.applied_reference_paths),
        "external_reference_urls": list(entry.external_reference_urls),
        "applied_external_reference_urls": list(entry.applied_external_reference_urls),
        "operationalization_modes": list(entry.operationalization_modes),
        "operationalization_paths": list(entry.operationalization_paths),
        "tags": list(entry.tags),
    }


def _print_standard_entry(entry: StandardIndexEntry) -> None:
    print(f"- {entry.standard_id} [{entry.category}, owner={entry.owner}]")
    print(f"  {entry.title}")
    print(f"  {entry.summary}")
    print(
        "  Operationalization: "
        + ", ".join(entry.operationalization_modes)
        + f" across {len(entry.operationalization_paths)} surface(s)"
    )
