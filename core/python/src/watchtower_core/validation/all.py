"""Aggregate validation helpers built on reusable-core suite orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.control_plane.loader import PACK_SETTINGS_PATH, ControlPlaneLoader
from watchtower_core.validation.acceptance import AcceptanceReconciliationService
from watchtower_core.validation.models import ValidationResult
from watchtower_core.validation.suite import (
    ValidationSuiteService,
    ValidationSuiteTargetResolver,
)

VALIDATION_ALL_FAMILIES: tuple[str, ...] = (
    "front_matter",
    "document_semantics",
    "artifacts",
    "acceptance",
)
_STEP_KIND_TO_FAMILY = {
    "front_matter": "front_matter",
    "document_semantics": "document_semantics",
    "artifact": "artifacts",
}


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
    """Run a repo baseline suite plus acceptance reconciliation."""

    def __init__(
        self,
        loader: ControlPlaneLoader,
        *,
        suite_id: str,
        pack_settings_path: str = PACK_SETTINGS_PATH,
        suite_target_resolver: ValidationSuiteTargetResolver | None = None,
    ) -> None:
        self._loader = loader
        self._suite_id = suite_id
        self._pack_settings_path = pack_settings_path
        self._suite = ValidationSuiteService(
            loader,
            target_resolver=suite_target_resolver,
        )
        self._acceptance = AcceptanceReconciliationService(loader)

    def run(
        self,
        *,
        included_families: tuple[str, ...] | None = None,
    ) -> ValidationAllResult:
        """Run the selected validation families and return their aggregate results."""

        requested_families = (
            set(VALIDATION_ALL_FAMILIES)
            if included_families is None
            else set(included_families)
        )
        unknown_families = requested_families.difference(VALIDATION_ALL_FAMILIES)
        if unknown_families:
            unknown = ", ".join(sorted(unknown_families))
            raise ValueError(f"validate all received unknown validation families: {unknown}")

        resolved_families = tuple(
            family for family in VALIDATION_ALL_FAMILIES if family in requested_families
        )
        if not resolved_families:
            raise ValueError("validate all requires at least one validation family.")

        records: list[ValidationAllRecord] = []
        suite_step_kinds = tuple(
            step_kind
            for step_kind, family in _STEP_KIND_TO_FAMILY.items()
            if family in requested_families
        )
        if suite_step_kinds:
            suite_result = self._suite.run(
                self._suite_id,
                pack_settings_path=self._pack_settings_path,
                included_step_kinds=suite_step_kinds,
            )
            records.extend(
                ValidationAllRecord(
                    family=_STEP_KIND_TO_FAMILY[record.step_kind],
                    target=record.target,
                    result=record.result,
                )
                for record in suite_result.records
            )

        if "acceptance" in requested_families:
            for trace_id in self._acceptance.acceptance_trace_ids():
                result = self._acceptance.validate(trace_id)
                records.append(
                    ValidationAllRecord(
                        family="acceptance",
                        target=trace_id,
                        result=result,
                    )
                )

        return ValidationAllResult(
            records=tuple(records),
            included_families=resolved_families,
        )


__all__ = [
    "VALIDATION_ALL_FAMILIES",
    "ValidationAllRecord",
    "ValidationAllResult",
    "ValidationAllService",
    "ValidationFamilySummary",
]
