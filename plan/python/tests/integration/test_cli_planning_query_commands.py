from __future__ import annotations

from watchtower_plan.cli import query_lookup_handlers, query_rendered_handlers
from watchtower_plan.query.coordination import CoordinationQueryResult
from watchtower_plan.workspace.service import PlanReadinessIndexEntry, PlanTaskIndexEntry

from tests.cli_command_helpers import run_json_command
from watchtower_core.control_plane.models import (
    CoordinationIndex,
    CoordinationRecentInitiativeSummary,
    CoordinationTaskSummary,
    InitiativeActiveTaskSummary,
    InitiativeIndexEntry,
)

ACTIVE_TRACE_ID = "trace.example_live_query_active"
ACTIVE_INITIATIVE_ID = "initiative.example_live_query_active"
ACTIVE_TASK_ID = "task.example_live_query_active.seed_live_query_task_details"
DEPENDENCY_TASK_ID = "task.example_live_query_active.review_live_query_dependency_details"
COMPLETED_TRACE_ID = "trace.example_live_query_completed"
DISCREPANCY_TRACE_ID = "trace.plan_core_documentation_template_authority_foundation"
WATCHTOWER_PROJECT_ID = "project.watchtower"

_ACTIVE_TASK_ENTRY = PlanTaskIndexEntry(
    task_id=ACTIVE_TASK_ID,
    initiative_id=ACTIVE_INITIATIVE_ID,
    project_id=None,
    trace_id=ACTIVE_TRACE_ID,
    initiative_title="Example Live Query Active",
    title="Seed live query task details",
    summary="Provides one upstream dependency target for query coverage.",
    status="active",
    task_status="planned",
    task_kind="feature",
    priority="high",
    owner="repository_maintainer",
    doc_path="plan/initiatives/example_live_query_active/.wt/tasks/seed_live_query_task_details/task.json",
    updated_at="2026-03-19T10:40:00Z",
)
_DEPENDENCY_TASK_ENTRY = PlanTaskIndexEntry(
    task_id=DEPENDENCY_TASK_ID,
    initiative_id=ACTIVE_INITIATIVE_ID,
    project_id=None,
    trace_id=ACTIVE_TRACE_ID,
    initiative_title="Example Live Query Active",
    title="Review live query dependency details",
    summary="Provides dependency detail coverage for task queries.",
    status="active",
    task_status="blocked",
    task_kind="feature",
    priority="high",
    owner="repository_maintainer",
    doc_path=(
        "plan/initiatives/example_live_query_active/.wt/tasks/"
        "review_live_query_dependency_details/task.json"
    ),
    updated_at="2026-03-19T10:45:00Z",
    blocked_by=(ACTIVE_TASK_ID,),
    depends_on=(ACTIVE_TASK_ID,),
)

_ACTIVE_INITIATIVE_ENTRY = InitiativeIndexEntry(
    trace_id=ACTIVE_TRACE_ID,
    title="Example Live Query Active",
    summary="Fixture initiative for live query command coverage.",
    artifact_status="active",
    initiative_status="active",
    current_phase="in_progress",
    updated_at="2026-03-19T10:45:00Z",
    open_task_count=2,
    blocked_task_count=1,
    key_surface_path="plan/initiatives/example_live_query_active/plan.md",
    next_action="Review the blocked task dependency details.",
    next_surface_path="plan/initiatives/example_live_query_active/.wt/tasks/review_live_query_dependency_details/task.json",
    initiative_id=ACTIVE_INITIATIVE_ID,
    slug="example_live_query_active",
    scope_type="pack_wide",
    primary_owner="repository_maintainer",
    active_owners=("repository_maintainer",),
    active_task_ids=(ACTIVE_TASK_ID, DEPENDENCY_TASK_ID),
    active_task_summaries=(
        InitiativeActiveTaskSummary(
            task_id=ACTIVE_TASK_ID,
            title="Seed live query task details",
            task_status="planned",
            priority="high",
            owner="repository_maintainer",
            doc_path=_ACTIVE_TASK_ENTRY.doc_path,
            is_actionable=True,
        ),
        InitiativeActiveTaskSummary(
            task_id=DEPENDENCY_TASK_ID,
            title="Review live query dependency details",
            task_status="blocked",
            priority="high",
            owner="repository_maintainer",
            doc_path=_DEPENDENCY_TASK_ENTRY.doc_path,
            is_actionable=False,
            blocked_by=(ACTIVE_TASK_ID,),
            depends_on=(ACTIVE_TASK_ID,),
        ),
    ),
    blocked_by_task_ids=(ACTIVE_TASK_ID,),
    task_ids=(ACTIVE_TASK_ID, DEPENDENCY_TASK_ID),
)
_COMPLETED_INITIATIVE_ENTRY = InitiativeIndexEntry(
    trace_id=COMPLETED_TRACE_ID,
    title="Example Live Query Completed",
    summary="Fixture initiative for completed-history query coverage.",
    artifact_status="active",
    initiative_status="completed",
    current_phase="closed",
    updated_at="2026-03-19T11:00:00Z",
    open_task_count=0,
    blocked_task_count=0,
    key_surface_path="plan/initiatives/example_live_query_completed/plan.md",
    next_action="Review the closeout recap if historical context is needed.",
    next_surface_path=(
        "plan/initiatives/example_live_query_completed/.wt/closeout/"
        "closeout_recap.bootstrap.json"
    ),
    initiative_id="initiative.example_live_query_completed",
    slug="example_live_query_completed",
    scope_type="pack_wide",
    primary_owner="repository_maintainer",
    active_owners=("repository_maintainer",),
    task_ids=("task.example_live_query_completed.seed_closed_query_task",),
    closed_at="2026-03-19T11:00:00Z",
    closure_reason="Fixture completed initiative for historical query coverage.",
)
_READINESS_ENTRY = PlanReadinessIndexEntry(
    initiative_id=ACTIVE_INITIATIVE_ID,
    project_id=None,
    trace_id=ACTIVE_TRACE_ID,
    title="Example Live Query Active",
    initiative_root="plan/initiatives/example_live_query_active",
    lifecycle_stage="ready_for_execution",
    review_status="approved",
    capture_complete=True,
    machine_valid=True,
    approval_status="approved",
    ready_for_execution=True,
    blocking_reasons=(),
    updated_at="2026-03-19T10:45:00Z",
)
_ACTIVE_COORDINATION_INDEX = CoordinationIndex(
    schema_id="urn:watchtower:schema:coordination-index:v1",
    artifact_id="index.coordination",
    title="Coordination Index",
    status="active",
    updated_at="2026-03-19T10:45:00Z",
    coordination_mode="active_work",
    summary="One active initiative remains in progress.",
    recommended_next_action="Open the initiative task document and unblock execution.",
    recommended_surface_path=_ACTIVE_INITIATIVE_ENTRY.next_surface_path,
    active_initiative_count=1,
    blocked_task_count=1,
    actionable_task_count=1,
    entries=(_ACTIVE_INITIATIVE_ENTRY,),
    actionable_tasks=(
        CoordinationTaskSummary(
            trace_id=ACTIVE_TRACE_ID,
            initiative_title=_ACTIVE_INITIATIVE_ENTRY.title,
            task_id=ACTIVE_TASK_ID,
            title=_ACTIVE_TASK_ENTRY.title,
            task_status=_ACTIVE_TASK_ENTRY.task_status,
            priority=_ACTIVE_TASK_ENTRY.priority,
            owner=_ACTIVE_TASK_ENTRY.owner,
            doc_path=_ACTIVE_TASK_ENTRY.doc_path,
            is_actionable=True,
        ),
    ),
    recent_closed_initiatives=(
        CoordinationRecentInitiativeSummary(
            trace_id=COMPLETED_TRACE_ID,
            title=_COMPLETED_INITIATIVE_ENTRY.title,
            initiative_status=_COMPLETED_INITIATIVE_ENTRY.initiative_status,
            closed_at=_COMPLETED_INITIATIVE_ENTRY.closed_at or "2026-03-19T11:00:00Z",
            key_surface_path=_COMPLETED_INITIATIVE_ENTRY.key_surface_path,
            closure_reason=_COMPLETED_INITIATIVE_ENTRY.closure_reason,
        ),
    ),
)
_HISTORY_COORDINATION_INDEX = CoordinationIndex(
    schema_id="urn:watchtower:schema:coordination-index:v1",
    artifact_id="index.coordination",
    title="Coordination Index",
    status="active",
    updated_at="2026-03-19T11:00:00Z",
    coordination_mode="ready_for_bootstrap",
    summary="No active initiatives remain after the closeout fixture.",
    recommended_next_action="Bootstrap the next initiative when new work is ready.",
    recommended_surface_path="plan/plan_overview.md",
    active_initiative_count=0,
    blocked_task_count=0,
    actionable_task_count=0,
    entries=(),
    actionable_tasks=(),
    recent_closed_initiatives=_ACTIVE_COORDINATION_INDEX.recent_closed_initiatives,
)


class _FakeTaskQueryService:
    def __init__(self, _loader) -> None:
        self._entries = (_ACTIVE_TASK_ENTRY, _DEPENDENCY_TASK_ENTRY)

    def search(self, params) -> tuple[PlanTaskIndexEntry, ...]:
        entries = self._entries
        task_ids = {task_id.casefold() for task_id in getattr(params, "task_ids", ())}
        if task_ids:
            entries = tuple(
                entry for entry in entries if entry.task_id.casefold() in task_ids
            )
        trace_id = getattr(params, "trace_id", None)
        if trace_id is not None:
            entries = tuple(
                entry for entry in entries if entry.trace_id.casefold() == trace_id.casefold()
            )
        return entries

    def get(self, task_id: str) -> PlanTaskIndexEntry:
        for entry in self._entries:
            if entry.task_id == task_id:
                return entry
        raise KeyError(task_id)

    def reverse_dependencies_for(
        self,
        task_ids: tuple[str, ...],
    ) -> dict[str, tuple[PlanTaskIndexEntry, ...]]:
        reverse_map = {
            ACTIVE_TASK_ID: (_DEPENDENCY_TASK_ENTRY,),
            DEPENDENCY_TASK_ID: (),
        }
        return {task_id: reverse_map.get(task_id, ()) for task_id in task_ids}


class _FakeReadinessQueryService:
    def __init__(self, _loader) -> None:
        pass

    def search(self, params) -> tuple[PlanReadinessIndexEntry, ...]:
        if params.initiative_id is not None and params.initiative_id != ACTIVE_INITIATIVE_ID:
            return ()
        if params.trace_id is not None and params.trace_id != ACTIVE_TRACE_ID:
            return ()
        return (_READINESS_ENTRY,)


class _FakeInitiativeQueryService:
    def __init__(self, _loader) -> None:
        self._entries = (_ACTIVE_INITIATIVE_ENTRY, _COMPLETED_INITIATIVE_ENTRY)

    def search(self, params) -> tuple[InitiativeIndexEntry, ...]:
        entries = self._entries
        trace_id = getattr(params, "trace_id", None)
        if trace_id is not None:
            entries = tuple(entry for entry in entries if entry.trace_id == trace_id)
        initiative_status = getattr(params, "initiative_status", None)
        if initiative_status is not None:
            entries = tuple(
                entry
                for entry in entries
                if entry.initiative_status.casefold() == initiative_status.casefold()
            )
        current_phase = getattr(params, "current_phase", None)
        if current_phase is not None:
            entries = tuple(
                entry
                for entry in entries
                if entry.current_phase.casefold() == current_phase.casefold()
            )
        return entries


class _FakeCoordinationQueryService:
    def __init__(self, _loader) -> None:
        pass

    def search(self, params) -> CoordinationQueryResult:
        initiative_status = getattr(params, "initiative_status", None) or "active"
        if initiative_status.casefold() != "active":
            entries = (_COMPLETED_INITIATIVE_ENTRY,)
            if getattr(params, "trace_id", None) == COMPLETED_TRACE_ID:
                return CoordinationQueryResult(
                    index=_HISTORY_COORDINATION_INDEX,
                    entries=entries,
                )
            if getattr(params, "trace_id", None) is not None:
                return CoordinationQueryResult(
                    index=_HISTORY_COORDINATION_INDEX,
                    entries=(),
                )
            return CoordinationQueryResult(index=_HISTORY_COORDINATION_INDEX, entries=entries)

        entries = (_ACTIVE_INITIATIVE_ENTRY,)
        if getattr(params, "trace_id", None) is not None and params.trace_id != ACTIVE_TRACE_ID:
            entries = ()
        return CoordinationQueryResult(index=_ACTIVE_COORDINATION_INDEX, entries=entries)


def _patch_plan_query_services(monkeypatch) -> None:
    monkeypatch.setattr(
        query_lookup_handlers,
        "TaskQueryService",
        _FakeTaskQueryService,
    )
    monkeypatch.setattr(
        query_lookup_handlers,
        "ReadinessQueryService",
        _FakeReadinessQueryService,
    )
    monkeypatch.setattr(
        query_rendered_handlers,
        "InitiativeQueryService",
        _FakeInitiativeQueryService,
    )
    monkeypatch.setattr(
        query_rendered_handlers,
        "CoordinationQueryService",
        _FakeCoordinationQueryService,
    )


def test_query_acceptance_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "acceptance",
            "--trace-id",
            "trace.governed_acceptance_example",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query acceptance"
    assert payload["status"] == "ok"
    assert any(
        entry["contract_id"] == "contract.acceptance.governed_acceptance_example"
        for entry in payload["results"]
    )


def test_query_evidence_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "query",
            "evidence",
            "--trace-id",
            "trace.governed_acceptance_example",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core query evidence"
    assert payload["status"] == "ok"
    assert any(
        entry["evidence_id"] == "evidence.governed_acceptance_example.validation_baseline"
        for entry in payload["results"]
    )


def test_query_tasks_supports_json_output(monkeypatch, capsys) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "tasks", "--trace-id", ACTIVE_TRACE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query tasks"
    assert payload["status"] == "ok"
    entry = next(entry for entry in payload["results"] if entry["task_id"] == ACTIVE_TASK_ID)
    assert entry["status"] == "active"
    assert entry["task_status"] in {
        "planned",
        "ready",
        "in_progress",
        "in_review",
        "blocked",
        "completed",
        "cancelled",
    }
    assert entry["task_status"] != "active"
    assert all(entry["trace_id"] == ACTIVE_TRACE_ID for entry in payload["results"])


def test_query_tasks_supports_dependency_details_json_output(monkeypatch, capsys) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "query",
            "tasks",
            "--task-id",
            DEPENDENCY_TASK_ID,
            "--include-dependency-details",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query tasks"
    entry = payload["results"][0]
    assert entry["task_id"] == DEPENDENCY_TASK_ID
    assert "blocked_by_details" in entry
    assert "depends_on_details" in entry
    assert "reverse_dependency_details" in entry


def test_query_initiatives_supports_json_output(monkeypatch, capsys) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "initiatives", "--trace-id", ACTIVE_TRACE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query initiatives"
    assert payload["status"] == "ok"
    assert "default_initiative_status" not in payload
    assert any(entry["trace_id"] == ACTIVE_TRACE_ID for entry in payload["results"])


def test_query_coordination_defaults_to_active_status(monkeypatch, capsys) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(capsys, ["plan", "query", "coordination"])

    assert result == 0
    assert payload["command"] == "watchtower-core plan query coordination"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"
    assert payload["coordination_mode"] in {
        "active_work",
        "blocked_work",
        "ready_for_bootstrap",
    }
    assert payload["recommended_next_action"]
    assert payload["recommended_surface_path"]
    assert "actionable_tasks" in payload
    assert "recent_closed_initiatives" in payload
    assert any(entry["trace_id"] == ACTIVE_TRACE_ID for entry in payload["results"])


def test_query_coordination_supports_explicit_historical_lookup(
    monkeypatch,
    capsys,
) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "query",
            "coordination",
            "--initiative-status",
            "completed",
            "--trace-id",
            COMPLETED_TRACE_ID,
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query coordination"
    assert payload["status"] == "ok"
    matched = next(entry for entry in payload["results"] if entry["trace_id"] == COMPLETED_TRACE_ID)
    assert matched["artifact_status"] == "active"
    assert matched["initiative_status"] == "completed"
    assert "status" not in matched


def test_query_readiness_supports_json_output(monkeypatch, capsys) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "readiness", "--initiative-id", ACTIVE_INITIATIVE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query readiness"
    assert payload["status"] == "ok"
    assert any(entry["initiative_id"] == ACTIVE_INITIATIVE_ID for entry in payload["results"])


def test_query_artifacts_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "artifacts", "--artifact-family", "artifact_index"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query artifacts"
    assert payload["status"] == "ok"
    assert any(entry["artifact_id"] == "index.artifacts" for entry in payload["results"])


def test_query_discrepancies_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "discrepancies", "--trace-id", DISCREPANCY_TRACE_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query discrepancies"
    assert payload["status"] == "ok"
    assert payload["result_count"] >= 0
    if payload["results"]:
        assert all(entry["trace_id"] == DISCREPANCY_TRACE_ID for entry in payload["results"])


def test_query_projects_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "projects", "--project-id", WATCHTOWER_PROJECT_ID],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query projects"
    assert payload["status"] == "ok"
    assert payload["results"][0]["project_id"] == WATCHTOWER_PROJECT_ID


def test_query_project_context_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        ["plan", "query", "project-context", "--project-slug", "watchtower"],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query project-context"
    assert payload["status"] == "ok"
    assert payload["result"]["project_id"] == "project.watchtower"
    assert payload["result"]["pack_context"]["pack_id"] == "pack.plan"
    assert payload["result"]["initiative_root"] == "plan/projects/watchtower/initiatives"
    assert len(payload["result"]["repository_links"]) >= 1


def test_query_initiatives_uses_explicit_artifact_status_field(monkeypatch, capsys) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "query",
            "initiatives",
            "--trace-id",
            COMPLETED_TRACE_ID,
            "--initiative-status",
            "completed",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query initiatives"
    entry = next(item for item in payload["results"] if item["trace_id"] == COMPLETED_TRACE_ID)
    assert entry["artifact_status"] == "active"
    assert entry["initiative_status"] == "completed"
    assert "status" not in entry


def test_query_initiatives_defaults_to_active_status_when_filterless(
    monkeypatch,
    capsys,
) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(capsys, ["plan", "query", "initiatives"])

    assert result == 0
    assert payload["command"] == "watchtower-core plan query initiatives"
    assert payload["status"] == "ok"
    assert payload["default_initiative_status"] == "active"
    assert payload["result_count"] >= 1
    assert all(entry["initiative_status"] == "active" for entry in payload["results"])


def test_query_initiatives_supports_closed_current_phase_history_lookup(
    monkeypatch,
    capsys,
) -> None:
    _patch_plan_query_services(monkeypatch)
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "query",
            "initiatives",
            "--initiative-status",
            "completed",
            "--current-phase",
            "closed",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query initiatives"
    assert payload["result_count"] > 0
    assert any(entry["trace_id"] == COMPLETED_TRACE_ID for entry in payload["results"])
    assert all(entry["current_phase"] == "closed" for entry in payload["results"])


def test_query_authority_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "query",
            "authority",
            "--question-id",
            "authority.planning.deep_trace_context",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query authority"
    assert payload["status"] == "ok"
    assert payload["results"][0]["question_id"] == "authority.planning.deep_trace_context"
    assert payload["results"][0]["artifact_kind"] == "traceability_index"
    assert payload["results"][0]["preferred_command"] == "watchtower-core plan query trace"


def test_query_trace_supports_json_output(capsys) -> None:
    result, payload = run_json_command(
        capsys,
        [
            "plan",
            "query",
            "trace",
            "--trace-id",
            "trace.governed_acceptance_example",
        ],
    )

    assert result == 0
    assert payload["command"] == "watchtower-core plan query trace"
    assert payload["status"] == "ok"
    assert payload["result"]["trace_id"] == "trace.governed_acceptance_example"
