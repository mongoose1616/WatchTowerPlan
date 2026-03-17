"""Typed models for schema catalog and registry artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.workspace import WorkspaceConfig


@dataclass(frozen=True, slots=True)
class SchemaCatalogRecord:
    """Catalog entry for a published schema."""

    schema_id: str
    title: str
    description: str
    status: str
    schema_family: str
    subject_kind: str
    version: str
    canonical_relative_path: str
    canonical_path: Path
    aliases: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        workspace_config: WorkspaceConfig,
    ) -> SchemaCatalogRecord:
        return cls(
            schema_id=document["schema_id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            schema_family=document["schema_family"],
            subject_kind=document["subject_kind"],
            version=document["version"],
            canonical_relative_path=document["canonical_path"],
            canonical_path=workspace_config.resolve_path(document["canonical_path"]),
            aliases=tuple(document.get("aliases", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class SchemaCatalog:
    """Typed schema-catalog artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    records: tuple[SchemaCatalogRecord, ...]

    @classmethod
    def from_document(
        cls,
        document: dict[str, Any],
        workspace_config: WorkspaceConfig,
    ) -> SchemaCatalog:
        records = tuple(
            SchemaCatalogRecord.from_document(record, workspace_config)
            for record in document["schemas"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            records=records,
        )

    @classmethod
    def merge(cls, *catalogs: SchemaCatalog) -> SchemaCatalog:
        """Return one schema catalog with records combined in declaration order."""

        if not catalogs:
            raise ValueError("SchemaCatalog.merge requires at least one catalog.")

        primary = catalogs[0]
        merged_records: list[SchemaCatalogRecord] = []
        seen_schema_ids: set[str] = set()
        for catalog in catalogs:
            if catalog.schema_id != primary.schema_id:
                raise ValueError("Merged schema catalogs must share the same $schema value.")
            if catalog.artifact_id != primary.artifact_id:
                raise ValueError("Merged schema catalogs must share the same artifact ID.")
            for record in catalog.records:
                if record.schema_id in seen_schema_ids:
                    raise ValueError(
                        f"Merged schema catalogs contain duplicate schema IDs: {record.schema_id}"
                    )
                seen_schema_ids.add(record.schema_id)
                merged_records.append(record)

        return cls(
            schema_id=primary.schema_id,
            artifact_id=primary.artifact_id,
            title=primary.title,
            status=primary.status,
            records=tuple(merged_records),
        )

    def get(self, schema_id: str) -> SchemaCatalogRecord:
        """Return a catalog record by schema identifier."""
        for record in self.records:
            if record.schema_id == schema_id:
                return record
        raise KeyError(schema_id)


@dataclass(frozen=True, slots=True)
class ValidatorDefinition:
    """Validator registry entry."""

    validator_id: str
    title: str
    description: str
    status: str
    engine: str
    artifact_kind: str
    applies_to: tuple[str, ...]
    schema_ids: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidatorDefinition:
        return cls(
            validator_id=document["id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            engine=document["engine"],
            artifact_kind=document["artifact_kind"],
            applies_to=tuple(document["applies_to"]),
            schema_ids=tuple(document.get("schema_ids", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ValidatorRegistry:
    """Typed validator-registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    validators: tuple[ValidatorDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidatorRegistry:
        validators = tuple(
            ValidatorDefinition.from_document(entry) for entry in document["validators"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            validators=validators,
        )

    @classmethod
    def merge(cls, *registries: ValidatorRegistry) -> ValidatorRegistry:
        """Return one validator registry with entries combined in declaration order."""

        if not registries:
            raise ValueError("ValidatorRegistry.merge requires at least one registry.")

        primary = registries[0]
        merged_validators: list[ValidatorDefinition] = []
        seen_validator_ids: set[str] = set()
        for registry in registries:
            if registry.schema_id != primary.schema_id:
                raise ValueError(
                    "Merged validator registries must share the same $schema value."
                )
            if registry.artifact_id != primary.artifact_id:
                raise ValueError(
                    "Merged validator registries must share the same artifact ID."
                )
            for validator in registry.validators:
                if validator.validator_id in seen_validator_ids:
                    raise ValueError(
                        "Merged validator registries contain duplicate validator IDs: "
                        f"{validator.validator_id}"
                    )
                seen_validator_ids.add(validator.validator_id)
                merged_validators.append(validator)

        return cls(
            schema_id=primary.schema_id,
            artifact_id=primary.artifact_id,
            title=primary.title,
            status=primary.status,
            validators=tuple(merged_validators),
        )

    def get(self, validator_id: str) -> ValidatorDefinition:
        """Return a validator definition by identifier."""
        for entry in self.validators:
            if entry.validator_id == validator_id:
                return entry
        raise KeyError(validator_id)


@dataclass(frozen=True, slots=True)
class ValidationSuiteStepDefinition:
    """Validation suite step definition."""

    step_id: str
    title: str
    description: str
    step_kind: str
    paths: tuple[str, ...] = ()
    validator_id: str | None = None
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationSuiteStepDefinition:
        return cls(
            step_id=document["id"],
            title=document["title"],
            description=document["description"],
            step_kind=document["step_kind"],
            paths=tuple(document.get("paths", ())),
            validator_id=document.get("validator_id"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ValidationSuiteDefinition:
    """Validation suite definition."""

    suite_id: str
    title: str
    description: str
    status: str
    steps: tuple[ValidationSuiteStepDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationSuiteDefinition:
        return cls(
            suite_id=document["id"],
            title=document["title"],
            description=document["description"],
            status=document["status"],
            steps=tuple(
                ValidationSuiteStepDefinition.from_document(entry)
                for entry in document["steps"]
            ),
            notes=document.get("notes"),
        )

    def get_step(self, step_id: str) -> ValidationSuiteStepDefinition:
        """Return one validation suite step by identifier."""

        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(step_id)


@dataclass(frozen=True, slots=True)
class ValidationSuiteRegistry:
    """Typed validation-suite registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    suites: tuple[ValidationSuiteDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ValidationSuiteRegistry:
        suites = tuple(
            ValidationSuiteDefinition.from_document(entry) for entry in document["suites"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            suites=suites,
        )

    def get(self, suite_id: str) -> ValidationSuiteDefinition:
        """Return one validation suite by identifier."""

        for suite in self.suites:
            if suite.suite_id == suite_id:
                return suite
        raise KeyError(suite_id)


@dataclass(frozen=True, slots=True)
class AuthorityMapEntry:
    """Authority-map registry entry."""

    question_id: str
    domain: str
    question: str
    status: str
    artifact_kind: str
    canonical_path: str
    preferred_command: str
    fallback_paths: tuple[str, ...]
    preferred_human_path: str | None = None
    status_fields: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> AuthorityMapEntry:
        return cls(
            question_id=document["question_id"],
            domain=document["domain"],
            question=document["question"],
            status=document["status"],
            artifact_kind=document["artifact_kind"],
            canonical_path=document["canonical_path"],
            preferred_command=document["preferred_command"],
            fallback_paths=tuple(document["fallback_paths"]),
            preferred_human_path=document.get("preferred_human_path"),
            status_fields=tuple(document.get("status_fields", ())),
            aliases=tuple(document.get("aliases", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class AuthorityMap:
    """Typed authority-map registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[AuthorityMapEntry, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> AuthorityMap:
        entries = tuple(
            AuthorityMapEntry.from_document(entry) for entry in document["entries"]
        )
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=entries,
        )

    def get(self, question_id: str) -> AuthorityMapEntry:
        """Return one authority-map entry by identifier."""
        for entry in self.entries:
            if entry.question_id == question_id:
                return entry
        raise KeyError(question_id)


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
            WorkflowMetadataDefinition.from_document(entry)
            for entry in document["entries"]
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
class HumanSurfacePolicySurfaceDefinition:
    """One governed human-facing surface under a declared root."""

    relative_path: str
    entity_shape: str
    surface_role: str
    mode: str
    authorship_mode: str
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> HumanSurfacePolicySurfaceDefinition:
        return cls(
            relative_path=document["relative_path"],
            entity_shape=document["entity_shape"],
            surface_role=document["surface_role"],
            mode=document["mode"],
            authorship_mode=document["authorship_mode"],
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class HumanSurfacePolicyEntry:
    """One human-surface placement rule for a root or root pattern."""

    policy_id: str
    path_pattern: str
    match_mode: str
    root_kind: str
    entry_status: str
    governing_surfaces: tuple[str, ...]
    clarifying_rule: str
    surfaces: tuple[HumanSurfacePolicySurfaceDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> HumanSurfacePolicyEntry:
        return cls(
            policy_id=document["policy_id"],
            path_pattern=document["path_pattern"],
            match_mode=document["match_mode"],
            root_kind=document["root_kind"],
            entry_status=document["entry_status"],
            governing_surfaces=tuple(document.get("governing_surfaces", ())),
            clarifying_rule=document["clarifying_rule"],
            surfaces=tuple(
                HumanSurfacePolicySurfaceDefinition.from_document(item)
                for item in document["surfaces"]
            ),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class HumanSurfacePolicyRegistry:
    """Typed human-surface placement policy registry."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[HumanSurfacePolicyEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> HumanSurfacePolicyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                HumanSurfacePolicyEntry.from_document(item)
                for item in document["entries"]
            ),
            notes=document.get("notes"),
        )

    def get(self, policy_id: str) -> HumanSurfacePolicyEntry:
        """Return one policy entry by identifier."""

        for entry in self.entries:
            if entry.policy_id == policy_id:
                return entry
        raise KeyError(policy_id)


@dataclass(frozen=True, slots=True)
class RetentionPolicyEntry:
    """One retention-policy rule for a live or legacy repository subtree."""

    policy_id: str
    path_pattern: str
    match_mode: str
    path_kind: str
    phase_qualifier: str
    entry_status: str
    current_disposition: str
    clean_endstate_disposition: str
    operational_visibility: str
    purge_gate: str
    governing_surfaces: tuple[str, ...]
    clarifying_rule: str
    surviving_authority_paths: tuple[str, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RetentionPolicyEntry:
        return cls(
            policy_id=document["policy_id"],
            path_pattern=document["path_pattern"],
            match_mode=document["match_mode"],
            path_kind=document["path_kind"],
            phase_qualifier=document["phase_qualifier"],
            entry_status=document["entry_status"],
            current_disposition=document["current_disposition"],
            clean_endstate_disposition=document["clean_endstate_disposition"],
            operational_visibility=document["operational_visibility"],
            purge_gate=document["purge_gate"],
            governing_surfaces=tuple(document["governing_surfaces"]),
            clarifying_rule=document["clarifying_rule"],
            surviving_authority_paths=tuple(document["surviving_authority_paths"]),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class RetentionPolicyRegistry:
    """Typed retention-policy registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[RetentionPolicyEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RetentionPolicyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                RetentionPolicyEntry.from_document(item) for item in document["entries"]
            ),
            notes=document.get("notes"),
        )

    def get(self, policy_id: str) -> RetentionPolicyEntry:
        """Return one policy entry by identifier."""

        for entry in self.entries:
            if entry.policy_id == policy_id:
                return entry
        raise KeyError(policy_id)


@dataclass(frozen=True, slots=True)
class ArtifactFamilyEntry:
    """One governed artifact-family entry for one pack-local family."""

    family_id: str
    entry_status: str
    summary: str
    canonical_schema_id: str
    placement_roots: tuple[str, ...]
    status_field: str
    allowed_status_values: tuple[str, ...] = ()
    renderable: bool = False
    rendered_companion_surface_ids: tuple[str, ...] = ()
    derived_index_ids: tuple[str, ...] = ()
    visibility: str = "hidden"
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ArtifactFamilyEntry:
        return cls(
            family_id=document["family_id"],
            entry_status=document["entry_status"],
            summary=document["summary"],
            canonical_schema_id=document["canonical_schema_id"],
            placement_roots=tuple(document["placement_roots"]),
            status_field=document["status_field"],
            allowed_status_values=tuple(document.get("allowed_status_values", ())),
            renderable=bool(document["renderable"]),
            rendered_companion_surface_ids=tuple(
                document.get("rendered_companion_surface_ids", ())
            ),
            derived_index_ids=tuple(document["derived_index_ids"]),
            visibility=document["visibility"],
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ArtifactFamilyRegistry:
    """Typed artifact-family registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[ArtifactFamilyEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ArtifactFamilyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(ArtifactFamilyEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, family_id: str) -> ArtifactFamilyEntry:
        """Return one artifact-family entry by identifier."""

        for entry in self.entries:
            if entry.family_id == family_id:
                return entry
        raise KeyError(family_id)


@dataclass(frozen=True, slots=True)
class LifecycleStageEntry:
    """One governed lifecycle-stage entry for plan-runtime work."""

    stage_id: str
    value: str
    entry_status: str
    summary: str
    current_phase: str
    terminal: bool
    allowed_families: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> LifecycleStageEntry:
        return cls(
            stage_id=document["stage_id"],
            value=document["value"],
            entry_status=document["entry_status"],
            summary=document["summary"],
            current_phase=document["current_phase"],
            terminal=bool(document["terminal"]),
            allowed_families=tuple(document.get("allowed_families", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class LifecycleStageRegistry:
    """Typed lifecycle-stage registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[LifecycleStageEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> LifecycleStageRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(LifecycleStageEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, value: str) -> LifecycleStageEntry:
        """Return one lifecycle-stage entry by value."""

        for entry in self.entries:
            if entry.value == value:
                return entry
        raise KeyError(value)


@dataclass(frozen=True, slots=True)
class ReviewStatusEntry:
    """One governed review-status entry for plan-runtime approval state."""

    review_status_id: str
    value: str
    entry_status: str
    summary: str
    allows_execution: bool
    allowed_families: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ReviewStatusEntry:
        return cls(
            review_status_id=document["review_status_id"],
            value=document["value"],
            entry_status=document["entry_status"],
            summary=document["summary"],
            allows_execution=bool(document["allows_execution"]),
            allowed_families=tuple(document.get("allowed_families", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ReviewStatusRegistry:
    """Typed review-status registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[ReviewStatusEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ReviewStatusRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(ReviewStatusEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, value: str) -> ReviewStatusEntry:
        """Return one review-status entry by value."""

        for entry in self.entries:
            if entry.value == value:
                return entry
        raise KeyError(value)


@dataclass(frozen=True, slots=True)
class SourceTypeEntry:
    """One governed source-type entry for plan-runtime provenance."""

    source_type_id: str
    value: str
    entry_status: str
    summary: str
    source_class: str
    allowed_families: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> SourceTypeEntry:
        return cls(
            source_type_id=document["source_type_id"],
            value=document["value"],
            entry_status=document["entry_status"],
            summary=document["summary"],
            source_class=document["source_class"],
            allowed_families=tuple(document.get("allowed_families", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class SourceTypeRegistry:
    """Typed source-type registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[SourceTypeEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> SourceTypeRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(SourceTypeEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, value: str) -> SourceTypeEntry:
        """Return one source-type entry by value."""

        for entry in self.entries:
            if entry.value == value:
                return entry
        raise KeyError(value)


@dataclass(frozen=True, slots=True)
class RenderedSurfaceColumnDefinition:
    """Rendered-surface column definition."""

    header: str
    field: str
    formatter: str
    path_field: str | None = None
    label_field: str | None = None
    empty_value: str | None = None
    enabled_when_key: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceColumnDefinition:
        return cls(
            header=document["header"],
            field=document["field"],
            formatter=document["formatter"],
            path_field=document.get("path_field"),
            label_field=document.get("label_field"),
            empty_value=document.get("empty_value"),
            enabled_when_key=document.get("enabled_when_key"),
        )


@dataclass(frozen=True, slots=True)
class RenderedSurfaceSectionDefinition:
    """Rendered-surface section definition."""

    section_id: str
    kind: str
    source_key: str
    title: str | None = None
    empty_message: str | None = None
    columns: tuple[RenderedSurfaceColumnDefinition, ...] = ()
    label_field: str | None = None
    count_field: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceSectionDefinition:
        return cls(
            section_id=document["section_id"],
            kind=document["kind"],
            source_key=document["source_key"],
            title=document.get("title"),
            empty_message=document.get("empty_message"),
            columns=tuple(
                RenderedSurfaceColumnDefinition.from_document(item)
                for item in document.get("columns", ())
            ),
            label_field=document.get("label_field"),
            count_field=document.get("count_field"),
        )


@dataclass(frozen=True, slots=True)
class RenderedSurfaceDefinition:
    """Rendered-surface registry entry."""

    surface_id: str
    title: str
    output_path: str
    sections: tuple[RenderedSurfaceSectionDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceDefinition:
        return cls(
            surface_id=document["surface_id"],
            title=document["title"],
            output_path=document["output_path"],
            sections=tuple(
                RenderedSurfaceSectionDefinition.from_document(item)
                for item in document["sections"]
            ),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class RenderedSurfaceRegistry:
    """Typed rendered-surface registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    surfaces: tuple[RenderedSurfaceDefinition, ...]

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> RenderedSurfaceRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            surfaces=tuple(
                RenderedSurfaceDefinition.from_document(item)
                for item in document["surfaces"]
            ),
        )

    def get(self, surface_id: str) -> RenderedSurfaceDefinition:
        """Return one rendered-surface definition by identifier."""
        for surface in self.surfaces:
            if surface.surface_id == surface_id:
                return surface
        raise KeyError(surface_id)
