from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.closeout import TracePurgeService
from watchtower_core.control_plane.loader import (
    DECISION_INDEX_PATH,
    DESIGN_DOCUMENT_INDEX_PATH,
    PRD_INDEX_PATH,
    TASK_INDEX_PATH,
    TRACE_PURGE_LEDGER_DIRECTORY,
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_core.repo_ops.sync.all import AllSyncRecord, AllSyncResult

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_purge_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    for relative_path in (
        "docs/planning/prds",
        "docs/planning/decisions",
        "docs/planning/design/features",
        "docs/planning/design/implementation",
        "docs/planning/tasks/closed/archive/2026/03/10",
        "docs/standards/governance",
    ):
        (repo_root / relative_path).mkdir(parents=True, exist_ok=True)
    return repo_root


def _load_json(repo_root: Path, relative_path: str) -> dict[str, object]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def _write_json(repo_root: Path, relative_path: str, document: dict[str, object]) -> None:
    (repo_root / relative_path).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / relative_path).write_text(
        f"{json.dumps(document, indent=2)}\n",
        encoding="utf-8",
    )


def _write_text(repo_root: Path, relative_path: str, content: str) -> None:
    (repo_root / relative_path).parent.mkdir(parents=True, exist_ok=True)
    (repo_root / relative_path).write_text(content, encoding="utf-8")


def _configure_trace_fixture(repo_root: Path) -> None:
    trace_id = "trace.example_purge"
    prd_id = "prd.example_purge"
    decision_id = "decision.example_purge_direction"
    feature_design_id = "design.features.example_purge"
    implementation_plan_id = "design.implementation.example_purge"
    task_id = "task.example_purge.cleanup.001"
    acceptance_contract_id = "contract.acceptance.example_purge"
    evidence_id = "evidence.example_purge.planning_baseline"
    acceptance_id = "ac.example_purge.001"

    prd_path = "docs/planning/prds/example_purge.md"
    decision_path = "docs/planning/decisions/example_purge_direction.md"
    feature_design_path = "docs/planning/design/features/example_purge.md"
    implementation_plan_path = "docs/planning/design/implementation/example_purge.md"
    task_path = "docs/planning/tasks/closed/archive/2026/03/10/example_purge_cleanup.md"
    authority_path = "docs/standards/governance/example_retained_authority.md"
    contract_path = (
        "core/control_plane/contracts/acceptance/example_purge_acceptance.v1.json"
    )
    evidence_path = (
        "core/control_plane/ledgers/validation_evidence/"
        "example_purge_planning_baseline.v1.json"
    )

    for relative_path in (
        prd_path,
        decision_path,
        feature_design_path,
        implementation_plan_path,
        task_path,
    ):
        _write_text(repo_root, relative_path, f"# {relative_path}\n")
    _write_text(repo_root, authority_path, "# Example retained authority\n")

    prd_index = _load_json(repo_root, PRD_INDEX_PATH)
    prd_entries = prd_index["entries"]
    assert isinstance(prd_entries, list)
    prd_entry = dict(prd_entries[0])
    prd_entry.update(
        {
            "trace_id": trace_id,
            "prd_id": prd_id,
            "title": "Example Purge PRD",
            "summary": "Fixture PRD for purge tests.",
            "doc_path": prd_path,
            "updated_at": "2026-03-10T20:00:00Z",
            "requirement_ids": ["req.example_purge.001"],
            "acceptance_ids": [acceptance_id],
            "linked_decision_ids": [decision_id],
            "linked_design_ids": [feature_design_id],
            "linked_plan_ids": [implementation_plan_id],
            "related_paths": [prd_path, authority_path],
        }
    )
    prd_index["entries"] = [prd_entry]
    _write_json(repo_root, PRD_INDEX_PATH, prd_index)

    decision_index = _load_json(repo_root, DECISION_INDEX_PATH)
    decision_entries = decision_index["entries"]
    assert isinstance(decision_entries, list)
    decision_entry = dict(decision_entries[0])
    decision_entry.update(
        {
            "trace_id": trace_id,
            "decision_id": decision_id,
            "title": "Example Purge Direction",
            "summary": "Fixture decision for purge tests.",
            "doc_path": decision_path,
            "updated_at": "2026-03-10T20:05:00Z",
            "linked_prd_ids": [prd_id],
            "linked_design_ids": [feature_design_id],
            "linked_plan_ids": [implementation_plan_id],
            "related_paths": [decision_path, authority_path],
        }
    )
    decision_index["entries"] = [decision_entry]
    _write_json(repo_root, DECISION_INDEX_PATH, decision_index)

    design_index = _load_json(repo_root, DESIGN_DOCUMENT_INDEX_PATH)
    design_entries = design_index["entries"]
    assert isinstance(design_entries, list)
    feature_entry = dict(design_entries[0])
    feature_entry.update(
        {
            "document_id": feature_design_id,
            "trace_id": trace_id,
            "family": "feature_design",
            "title": "Example Purge Feature Design",
            "summary": "Fixture feature design for purge tests.",
            "doc_path": feature_design_path,
            "updated_at": "2026-03-10T20:10:00Z",
            "source_paths": [prd_path],
            "related_paths": [feature_design_path, authority_path],
        }
    )
    implementation_entry = dict(feature_entry)
    implementation_entry.update(
        {
            "document_id": implementation_plan_id,
            "family": "implementation_plan",
            "title": "Example Purge Implementation Plan",
            "summary": "Fixture implementation plan for purge tests.",
            "doc_path": implementation_plan_path,
            "updated_at": "2026-03-10T20:15:00Z",
            "source_paths": [feature_design_path],
            "related_paths": [implementation_plan_path, authority_path],
        }
    )
    design_index["entries"] = [feature_entry, implementation_entry]
    _write_json(repo_root, DESIGN_DOCUMENT_INDEX_PATH, design_index)

    task_index = _load_json(repo_root, TASK_INDEX_PATH)
    task_entries = task_index["entries"]
    assert isinstance(task_entries, list)
    task_entry = dict(task_entries[0])
    task_entry.update(
        {
            "task_id": task_id,
            "trace_id": trace_id,
            "title": "Example purge cleanup task",
            "summary": "Fixture closed task for purge tests.",
            "status": "active",
            "task_status": "done",
            "task_kind": "governance",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": task_path,
            "updated_at": "2026-03-10T20:20:00Z",
            "related_ids": [prd_id, decision_id],
            "applies_to": [prd_path],
        }
    )
    task_index["entries"] = [task_entry]
    _write_json(repo_root, TASK_INDEX_PATH, task_index)

    _write_json(
        repo_root,
        contract_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:contracts:acceptance-contract:v1",
            "id": acceptance_contract_id,
            "title": "Example Purge Acceptance Contract",
            "status": "active",
            "trace_id": trace_id,
            "source_prd_id": prd_id,
            "entries": [
                {
                    "acceptance_id": acceptance_id,
                    "summary": "The example purge fixture stays coherent before purge.",
                    "source_requirement_ids": ["req.example_purge.001"],
                    "validation_targets": [prd_path, decision_path],
                    "related_paths": [contract_path, evidence_path],
                }
            ],
        },
    )

    _write_json(
        repo_root,
        evidence_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:ledgers:validation-evidence:v1",
            "id": evidence_id,
            "title": "Example Purge Validation Evidence",
            "status": "active",
            "trace_id": trace_id,
            "overall_result": "passed",
            "recorded_at": "2026-03-10T20:30:00Z",
            "source_prd_ids": [prd_id],
            "source_decision_ids": [decision_id],
            "source_design_ids": [feature_design_id],
            "source_plan_ids": [implementation_plan_id],
            "source_acceptance_contract_ids": [acceptance_contract_id],
            "checks": [
                {
                    "check_id": "check.example_purge.acceptance",
                    "title": "Example purge acceptance check",
                    "result": "passed",
                    "subject_paths": [prd_path],
                    "validator_id": "validator.control_plane.acceptance_contract",
                    "acceptance_ids": [acceptance_id],
                }
            ],
            "related_paths": [evidence_path, contract_path],
        },
    )

    traceability_index = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    trace_entries = traceability_index["entries"]
    assert isinstance(trace_entries, list)
    trace_entry = dict(trace_entries[0])
    trace_entry.update(
        {
            "trace_id": trace_id,
            "title": "Example Purge Trace",
            "summary": "Fixture trace for purge tests.",
            "status": "active",
            "initiative_status": "completed",
            "updated_at": "2026-03-10T20:30:00Z",
            "closed_at": "2026-03-10T20:25:00Z",
            "closure_reason": "Completed and ready for purge testing.",
            "prd_ids": [prd_id],
            "decision_ids": [decision_id],
            "design_ids": [feature_design_id],
            "plan_ids": [implementation_plan_id],
            "task_ids": [task_id],
            "requirement_ids": ["req.example_purge.001"],
            "acceptance_ids": [acceptance_id],
            "acceptance_contract_ids": [acceptance_contract_id],
            "validator_ids": ["validator.control_plane.acceptance_contract"],
            "evidence_ids": [evidence_id],
            "related_paths": [
                prd_path,
                decision_path,
                feature_design_path,
                implementation_plan_path,
                task_path,
                contract_path,
                evidence_path,
                authority_path,
            ],
        }
    )
    traceability_index["entries"] = [trace_entry]
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_index)


class _FakeAllSyncService:
    def __init__(self, loader: ControlPlaneLoader) -> None:
        self.loader = loader

    def run(
        self,
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ) -> AllSyncResult:
        return AllSyncResult(
            records=(
                AllSyncRecord(
                    target="repository-paths",
                    artifact_kind="index",
                    relative_output_path="core/control_plane/indexes/repository_paths/repository_path_index.v1.json",
                    output_path=(
                        "core/control_plane/indexes/repository_paths/repository_path_index.v1.json"
                        if write
                        else None
                    ),
                    wrote=write,
                    record_count=1,
                    details={},
                ),
                AllSyncRecord(
                    target="planning-catalog",
                    artifact_kind="index",
                    relative_output_path="core/control_plane/indexes/planning/planning_catalog.v1.json",
                    output_path=(
                        "core/control_plane/indexes/planning/planning_catalog.v1.json"
                        if write
                        else None
                    ),
                    wrote=write,
                    record_count=1,
                    details={},
                ),
            ),
            wrote=write,
            output_dir=str(output_dir.resolve()) if output_dir is not None else None,
        )


def test_trace_purge_writes_ledger_and_deletes_package(tmp_path: Path) -> None:
    repo_root = _build_purge_fixture_repo(tmp_path)
    _configure_trace_fixture(repo_root)

    service = TracePurgeService(
        ControlPlaneLoader(repo_root),
        all_sync_factory=_FakeAllSyncService,
    )
    result = service.purge(trace_id="trace.example_purge", write=True)

    assert result.wrote is True
    assert result.refreshed_targets == ("repository-paths", "planning-catalog")
    for relative_path in result.removed_paths:
        assert not (repo_root / relative_path).exists()

    purge_ledger_path = (
        repo_root / "core/control_plane/ledgers/purges/example_purge_purge_record.v1.json"
    )
    assert purge_ledger_path.exists()
    purge_document = json.loads(purge_ledger_path.read_text(encoding="utf-8"))
    assert purge_document["trace_id"] == "trace.example_purge"
    assert purge_document["surviving_authority_paths"] == [
        "docs/standards/governance/example_retained_authority.md"
    ]


def test_trace_purge_rejects_surviving_external_references(tmp_path: Path) -> None:
    repo_root = _build_purge_fixture_repo(tmp_path)
    _configure_trace_fixture(repo_root)
    _write_text(
        repo_root,
        "docs/standards/governance/blocking_reference.md",
        "See docs/planning/prds/example_purge.md before deleting it.\n",
    )

    service = TracePurgeService(
        ControlPlaneLoader(repo_root),
        all_sync_factory=_FakeAllSyncService,
    )

    try:
        service.purge(trace_id="trace.example_purge", write=False)
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected purge guard to reject surviving external references.")

    assert "docs/standards/governance/blocking_reference.md" in message


def test_trace_purge_prefers_explicit_authority_paths_over_defaults(tmp_path: Path) -> None:
    repo_root = _build_purge_fixture_repo(tmp_path)
    _configure_trace_fixture(repo_root)

    service = TracePurgeService(
        ControlPlaneLoader(repo_root),
        all_sync_factory=_FakeAllSyncService,
    )
    result = service.purge(
        trace_id="trace.example_purge",
        retained_authority_paths=(
            "docs/standards/governance/example_retained_authority.md",
        ),
        write=False,
    )

    assert result.retained_authority_paths == (
        "docs/standards/governance/example_retained_authority.md",
    )


def test_trace_purge_rejects_duplicate_ledger_records(tmp_path: Path) -> None:
    repo_root = _build_purge_fixture_repo(tmp_path)
    _configure_trace_fixture(repo_root)
    _write_json(
        repo_root,
        f"{TRACE_PURGE_LEDGER_DIRECTORY}/example_purge_purge_record.v1.json",
        {
            "$schema": "urn:watchtower:schema:artifacts:ledgers:trace-purge-record:v1",
            "id": "purge.example_purge",
            "title": "Trace Purge Record for Example Purge Trace",
            "status": "active",
            "trace_id": "trace.example_purge",
            "initiative_status": "completed",
            "closed_at": "2026-03-10T20:25:00Z",
            "purged_at": "2026-03-10T20:35:00Z",
            "closure_reason": "Completed and ready for purge testing.",
            "summary": "Fixture duplicate ledger record.",
            "surviving_authority_paths": [
                "docs/standards/governance/example_retained_authority.md"
            ],
            "purged_paths": [
                "docs/planning/prds/example_purge.md"
            ],
        },
    )

    service = TracePurgeService(
        ControlPlaneLoader(repo_root),
        all_sync_factory=_FakeAllSyncService,
    )

    try:
        service.purge(trace_id="trace.example_purge", write=False)
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected purge guard to reject duplicate ledger records.")

    assert "already has a purge ledger entry" in message
