"""Documentation, template, and workflow catalog models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class WorkflowMetadataDefinition:
    """Workflow metadata registry entry."""

    workflow_id: str
    phase_type: str
    task_family: str
    primary_risks: tuple[str, ...]
    extra_trigger_tags: tuple[str, ...] = ()
    companion_workflow_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> WorkflowMetadataDefinition:
        return cls(
            workflow_id=document["workflow_id"],
            phase_type=document["phase_type"],
            task_family=document["task_family"],
            primary_risks=tuple(document["primary_risks"]),
            extra_trigger_tags=tuple(document.get("extra_trigger_tags", ())),
            companion_workflow_ids=tuple(document.get("companion_workflow_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class WorkflowMetadataRegistry:
    """Typed workflow-metadata registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[WorkflowMetadataDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> WorkflowMetadataRegistry:
        entries = tuple(
            WorkflowMetadataDefinition.from_document(entry) for entry in document["entries"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, workflow_id: str) -> WorkflowMetadataDefinition:
        """Return one workflow metadata entry by workflow identifier."""
        for entry in self.entries:
            if entry.workflow_id == workflow_id:
                return entry
        raise KeyError(workflow_id)


@dataclass(frozen=True, slots=True)
class DocumentationFamilyEntry:
    """One governed documentation-family binding."""

    family_id: str
    entry_status: str
    summary: str
    front_matter_base_schema_id: str
    front_matter_schema_id: str
    template_ids: tuple[str, ...]
    allowed_roots: tuple[str, ...]
    authorship_mode: str
    required_index_ids: tuple[str, ...]
    section_spec_schema_id: str | None = None
    required_rendered_surface_ids: tuple[str, ...] = ()
    mirror_group_id: str | None = None
    required_mirror_roots: tuple[str, ...] = ()
    equivalence_mode: str | None = None
    mirror_update_mode: str | None = None
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> DocumentationFamilyEntry:
        return cls(
            family_id=document["family_id"],
            entry_status=document["entry_status"],
            summary=document["summary"],
            front_matter_base_schema_id=document["front_matter_base_schema_id"],
            front_matter_schema_id=document["front_matter_schema_id"],
            template_ids=tuple(document["template_ids"]),
            allowed_roots=tuple(document["allowed_roots"]),
            authorship_mode=document["authorship_mode"],
            required_index_ids=tuple(document["required_index_ids"]),
            section_spec_schema_id=document.get("section_spec_schema_id"),
            required_rendered_surface_ids=tuple(document.get("required_rendered_surface_ids", ())),
            mirror_group_id=document.get("mirror_group_id"),
            required_mirror_roots=tuple(document.get("required_mirror_roots", ())),
            equivalence_mode=document.get("equivalence_mode"),
            mirror_update_mode=document.get("mirror_update_mode"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class DocumentationFamilyRegistry:
    """Typed documentation-family registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[DocumentationFamilyEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> DocumentationFamilyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                DocumentationFamilyEntry.from_document(item) for item in document["entries"]
            ),
            notes=document.get("notes"),
        )

    def get(self, family_id: str) -> DocumentationFamilyEntry:
        """Return one documentation-family entry by identifier."""

        for entry in self.entries:
            if entry.family_id == family_id:
                return entry
        raise KeyError(family_id)


@dataclass(frozen=True, slots=True)
class TemplateGuidance:
    """Structured LLM-facing template guidance metadata."""

    authoring_goal: str
    hard_requirements: tuple[str, ...] = ()
    advisory_notes: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TemplateGuidance:
        return cls(
            authoring_goal=document["authoring_goal"],
            hard_requirements=tuple(document.get("hard_requirements", ())),
            advisory_notes=tuple(document.get("advisory_notes", ())),
        )


@dataclass(frozen=True, slots=True)
class TemplateSectionCardinalityRule:
    """Cardinality constraint for one template section."""

    section_id: str
    min_occurs: int
    max_occurs: int
    mutually_exclusive_group: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TemplateSectionCardinalityRule:
        return cls(
            section_id=document["section_id"],
            min_occurs=int(document["min_occurs"]),
            max_occurs=int(document["max_occurs"]),
            mutually_exclusive_group=document.get("mutually_exclusive_group"),
        )


@dataclass(frozen=True, slots=True)
class TemplateCatalogEntry:
    """One governed template-catalog entry."""

    template_id: str
    entry_status: str
    authorship_mode: str
    template_path: str
    required_section_ids: tuple[str, ...]
    optional_section_ids: tuple[str, ...]
    section_order: tuple[str, ...]
    llm_guidance_mode: str
    allowed_roots: tuple[str, ...]
    family_id: str | None = None
    surface_id: str | None = None
    front_matter_schema_id: str | None = None
    prohibited_section_ids: tuple[str, ...] = ()
    section_cardinality_rules: tuple[TemplateSectionCardinalityRule, ...] = ()
    section_spec_schema_id: str | None = None
    llm_guidance: TemplateGuidance | None = None
    operator_notes: str | None = None
    required_rendered_surface_ids: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TemplateCatalogEntry:
        guidance_document = document.get("llm_guidance")
        return cls(
            template_id=document["template_id"],
            entry_status=document["entry_status"],
            authorship_mode=document["authorship_mode"],
            template_path=document["template_path"],
            required_section_ids=tuple(document["required_section_ids"]),
            optional_section_ids=tuple(document["optional_section_ids"]),
            section_order=tuple(document["section_order"]),
            llm_guidance_mode=document["llm_guidance_mode"],
            allowed_roots=tuple(document["allowed_roots"]),
            family_id=document.get("family_id"),
            surface_id=document.get("surface_id"),
            front_matter_schema_id=document.get("front_matter_schema_id"),
            prohibited_section_ids=tuple(document.get("prohibited_section_ids", ())),
            section_cardinality_rules=tuple(
                TemplateSectionCardinalityRule.from_document(item)
                for item in document.get("section_cardinality_rules", ())
            ),
            section_spec_schema_id=document.get("section_spec_schema_id"),
            llm_guidance=(
                TemplateGuidance.from_document(guidance_document)
                if isinstance(guidance_document, dict)
                else None
            ),
            operator_notes=document.get("operator_notes"),
            required_rendered_surface_ids=tuple(document.get("required_rendered_surface_ids", ())),
        )


@dataclass(frozen=True, slots=True)
class TemplateCatalog:
    """Typed template-catalog artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[TemplateCatalogEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> TemplateCatalog:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(TemplateCatalogEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, template_id: str) -> TemplateCatalogEntry:
        """Return one template entry by identifier."""

        for entry in self.entries:
            if entry.template_id == template_id:
                return entry
        raise KeyError(template_id)
