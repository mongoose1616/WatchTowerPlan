"""Reusable control-plane helpers and typed pack-runtime models."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from watchtower_core.control_plane.actors import ActorRegistryHelper, ActorRegistryIssue
    from watchtower_core.control_plane.artifact_family import (
        ArtifactFamilyHelper,
        ArtifactFamilyIssue,
    )
    from watchtower_core.control_plane.discrepancy import (
        DISCREPANCY_RECORD_SCHEMA_ID,
        DiscrepancyDescriptor,
        DiscrepancyHelper,
        DiscrepancyIssue,
    )
    from watchtower_core.control_plane.documentation_family import (
        DocumentationFamilyHelper,
        DocumentationFamilyIssue,
    )
    from watchtower_core.control_plane.event_stream import (
        EventStreamDescriptor,
        EventStreamHelper,
        EventStreamWriteRequest,
    )
    from watchtower_core.control_plane.extraction_output import (
        EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID,
        ExtractionCandidateKnowledgeSpec,
        ExtractionObservationSpec,
        ExtractionOutputEnvelopeHelper,
        ExtractionOutputEnvelopeWriteResult,
    )
    from watchtower_core.control_plane.governance_surfaces import (
        GovernanceSurfaceResolution,
        GovernanceSurfaceResolver,
    )
    from watchtower_core.control_plane.human_surface_policy import (
        HumanSurfacePolicyHelper,
        HumanSurfacePolicyIssue,
    )
    from watchtower_core.control_plane.loader import ControlPlaneLoader
    from watchtower_core.control_plane.pack_context import PackContext
    from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
    from watchtower_core.control_plane.path_ids import PlanInitiativeLocation, PlanPathIdHelper
    from watchtower_core.control_plane.project_surface_policy import (
        ProjectSurfacePolicyHelper,
        ProjectSurfacePolicyIssue,
    )
    from watchtower_core.control_plane.promotion_policy import (
        PromotionPolicyHelper,
        PromotionPolicyIssue,
    )
    from watchtower_core.control_plane.retention_policy import (
        RetentionPolicyHelper,
        RetentionPolicyIssue,
    )
    from watchtower_core.control_plane.schemas import SchemaStore, SupplementalSchemaDocument
    from watchtower_core.control_plane.template_catalog import (
        TemplateCatalogHelper,
        TemplateCatalogIssue,
    )
    from watchtower_core.control_plane.terminology import (
        PlanningVocabularyHelper,
        TerminologyHelper,
        TerminologyResolution,
        TerminologyTerm,
    )
    from watchtower_core.control_plane.workflow_catalog import (
        WorkflowCatalogHelper,
        WorkflowCatalogSnapshot,
    )
    from watchtower_core.control_plane.workspace import (
        ArtifactSource,
        ArtifactStore,
        FileSystemArtifactIO,
        WorkspaceConfig,
    )

_EXPORTS: dict[str, tuple[str, str]] = {
    "ActorRegistryHelper": ("watchtower_core.control_plane.actors", "ActorRegistryHelper"),
    "ActorRegistryIssue": ("watchtower_core.control_plane.actors", "ActorRegistryIssue"),
    "ArtifactFamilyHelper": (
        "watchtower_core.control_plane.artifact_family",
        "ArtifactFamilyHelper",
    ),
    "ArtifactFamilyIssue": (
        "watchtower_core.control_plane.artifact_family",
        "ArtifactFamilyIssue",
    ),
    "ArtifactSource": ("watchtower_core.control_plane.workspace", "ArtifactSource"),
    "ArtifactStore": ("watchtower_core.control_plane.workspace", "ArtifactStore"),
    "ControlPlaneLoader": ("watchtower_core.control_plane.loader", "ControlPlaneLoader"),
    "DISCREPANCY_RECORD_SCHEMA_ID": (
        "watchtower_core.control_plane.discrepancy",
        "DISCREPANCY_RECORD_SCHEMA_ID",
    ),
    "DocumentationFamilyHelper": (
        "watchtower_core.control_plane.documentation_family",
        "DocumentationFamilyHelper",
    ),
    "DocumentationFamilyIssue": (
        "watchtower_core.control_plane.documentation_family",
        "DocumentationFamilyIssue",
    ),
    "EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID": (
        "watchtower_core.control_plane.extraction_output",
        "EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID",
    ),
    "DiscrepancyDescriptor": (
        "watchtower_core.control_plane.discrepancy",
        "DiscrepancyDescriptor",
    ),
    "DiscrepancyHelper": ("watchtower_core.control_plane.discrepancy", "DiscrepancyHelper"),
    "DiscrepancyIssue": ("watchtower_core.control_plane.discrepancy", "DiscrepancyIssue"),
    "EventStreamDescriptor": (
        "watchtower_core.control_plane.event_stream",
        "EventStreamDescriptor",
    ),
    "EventStreamHelper": ("watchtower_core.control_plane.event_stream", "EventStreamHelper"),
    "EventStreamWriteRequest": (
        "watchtower_core.control_plane.event_stream",
        "EventStreamWriteRequest",
    ),
    "ExtractionCandidateKnowledgeSpec": (
        "watchtower_core.control_plane.extraction_output",
        "ExtractionCandidateKnowledgeSpec",
    ),
    "ExtractionObservationSpec": (
        "watchtower_core.control_plane.extraction_output",
        "ExtractionObservationSpec",
    ),
    "ExtractionOutputEnvelopeHelper": (
        "watchtower_core.control_plane.extraction_output",
        "ExtractionOutputEnvelopeHelper",
    ),
    "ExtractionOutputEnvelopeWriteResult": (
        "watchtower_core.control_plane.extraction_output",
        "ExtractionOutputEnvelopeWriteResult",
    ),
    "FileSystemArtifactIO": (
        "watchtower_core.control_plane.workspace",
        "FileSystemArtifactIO",
    ),
    "GovernanceSurfaceResolution": (
        "watchtower_core.control_plane.governance_surfaces",
        "GovernanceSurfaceResolution",
    ),
    "GovernanceSurfaceResolver": (
        "watchtower_core.control_plane.governance_surfaces",
        "GovernanceSurfaceResolver",
    ),
    "HumanSurfacePolicyHelper": (
        "watchtower_core.control_plane.human_surface_policy",
        "HumanSurfacePolicyHelper",
    ),
    "HumanSurfacePolicyIssue": (
        "watchtower_core.control_plane.human_surface_policy",
        "HumanSurfacePolicyIssue",
    ),
    "PackContext": ("watchtower_core.control_plane.pack_context", "PackContext"),
    "PackWorkspacePaths": (
        "watchtower_core.control_plane.pack_workspace",
        "PackWorkspacePaths",
    ),
    "PlanInitiativeLocation": (
        "watchtower_core.control_plane.path_ids",
        "PlanInitiativeLocation",
    ),
    "PlanPathIdHelper": ("watchtower_core.control_plane.path_ids", "PlanPathIdHelper"),
    "PlanningVocabularyHelper": (
        "watchtower_core.control_plane.terminology",
        "PlanningVocabularyHelper",
    ),
    "PromotionPolicyHelper": (
        "watchtower_core.control_plane.promotion_policy",
        "PromotionPolicyHelper",
    ),
    "PromotionPolicyIssue": (
        "watchtower_core.control_plane.promotion_policy",
        "PromotionPolicyIssue",
    ),
    "ProjectSurfacePolicyHelper": (
        "watchtower_core.control_plane.project_surface_policy",
        "ProjectSurfacePolicyHelper",
    ),
    "ProjectSurfacePolicyIssue": (
        "watchtower_core.control_plane.project_surface_policy",
        "ProjectSurfacePolicyIssue",
    ),
    "RetentionPolicyHelper": (
        "watchtower_core.control_plane.retention_policy",
        "RetentionPolicyHelper",
    ),
    "RetentionPolicyIssue": (
        "watchtower_core.control_plane.retention_policy",
        "RetentionPolicyIssue",
    ),
    "SchemaStore": ("watchtower_core.control_plane.schemas", "SchemaStore"),
    "SupplementalSchemaDocument": (
        "watchtower_core.control_plane.schemas",
        "SupplementalSchemaDocument",
    ),
    "TemplateCatalogHelper": (
        "watchtower_core.control_plane.template_catalog",
        "TemplateCatalogHelper",
    ),
    "TemplateCatalogIssue": (
        "watchtower_core.control_plane.template_catalog",
        "TemplateCatalogIssue",
    ),
    "TerminologyHelper": ("watchtower_core.control_plane.terminology", "TerminologyHelper"),
    "TerminologyResolution": (
        "watchtower_core.control_plane.terminology",
        "TerminologyResolution",
    ),
    "TerminologyTerm": ("watchtower_core.control_plane.terminology", "TerminologyTerm"),
    "WorkflowCatalogHelper": (
        "watchtower_core.control_plane.workflow_catalog",
        "WorkflowCatalogHelper",
    ),
    "WorkflowCatalogSnapshot": (
        "watchtower_core.control_plane.workflow_catalog",
        "WorkflowCatalogSnapshot",
    ),
    "WorkspaceConfig": ("watchtower_core.control_plane.workspace", "WorkspaceConfig"),
}

__all__ = [
    "ActorRegistryHelper",
    "ActorRegistryIssue",
    "ArtifactSource",
    "ArtifactStore",
    "ArtifactFamilyHelper",
    "ArtifactFamilyIssue",
    "ControlPlaneLoader",
    "DISCREPANCY_RECORD_SCHEMA_ID",
    "DocumentationFamilyHelper",
    "DocumentationFamilyIssue",
    "EXTRACTION_OUTPUT_ENVELOPE_SCHEMA_ID",
    "DiscrepancyDescriptor",
    "DiscrepancyHelper",
    "DiscrepancyIssue",
    "EventStreamDescriptor",
    "EventStreamHelper",
    "EventStreamWriteRequest",
    "ExtractionCandidateKnowledgeSpec",
    "ExtractionObservationSpec",
    "ExtractionOutputEnvelopeHelper",
    "ExtractionOutputEnvelopeWriteResult",
    "FileSystemArtifactIO",
    "GovernanceSurfaceResolution",
    "GovernanceSurfaceResolver",
    "HumanSurfacePolicyHelper",
    "HumanSurfacePolicyIssue",
    "PackContext",
    "PackWorkspacePaths",
    "PlanInitiativeLocation",
    "PlanPathIdHelper",
    "PlanningVocabularyHelper",
    "PromotionPolicyHelper",
    "PromotionPolicyIssue",
    "ProjectSurfacePolicyHelper",
    "ProjectSurfacePolicyIssue",
    "RetentionPolicyHelper",
    "RetentionPolicyIssue",
    "SchemaStore",
    "SupplementalSchemaDocument",
    "TemplateCatalogHelper",
    "TemplateCatalogIssue",
    "TerminologyHelper",
    "TerminologyResolution",
    "TerminologyTerm",
    "WorkflowCatalogHelper",
    "WorkflowCatalogSnapshot",
    "WorkspaceConfig",
]


def __getattr__(name: str) -> object:
    try:
        module_name, attribute_name = _EXPORTS[name]
    except KeyError as exc:  # pragma: no cover - Python import protocol
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
    value = getattr(import_module(module_name), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
