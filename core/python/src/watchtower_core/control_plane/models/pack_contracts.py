"""Typed models for pack-facing contract surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _tuple_of_strings(document: dict[str, Any], key: str) -> tuple[str, ...]:
    """Return one optional tuple-of-string field from a raw document."""

    return tuple(document.get(key, ()))


@dataclass(frozen=True, slots=True)
class PackWorkspaceRoots:
    """Declared repository-relative workspace roots for one active pack."""

    workspace_root: str
    machine_root: str
    docs_root: str
    workflows_root: str
    tracking_root: str
    initiatives_root: str
    projects_root: str
    overview_path: str

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PackWorkspaceRoots:
        return cls(
            workspace_root=document["workspace_root"],
            machine_root=document["machine_root"],
            docs_root=document["docs_root"],
            workflows_root=document["workflows_root"],
            tracking_root=document["tracking_root"],
            initiatives_root=document["initiatives_root"],
            projects_root=document["projects_root"],
            overview_path=document["overview_path"],
        )


@dataclass(frozen=True, slots=True)
class PackSurfaceDeclaration:
    """Shared declaration shape used by pack settings and governance surface maps."""

    surface_name: str
    surface_kind: str
    path: str
    authority: str
    visibility: str
    rebuildable: bool | None = None
    depends_on: tuple[str, ...] = ()
    builder: str | None = None
    source_surface: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PackSurfaceDeclaration:
        return cls(
            surface_name=document["surface_name"],
            surface_kind=document["surface_kind"],
            path=document["path"],
            authority=document["authority"],
            visibility=document["visibility"],
            rebuildable=document.get("rebuildable"),
            depends_on=_tuple_of_strings(document, "depends_on"),
            builder=document.get("builder"),
            source_surface=document.get("source_surface"),
        )


@dataclass(frozen=True, slots=True)
class PackSettings:
    """Typed pack-settings load root."""

    schema_id: str
    surface_name: str
    contract_version: str
    description: str
    updated_at: str
    pack_id: str
    workspace_roots: PackWorkspaceRoots
    default_validation_suite_id: str
    surfaces: tuple[PackSurfaceDeclaration, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PackSettings:
        return cls(
            schema_id=document["$schema"],
            surface_name=document["surface_name"],
            contract_version=document["contract_version"],
            description=document["description"],
            updated_at=document["updated_at"],
            pack_id=document["pack_id"],
            workspace_roots=PackWorkspaceRoots.from_document(document["workspace_roots"]),
            default_validation_suite_id=document["default_validation_suite_id"],
            surfaces=tuple(
                PackSurfaceDeclaration.from_document(entry)
                for entry in document["surfaces"]
            ),
            notes=document.get("notes"),
        )

    def get(self, surface_name: str) -> PackSurfaceDeclaration:
        """Return one declared surface by name."""

        for declaration in self.surfaces:
            if declaration.surface_name == surface_name:
                return declaration
        raise KeyError(surface_name)


@dataclass(frozen=True, slots=True)
class GovernanceSurfaceMap:
    """Typed governance-surface map."""

    schema_id: str
    surface_name: str
    contract_version: str
    description: str
    updated_at: str
    surfaces: tuple[PackSurfaceDeclaration, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> GovernanceSurfaceMap:
        return cls(
            schema_id=document["$schema"],
            surface_name=document["surface_name"],
            contract_version=document["contract_version"],
            description=document["description"],
            updated_at=document["updated_at"],
            surfaces=tuple(
                PackSurfaceDeclaration.from_document(entry)
                for entry in document["surfaces"]
            ),
            notes=document.get("notes"),
        )

    def get(self, surface_name: str) -> PackSurfaceDeclaration:
        """Return one declared governance surface by name."""

        for declaration in self.surfaces:
            if declaration.surface_name == surface_name:
                return declaration
        raise KeyError(surface_name)


@dataclass(frozen=True, slots=True)
class PathPatternEntry:
    """Typed path-pattern registry entry."""

    family_name: str
    path_kind: str
    path_pattern: str
    entity_shape: str
    visibility: str
    authoritative: bool
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PathPatternEntry:
        return cls(
            family_name=document["family_name"],
            path_kind=document["path_kind"],
            path_pattern=document["path_pattern"],
            entity_shape=document["entity_shape"],
            visibility=document["visibility"],
            authoritative=document["authoritative"],
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class PathPatternRegistry:
    """Typed path-pattern registry."""

    schema_id: str
    surface_name: str
    contract_version: str
    description: str
    updated_at: str
    patterns: tuple[PathPatternEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> PathPatternRegistry:
        return cls(
            schema_id=document["$schema"],
            surface_name=document["surface_name"],
            contract_version=document["contract_version"],
            description=document["description"],
            updated_at=document["updated_at"],
            patterns=tuple(
                PathPatternEntry.from_document(entry) for entry in document["patterns"]
            ),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class StatusRegistryEntry:
    """Typed status-registry entry."""

    value: str
    entry_status: str
    summary: str
    allowed_families: tuple[str, ...] = ()
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> StatusRegistryEntry:
        return cls(
            value=document["value"],
            entry_status=document["entry_status"],
            summary=document["summary"],
            allowed_families=_tuple_of_strings(document, "allowed_families"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class StatusRegistry:
    """Typed status registry."""

    schema_id: str
    surface_name: str
    contract_version: str
    description: str
    updated_at: str
    statuses: tuple[StatusRegistryEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> StatusRegistry:
        return cls(
            schema_id=document["$schema"],
            surface_name=document["surface_name"],
            contract_version=document["contract_version"],
            description=document["description"],
            updated_at=document["updated_at"],
            statuses=tuple(
                StatusRegistryEntry.from_document(entry)
                for entry in document["statuses"]
            ),
            notes=document.get("notes"),
        )

    def get(self, value: str) -> StatusRegistryEntry:
        """Return one status entry by value."""

        for entry in self.statuses:
            if entry.value == value:
                return entry
        raise KeyError(value)


@dataclass(frozen=True, slots=True)
class ActorEntry:
    """Typed actor-registry entry."""

    actor_id: str
    actor_type: str
    label: str
    role: str | None = None
    scope: str | None = None
    external_account_ref: str | None = None
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ActorEntry:
        return cls(
            actor_id=document["actor_id"],
            actor_type=document["actor_type"],
            label=document["label"],
            role=document.get("role"),
            scope=document.get("scope"),
            external_account_ref=document.get("external_account_ref"),
            notes=document.get("notes"),
        )


@dataclass(frozen=True, slots=True)
class ActorRegistry:
    """Typed actor registry."""

    schema_id: str
    surface_name: str
    contract_version: str
    description: str
    updated_at: str
    actors: tuple[ActorEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ActorRegistry:
        return cls(
            schema_id=document["$schema"],
            surface_name=document["surface_name"],
            contract_version=document["contract_version"],
            description=document["description"],
            updated_at=document["updated_at"],
            actors=tuple(ActorEntry.from_document(entry) for entry in document["actors"]),
            notes=document.get("notes"),
        )

    def get(self, actor_id: str) -> ActorEntry:
        """Return one actor entry by identifier."""

        for entry in self.actors:
            if entry.actor_id == actor_id:
                return entry
        raise KeyError(actor_id)


@dataclass(frozen=True, slots=True)
class ExtractionObservation:
    """One observation recorded in a structured extraction-output envelope."""

    observation_id: str
    summary: str
    tags: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ExtractionObservation:
        return cls(
            observation_id=document["observation_id"],
            summary=document["summary"],
            tags=_tuple_of_strings(document, "tags"),
        )


@dataclass(frozen=True, slots=True)
class ExtractionCandidateKnowledge:
    """One candidate durable-knowledge entry extracted from source material."""

    candidate_id: str
    title: str
    summary: str
    knowledge_family: str
    evidence_artifact_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ExtractionCandidateKnowledge:
        return cls(
            candidate_id=document["candidate_id"],
            title=document["title"],
            summary=document["summary"],
            knowledge_family=document["knowledge_family"],
            evidence_artifact_ids=_tuple_of_strings(document, "evidence_artifact_ids"),
            tags=_tuple_of_strings(document, "tags"),
        )


@dataclass(frozen=True, slots=True)
class ExtractionOutputEnvelopeArtifact:
    """Typed extraction-output envelope artifact."""

    schema_id: str
    artifact_id: str
    title: str
    summary: str
    status: str
    pack_id: str
    work_item_id: str
    trace_id: str
    source_note_id: str
    workflow_run_id: str
    extraction_method: str
    created_at: str
    observations: tuple[ExtractionObservation, ...]
    candidate_knowledge: tuple[ExtractionCandidateKnowledge, ...]
    artifact_manifest_id: str | None = None
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ExtractionOutputEnvelopeArtifact:
        return cls(
            schema_id=document["$schema"],
            artifact_id=document["id"],
            title=document["title"],
            summary=document["summary"],
            status=document["status"],
            pack_id=document["pack_id"],
            work_item_id=document["work_item_id"],
            trace_id=document["trace_id"],
            source_note_id=document["source_note_id"],
            workflow_run_id=document["workflow_run_id"],
            extraction_method=document["extraction_method"],
            created_at=document["created_at"],
            observations=tuple(
                ExtractionObservation.from_document(entry)
                for entry in document["observations"]
            ),
            candidate_knowledge=tuple(
                ExtractionCandidateKnowledge.from_document(entry)
                for entry in document["candidate_knowledge"]
            ),
            artifact_manifest_id=document.get("artifact_manifest_id"),
            notes=document.get("notes"),
        )

    @property
    def observation_count(self) -> int:
        """Return the number of captured observations."""

        return len(self.observations)

    @property
    def knowledge_count(self) -> int:
        """Return the number of candidate durable-knowledge entries."""

        return len(self.candidate_knowledge)

    @property
    def knowledge_families(self) -> tuple[str, ...]:
        """Return the unique candidate knowledge families covered by the envelope."""

        return tuple(
            sorted(
                {
                    entry.knowledge_family
                    for entry in self.candidate_knowledge
                }
            )
        )

    @property
    def evidence_artifact_ids(self) -> tuple[str, ...]:
        """Return the unique evidence artifact references cited by the envelope."""

        return tuple(
            sorted(
                {
                    artifact_id
                    for entry in self.candidate_knowledge
                    for artifact_id in entry.evidence_artifact_ids
                }
            )
        )


@dataclass(frozen=True, slots=True)
class ArtifactIndexEntry:
    """Typed artifact-index entry."""

    artifact_id: str
    artifact_family: str
    path: str
    pack: str
    status: str
    authoritative: bool
    hidden: bool
    derived: bool
    created_at: str
    updated_at: str
    subdomain: str | None = None
    context_ids: tuple[str, ...] = ()
    title: str | None = None
    summary: str | None = None
    parent_artifact_id: str | None = None
    related_artifact_ids: tuple[str, ...] = ()
    route_id: str | None = None
    rendered_view_path: str | None = None
    workflow_surface: str | None = None
    review_status: str | None = None
    source_context: str | None = None
    source_channel: str | None = None
    source_summary: str | None = None
    source_url: str | None = None
    source_ref: str | None = None
    source_type: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ArtifactIndexEntry:
        return cls(
            artifact_id=document["artifact_id"],
            artifact_family=document["artifact_family"],
            path=document["path"],
            pack=document["pack"],
            status=document["status"],
            authoritative=document["authoritative"],
            hidden=document["hidden"],
            derived=document["derived"],
            created_at=document["created_at"],
            updated_at=document["updated_at"],
            subdomain=document.get("subdomain"),
            context_ids=_tuple_of_strings(document, "context_ids"),
            title=document.get("title"),
            summary=document.get("summary"),
            parent_artifact_id=document.get("parent_artifact_id"),
            related_artifact_ids=_tuple_of_strings(document, "related_artifact_ids"),
            route_id=document.get("route_id"),
            rendered_view_path=document.get("rendered_view_path"),
            workflow_surface=document.get("workflow_surface"),
            review_status=document.get("review_status"),
            source_context=document.get("source_context"),
            source_channel=document.get("source_channel"),
            source_summary=document.get("source_summary"),
            source_url=document.get("source_url"),
            source_ref=document.get("source_ref"),
            source_type=document.get("source_type"),
        )


@dataclass(frozen=True, slots=True)
class ArtifactIndex:
    """Typed artifact index."""

    schema_id: str
    surface_name: str
    contract_version: str
    description: str
    updated_at: str
    artifacts: tuple[ArtifactIndexEntry, ...]
    notes: str | None = None

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> ArtifactIndex:
        return cls(
            schema_id=document["$schema"],
            surface_name=document["surface_name"],
            contract_version=document["contract_version"],
            description=document["description"],
            updated_at=document["updated_at"],
            artifacts=tuple(
                ArtifactIndexEntry.from_document(entry)
                for entry in document["artifacts"]
            ),
            notes=document.get("notes"),
        )

    def get(self, artifact_id: str) -> ArtifactIndexEntry:
        """Return one artifact entry by identifier."""

        for entry in self.artifacts:
            if entry.artifact_id == artifact_id:
                return entry
        raise KeyError(artifact_id)
