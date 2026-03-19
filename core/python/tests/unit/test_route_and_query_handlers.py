from __future__ import annotations

import argparse
import json
from types import SimpleNamespace

from watchtower_core.cli import (
    query_coordination_lookup_handlers,
    query_coordination_rendered_handlers,
    route_handlers,
)


def _route_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "request": "review code and commit",
        "task_type": None,
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _query_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "query": None,
        "project_slug": None,
        "project_id": None,
        "slug": None,
        "artifact_id": None,
        "artifact_family": None,
        "context_id": None,
        "source_context": None,
        "source_channel": None,
        "task_id": [],
        "trace_id": None,
        "initiative_id": None,
        "task_status": None,
        "priority": None,
        "owner": None,
        "task_kind": None,
        "blocked_only": False,
        "ready_for_execution": None,
        "lifecycle_stage": None,
        "review_status": None,
        "category": None,
        "severity": None,
        "status": None,
        "repository_role": None,
        "authoritative": None,
        "derived": None,
        "hidden": None,
        "blocking_only": False,
        "blocked_by": None,
        "depends_on": None,
        "limit": 20,
        "include_dependency_details": False,
        "initiative_status": None,
        "current_phase": None,
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _task_entry(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "task_id": "task.example.001",
        "trace_id": "trace.example",
        "title": "Example task",
        "summary": "Task summary.",
        "status": "active",
        "task_status": "planned",
        "task_kind": "feature",
        "priority": "high",
        "owner": "repository_maintainer",
        "doc_path": "plan/initiatives/example/.wt/tasks/example/task.json",
        "updated_at": "2026-03-10T23:59:59Z",
        "blocked_by": ("task.blocker.001",),
        "depends_on": ("task.depends.001",),
        "related_ids": (),
        "applies_to": (),
        "github_repository": None,
        "github_issue_number": None,
        "github_issue_node_id": None,
        "github_project_owner": None,
        "github_project_owner_type": None,
        "github_project_number": None,
        "github_project_item_id": None,
        "github_synced_at": None,
        "tags": (),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _active_task_summary(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "trace_id": "trace.example",
        "initiative_title": "Example Initiative",
        "task_id": "task.example.001",
        "title": "Example task",
        "task_status": "planned",
        "priority": "high",
        "owner": "repository_maintainer",
        "doc_path": "plan/initiatives/example/.wt/tasks/example/task.json",
        "is_actionable": True,
        "blocked_by": (),
        "depends_on": (),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _artifact_entry(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "artifact_id": "initiative.example",
        "artifact_family": "initiative_state",
        "path": "plan/initiatives/example/.wt/initiative.json",
        "pack": "pack.plan",
        "subdomain": "plan",
        "status": "ready_for_execution",
        "authoritative": True,
        "hidden": True,
        "derived": False,
        "created_at": "2026-03-10T23:59:59Z",
        "updated_at": "2026-03-10T23:59:59Z",
        "context_ids": ("initiative.example", "trace.example", "pack.plan"),
        "title": "Example Initiative",
        "summary": "Example initiative artifact.",
        "parent_artifact_id": None,
        "related_artifact_ids": (),
        "route_id": None,
        "rendered_view_path": "plan/initiatives/example/plan.md",
        "workflow_surface": None,
        "review_status": "approved",
        "source_context": "initiative.example",
        "source_channel": "initiative_package",
        "source_summary": "Example initiative artifact.",
        "source_url": None,
        "source_ref": None,
        "source_type": "initiative_state",
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _initiative_entry(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "initiative_id": "initiative.example",
        "trace_id": "trace.example",
        "slug": "example",
        "title": "Example Initiative",
        "summary": "Initiative summary.",
        "artifact_status": "active",
        "initiative_status": "active",
        "scope_type": "pack_wide",
        "project_id": None,
        "current_phase": "execution",
        "updated_at": "2026-03-10T23:59:59Z",
        "open_task_count": 1,
        "blocked_task_count": 0,
        "key_surface_path": "plan/initiatives/example/initiative_brief.md",
        "next_action": "Start execution.",
        "next_surface_path": "plan/initiatives/example/implementation_slice.md",
        "primary_owner": "repository_maintainer",
        "active_owners": ("repository_maintainer",),
        "active_task_ids": ("task.example.001",),
        "active_task_summaries": (_active_task_summary(),),
        "blocked_by_task_ids": (),
        "source_surface_paths": (
            "plan/initiatives/example/initiative_brief.md",
            "plan/initiatives/example/design_record.md",
            "plan/initiatives/example/implementation_slice.md",
        ),
        "task_ids": ("task.example.001",),
        "acceptance_ids": ("ac.example.001",),
        "acceptance_contract_ids": ("contract.acceptance.example",),
        "evidence_ids": ("evidence.example",),
        "closed_at": None,
        "closure_reason": None,
        "superseded_by_trace_id": None,
        "related_paths": ("plan/initiatives/example/initiative_brief.md",),
        "tags": ("traceability",),
        "notes": "Example notes.",
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)
def test_route_preview_prints_no_match_guidance(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(selected_routes=(), selected_workflows=(), warnings=())

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(_route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No route matched the request text strongly enough." in captured.out


def test_route_preview_supports_human_route_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def preview(self, *, request_text: str, task_type: str | None) -> SimpleNamespace:
            return SimpleNamespace(
                selected_routes=(
                    SimpleNamespace(
                        route_id="route.repository_review",
                        task_type="Repository Review",
                        score=0.9,
                        matched_keywords=("review",),
                        required_workflow_ids=("workflow.repository_review",),
                        required_workflow_paths=("core/workflows/modules/repository_review.md",),
                    ),
                ),
                selected_workflows=(
                    SimpleNamespace(
                        workflow_id="workflow.repository_review",
                        title="Repository Review",
                        doc_path="core/workflows/modules/repository_review.md",
                        phase_type="assessment",
                        task_family="review",
                    ),
                ),
                warnings=("Prefer a bounded scope.",),
            )

    monkeypatch.setattr(route_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(route_handlers, "RoutePreviewService", FakeService)

    result = route_handlers._run_route_preview(_route_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Selected routes:" in captured.out
    assert "workflow.repository_review" in captured.out
    assert "Warning: Prefer a bounded scope." in captured.out

def test_query_tasks_prints_dependency_details(monkeypatch, capsys) -> None:
    blocker = _task_entry(task_id="task.blocker.001", title="Blocker", task_status="completed")
    dependency = _task_entry(task_id="task.depends.001", title="Dependency", task_status="completed")
    reverse = _task_entry(task_id="task.reverse.001", title="Reverse", task_status="planned")

    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (_task_entry(),)

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

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_coordination_lookup_handlers, "TaskQueryService", FakeService)

    result = query_coordination_lookup_handlers._run_query_tasks(
        _query_args(include_dependency_details=True)
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Found 1 task entry:" in captured.out
    assert "Blocked by: task.blocker.001" in captured.out
    assert "Reverse dependencies: task.reverse.001" in captured.out


def test_task_entry_payload_keeps_artifact_and_workflow_statuses_distinct() -> None:
    payload = query_coordination_lookup_handlers._task_entry_payload(
        _task_entry(),
        service=SimpleNamespace(),
        reverse_dependencies={},
        include_dependency_details=False,
    )

    assert payload["status"] == "active"
    assert payload["task_status"] == "planned"


def test_query_tasks_skips_dependency_detail_work_when_not_requested(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (_task_entry(),)

        def reverse_dependencies_for(
            self,
            task_ids: tuple[str, ...],
        ) -> dict[str, tuple[SimpleNamespace, ...]]:
            raise AssertionError("reverse_dependencies_for should not be called")

        def get(self, task_id: str) -> SimpleNamespace:
            raise AssertionError("get should not be called without dependency details")

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_coordination_lookup_handlers, "TaskQueryService", FakeService)

    result = query_coordination_lookup_handlers._run_query_tasks(_query_args())

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

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(query_coordination_lookup_handlers, "TaskQueryService", FakeService)

    result = query_coordination_lookup_handlers._run_query_tasks(_query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No task entries matched the requested filters." in captured.out


def test_query_artifacts_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def search(self, params: object) -> tuple[SimpleNamespace, ...]:
            return (_artifact_entry(),)

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_coordination_lookup_handlers,
        "ArtifactQueryService",
        FakeService,
    )

    result = query_coordination_lookup_handlers._run_query_artifacts(_query_args())

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
            return (_initiative_entry(),)

    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "ControlPlaneLoader",
        lambda: object(),
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "InitiativeQueryService",
        FakeService,
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "serialize_initiative_entry",
        lambda entry, *, compact=False: (_ for _ in ()).throw(
            AssertionError("serialize_initiative_entry should not be called")
        ),
    )

    result = query_coordination_rendered_handlers._run_query_initiatives(_query_args())

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

    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "ControlPlaneLoader",
        lambda: object(),
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "InitiativeQueryService",
        FakeService,
    )

    result = query_coordination_rendered_handlers._run_query_initiatives(_query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No active initiative entries matched the requested filters." in captured.out
    assert (
        "Pass --initiative-status completed|cancelled|superseded for history browsing."
        in captured.out
    )


def test_query_coordination_supports_json_defaults(monkeypatch, capsys) -> None:
    result_entry = _initiative_entry()

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
                    actionable_tasks=(_active_task_summary(),),
                ),
                entries=(result_entry,),
            )

    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "ControlPlaneLoader",
        lambda: object(),
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "CoordinationQueryService",
        FakeService,
    )

    result = query_coordination_rendered_handlers._run_query_coordination(
        _query_args(format="json")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core query coordination"
    assert payload["default_initiative_status"] == "active"
    assert payload["actionable_tasks"][0]["task_id"] == "task.example.001"


def test_query_coordination_prints_recent_closeouts_when_no_active_entries(
    monkeypatch,
    capsys,
) -> None:
    recent_closeout = _initiative_entry(
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

    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "ControlPlaneLoader",
        lambda: object(),
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "CoordinationQueryService",
        FakeService,
    )

    result = query_coordination_rendered_handlers._run_query_coordination(_query_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Coordination mode: ready_for_bootstrap" in captured.out
    assert "Recent closeouts:" in captured.out
    assert "trace.closed [completed] 2026-03-10T23:59:59Z" in captured.out


def test_query_coordination_prints_active_entry_summary(monkeypatch, capsys) -> None:
    result_entry = _initiative_entry()

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
                    actionable_tasks=(_active_task_summary(),),
                ),
                entries=(result_entry,),
            )

    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "ControlPlaneLoader",
        lambda: object(),
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "CoordinationQueryService",
        FakeService,
    )
    monkeypatch.setattr(
        query_coordination_rendered_handlers,
        "serialize_initiative_entry",
        lambda entry, *, compact=False: (_ for _ in ()).throw(
            AssertionError("serialize_initiative_entry should not be called")
        ),
    )

    result = query_coordination_rendered_handlers._run_query_coordination(_query_args())

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

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_coordination_lookup_handlers,
        "TraceabilityQueryService",
        FakeService,
    )

    result = query_coordination_lookup_handlers._run_query_trace(
        _query_args(trace_id="trace.unknown")
    )

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

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_coordination_lookup_handlers,
        "TraceabilityQueryService",
        FakeService,
    )

    result = query_coordination_lookup_handlers._run_query_trace(
        _query_args(trace_id="trace.example")
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "trace.example: Example Trace" in captured.out
    assert "Closure Reason: Completed for tests." in captured.out
    assert "Superseded By: trace.next" in captured.out
    assert "Acceptance Contracts: contract.acceptance.example" in captured.out
    assert "Evidence: evidence.example" in captured.out


def test_query_project_context_prints_human_summary(monkeypatch, capsys) -> None:
    project_context = SimpleNamespace(
        pack_context=SimpleNamespace(
            pack_settings=SimpleNamespace(
                pack_id="pack.plan",
            ),
            pack_settings_path="plan/.wt/manifests/pack_settings.json",
        ),
        project_id="project.watchtower",
        slug="watchtower",
        title="WatchTower",
        summary="Operator-facing target.",
        status="active",
        project_root="plan/projects/watchtower",
        initiative_root="plan/projects/watchtower/initiatives",
        repository_links=(
            SimpleNamespace(
                repository_id="repository.watchtower.planning",
                repository_role="planning",
                repository_locator="/home/j/WatchTowerPlan",
                repository_kind="planning",
                owner="repository_maintainer",
                access="local_write",
                active=True,
            ),
        ),
    )

    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_coordination_lookup_handlers,
        "load_project_context",
        lambda loader, project_slug: project_context,
    )

    result = query_coordination_lookup_handlers._run_query_project_context(
        _query_args(project_slug="watchtower")
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "project.watchtower: WatchTower [active]" in captured.out
    assert "Pack Context: pack.plan via plan/.wt/manifests/pack_settings.json" in captured.out
    assert "Initiative Root: plan/projects/watchtower/initiatives" in captured.out
    assert "- planning: /home/j/WatchTowerPlan [planning, active]" in captured.out


def test_query_project_context_supports_json_errors(monkeypatch, capsys) -> None:
    monkeypatch.setattr(query_coordination_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_coordination_lookup_handlers,
        "load_project_context",
        lambda loader, project_slug: (_ for _ in ()).throw(
            ValueError("Project root is missing: plan/projects/watchtower.")
        ),
    )

    result = query_coordination_lookup_handlers._run_query_project_context(
        _query_args(project_slug="watchtower", format="json")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core query project-context",
        "message": "Project root is missing: plan/projects/watchtower.",
        "status": "error",
    }
