from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_plan.initiatives import (
    InitiativeBootstrapParams,
    InitiativePackageService,
    InitiativeTaskSpec,
)
from watchtower_plan.plan_workspace import PLAN_TASK_INDEX_PATH
from watchtower_plan.sync import TraceabilityIndexSyncService

from tests.fixture_repo_support import (
    materialize_minimal_plan_pack,
)
from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]


def _initiative_state_path_for_trace(repo_root: Path, trace_id: str) -> Path:
    for path in sorted(repo_root.glob("plan/**/.wt/initiative.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("trace_id") == trace_id:
            return path
    raise AssertionError(f"Unable to locate initiative state for {trace_id}")


def _bootstrap_packwide_trace(
    repo_root: Path,
    *,
    initiative_slug: str,
    updated_at: str,
) -> str:
    loader = ControlPlaneLoader(repo_root)
    InitiativePackageService(loader).bootstrap_packwide(
        InitiativeBootstrapParams(
            trace_id=f"trace.{initiative_slug}",
            title=initiative_slug.replace("_", " ").title(),
            summary=f"Bootstraps {initiative_slug} for traceability-sync tests.",
            initiative_slug=initiative_slug,
            task_specs=(
                InitiativeTaskSpec(
                    title="Seed initiative state",
                    summary="Seeds one live task for traceability coverage.",
                    slug="seed_state",
                    task_id=f"task.{initiative_slug}.seed_state",
                ),
            ),
            updated_at=updated_at,
        ),
        write=True,
    )
    return f"trace.{initiative_slug}"


def test_traceability_index_sync_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = TraceabilityIndexSyncService(loader)

    document = service.build_document()

    loader.schema_store.validate_instance(document)
    entries = document["entries"]
    assert isinstance(entries, list)
    assert entries
    assert all(isinstance(entry.get("trace_id"), str) for entry in entries)
    assert all(str(entry["trace_id"]).startswith("trace.") for entry in entries)


def test_traceability_index_sync_writes_temp_output(tmp_path: Path) -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = TraceabilityIndexSyncService(loader)
    output_path = tmp_path / "traceability_index.json"

    document = service.build_document()
    written_path = service.write_document(document, output_path)

    assert written_path == output_path
    written_document = json.loads(output_path.read_text(encoding="utf-8"))
    assert written_document["id"] == "index.traceability"


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    (repo_root / "core/python").mkdir(parents=True)
    _bootstrap_packwide_trace(
        repo_root,
        initiative_slug="traceability_runtime_fixture",
        updated_at="2026-03-10T18:00:00Z",
    )
    return repo_root


def _build_full_plan_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    materialize_minimal_plan_pack(repo_root, REPO_ROOT)
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def test_traceability_index_sync_uses_closed_at_as_effective_updated_at(
    tmp_path: Path,
) -> None:
    repo_root = _build_full_plan_fixture_repo(tmp_path)
    trace_id = _bootstrap_packwide_trace(
        repo_root,
        initiative_slug="traceability_effective_updated",
        updated_at="2026-03-10T19:00:00Z",
    )
    initiative_path = _initiative_state_path_for_trace(repo_root, trace_id)
    initiative_document = json.loads(initiative_path.read_text(encoding="utf-8"))
    initiative_document["status"] = "completed"
    initiative_document["updated_at"] = "2099-03-10T19:00:00Z"
    initiative_document["closed_at"] = "2099-03-10T23:59:59Z"
    initiative_document["closure_reason"] = "Closed for sync regression coverage."
    initiative_path.write_text(
        f"{json.dumps(initiative_document, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    rebuilt_target = next(entry for entry in rebuilt_entries if entry["trace_id"] == trace_id)
    assert rebuilt_target["updated_at"] == "2099-03-10T23:59:59Z"


def test_traceability_index_sync_reopens_completed_initiative_when_active_task_reappears(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    trace_id = "trace.synthetic_reopened_follow_up"
    traceability_path = (
        repo_root / "core/control_plane/indexes/traceability/traceability_index.json"
    )
    task_index_path = repo_root / PLAN_TASK_INDEX_PATH

    traceability_document = json.loads(traceability_path.read_text(encoding="utf-8"))
    trace_entries = traceability_document["entries"]
    assert isinstance(trace_entries, list)
    target_trace = dict(trace_entries[0])
    target_trace.update(
        {
            "trace_id": trace_id,
            "title": "Synthetic Reopened Follow Up",
            "summary": "Synthetic traceability entry reopened by an active task.",
            "initiative_status": "completed",
            "updated_at": "2026-03-10T20:00:00Z",
            "closed_at": "2026-03-10T20:30:00Z",
            "closure_reason": "Closed before a follow-up task was discovered.",
            "task_ids": ["task.synthetic_reopened_follow_up.seed_state"],
        }
    )
    traceability_document["entries"] = [target_trace, *trace_entries]
    traceability_path.write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )

    task_index_document = json.loads(task_index_path.read_text(encoding="utf-8"))
    task_entries = task_index_document["entries"]
    assert isinstance(task_entries, list)
    target_task = dict(task_entries[0])
    target_task.update(
        {
            "initiative_id": "initiative.synthetic_reopened_follow_up",
            "trace_id": trace_id,
            "initiative_title": "Synthetic Reopened Follow Up",
            "title": "Reopened live-query follow-up",
            "summary": "Reopens the trace when a ready task reappears.",
            "status": "active",
            "task_status": "ready",
            "task_kind": "governance",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": (
                "plan/initiatives/synthetic_reopened_follow_up/.wt/tasks/follow_up_ready/task.json"
            ),
            "updated_at": "2099-03-10T23:59:59Z",
        }
    )
    task_index_document["entries"] = [target_task, *task_entries]
    task_index_path.write_text(
        f"{json.dumps(task_index_document, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    rebuilt_target = next(entry for entry in rebuilt_entries if entry["trace_id"] == trace_id)
    assert rebuilt_target["initiative_status"] == "active"
    assert rebuilt_target["updated_at"] == "2099-03-10T23:59:59Z"
    assert "closed_at" not in rebuilt_target
    assert "closure_reason" not in rebuilt_target


def test_traceability_index_sync_prefers_latest_same_rank_note(tmp_path: Path) -> None:
    repo_root = _build_full_plan_fixture_repo(tmp_path)
    evidence_root = repo_root / "core/control_plane/records/validation_evidence"
    trace_id = _bootstrap_packwide_trace(
        repo_root,
        initiative_slug="traceability_note_preference",
        updated_at="2026-03-14T03:00:00Z",
    )
    template_path = next(evidence_root.glob("*.json"))
    template = json.loads(template_path.read_text(encoding="utf-8"))

    earlier = dict(template)
    earlier["trace_id"] = trace_id
    earlier["id"] = "evidence.traceability_note_preference.synthetic_earlier"
    earlier["notes"] = "Earlier checkpoint note."
    earlier["recorded_at"] = "2099-03-14T03:56:23Z"
    (evidence_root / "synthetic_earlier.json").write_text(
        f"{json.dumps(earlier, indent=2)}\n",
        encoding="utf-8",
    )

    later = dict(template)
    later["trace_id"] = trace_id
    later["id"] = "evidence.traceability_note_preference.synthetic_later"
    later["notes"] = "Latest checkpoint note."
    later["recorded_at"] = "2099-03-14T23:59:59Z"
    (evidence_root / "synthetic_later.json").write_text(
        f"{json.dumps(later, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    rebuilt_target = next(entry for entry in rebuilt_entries if entry["trace_id"] == trace_id)
    assert rebuilt_target["notes"] == "Latest checkpoint note."


def test_traceability_index_sync_keeps_closed_live_initiative_state_over_stale_existing_entry(
    tmp_path: Path,
) -> None:
    repo_root = _build_full_plan_fixture_repo(tmp_path)
    trace_id = _bootstrap_packwide_trace(
        repo_root,
        initiative_slug="traceability_closed_state",
        updated_at="2026-03-17T19:00:00Z",
    )
    initiative_path = _initiative_state_path_for_trace(repo_root, trace_id)
    initiative_document = json.loads(initiative_path.read_text(encoding="utf-8"))
    initiative_document["status"] = "completed"
    initiative_document["closed_at"] = "2026-03-17T19:38:14Z"
    initiative_document["closure_reason"] = (
        "Closed for traceability closed-state regression coverage."
    )
    initiative_path.write_text(
        f"{json.dumps(initiative_document, indent=2)}\n",
        encoding="utf-8",
    )
    task_index_path = repo_root / PLAN_TASK_INDEX_PATH
    task_index_document = json.loads(task_index_path.read_text(encoding="utf-8"))
    task_entries = task_index_document["entries"]
    assert isinstance(task_entries, list)
    for entry in task_entries:
        if entry.get("trace_id") == trace_id:
            entry["task_status"] = "completed"
            entry["updated_at"] = "2026-03-17T19:38:14Z"
    task_index_path.write_text(
        f"{json.dumps(task_index_document, indent=2)}\n",
        encoding="utf-8",
    )
    traceability_path = (
        repo_root / "core/control_plane/indexes/traceability/traceability_index.json"
    )

    traceability_document = json.loads(traceability_path.read_text(encoding="utf-8"))
    trace_entries = traceability_document["entries"]
    assert isinstance(trace_entries, list)
    target_trace = next(entry for entry in trace_entries if entry["trace_id"] == trace_id)
    target_trace["initiative_status"] = "active"
    target_trace.pop("closed_at", None)
    target_trace.pop("closure_reason", None)
    traceability_path.write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)
    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    rebuilt_target = next(entry for entry in rebuilt_entries if entry["trace_id"] == trace_id)
    assert rebuilt_target["initiative_status"] == "completed"
    assert rebuilt_target["closed_at"] == "2026-03-17T19:38:14Z"
    assert (
        rebuilt_target["closure_reason"]
        == "Closed for traceability closed-state regression coverage."
    )


def test_traceability_index_sync_drops_active_acceptance_only_traces_without_live_state(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    trace_id = "trace.synthetic_acceptance_only"
    acceptance_root = repo_root / "core/control_plane/contracts/acceptance"
    evidence_root = repo_root / "core/control_plane/records/validation_evidence"

    acceptance_template = json.loads(
        next(acceptance_root.glob("*.json")).read_text(encoding="utf-8")
    )
    acceptance_template["id"] = "contract.acceptance.synthetic_acceptance_only"
    acceptance_template["trace_id"] = trace_id
    acceptance_template["title"] = "Synthetic Acceptance Only"
    acceptance_template["source_surface_path"] = (
        "plan/initiatives/synthetic_acceptance_only/initiative_brief.md"
    )
    (acceptance_root / "synthetic_acceptance_only.json").write_text(
        f"{json.dumps(acceptance_template, indent=2)}\n",
        encoding="utf-8",
    )

    evidence_template = json.loads(next(evidence_root.glob("*.json")).read_text(encoding="utf-8"))
    evidence_template["id"] = "evidence.synthetic_acceptance_only.validation"
    evidence_template["trace_id"] = trace_id
    evidence_template["title"] = "Synthetic Acceptance Only Validation"
    evidence_template["source_surface_paths"] = [
        "plan/initiatives/synthetic_acceptance_only/initiative_brief.md"
    ]
    evidence_template["source_acceptance_contract_ids"] = [
        "contract.acceptance.synthetic_acceptance_only"
    ]
    (evidence_root / "synthetic_acceptance_only.json").write_text(
        f"{json.dumps(evidence_template, indent=2)}\n",
        encoding="utf-8",
    )

    loader = ControlPlaneLoader(repo_root)

    rebuilt = TraceabilityIndexSyncService(loader).build_document()

    rebuilt_entries = rebuilt["entries"]
    assert isinstance(rebuilt_entries, list)
    assert all(entry["trace_id"] != trace_id for entry in rebuilt_entries)
