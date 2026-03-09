"""Control-plane loader and schema-resolution errors."""

from __future__ import annotations


class ControlPlaneError(Exception):
    """Base class for control-plane loading failures."""


class RepoRootNotFoundError(ControlPlaneError):
    """Raised when the repository root cannot be discovered."""


class ArtifactLoadError(ControlPlaneError):
    """Raised when a governed artifact cannot be loaded from disk."""


class SchemaResolutionError(ControlPlaneError):
    """Raised when a published schema cannot be resolved locally."""
