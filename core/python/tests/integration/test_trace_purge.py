from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_minimal_plan_pack,
)
from watchtower_core.control_plane.loader import (
    TRACE_PURGE_LEDGER_DIRECTORY,
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_plan.closeout import TracePurgeService
from watchtower_plan.plan_workspace import (
    PLAN_INITIATIVE_INDEX_PATH,
    PLAN_TASK_INDEX_PATH,
)
from watchtower_plan.sync.all import AllSyncRecord, AllSyncResult

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_purge_fixture_repo(repo_root: Path) -> Path:
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    (repo_root / "plan/docs/standards/governance").mkdir(parents=True, exist_ok=True)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_live_purge_fixture",
        title="Example Live Purge Fixture",
        summary="Seeds one live initiative package so purge tests can derive fixture entries without relying on retained repo history.",
    )
    return repo_root


@pytest.fixture(scope="module")
def purge_fixture_baseline(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_purge_fixture_repo(
        tmp_path_factory.mktemp("trace_purge_baseline") / "repo"
    )


@pytest.fixture
def purge_fixture_repo(tmp_path: Path, purge_fixture_baseline: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(purge_fixture_baseline, repo_root)
    return repo_root


def _load_json(repo_root: Path, relative_path: str) -> dict[str, object]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def _write_json(repo_root: Path, relative_path: str, document: dict[str, object]) -> None:
    path = repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def _write_text(repo_root: Path, relative_path: str, content: str) -> None:
    path = repo_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _configure_trace_fixture(repo_root: Path) -> None:
    trace_id = "trace.example_purge"
    initiative_root = "plan/initiatives/example_purge"
    task_id = "task.example_purge.cleanup.001"
    task_path = f"{initiative_root}/.wt/tasks/example_purge_cleanup/task.json"
    task_event_path = f"{initiative_root}/.wt/tasks/example_purge_cleanup/events/0001_created.json"
    initiative_state_path = f"{initiative_root}/.wt/initiative.json"
    authority_path = "plan/docs/standards/governance/example_retained_authority.md"
    contract_path = "core/control_plane/contracts/acceptance/example_purge_acceptance.json"
    evidence_path = (
        "core/control_plane/ledgers/validation_evidence/"
        "example_purge_planning_baseline.json"
    )

    for relative_path in (
        f"{initiative_root}/plan.md",
        f"{initiative_root}/progress.md",
        f"{initiative_root}/summary.md",
    ):
        _write_text(repo_root, relative_path, f"# {relative_path}\n")

    _write_json(
        repo_root,
        initiative_state_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:plan:initiative-state:v1",
            "initiative_id": "initiative.example_purge",
            "trace_id": trace_id,
            "title": "Example Purge Initiative",
            "summary": "Fixture initiative package for purge tests.",
            "status": "completed",
            "updated_at": "2026-03-10T20:30:00Z",
            "closed_at": "2026-03-10T20:25:00Z",
            "closure_reason": "Completed and ready for purge testing.",
            "task_ids": [task_id],
            "acceptance_contract_ids": ["contract.acceptance.example_purge"],
            "evidence_ids": ["evidence.example_purge.planning_baseline"],
            "authored_inputs": [
                {
                    "path": f"{initiative_root}/plan.md",
                    "artifact_id": "plan.example_purge",
                    "kind": "plan",
                }
            ],
        },
    )
    _write_json(
        repo_root,
        task_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:plan:task-state:v1",
            "task_id": task_id,
            "slug": "example_purge_cleanup",
            "initiative_id": "initiative.example_purge",
            "trace_id": trace_id,
            "title": "Example purge cleanup task",
            "summary": "Fixture closed task for purge tests.",
            "status": "active",
            "task_status": "completed",
            "task_kind": "governance",
            "priority": "high",
            "owner": "repository_maintainer",
            "created_at": "2026-03-10T20:20:00Z",
            "updated_at": "2026-03-10T20:20:00Z",
            "scope_items": ["Remove the trace package."],
            "done_when_items": ["The fixture task is terminal."],
        },
    )
    _write_json(
        repo_root,
        task_event_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:event-stream:record:v1",
            "event_id": "event.example_purge_cleanup.created",
            "event_type": "task_created",
            "recorded_at": "2026-03-10T20:20:00Z",
            "payload": {"task_id": task_id},
        },
    )
    _write_text(repo_root, authority_path, "# Example retained authority\n")

    _write_json(
        repo_root,
        contract_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:contracts:acceptance-contract:v1",
            "id": "contract.acceptance.example_purge",
            "title": "Example Purge Acceptance Contract",
            "status": "active",
            "trace_id": trace_id,
            "source_surface_path": f"{initiative_root}/initiative_brief.md",
            "entries": [
                {
                    "acceptance_id": "ac.example_purge.001",
                    "summary": "The example purge fixture stays coherent before purge.",
                    "source_requirement_ids": ["req.example_purge.001"],
                    "validation_targets": [task_path, f"{initiative_root}/plan.md"],
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
            "id": "evidence.example_purge.planning_baseline",
            "title": "Example Purge Validation Evidence",
            "status": "active",
            "trace_id": trace_id,
            "overall_result": "passed",
            "recorded_at": "2026-03-10T20:30:00Z",
            "source_surface_paths": [
                f"{initiative_root}/initiative_brief.md",
                f"{initiative_root}/design_record.md",
                f"{initiative_root}/implementation_slice.md",
            ],
            "source_acceptance_contract_ids": ["contract.acceptance.example_purge"],
            "checks": [
                {
                    "check_id": "check.example_purge.acceptance",
                    "title": "Example purge acceptance check",
                    "result": "passed",
                    "subject_paths": [task_path, f"{initiative_root}/plan.md"],
                    "validator_id": "validator.trace.acceptance_reconciliation",
                    "acceptance_ids": ["ac.example_purge.001"],
                }
            ],
            "related_paths": [evidence_path, contract_path],
        },
    )

    initiative_index = _load_json(repo_root, PLAN_INITIATIVE_INDEX_PATH)
    initiative_entry = dict(initiative_index["entries"][0])
    initiative_entry.update(
        {
            "trace_id": trace_id,
            "title": "Example Purge Initiative",
            "summary": "Fixture initiative package for purge tests.",
            "artifact_status": "active",
            "initiative_status": "completed",
            "current_phase": "closed",
            "updated_at": "2026-03-10T20:30:00Z",
            "open_task_count": 0,
            "blocked_task_count": 0,
            "key_surface_path": f"{initiative_root}/plan.md",
            "next_action": "No further default action. Initiative is completed.",
            "next_surface_path": f"{initiative_root}/summary.md",
            "initiative_id": "initiative.example_purge",
            "slug": "example_purge",
            "scope_type": "pack_wide",
            "active_owners": ["repository_maintainer"],
            "task_ids": [task_id],
            "acceptance_contract_ids": ["contract.acceptance.example_purge"],
            "evidence_ids": ["evidence.example_purge.planning_baseline"],
            "closed_at": "2026-03-10T20:25:00Z",
            "closure_reason": "Completed and ready for purge testing.",
            "related_paths": [
                f"{initiative_root}/plan.md",
                f"{initiative_root}/progress.md",
                f"{initiative_root}/summary.md",
                authority_path,
                contract_path,
                evidence_path,
            ],
        }
    )
    initiative_entry.pop("active_task_ids", None)
    initiative_entry.pop("active_task_summaries", None)
    initiative_entry.pop("blocked_by_task_ids", None)
    initiative_index["entries"] = [initiative_entry]
    _write_json(repo_root, PLAN_INITIATIVE_INDEX_PATH, initiative_index)

    task_index = _load_json(repo_root, PLAN_TASK_INDEX_PATH)
    task_entry = dict(task_index["entries"][0])
    task_entry.update(
        {
            "task_id": task_id,
            "trace_id": trace_id,
            "title": "Example purge cleanup task",
            "summary": "Fixture closed task for purge tests.",
            "status": "active",
            "task_status": "completed",
            "task_kind": "governance",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": task_path,
            "updated_at": "2026-03-10T20:20:00Z",
        }
    )
    task_index["entries"] = [task_entry]
    _write_json(repo_root, PLAN_TASK_INDEX_PATH, task_index)

    traceability_index = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    trace_entry = dict(traceability_index["entries"][0])
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
            "source_surface_paths": [f"{initiative_root}/initiative_brief.md"],
            "task_ids": [task_id],
            "requirement_ids": ["req.example_purge.001"],
            "acceptance_ids": ["ac.example_purge.001"],
            "acceptance_contract_ids": ["contract.acceptance.example_purge"],
            "validator_ids": ["validator.trace.acceptance_reconciliation"],
            "evidence_ids": ["evidence.example_purge.planning_baseline"],
            "related_paths": [
                f"{initiative_root}/plan.md",
                f"{initiative_root}/progress.md",
                f"{initiative_root}/summary.md",
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
                    relative_output_path="core/control_plane/indexes/repository_paths/repository_path_index.json",
                    output_path=(
                        "core/control_plane/indexes/repository_paths/repository_path_index.json"
                        if write
                        else None
                    ),
                    wrote=write,
                    record_count=1,
                    details={},
                ),
                AllSyncRecord(
                    target="initiative-index",
                    artifact_kind="index",
                    relative_output_path=PLAN_INITIATIVE_INDEX_PATH,
                    output_path=PLAN_INITIATIVE_INDEX_PATH if write else None,
                    wrote=write,
                    record_count=1,
                    details={},
                ),
            ),
            wrote=write,
            output_dir=str(output_dir.resolve()) if output_dir is not None else None,
        )


def test_trace_purge_writes_ledger_and_deletes_package(purge_fixture_repo: Path) -> None:
    repo_root = purge_fixture_repo
    _configure_trace_fixture(repo_root)

    service = TracePurgeService(
        ControlPlaneLoader(repo_root),
        all_sync_factory=_FakeAllSyncService,
    )
    result = service.purge(trace_id="trace.example_purge", write=True)

    assert result.wrote is True
    assert result.refreshed_targets == ("repository-paths", "initiative-index")
    for relative_path in result.removed_paths:
        assert not (repo_root / relative_path).exists()

    assert not (repo_root / "plan/initiatives/example_purge").exists()
    assert (repo_root / "plan/docs/standards/governance/example_retained_authority.md").exists()

    purge_ledger_path = (
        repo_root / "core/control_plane/ledgers/purges/example_purge_purge_record.json"
    )
    assert purge_ledger_path.exists()
    purge_document = json.loads(purge_ledger_path.read_text(encoding="utf-8"))
    assert purge_document["trace_id"] == "trace.example_purge"
    assert purge_document["surviving_authority_paths"] == [
        "plan/docs/standards/governance/example_retained_authority.md"
    ]


def test_trace_purge_rejects_surviving_external_references(
    purge_fixture_repo: Path,
) -> None:
    repo_root = purge_fixture_repo
    _configure_trace_fixture(repo_root)
    _write_text(
        repo_root,
        "plan/docs/standards/governance/blocking_reference.md",
        "See plan/initiatives/example_purge/plan.md before deleting it.\n",
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

    assert "plan/docs/standards/governance/blocking_reference.md" in message


def test_trace_purge_prefers_explicit_authority_paths_over_defaults(
    purge_fixture_repo: Path,
) -> None:
    repo_root = purge_fixture_repo
    _configure_trace_fixture(repo_root)

    service = TracePurgeService(
        ControlPlaneLoader(repo_root),
        all_sync_factory=_FakeAllSyncService,
    )
    result = service.purge(
        trace_id="trace.example_purge",
        retained_authority_paths=(
            "plan/docs/standards/governance/example_retained_authority.md",
        ),
        write=False,
    )

    assert result.retained_authority_paths == (
        "plan/docs/standards/governance/example_retained_authority.md",
    )


def test_trace_purge_rejects_duplicate_ledger_records(
    purge_fixture_repo: Path,
) -> None:
    repo_root = purge_fixture_repo
    _configure_trace_fixture(repo_root)
    _write_json(
        repo_root,
        f"{TRACE_PURGE_LEDGER_DIRECTORY}/example_purge_purge_record.json",
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
                "plan/docs/standards/governance/example_retained_authority.md"
            ],
            "purged_paths": [
                "plan/initiatives/example_purge/plan.md"
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
