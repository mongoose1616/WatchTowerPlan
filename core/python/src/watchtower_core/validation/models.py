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


@dataclass(frozen=True, slots=True)
class ValidationSuiteRecord:
    """One validation target executed by a validation-suite step."""

    step_id: str
    step_kind: str
    target: str
    result: ValidationResult

    @property
    def issue_count(self) -> int:
        """Return the number of issues attached to the underlying result."""

        return self.result.issue_count


@dataclass(frozen=True, slots=True)
class ValidationSuiteStepSummary:
    """Summary counts for one validation-suite step."""

    step_id: str
    step_kind: str
    total_count: int
    passed_count: int
    failed_count: int


@dataclass(frozen=True, slots=True)
class ValidationSuiteResult:
    """Aggregated output for one validation suite run."""

    suite_id: str
    pack_settings_path: str
    records: tuple[ValidationSuiteRecord, ...]

    @property
    def passed(self) -> bool:
        """Return True when every executed validation passed."""

        return all(record.result.passed for record in self.records)

    @property
    def total_count(self) -> int:
        """Return the total number of validation targets executed."""

        return len(self.records)

    @property
    def passed_count(self) -> int:
        """Return the number of passing validation targets."""

        return sum(1 for record in self.records if record.result.passed)

    @property
    def failed_count(self) -> int:
        """Return the number of failing validation targets."""

        return self.total_count - self.passed_count

    @property
    def step_summaries(self) -> tuple[ValidationSuiteStepSummary, ...]:
        """Return per-step counts in execution order."""

        summaries: list[ValidationSuiteStepSummary] = []
        seen_steps: set[str] = set()
        for record in self.records:
            if record.step_id in seen_steps:
                continue
            seen_steps.add(record.step_id)
            step_records = tuple(
                candidate for candidate in self.records if candidate.step_id == record.step_id
            )
            passed_count = sum(1 for candidate in step_records if candidate.result.passed)
            summaries.append(
                ValidationSuiteStepSummary(
                    step_id=record.step_id,
                    step_kind=record.step_kind,
                    total_count=len(step_records),
                    passed_count=passed_count,
                    failed_count=len(step_records) - passed_count,
                )
            )
        return tuple(summaries)
