"""Compatibility re-exports for planning and documentation index artifacts."""

from watchtower_core.control_plane.models.knowledge_indexes import (
    FoundationIndex,
    FoundationIndexEntry,
    ReferenceIndex,
    ReferenceIndexEntry,
    StandardIndex,
    StandardIndexEntry,
    WorkflowIndex,
    WorkflowIndexEntry,
)
from watchtower_core.control_plane.models.planning_documents import (
    DecisionIndex,
    DecisionIndexEntry,
    DesignDocumentIndex,
    DesignDocumentIndexEntry,
    PrdIndex,
    PrdIndexEntry,
)

__all__ = [
    "DecisionIndex",
    "DecisionIndexEntry",
    "DesignDocumentIndex",
    "DesignDocumentIndexEntry",
    "FoundationIndex",
    "FoundationIndexEntry",
    "PrdIndex",
    "PrdIndexEntry",
    "ReferenceIndex",
    "ReferenceIndexEntry",
    "StandardIndex",
    "StandardIndexEntry",
    "WorkflowIndex",
    "WorkflowIndexEntry",
]
