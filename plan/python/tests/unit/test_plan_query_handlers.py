from __future__ import annotations

import json
from types import SimpleNamespace

from watchtower_plan.cli import query_lookup_handlers, query_rendered_handlers

from tests.unit.route_query_handler_test_support import (
    active_task_summary,
    artifact_entry,
    initiative_entry,
    query_args,
    task_entry,
)


def test_query_tasks_prints_dependency_details(monkeypatch, capsys) -> None:
    blocker = task_entry(task_id="task.blocker.001", title="Blocker", task_status="completed")
    dependency = task_entry(task_id="task.depends.001", title="Dependency", task_status="completed")
    reverse = task_entry(task_id="task.reverse.001", title="Reverse", task_status="planned")

    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (task_entry(),)

        def reverse_dependencies_for(
            self,
            task_ids: tuple[str, ...],
        ) -> dict[str, tuple[SimpleNamespace, ...]]:
            assert task_ids == ("task.example.001",)
            return {"task.example.001": (reverse,)}

        def get(self, task_id: str) -> SimpleNamespace:
            if task_id == "task.blocker.001":
                return blocker
            return dependency

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_lookup_handlers, "TaskQueryService", FakeService)

    result = query_lookup_handlers._run_query_tasks(query_args(include_dependency_details=True))

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 task entry:" in captured.out
    assert "Blocked by: task.blocker.001" in captured.out
    assert "Reverse dependencies: task.reverse.001" in captured.out


def test_task_entry_payload_keeps_artifact_and_workflow_statuses_distinct() -> None:
    payload = query_lookup_handlers._task_entry_payload(
        task_entry(),
        service=SimpleNamespace(),
        reverse_dependencies={},
        include_dependency_details=False,
    )

    assert payload["status"] == "active"
    assert payload["task_status"] == "planned"


def test_query_tasks_skips_dependency_detail_work_when_not_requested(
    monkeypatch,
    capsys,
) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (task_entry(),)

        def reverse_dependencies_for(
            self,
            task_ids: tuple[str, ...],
        ) -> dict[str, tuple[SimpleNamespace, ...]]:
            raise AssertionError("reverse_dependencies_for should not be called")

        def get(self, task_id: str) -> SimpleNamespace:
            raise AssertionError("get should not be called without dependency details")

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_lookup_handlers, "TaskQueryService", FakeService)

    result = query_lookup_handlers._run_query_tasks(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 task entry:" in captured.out
    assert "Reverse dependencies:" not in captured.out


def test_query_tasks_prints_empty_message(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return ()

        def reverse_dependencies_for(
            self,
            task_ids: tuple[str, ...],
        ) -> dict[str, tuple[SimpleNamespace, ...]]:
            return {}

        def get(self, task_id: str) -> SimpleNamespace:
            raise AssertionError("get should not be called for empty results")

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_lookup_handlers, "TaskQueryService", FakeService)

    result = query_lookup_handlers._run_query_tasks(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No task entries matched the requested filters." in captured.out


def test_query_artifacts_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (artifact_entry(),)

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_lookup_handlers, "ArtifactQueryService", FakeService)

    result = query_lookup_handlers._run_query_artifacts(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 artifact entry:" in captured.out
    assert "initiative.example [initiative_state, ready_for_execution]" in captured.out
    assert "Source: initiative.example / initiative_package" in captured.out


def test_query_initiatives_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (initiative_entry(),)

    monkeypatch.setattr(query_rendered_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_rendered_handlers, "InitiativeQueryService", FakeService)
    monkeypatch.setattr(
        query_rendered_handlers,
        "serialize_initiative_entry",
        lambda entry, *, compact=False: (_ for _ in ()).throw(
            AssertionError("serialize_initiative_entry should not be called")
        ),
    )

    result = query_rendered_handlers._run_query_initiatives(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 initiative entry:" in captured.out
    assert "Owners: repository_maintainer" in captured.out
    assert "Task:" not in captured.out


def test_query_initiatives_prints_empty_message(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return ()

    monkeypatch.setattr(query_rendered_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_rendered_handlers, "InitiativeQueryService", FakeService)

    result = query_rendered_handlers._run_query_initiatives(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No active initiative entries matched the requested filters." in captured.out
    assert (
        "Pass --initiative-status completed|cancelled|superseded for history browsing."
        in captured.out
    )


def test_query_coordination_supports_json_defaults(monkeypatch, capsys) -> None:
    result_entry = initiative_entry()

    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> SimpleNamespace:
            return SimpleNamespace(
                index=SimpleNamespace(
                    coordination_mode="active_work",
                    summary="Summary.",
                    recommended_next_action="Start execution.",
                    recommended_surface_path="plan/tracking/task_tracking.md",
                    active_initiative_count=1,
                    blocked_task_count=0,
                    actionable_task_count=1,
                    recent_closed_initiatives=(),
                    actionable_tasks=(active_task_summary(),),
                ),
                entries=(result_entry,),
            )

    monkeypatch.setattr(query_rendered_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_rendered_handlers, "CoordinationQueryService", FakeService)

    result = query_rendered_handlers._run_query_coordination(query_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan query coordination"
    assert payload["default_initiative_status"] == "active"
    assert payload["actionable_tasks"][0]["task_id"] == "task.example.001"


def test_query_coordination_prints_recent_closeouts_when_no_active_entries(
    monkeypatch,
    capsys,
) -> None:
    recent_closeout = initiative_entry(
        trace_id="trace.closed",
        title="Closed Initiative",
        initiative_status="completed",
        closed_at="2026-03-10T23:59:59Z",
    )

    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> SimpleNamespace:
            return SimpleNamespace(
                index=SimpleNamespace(
                    coordination_mode="ready_for_bootstrap",
                    summary="No active initiatives.",
                    recommended_next_action="Bootstrap a new initiative.",
                    recommended_surface_path="plan/tracking/coordination_tracking.md",
                    active_initiative_count=0,
                    blocked_task_count=0,
                    actionable_task_count=0,
                    recent_closed_initiatives=(recent_closeout,),
                    actionable_tasks=(),
                ),
                entries=(),
            )

    monkeypatch.setattr(query_rendered_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_rendered_handlers, "CoordinationQueryService", FakeService)

    result = query_rendered_handlers._run_query_coordination(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Coordination mode: ready_for_bootstrap" in captured.out
    assert "Recent closeouts:" in captured.out
    assert "trace.closed [completed] 2026-03-10T23:59:59Z" in captured.out


def test_query_coordination_prints_active_entry_summary(monkeypatch, capsys) -> None:
    result_entry = initiative_entry()

    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> SimpleNamespace:
            return SimpleNamespace(
                index=SimpleNamespace(
                    coordination_mode="active_work",
                    summary="Summary.",
                    recommended_next_action="Start execution.",
                    recommended_surface_path="plan/tracking/task_tracking.md",
                    active_initiative_count=1,
                    blocked_task_count=0,
                    actionable_task_count=1,
                    recent_closed_initiatives=(),
                    actionable_tasks=(active_task_summary(),),
                ),
                entries=(result_entry,),
            )

    monkeypatch.setattr(query_rendered_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_rendered_handlers, "CoordinationQueryService", FakeService)
    monkeypatch.setattr(
        query_rendered_handlers,
        "serialize_initiative_entry",
        lambda entry, *, compact=False: (_ for _ in ()).throw(
            AssertionError("serialize_initiative_entry should not be called")
        ),
    )

    result = query_rendered_handlers._run_query_coordination(query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 initiative entry:" in captured.out
    assert "Task: task.example.001 [planned, high, actionable]" in captured.out
    assert "Open first: plan/tracking/task_tracking.md" in captured.out


def test_query_trace_reports_unknown_trace(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def get(self, trace_id: str) -> SimpleNamespace:
            raise KeyError(trace_id)

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_lookup_handlers, "TraceabilityQueryService", FakeService)

    result = query_lookup_handlers._run_query_trace(query_args(trace_id="trace.unknown"))

    captured = capsys.readouterr()
    assert result == 1
    assert "Unknown trace ID: trace.unknown" in captured.out


def test_query_trace_prints_human_summary(monkeypatch, capsys) -> None:
    trace_entry = SimpleNamespace(
        trace_id="trace.example",
        title="Example Trace",
        summary="Trace summary.",
        status="active",
        initiative_status="completed",
        updated_at="2026-03-10T23:59:59Z",
        closed_at="2026-03-10T23:59:59Z",
        closure_reason="Completed for tests.",
        superseded_by_trace_id="trace.next",
        source_surface_paths=(
            "plan/initiatives/example/initiative_brief.md",
            "plan/initiatives/example/design_record.md",
            "plan/initiatives/example/implementation_slice.md",
        ),
        task_ids=("task.example.001",),
        requirement_ids=("req.example.001",),
        acceptance_ids=("ac.example.001",),
        acceptance_contract_ids=("contract.acceptance.example",),
        validator_ids=("validator.trace.acceptance_reconciliation",),
        evidence_ids=("evidence.example",),
        related_paths=("plan/initiatives/example/initiative_brief.md",),
        tags=("traceability",),
        notes="Example notes.",
    )

    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def get(self, trace_id: str) -> SimpleNamespace:
            assert trace_id == "trace.example"
            return trace_entry

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_lookup_handlers, "TraceabilityQueryService", FakeService)

    result = query_lookup_handlers._run_query_trace(query_args(trace_id="trace.example"))

    captured = capsys.readouterr()
    assert result == 0
    assert "trace.example: Example Trace" in captured.out
    assert "Closure Reason: Completed for tests." in captured.out
    assert "Superseded By: trace.next" in captured.out
    assert "Acceptance Contracts: contract.acceptance.example" in captured.out
    assert "Evidence: evidence.example" in captured.out
