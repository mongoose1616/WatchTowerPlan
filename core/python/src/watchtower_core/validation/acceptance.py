"""Semantic acceptance and evidence reconciliation for traced initiatives."""

from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import TraceabilityEntry
from watchtower_core.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    PrdQueryService,
    PrdSearchParams,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
)
from watchtower_core.validation.models import ValidationIssue, ValidationResult

ACCEPTANCE_RECONCILIATION_VALIDATOR_ID = "validator.trace.acceptance_reconciliation"


class AcceptanceReconciliationService:
    """Validate one trace across PRD acceptance IDs, contracts, evidence, and traceability."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def validate(self, trace_id: str) -> ValidationResult:
        """Return semantic reconciliation results for one trace."""
        issues: list[ValidationIssue] = []
        trace_entry = self._load_trace_entry(trace_id, issues)
        prds = PrdQueryService(self._loader).search(PrdSearchParams(trace_id=trace_id))
        contracts = AcceptanceContractQueryService(self._loader).search(
            AcceptanceContractSearchParams(trace_id=trace_id)
        )
        evidence_artifacts = ValidationEvidenceQueryService(self._loader).search(
            ValidationEvidenceSearchParams(trace_id=trace_id)
        )
        validator_ids = {
            definition.validator_id
            for definition in self._loader.load_validator_registry().validators
        }

        target_path = (
            contracts[0].doc_path
            if contracts
            else "core/control_plane/contracts/acceptance/"
        )

        if len(prds) != 1:
            issues.append(
                ValidationIssue(
                    code="trace_prd_count_invalid",
                    message=(
                        f"Trace {trace_id} should resolve to exactly one PRD index entry, "
                        f"found {len(prds)}."
                    ),
                    location="prd_index",
                )
            )

        if len(contracts) != 1:
            issues.append(
                ValidationIssue(
                    code="acceptance_contract_count_invalid",
                    message=(
                        f"Trace {trace_id} should resolve to exactly one acceptance contract, "
                        f"found {len(contracts)}."
                    ),
                    location="acceptance_contracts",
                )
            )

        if trace_entry is None or not prds or not contracts:
            return ValidationResult(
                validator_id=ACCEPTANCE_RECONCILIATION_VALIDATOR_ID,
                target_path=target_path,
                engine="python",
                schema_ids=(),
                passed=not issues,
                issues=tuple(issues),
            )

        prd = prds[0]
        contract = contracts[0]
        prd_acceptance_ids = set(prd.acceptance_ids)
        contract_acceptance_ids = {entry.acceptance_id for entry in contract.entries}
        trace_acceptance_ids = set(trace_entry.acceptance_ids)
        trace_contract_ids = set(trace_entry.acceptance_contract_ids)
        trace_evidence_ids = set(trace_entry.evidence_ids)

        if contract.source_prd_id != prd.prd_id:
            issues.append(
                ValidationIssue(
                    code="acceptance_contract_source_prd_mismatch",
                    message=(
                        f"Acceptance contract {contract.contract_id} points to "
                        f"{contract.source_prd_id}, not {prd.prd_id}."
                    ),
                    location="acceptance_contract.source_prd_id",
                )
            )

        self._compare_id_sets(
            issues,
            expected=prd_acceptance_ids,
            actual=contract_acceptance_ids,
            missing_code="acceptance_ids_missing_in_contract",
            extra_code="acceptance_ids_extra_in_contract",
            missing_location="acceptance_contract.entries",
            extra_location="acceptance_contract.entries",
            missing_message_prefix=(
                "Acceptance IDs published by the PRD are missing from the acceptance contract"
            ),
            extra_message_prefix=(
                "Acceptance IDs published by the acceptance contract are not present in the PRD"
            ),
        )
        self._compare_id_sets(
            issues,
            expected=prd_acceptance_ids,
            actual=trace_acceptance_ids,
            missing_code="acceptance_ids_missing_in_traceability",
            extra_code="acceptance_ids_extra_in_traceability",
            missing_location="traceability.acceptance_ids",
            extra_location="traceability.acceptance_ids",
            missing_message_prefix=(
                "Acceptance IDs published by the PRD are missing from traceability"
            ),
            extra_message_prefix=(
                "Acceptance IDs published by traceability are not present in the PRD"
            ),
        )

        if contract.contract_id not in trace_contract_ids:
            issues.append(
                ValidationIssue(
                    code="acceptance_contract_missing_in_traceability",
                    message=(
                        f"Traceability entry for {trace_id} does not list "
                        f"{contract.contract_id} in acceptance_contract_ids."
                    ),
                    location="traceability.acceptance_contract_ids",
                )
            )
        extra_trace_contract_ids = trace_contract_ids - {entry.contract_id for entry in contracts}
        if extra_trace_contract_ids:
            issues.append(
                ValidationIssue(
                    code="acceptance_contract_ids_extra_in_traceability",
                    message=(
                        "Traceability lists acceptance contracts not found for this trace: "
                        f"{', '.join(sorted(extra_trace_contract_ids))}."
                    ),
                    location="traceability.acceptance_contract_ids",
                )
            )

        coverage: set[str] = set()
        evidence_ids = {artifact.evidence_id for artifact in evidence_artifacts}
        for item in contract.entries:
            for validator_id in item.required_validator_ids:
                if validator_id not in validator_ids:
                    issues.append(
                        ValidationIssue(
                            code="required_validator_missing",
                            message=(
                                f"Acceptance item {item.acceptance_id} requires unknown validator "
                                f"{validator_id}."
                            ),
                            location=f"acceptance_contract.entries[{item.acceptance_id}]",
                        )
                    )

        for artifact in evidence_artifacts:
            for contract_id in artifact.source_acceptance_contract_ids:
                if contract_id != contract.contract_id:
                    issues.append(
                        ValidationIssue(
                            code="evidence_acceptance_contract_mismatch",
                            message=(
                                f"Validation evidence {artifact.evidence_id} points to "
                                f"{contract_id}, not {contract.contract_id}."
                            ),
                            location=f"validation_evidence.{artifact.evidence_id}",
                        )
                    )
            for check in artifact.checks:
                if check.validator_id is not None and check.validator_id not in validator_ids:
                    issues.append(
                        ValidationIssue(
                            code="evidence_validator_missing",
                            message=(
                                f"Validation evidence check {check.check_id} references unknown "
                                f"validator {check.validator_id}."
                            ),
                            location=f"validation_evidence.{artifact.evidence_id}.{check.check_id}",
                        )
                    )
                for acceptance_id in check.acceptance_ids:
                    if acceptance_id not in prd_acceptance_ids:
                        issues.append(
                            ValidationIssue(
                                code="evidence_acceptance_id_unknown",
                                message=(
                                    f"Validation evidence check {check.check_id} "
                                    f"references unknown acceptance ID {acceptance_id}."
                                ),
                                location=(
                                    f"validation_evidence.{artifact.evidence_id}.{check.check_id}"
                                ),
                            )
                        )
                        continue
                    coverage.add(acceptance_id)

        missing_trace_evidence_ids = trace_evidence_ids - evidence_ids
        if missing_trace_evidence_ids:
            issues.append(
                ValidationIssue(
                    code="traceability_evidence_ids_missing",
                    message=(
                        "Traceability lists validation-evidence IDs that were not found for this "
                        f"trace: {', '.join(sorted(missing_trace_evidence_ids))}."
                    ),
                    location="traceability.evidence_ids",
                )
            )
        extra_evidence_ids = evidence_ids - trace_evidence_ids
        if extra_evidence_ids:
            issues.append(
                ValidationIssue(
                    code="traceability_evidence_ids_out_of_sync",
                    message=(
                        "Validation evidence exists for this trace but is not listed in "
                        f"traceability: {', '.join(sorted(extra_evidence_ids))}."
                    ),
                    location="traceability.evidence_ids",
                )
            )

        uncovered_acceptance_ids = contract_acceptance_ids - coverage
        if uncovered_acceptance_ids:
            issues.append(
                ValidationIssue(
                    code="acceptance_ids_missing_evidence_coverage",
                    message=(
                        "Acceptance IDs do not have durable evidence coverage: "
                        f"{', '.join(sorted(uncovered_acceptance_ids))}."
                    ),
                    location="validation_evidence.checks",
                )
            )

        return ValidationResult(
            validator_id=ACCEPTANCE_RECONCILIATION_VALIDATOR_ID,
            target_path=target_path,
            engine="python",
            schema_ids=(),
            passed=not issues,
            issues=tuple(issues),
        )

    def _load_trace_entry(
        self,
        trace_id: str,
        issues: list[ValidationIssue],
    ) -> TraceabilityEntry | None:
        try:
            return self._loader.load_traceability_index().get(trace_id)
        except KeyError:
            issues.append(
                ValidationIssue(
                    code="traceability_entry_missing",
                    message=f"Traceability entry does not exist for trace_id {trace_id}.",
                    location="traceability",
                )
            )
            return None

    @staticmethod
    def _compare_id_sets(
        issues: list[ValidationIssue],
        *,
        expected: set[str],
        actual: set[str],
        missing_code: str,
        extra_code: str,
        missing_location: str,
        extra_location: str,
        missing_message_prefix: str,
        extra_message_prefix: str,
    ) -> None:
        missing = expected - actual
        if missing:
            issues.append(
                ValidationIssue(
                    code=missing_code,
                    message=f"{missing_message_prefix}: {', '.join(sorted(missing))}.",
                    location=missing_location,
                )
            )
        extra = actual - expected
        if extra:
            issues.append(
                ValidationIssue(
                    code=extra_code,
                    message=f"{extra_message_prefix}: {', '.join(sorted(extra))}.",
                    location=extra_location,
                )
            )
