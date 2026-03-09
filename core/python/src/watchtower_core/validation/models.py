"""Typed result models for validation services."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One validation issue returned by a runner."""

    code: str
    message: str
    location: str | None = None
    schema_id: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Structured validation result for one target and validator."""

    validator_id: str
    target_path: str
    engine: str
    schema_ids: tuple[str, ...]
    passed: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def issue_count(self) -> int:
        """Return the number of issues attached to this result."""
        return len(self.issues)
