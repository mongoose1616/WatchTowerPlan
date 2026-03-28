"""Shared presentation helpers for query handlers."""

from __future__ import annotations

from watchtower_core.control_plane.models import (
    AuthorityMapEntry,
    TemplateCatalogEntry,
    TemplateGuidance,
    TemplateSectionCardinalityRule,
)


def authority_entry_payload(entry: AuthorityMapEntry) -> dict[str, object]:
    """Return one JSON-safe authority-map payload."""

    return {
        "question_id": entry.question_id,
        "domain": entry.domain,
        "question": entry.question,
        "status": entry.status,
        "artifact_kind": entry.artifact_kind,
        "canonical_path": entry.canonical_path,
        "preferred_command": entry.preferred_command,
        "preferred_human_path": entry.preferred_human_path,
        "status_fields": list(entry.status_fields),
        "fallback_paths": list(entry.fallback_paths),
        "aliases": list(entry.aliases),
        "notes": entry.notes,
    }


def print_authority_entry(entry: AuthorityMapEntry) -> None:
    """Render one authority-map entry in human-readable form."""

    print(f"- {entry.question_id} [{entry.domain} -> {entry.artifact_kind}]")
    print(f"  {entry.question}")
    print(f"  Canonical: {entry.canonical_path}")
    print(f"  Command: {entry.preferred_command}")
    if entry.preferred_human_path is not None:
        print(f"  Human: {entry.preferred_human_path}")
    if entry.status_fields:
        print(f"  Status fields: {', '.join(entry.status_fields)}")


def template_catalog_entry_payload(entry: TemplateCatalogEntry) -> dict[str, object]:
    """Return one JSON-safe template-catalog payload."""

    return {
        "template_id": entry.template_id,
        "family_id": entry.family_id,
        "surface_id": entry.surface_id,
        "entry_status": entry.entry_status,
        "authorship_mode": entry.authorship_mode,
        "template_path": entry.template_path,
        "front_matter_schema_id": entry.front_matter_schema_id,
        "required_section_ids": list(entry.required_section_ids),
        "optional_section_ids": list(entry.optional_section_ids),
        "section_order": list(entry.section_order),
        "prohibited_section_ids": list(entry.prohibited_section_ids),
        "section_cardinality_rules": [
            _section_cardinality_rule_payload(rule) for rule in entry.section_cardinality_rules
        ],
        "section_spec_schema_id": entry.section_spec_schema_id,
        "llm_guidance_mode": entry.llm_guidance_mode,
        "llm_guidance": _template_guidance_payload(entry.llm_guidance),
        "operator_notes": entry.operator_notes,
        "required_rendered_surface_ids": list(entry.required_rendered_surface_ids),
        "allowed_roots": list(entry.allowed_roots),
    }


def print_template_catalog_entry(entry: TemplateCatalogEntry) -> None:
    """Render one template-catalog entry in human-readable form."""

    print(f"- {entry.template_id} [{entry.entry_status}, {entry.authorship_mode}]")
    print(f"  Path: {entry.template_path}")
    if entry.family_id is not None:
        print(f"  Family: {entry.family_id}")
    if entry.surface_id is not None:
        print(f"  Surface: {entry.surface_id}")
    print(f"  Allowed roots: {', '.join(entry.allowed_roots)}")
    print(f"  Required sections: {', '.join(entry.required_section_ids)}")
    if entry.llm_guidance is not None:
        print(f"  Goal: {entry.llm_guidance.authoring_goal}")
    if entry.operator_notes is not None:
        print(f"  Notes: {entry.operator_notes}")


def _template_guidance_payload(guidance: TemplateGuidance | None) -> dict[str, object] | None:
    if guidance is None:
        return None
    return {
        "authoring_goal": guidance.authoring_goal,
        "hard_requirements": list(guidance.hard_requirements),
        "advisory_notes": list(guidance.advisory_notes),
    }


def _section_cardinality_rule_payload(
    rule: TemplateSectionCardinalityRule,
) -> dict[str, object]:
    return {
        "section_id": rule.section_id,
        "min_occurs": rule.min_occurs,
        "max_occurs": rule.max_occurs,
        "mutually_exclusive_group": rule.mutually_exclusive_group,
    }


__all__ = [
    "authority_entry_payload",
    "print_authority_entry",
    "print_template_catalog_entry",
    "template_catalog_entry_payload",
]
