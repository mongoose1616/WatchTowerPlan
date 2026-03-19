from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.integration.fixture_repo_support import (
    bootstrap_packwide_initiative,
    materialize_acceptance_and_evidence_paths,
    materialize_plan_pack,
)
from watchtower_core.closeout import InitiativeCloseoutService
from watchtower_core.control_plane.loader import (
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)
from watchtower_core.plan_runtime.plan_workspace import (
    PLAN_COORDINATION_INDEX_PATH as COORDINATION_INDEX_PATH,
    PLAN_INITIATIVE_INDEX_PATH as INITIATIVE_INDEX_PATH,
    PLAN_TASK_INDEX_PATH as TASK_INDEX_PATH,
)
from watchtower_core.plan_runtime.sync.coordination import CoordinationSyncService

REPO_ROOT = Path(__file__).resolve().parents[4]
CURRENT_ACCEPTANCE_PATH = (
    "core/control_plane/contracts/acceptance/"
    "governed_acceptance_example_acceptance.json"
)
CURRENT_TRACE_ID = "trace.governed_acceptance_example"


def _build_closeout_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_plan_pack(repo_root, REPO_ROOT)
    materialize_acceptance_and_evidence_paths(repo_root)
    bootstrap_packwide_initiative(
        repo_root,
        trace_id="trace.example_live_plan_closeout_fixture",
        title="Example Live Plan Closeout Fixture",
        summary="Seeds one live initiative package so closeout tests cover live-plan rejection and linked-task behavior without relying on retained repo history.",
    )
    return repo_root


def _load_json(repo_root: Path, relative_path: str) -> dict[str, object]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def _write_json(repo_root: Path, relative_path: str, document: dict[str, object]) -> None:
    (repo_root / relative_path).write_text(
        f"{json.dumps(document, indent=2)}\n",
        encoding="utf-8",
    )


def _seed_terminal_task_for_trace(repo_root: Path, trace_id: str, task_id: str) -> None:
    task_index_document = _load_json(repo_root, TASK_INDEX_PATH)
    task_entries = task_index_document["entries"]
    assert isinstance(task_entries, list)
    seeded_task = dict(task_entries[0])
    seeded_task.update(
        {
            "task_id": task_id,
            "trace_id": trace_id,
            "title": "Acceptance closeout fixture task",
            "summary": "Seeds a terminal task entry for closeout validation.",
            "status": "active",
            "task_status": "completed",
            "updated_at": "2026-03-10T23:10:00Z",
        }
    )
    task_index_document["entries"] = [seeded_task]
    _write_json(repo_root, TASK_INDEX_PATH, task_index_document)


def test_initiative_closeout_updates_effective_timestamps_and_coordination_outputs(
    monkeypatch,
    tmp_path: Path,
) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    initiative_index_document = _load_json(repo_root, INITIATIVE_INDEX_PATH)
    initiative_entries = initiative_index_document["entries"]
    assert isinstance(initiative_entries, list)
    initiative_trace_ids = {
        entry["trace_id"]
        for entry in initiative_entries
        if isinstance(entry, dict) and isinstance(entry.get("trace_id"), str)
    }
    target = next(
        entry
        for entry in entries
        if entry["trace_id"] not in initiative_trace_ids
    )
    fixture_trace_id = target["trace_id"]
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T19:43:34Z"
    target["task_ids"] = [f"task.{fixture_trace_id.removeprefix('trace.')}.closeout.001"]
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    (repo_root / TRACEABILITY_INDEX_PATH).write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )
    _seed_terminal_task_for_trace(
        repo_root,
        fixture_trace_id,
        f"task.{fixture_trace_id.removeprefix('trace.')}.closeout.001",
    )

    closed_at = "2026-03-10T23:59:59Z"
    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))
    shared_targets: dict[str, tuple[str, ...]] = {}
    original_run_closeout_shared_outputs = (
        CoordinationSyncService.run_closeout_shared_outputs
    )

    def wrapped_run_closeout_shared_outputs(
        self: CoordinationSyncService,
        *,
        write: bool = False,
        output_dir: Path | None = None,
    ):
        result = original_run_closeout_shared_outputs(
            self,
            write=write,
            output_dir=output_dir,
        )
        shared_targets["targets"] = tuple(record.target for record in result.records)
        return result

    monkeypatch.setattr(
        CoordinationSyncService,
        "run_closeout_shared_outputs",
        wrapped_run_closeout_shared_outputs,
    )
    result = service.close(
        trace_id=fixture_trace_id,
        initiative_status="completed",
        closure_reason="Closed for regression coverage.",
        closed_at=closed_at,
        write=True,
        allow_open_tasks=True,
        allow_acceptance_issues=True,
    )

    assert result.traceability_output_path is not None
    assert result.initiative_index_output_path is not None
    assert result.coordination_index_output_path is not None
    assert result.initiative_tracking_output_path is not None
    assert result.coordination_tracking_output_path is not None
    assert shared_targets["targets"] == (
        "initiative-index",
        "coordination-index",
        "initiative-tracking",
        "coordination-tracking",
    )

    written_traceability = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    written_trace_entry = next(
        entry
        for entry in written_traceability["entries"]
        if entry["trace_id"] == fixture_trace_id
    )
    assert written_trace_entry["updated_at"] == closed_at
    assert written_trace_entry["closed_at"] == closed_at

    written_initiative_index = _load_json(repo_root, INITIATIVE_INDEX_PATH)
    initiative_entries = written_initiative_index["entries"]
    assert isinstance(initiative_entries, list)
    assert not any(
        entry["trace_id"] == fixture_trace_id
        for entry in initiative_entries
        if isinstance(entry, dict)
        and isinstance(entry.get("trace_id"), str)
    )

    written_coordination_index = _load_json(repo_root, COORDINATION_INDEX_PATH)
    assert written_coordination_index["updated_at"] == max(
        entry["updated_at"]
        for entry in initiative_entries
        if isinstance(entry, dict)
        and isinstance(entry.get("updated_at"), str)
    )

    coordination_tracking = (repo_root / "plan/tracking/coordination_tracking.md").read_text(
        encoding="utf-8"
    )
    assert (
        f"_Updated At: `{written_coordination_index['updated_at']}`_"
        in coordination_tracking
    )


def test_initiative_closeout_rejects_open_tasks_without_override(tmp_path: Path) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    trace_id = "trace.example_open_closeout"
    task_id = "task.example_open_closeout.execution.001"

    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    trace_entries = traceability_document["entries"]
    assert isinstance(trace_entries, list)
    target_trace = trace_entries[0]
    assert isinstance(target_trace, dict)
    target_trace["trace_id"] = trace_id
    target_trace["title"] = "Example Open Closeout"
    target_trace["summary"] = "Fixture trace with open linked work."
    target_trace["initiative_status"] = "active"
    target_trace["updated_at"] = "2026-03-10T23:10:00Z"
    target_trace["task_ids"] = [task_id]
    target_trace.pop("closed_at", None)
    target_trace.pop("closure_reason", None)
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_document)

    task_index_document = _load_json(repo_root, TASK_INDEX_PATH)
    task_entries = task_index_document["entries"]
    assert isinstance(task_entries, list)
    target_task = task_entries[0]
    assert isinstance(target_task, dict)
    target_task["task_id"] = task_id
    target_task["title"] = "Example open task"
    target_task["summary"] = "Fixture task left open for closeout validation."
    target_task["trace_id"] = trace_id
    target_task["status"] = "active"
    target_task["task_status"] = "ready"
    target_task["doc_path"] = (
        "plan/initiatives/plan_task_authority_rendering_governance_recovery/.wt/tasks/"
        "align_bootstrap_sync_and_fixtures/task.json"
    )
    target_task["updated_at"] = "2026-03-10T23:10:00Z"
    _write_json(repo_root, TASK_INDEX_PATH, task_index_document)

    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))

    try:
        service.close(
            trace_id=trace_id,
            initiative_status="completed",
            closure_reason="Attempted closeout with active work still open.",
            write=False,
        )
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected initiative closeout to reject open linked tasks.")

    assert task_id in message
    assert "--allow-open-tasks" in message


def test_initiative_closeout_rejects_live_plan_trace_ids(tmp_path: Path) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    initiative_index_document = _load_json(repo_root, INITIATIVE_INDEX_PATH)
    initiative_entries = initiative_index_document["entries"]
    assert isinstance(initiative_entries, list)
    target_entry = next(
        entry
        for entry in initiative_entries
        if isinstance(entry, dict)
        and isinstance(entry.get("trace_id"), str)
        and isinstance(entry.get("slug"), str)
    )

    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))

    with pytest.raises(ValueError) as exc_info:
        service.close(
            trace_id=target_entry["trace_id"],
            initiative_status="completed",
            closure_reason="Should fail for live plan initiatives.",
            write=False,
        )

    message = str(exc_info.value)
    assert "live `plan/**` initiative package" in message
    assert "watchtower-core closeout plan-initiative" in message
    assert f"--initiative-slug {target_entry['slug']}" in message


def test_initiative_closeout_rejects_missing_linked_tasks_in_task_index(tmp_path: Path) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    trace_id = "trace.example_open_closeout"
    missing_task_id = "task.example_open_closeout.missing.001"

    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    trace_entries = traceability_document["entries"]
    assert isinstance(trace_entries, list)
    target_trace = trace_entries[0]
    assert isinstance(target_trace, dict)
    target_trace["trace_id"] = trace_id
    target_trace["title"] = "Example Open Closeout"
    target_trace["summary"] = "Fixture trace with stale linked task references."
    target_trace["initiative_status"] = "active"
    target_trace["updated_at"] = "2026-03-10T23:10:00Z"
    target_trace["task_ids"] = [missing_task_id]
    target_trace.pop("closed_at", None)
    target_trace.pop("closure_reason", None)
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_document)

    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))

    try:
        service.close(
            trace_id=trace_id,
            initiative_status="completed",
            closure_reason="Attempted closeout with stale task links.",
            write=False,
            allow_open_tasks=True,
        )
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected initiative closeout to reject missing linked tasks.")

    assert missing_task_id in message
    assert "Rebuild traceability and task surfaces before closeout" in message


def test_initiative_closeout_rejects_acceptance_issues_without_override(
    tmp_path: Path,
) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    task_id = "task.governed_acceptance_example.closeout.001"
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    target = next(entry for entry in entries if entry["trace_id"] == CURRENT_TRACE_ID)
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T23:10:00Z"
    target["task_ids"] = [task_id]
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_document)
    _seed_terminal_task_for_trace(repo_root, CURRENT_TRACE_ID, task_id)

    contract_path = repo_root / CURRENT_ACCEPTANCE_PATH
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["entries"] = contract["entries"][:1]
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")
    evidence_path = (
        repo_root
        / "core/control_plane/ledgers/validation_evidence/"
        "governed_acceptance_example_validation_baseline.json"
    )
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["checks"][0]["acceptance_ids"] = ["ac.missing_closeout_example.001"]
    evidence_path.write_text(f"{json.dumps(evidence, indent=2)}\n", encoding="utf-8")

    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))

    try:
        service.close(
            trace_id=CURRENT_TRACE_ID,
            initiative_status="completed",
            closure_reason="Attempted closeout with unresolved acceptance drift.",
            write=False,
            allow_open_tasks=True,
        )
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected initiative closeout to reject acceptance drift.")

    assert "acceptance reconciliation issue" in message
    assert "validate acceptance" in message
    assert "--allow-acceptance-issues" in message


def test_initiative_closeout_allows_explicit_acceptance_issue_override(
    tmp_path: Path,
) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    task_id = "task.governed_acceptance_example.closeout.001"
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    target = next(entry for entry in entries if entry["trace_id"] == CURRENT_TRACE_ID)
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T23:10:00Z"
    target["task_ids"] = [task_id]
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_document)
    _seed_terminal_task_for_trace(repo_root, CURRENT_TRACE_ID, task_id)

    contract_path = repo_root / CURRENT_ACCEPTANCE_PATH
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["entries"] = contract["entries"][:1]
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")
    evidence_path = (
        repo_root
        / "core/control_plane/ledgers/validation_evidence/"
        "governed_acceptance_example_validation_baseline.json"
    )
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["checks"][0]["acceptance_ids"] = ["ac.missing_closeout_example.001"]
    evidence_path.write_text(f"{json.dumps(evidence, indent=2)}\n", encoding="utf-8")

    result = InitiativeCloseoutService(ControlPlaneLoader(repo_root)).close(
        trace_id=CURRENT_TRACE_ID,
        initiative_status="completed",
        closure_reason=(
            "Explicitly allowed acceptance drift for cancellation-style "
            "closeout testing."
        ),
        write=False,
        allow_open_tasks=True,
        allow_acceptance_issues=True,
    )

    assert result.acceptance_issue_count > 0
    assert result.acceptance_issues_allowed is True
