"""Aggregate validation helpers for the current governed repository surfaces."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import cast

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
from watchtower_core.sync.workflow_index import WORKFLOW_DOC_ROOT, WORKFLOW_EXCLUDED_NAMES
from watchtower_core.validation.acceptance import AcceptanceReconciliationService
from watchtower_core.validation.artifact import ArtifactValidationService
from watchtower_core.validation.document_semantics import DocumentSemanticsValidationService
from watchtower_core.validation.errors import ValidationExecutionError, ValidationSelectionError
from watchtower_core.validation.front_matter import FrontMatterValidationService
from watchtower_core.validation.models import ValidationIssue, ValidationResult
from watchtower_core.validation.registry import VALIDATION_FAMILY_SPECS


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
        self._document_semantics = DocumentSemanticsValidationService(loader)
        self._artifact = ArtifactValidationService(loader)
        self._acceptance = AcceptanceReconciliationService(loader)

    def run(
        self,
        *,
        included_families: tuple[str, ...] | None = None,
    ) -> ValidationAllResult:
        """Run the selected validation families and return their aggregate results."""
        requested_families = (
            {spec.family for spec in VALIDATION_FAMILY_SPECS}
            if included_families is None
            else set(included_families)
        )
        unknown_families = requested_families.difference(
            spec.family for spec in VALIDATION_FAMILY_SPECS
        )
        if unknown_families:
            unknown = ", ".join(sorted(unknown_families))
            raise ValueError(f"validate all received unknown validation families: {unknown}")

        resolved_families: list[str] = []
        records: list[ValidationAllRecord] = []

        for spec in VALIDATION_FAMILY_SPECS:
            if spec.family not in requested_families:
                continue
            runner = cast(
                Callable[[], tuple[ValidationAllRecord, ...]],
                getattr(self, spec.runner_name),
            )
            resolved_families.append(spec.family)
            records.extend(runner())

        if not resolved_families:
            raise ValueError("validate all requires at least one validation family.")

        return ValidationAllResult(
            records=tuple(records),
            included_families=tuple(resolved_families),
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

    def _validate_document_semantics(self) -> tuple[ValidationAllRecord, ...]:
        records: list[ValidationAllRecord] = []
        for relative_path in self._document_semantics_targets():
            result = self._safe_validate_path(
                family="document_semantics",
                target=relative_path,
                runner=self._document_semantics.validate,
            )
            records.append(
                ValidationAllRecord(
                    family="document_semantics",
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

    def _document_semantics_targets(self) -> tuple[str, ...]:
        repo_root = self._loader.repo_root
        standards_root = repo_root / STANDARD_DOC_ROOT
        standards = tuple(
            path.relative_to(repo_root).as_posix()
            for path in sorted(standards_root.rglob("*.md"))
            if path.name not in STANDARD_EXCLUDED_NAMES
        )
        workflows_root = repo_root / WORKFLOW_DOC_ROOT
        workflows = tuple(
            path.relative_to(repo_root).as_posix()
            for path in sorted(workflows_root.glob("*.md"))
            if path.name not in WORKFLOW_EXCLUDED_NAMES
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
            *workflows,
        )

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
        targets: list[str] = []
        seen: set[str] = set()

        def add(trace_id: str) -> None:
            if trace_id in seen:
                return
            seen.add(trace_id)
            targets.append(trace_id)

        for trace_entry in self._loader.load_traceability_index().entries:
            if (
                trace_entry.acceptance_ids
                or trace_entry.acceptance_contract_ids
                or trace_entry.evidence_ids
            ):
                add(trace_entry.trace_id)
        for prd_entry in self._loader.load_prd_index().entries:
            if prd_entry.acceptance_ids:
                add(prd_entry.trace_id)
        for contract in self._loader.load_acceptance_contracts():
            add(contract.trace_id)
        for evidence in self._loader.load_validation_evidence_artifacts():
            add(evidence.trace_id)
        return tuple(targets)

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
