"""Recoverable error contract for pack discovery and runtime-view composition."""

from __future__ import annotations

from jsonschema import ValidationError

from watchtower_core.control_plane.errors import ControlPlaneError

RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS = (
    ControlPlaneError,
    ValidationError,
    ValueError,
)

__all__ = ["RECOVERABLE_PACK_DISCOVERY_EXCEPTIONS"]
