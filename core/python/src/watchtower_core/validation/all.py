"""Aggregate validation helpers for the current governed repository surfaces."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.sync.decision_index import DECISION_DOC_ROOT, DECISION_EXCLUDED_NAMES
from watchtower_core.sync.design_document_index import (
    DESIGN_EXCLUDED_NAMES,
    FEATURE_DESIGN_ROOT,
    IMPLEMENTATION_PLAN_ROOT,
)
from watchtower_core.sync.foundation_index import FOUNDATION_DOC_ROOT, FOUNDATION_EXCLUDED_NAMES
from watchtower_core.sync.planning_documents import iter_markdown_documents
from watchtower_core.sync.prd_index import PRD_DOC_ROOT, PRD_EXCLUDED_NAMES
from watchtower_core.sync.reference_index import REFERENCE_DOC_ROOT, REFERENCE_EXCLUDED_NAMES
from watchtower_core.sync.standard_index import STANDARD_DOC_ROOT, STANDARD_EXCLUDED_NAMES
from watchtower_core.sync.task_documents import (
    TASK_CLOSED_ROOT,
    TASK_EXCLUDED_NAMES,
    TASK_OPEN_ROOT,
)
from watchtower_core.validation.acceptance import AcceptanceReconciliationService
from watchtower_core.validation.artifact import ArtifactValidationService
from watchtower_core.validation.errors import ValidationExecutionError, ValidationSelectionError
from watchtower_core.validation.front_matter import FrontMatterValidationService
from watchtower_core.validation.models import ValidationIssue, ValidationResult


@dataclass(frozen=True, slots=True)
class ValidationAllRecord:
    """One validation target executed by the aggregate validator."""

    family: str
    target: str
    result: ValidationResult

    @property
    def issue_count(self) -> int:
        """Return the number of issues attached to the underlying result."""
        return self.result.issue_count


@dataclass(frozen=True, slots=True)
class ValidationFamilySummary:
    """Summary counts for one validation family."""

    family: str
    total_count: int
    passed_count: int
    failed_count: int


@dataclass(frozen=True, slots=True)
class ValidationAllResult:
    """Aggregated output for one validate-all run."""

    records: tuple[ValidationAllRecord, ...]
    included_families: tuple[str, ...]

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
    def family_summaries(self) -> tuple[ValidationFamilySummary, ...]:
        """Return per-family counts in execution order."""
        summaries: list[ValidationFamilySummary] = []
        for family in self.included_families:
            family_records = tuple(record for record in self.records if record.family == family)
            passed_count = sum(1 for record in family_records if record.result.passed)
            summaries.append(
                ValidationFamilySummary(
                    family=family,
                    total_count=len(family_records),
                    passed_count=passed_count,
                    failed_count=len(family_records) - passed_count,
                )
            )
        return tuple(summaries)


class ValidationAllService:
    """Run all explicit validation families in deterministic order."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._front_matter = FrontMatterValidationService(loader)
        self._artifact = ArtifactValidationService(loader)
        self._acceptance = AcceptanceReconciliationService(loader)

    def run(
        self,
        *,
        include_front_matter: bool = True,
        include_artifacts: bool = True,
        include_acceptance: bool = True,
    ) -> ValidationAllResult:
        """Run the selected validation families and return their aggregate results."""
        included_families: list[str] = []
        records: list[ValidationAllRecord] = []

        if include_front_matter:
            included_families.append("front_matter")
            records.extend(self._validate_front_matter())
        if include_artifacts:
            included_families.append("artifacts")
            records.extend(self._validate_artifacts())
        if include_acceptance:
            included_families.append("acceptance")
            records.extend(self._validate_acceptance())

        if not included_families:
            raise ValueError("validate all requires at least one validation family.")

        return ValidationAllResult(
            records=tuple(records),
            included_families=tuple(included_families),
        )

    def _validate_front_matter(self) -> tuple[ValidationAllRecord, ...]:
        records: list[ValidationAllRecord] = []
        for relative_path in self._front_matter_targets():
            result = self._safe_validate_path(
                family="front_matter",
                target=relative_path,
                runner=self._front_matter.validate,
            )
            records.append(
                ValidationAllRecord(
                    family="front_matter",
                    target=relative_path,
                    result=result,
                )
            )
        return tuple(records)

    def _validate_artifacts(self) -> tuple[ValidationAllRecord, ...]:
        records: list[ValidationAllRecord] = []
        for relative_path in self._artifact_targets():
            result = self._safe_validate_path(
                family="artifacts",
                target=relative_path,
                runner=self._artifact.validate,
            )
            records.append(
                ValidationAllRecord(
                    family="artifacts",
                    target=relative_path,
                    result=result,
                )
            )
        return tuple(records)

    def _validate_acceptance(self) -> tuple[ValidationAllRecord, ...]:
        records: list[ValidationAllRecord] = []
        for trace_id in self._acceptance_targets():
            result = self._acceptance.validate(trace_id)
            records.append(
                ValidationAllRecord(
                    family="acceptance",
                    target=trace_id,
                    result=result,
                )
            )
        return tuple(records)

    def _front_matter_targets(self) -> tuple[str, ...]:
        repo_root = self._loader.repo_root
        standards_root = repo_root / STANDARD_DOC_ROOT
        standards = tuple(
            path.relative_to(repo_root).as_posix()
            for path in sorted(standards_root.rglob("*.md"))
            if path.name not in STANDARD_EXCLUDED_NAMES
        )
        return (
            *iter_markdown_documents(
                repo_root,
                REFERENCE_DOC_ROOT,
                excluded_names=REFERENCE_EXCLUDED_NAMES,
            ),
            *iter_markdown_documents(
                repo_root,
                FOUNDATION_DOC_ROOT,
                excluded_names=FOUNDATION_EXCLUDED_NAMES,
            ),
            *standards,
            *iter_markdown_documents(
                repo_root,
                PRD_DOC_ROOT,
                excluded_names=PRD_EXCLUDED_NAMES,
            ),
            *iter_markdown_documents(
                repo_root,
                DECISION_DOC_ROOT,
                excluded_names=DECISION_EXCLUDED_NAMES,
            ),
            *iter_markdown_documents(
                repo_root,
                FEATURE_DESIGN_ROOT,
                excluded_names=DESIGN_EXCLUDED_NAMES,
            ),
            *iter_markdown_documents(
                repo_root,
                IMPLEMENTATION_PLAN_ROOT,
                excluded_names=DESIGN_EXCLUDED_NAMES,
            ),
            *iter_markdown_documents(
                repo_root,
                TASK_OPEN_ROOT,
                excluded_names=TASK_EXCLUDED_NAMES,
            ),
            *iter_markdown_documents(
                repo_root,
                TASK_CLOSED_ROOT,
                excluded_names=TASK_EXCLUDED_NAMES,
            ),
        )

    def _artifact_targets(self) -> tuple[str, ...]:
        registry = self._loader.load_validator_registry()
        repo_root = self._loader.repo_root
        ordered_paths: list[str] = []
        seen: set[str] = set()
        for validator in registry.validators:
            if validator.status != "active":
                continue
            if validator.engine != "json_schema":
                continue
            if validator.artifact_kind == "documentation_front_matter":
                continue
            for pattern in validator.applies_to:
                for relative_path in self._artifact_paths_for_pattern(repo_root, pattern):
                    if relative_path in seen:
                        continue
                    seen.add(relative_path)
                    ordered_paths.append(relative_path)
        return tuple(ordered_paths)

    def _artifact_paths_for_pattern(
        self,
        repo_root: Path,
        pattern: str,
    ) -> tuple[str, ...]:
        if pattern.endswith("/**"):
            relative_root = pattern.removesuffix("/**")
            return tuple(
                path.relative_to(repo_root).as_posix()
                for path in sorted((repo_root / relative_root).glob("*.json"))
            )
        if pattern.endswith(".json"):
            path = repo_root / pattern
            if path.exists():
                return (pattern,)
            return ()
        return ()

    def _acceptance_targets(self) -> tuple[str, ...]:
        return tuple(entry.trace_id for entry in self._loader.load_traceability_index().entries)

    def _safe_validate_path(
        self,
        *,
        family: str,
        target: str,
        runner: Callable[[str], ValidationResult],
    ) -> ValidationResult:
        try:
            return runner(target)
        except (ValidationExecutionError, ValidationSelectionError) as exc:
            return ValidationResult(
                validator_id=f"validator.{family}.aggregate_selection",
                target_path=target,
                engine="internal",
                schema_ids=(),
                passed=False,
                issues=(
                    ValidationIssue(
                        code="validation_target_resolution_error",
                        message=str(exc),
                        location=target,
                    ),
                ),
            )
