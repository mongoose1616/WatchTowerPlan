from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import (
    materialize_acceptance_and_evidence_paths,
    materialize_plan_pack,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_plan.query import (
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
    materialize_plan_pack(repo_root, REPO_ROOT)
    materialize_acceptance_and_evidence_paths(repo_root)
    return repo_root


def test_query_acceptance_contracts_by_trace_id() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    results = AcceptanceContractQueryService(loader).search(
        AcceptanceContractSearchParams(
            trace_id="trace.governed_acceptance_example"
        )
    )

    assert len(results) == 1
    assert (
        results[0].contract_id
        == "contract.acceptance.governed_acceptance_example"
    )
    assert {entry.acceptance_id for entry in results[0].entries} == {
        "ac.governed_acceptance_example.001",
    }


def test_query_validation_evidence_by_acceptance_id() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    results = ValidationEvidenceQueryService(loader).search(
        ValidationEvidenceSearchParams(
            acceptance_id="ac.governed_acceptance_example.001"
        )
    )

    assert len(results) == 1
    assert (
        results[0].evidence_id
        == "evidence.governed_acceptance_example.validation_baseline"
    )


def test_acceptance_reconciliation_passes_for_current_trace() -> None:
    service = AcceptanceReconciliationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("trace.governed_acceptance_example")

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

    first = service.validate("trace.governed_acceptance_example")
    second = service.validate("trace.governed_acceptance_example")

    assert first.passed is True
    assert second.passed is True
    assert counts == {
        "load_traceability_index": 1,
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
        / "core/control_plane/contracts/acceptance/"
        "governed_acceptance_example_acceptance.json"
    )
    evidence_path = (
        repo_root
        / "core/control_plane/ledgers/validation_evidence/"
        "governed_acceptance_example_validation_baseline.json"
    )

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    missing_task_path = "plan/initiatives/missing/.wt/tasks/missing/task.json"
    contract["entries"][0]["validation_targets"].append(missing_task_path)
    contract["entries"][0]["related_paths"] = [missing_task_path]
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["related_paths"] = [missing_task_path]
    evidence["checks"][0]["subject_paths"].append(missing_task_path)
    evidence_path.write_text(f"{json.dumps(evidence, indent=2)}\n", encoding="utf-8")

    result = AcceptanceReconciliationService(ControlPlaneLoader(repo_root)).validate(
        "trace.governed_acceptance_example"
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
