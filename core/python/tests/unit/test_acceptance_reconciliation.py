from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.query import (
    AcceptanceContractQueryService,
    AcceptanceContractSearchParams,
    ValidationEvidenceQueryService,
    ValidationEvidenceSearchParams,
)
from watchtower_core.validation import AcceptanceReconciliationService

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


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


def test_acceptance_reconciliation_reuses_snapshots_across_validate_calls(
    monkeypatch,
) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = AcceptanceReconciliationService(loader)
    counts = Counter()

    for name in (
        "load_traceability_index",
        "load_prd_index",
        "load_acceptance_contracts",
        "load_validation_evidence_artifacts",
        "load_validator_registry",
    ):
        original = getattr(loader, name)

        def make_wrapper(method_name, method):
            def wrapped(*args, **kwargs):
                counts[method_name] += 1
                return method(*args, **kwargs)

            return wrapped

        monkeypatch.setattr(loader, name, make_wrapper(name, original))

    first = service.validate("trace.core_python_foundation")
    second = service.validate("trace.core_python_foundation")

    assert first.passed is True
    assert second.passed is True
    assert counts == {
        "load_traceability_index": 1,
        "load_prd_index": 1,
        "load_acceptance_contracts": 1,
        "load_validation_evidence_artifacts": 1,
        "load_validator_registry": 1,
    }


def test_acceptance_reconciliation_reports_missing_repo_local_paths(
    tmp_path: Path,
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    contract_path = (
        repo_root
        / "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json"
    )
    evidence_path = (
        repo_root
        / "core/control_plane/ledgers/validation_evidence/"
        "core_python_foundation_traceability_validation.v1.json"
    )

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["entries"][0]["validation_targets"].append("docs/planning/tasks/open/missing_task.md")
    contract["entries"][0]["related_paths"] = ["docs/planning/tasks/open/missing_task.md"]
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["related_paths"] = ["docs/planning/tasks/open/missing_task.md"]
    evidence["checks"][0]["subject_paths"].append("docs/planning/tasks/open/missing_task.md")
    evidence_path.write_text(f"{json.dumps(evidence, indent=2)}\n", encoding="utf-8")

    result = AcceptanceReconciliationService(ControlPlaneLoader(repo_root)).validate(
        "trace.core_python_foundation"
    )

    assert result.passed is False
    assert {
        issue.code for issue in result.issues
    } >= {
        "acceptance_validation_target_missing",
        "acceptance_related_path_missing",
        "evidence_related_path_missing",
        "evidence_subject_path_missing",
    }
