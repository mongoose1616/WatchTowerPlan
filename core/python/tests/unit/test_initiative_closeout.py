from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import materialize_acceptance_and_evidence_paths
from watchtower_core.closeout import InitiativeCloseoutService
from watchtower_core.control_plane.loader import (
    COORDINATION_INDEX_PATH,
    INITIATIVE_INDEX_PATH,
    PLANNING_CATALOG_PATH,
    TASK_INDEX_PATH,
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_closeout_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    for relative_path in (
        "docs/planning",
        "docs/planning/prds",
        "docs/planning/decisions",
        "docs/planning/design",
        "docs/planning/initiatives",
    ):
        (repo_root / relative_path).mkdir(parents=True, exist_ok=True)
    materialize_acceptance_and_evidence_paths(repo_root)
    return repo_root


def _load_json(repo_root: Path, relative_path: str) -> dict[str, object]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def _write_json(repo_root: Path, relative_path: str, document: dict[str, object]) -> None:
    (repo_root / relative_path).write_text(
        f"{json.dumps(document, indent=2)}\n",
        encoding="utf-8",
    )


def test_initiative_closeout_updates_effective_timestamps_and_coordination_outputs(
    tmp_path: Path,
) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    target = next(
        entry
        for entry in entries
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T19:43:34Z"
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    (repo_root / TRACEABILITY_INDEX_PATH).write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )

    closed_at = "2026-03-10T23:59:59Z"
    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))
    result = service.close(
        trace_id="trace.end_to_end_repo_review_and_rationalization",
        initiative_status="completed",
        closure_reason="Closed for regression coverage.",
        closed_at=closed_at,
        write=True,
        allow_open_tasks=True,
    )

    assert result.traceability_output_path is not None
    assert result.initiative_index_output_path is not None
    assert result.planning_catalog_output_path is not None
    assert result.coordination_index_output_path is not None
    assert result.initiative_tracking_output_path is not None
    assert result.coordination_tracking_output_path is not None

    written_traceability = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    written_trace_entry = next(
        entry
        for entry in written_traceability["entries"]
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    assert written_trace_entry["updated_at"] == closed_at
    assert written_trace_entry["closed_at"] == closed_at

    written_initiative_index = _load_json(repo_root, INITIATIVE_INDEX_PATH)
    initiative_entry = next(
        entry
        for entry in written_initiative_index["entries"]
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    assert initiative_entry["updated_at"] == closed_at
    assert initiative_entry["closed_at"] == closed_at

    written_coordination_index = _load_json(repo_root, COORDINATION_INDEX_PATH)
    initiative_entries = written_initiative_index["entries"]
    assert isinstance(initiative_entries, list)
    assert written_coordination_index["updated_at"] == max(
        entry["updated_at"]
        for entry in initiative_entries
        if isinstance(entry, dict)
        and isinstance(entry.get("updated_at"), str)
    )

    written_planning_catalog = _load_json(repo_root, PLANNING_CATALOG_PATH)
    planning_entry = next(
        entry
        for entry in written_planning_catalog["entries"]
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    assert planning_entry["initiative_status"] == "completed"
    coordination = planning_entry.get("coordination")
    assert isinstance(coordination, dict)
    assert coordination["current_phase"] == "closed"

    coordination_tracking = (repo_root / "docs/planning/coordination_tracking.md").read_text(
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
    target_task["doc_path"] = "docs/planning/tasks/open/example_open_closeout.md"
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
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    target = next(entry for entry in entries if entry["trace_id"] == "trace.core_python_foundation")
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T23:10:00Z"
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_document)

    contract_path = (
        repo_root
        / "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json"
    )
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["entries"] = contract["entries"][:1]
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")

    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))

    try:
        service.close(
            trace_id="trace.core_python_foundation",
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
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    target = next(entry for entry in entries if entry["trace_id"] == "trace.core_python_foundation")
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T23:10:00Z"
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    _write_json(repo_root, TRACEABILITY_INDEX_PATH, traceability_document)

    contract_path = (
        repo_root
        / "core/control_plane/contracts/acceptance/core_python_foundation_acceptance.v1.json"
    )
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["entries"] = contract["entries"][:1]
    contract_path.write_text(f"{json.dumps(contract, indent=2)}\n", encoding="utf-8")

    result = InitiativeCloseoutService(ControlPlaneLoader(repo_root)).close(
        trace_id="trace.core_python_foundation",
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
