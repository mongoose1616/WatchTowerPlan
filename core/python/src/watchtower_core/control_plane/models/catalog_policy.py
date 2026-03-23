"""Policy, authority, lifecycle, and artifact registry models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
        entries = tuple(AuthorityMapEntry.from_document(entry) for entry in document["entries"])
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
                HumanSurfacePolicyEntry.from_document(item) for item in document["entries"]
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
class ProjectSurfacePolicySurfaceDefinition:
    """One declared project-root surface definition."""

    relative_path: str
    entity_shape: str
    surface_kind: str
    mode: str
    authorship_mode: str
    source_family: str | None = None
    required_metadata_fields: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ProjectSurfacePolicySurfaceDefinition:
        return cls(
            relative_path=document["relative_path"],
            entity_shape=document["entity_shape"],
            surface_kind=document["surface_kind"],
            mode=document["mode"],
            authorship_mode=document["authorship_mode"],
            source_family=document.get("source_family"),
            required_metadata_fields=tuple(document.get("required_metadata_fields", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ProjectSurfacePolicyEntry:
    """One project-root policy rule for allowed and required project surfaces."""

    policy_id: str
    path_pattern: str
    match_mode: str
    root_kind: str
    entry_status: str
    governing_surfaces: tuple[str, ...]
    clarifying_rule: str
    surfaces: tuple[ProjectSurfacePolicySurfaceDefinition, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ProjectSurfacePolicyEntry:
        return cls(
            policy_id=document["policy_id"],
            path_pattern=document["path_pattern"],
            match_mode=document["match_mode"],
            root_kind=document["root_kind"],
            entry_status=document["entry_status"],
            governing_surfaces=tuple(document.get("governing_surfaces", ())),
            clarifying_rule=document["clarifying_rule"],
            surfaces=tuple(
                ProjectSurfacePolicySurfaceDefinition.from_document(item)
                for item in document["surfaces"]
            ),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ProjectSurfacePolicyRegistry:
    """Typed project-surface policy registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[ProjectSurfacePolicyEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ProjectSurfacePolicyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(
                ProjectSurfacePolicyEntry.from_document(item) for item in document["entries"]
            ),
            notes=document.get("notes"),
        )

    def get(self, policy_id: str) -> ProjectSurfacePolicyEntry:
        """Return one project-surface policy entry by identifier."""

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
            entries=tuple(RetentionPolicyEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, policy_id: str) -> RetentionPolicyEntry:
        """Return one policy entry by identifier."""

        for entry in self.entries:
            if entry.policy_id == policy_id:
                return entry
        raise KeyError(policy_id)


@dataclass(frozen=True, slots=True)
class PromotionPolicyEntry:
    """One promotion-policy rule for initiative-local durable guidance extraction."""

    policy_id: str
    entry_status: str
    source_artifact_kinds: tuple[str, ...]
    target_family: str
    target_root: str
    required_review_path: str
    provenance_requirements: tuple[str, ...]
    mirror_update_mode: str
    mirror_roots: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PromotionPolicyEntry:
        return cls(
            policy_id=document["policy_id"],
            entry_status=document["entry_status"],
            source_artifact_kinds=tuple(document["source_artifact_kinds"]),
            target_family=document["target_family"],
            target_root=document["target_root"],
            required_review_path=document["required_review_path"],
            provenance_requirements=tuple(document["provenance_requirements"]),
            mirror_update_mode=document["mirror_update_mode"],
            mirror_roots=tuple(document.get("mirror_roots", ())),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class PromotionPolicyRegistry:
    """Typed promotion-policy registry artifact."""

    schema_id: str
    artifact_id: str
    title: str
    status: str
    entries: tuple[PromotionPolicyEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PromotionPolicyRegistry:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            status=document["status"],
            entries=tuple(PromotionPolicyEntry.from_document(item) for item in document["entries"]),
            notes=document.get("notes"),
        )

    def get(self, policy_id: str) -> PromotionPolicyEntry:
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
    """One governed lifecycle-stage entry for pack-runtime work."""

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
    """One governed review-status entry for pack-runtime approval state."""

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
    """One governed source-type entry for pack-runtime provenance."""

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
