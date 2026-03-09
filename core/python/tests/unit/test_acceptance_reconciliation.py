from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
)
from watchtower_core.validation import AcceptanceReconciliationService

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_query_acceptance_contracts_by_trace_id() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    results = AcceptanceContractQueryService(loader).search(
        AcceptanceContractSearchParams(trace_id="trace.core_python_foundation")
    )

    assert len(results) == 1
    assert results[0].contract_id == "contract.acceptance.core_python_foundation"
    assert {entry.acceptance_id for entry in results[0].entries} == {
        "ac.core_python_foundation.001",
        "ac.core_python_foundation.002",
        "ac.core_python_foundation.003",
        "ac.core_python_foundation.004",
    }


def test_query_validation_evidence_by_acceptance_id() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    results = ValidationEvidenceQueryService(loader).search(
        ValidationEvidenceSearchParams(acceptance_id="ac.core_python_foundation.003")
    )

    assert len(results) == 1
    assert (
        results[0].evidence_id
        == "evidence.core_python_foundation.traceability_baseline"
    )


def test_acceptance_reconciliation_passes_for_current_trace() -> None:
    service = AcceptanceReconciliationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("trace.core_python_foundation")

    assert result.passed is True
    assert result.validator_id == "validator.trace.acceptance_reconciliation"
    assert result.issue_count == 0


def test_acceptance_reconciliation_reports_missing_traceability_entry() -> None:
    service = AcceptanceReconciliationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("trace.missing_example")

    assert result.passed is False
    assert any(issue.code == "traceability_entry_missing" for issue in result.issues)
