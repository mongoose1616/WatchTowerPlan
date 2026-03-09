"""Errors raised by validation services."""

from __future__ import annotations


class ValidationExecutionError(RuntimeError):
    """Raised when validation could not be executed deterministically."""


class ValidationSelectionError(ValidationExecutionError):
    """Raised when a validator could not be resolved or selected."""
