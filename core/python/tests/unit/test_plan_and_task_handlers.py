from __future__ import annotations

import argparse
import json
from types import SimpleNamespace

from watchtower_plan.cli import handlers as plan_handlers
from watchtower_plan.cli import tasks as task_handlers


def _plan_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "trace_id": "trace.plan_example",
        "initiative_slug": "plan_example",
        "project_slug": None,
        "actor_id": "actor.repository_maintainer",
        "title": "Plan Example",
        "summary": "Plan summary.",
        "owner": "repository_maintainer",
        "updated_at": "2026-03-10T23:59:59Z",
        "write": False,
        "include_decision": False,
        "task_id": None,
        "task_owner": None,
        "task_kind": "governance",
        "task_priority": "medium",
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _task_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "task_id": "task.example.001",
        "trace_id": "trace.example",
        "clear_trace_id": False,
        "title": "Example task",
        "summary": "Task summary.",
        "task_kind": "feature",
        "priority": "high",
        "owner": "repository_maintainer",
        "task_status": "planned",
        "scope": ["Do the work."],
        "done_when": ["It is done."],
        "applies_to": [],
        "clear_applies_to": False,
        "related_id": [],
        "clear_related_ids": False,
        "depends_on": [],
        "clear_depends_on": False,
        "blocked_by": [],
        "clear_blocked_by": False,
        "file_stem": None,
        "updated_at": "2026-03-10T23:59:59Z",
        "next_owner": None,
        "write": False,
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_plan_bootstrap_supports_json_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def bootstrap_packwide(self, params: object, *, write: bool) -> SimpleNamespace:
            assert write is False
            return SimpleNamespace(
                initiative_id="initiative.plan_example",
                trace_id="trace.plan_example",
                initiative_root="plan/initiatives/plan_example",
                lifecycle_stage="capture_incomplete",
                review_status="pending",
                ready_for_execution=False,
                validation_passed=False,
                wrote=False,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "InitiativePackageService", FakeService)

    result = plan_handlers._run_plan_bootstrap(_plan_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan bootstrap"
    assert payload["initiative_id"] == "initiative.plan_example"
    assert payload["initiative_root"] == "plan/initiatives/plan_example"
    assert payload["lifecycle_stage"] == "capture_incomplete"
    assert payload["ready_for_execution"] is False


def test_plan_bootstrap_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def bootstrap_packwide(self, params: object, *, write: bool) -> SimpleNamespace:
            assert write is True
            return SimpleNamespace(
                initiative_id="initiative.plan_example",
                trace_id="trace.plan_example",
                initiative_root="plan/initiatives/plan_example",
                lifecycle_stage="ready_for_review",
                review_status="pending",
                ready_for_execution=False,
                validation_passed=True,
                wrote=True,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "InitiativePackageService", FakeService)

    result = plan_handlers._run_plan_bootstrap(_plan_args(write=True))

    captured = capsys.readouterr()
    assert result == 0
    assert "Bootstrapped live initiative package trace.plan_example." in captured.out
    assert "Initiative Root: plan/initiatives/plan_example" in captured.out
    assert "Lifecycle Stage: ready_for_review" in captured.out
    assert "Initiative state and derived plan surfaces were updated." in captured.out


def test_plan_confirm_inputs_supports_json_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def confirm_authored_inputs(
            self,
            initiative_slug: str,
            actor_id: str,
            *,
            write: bool,
        ) -> SimpleNamespace:
            assert initiative_slug == "plan_example"
            assert actor_id == "actor.repository_maintainer"
            assert write is False
            return SimpleNamespace(
                initiative_id="initiative.plan_example",
                trace_id="trace.plan_example",
                initiative_root="plan/initiatives/plan_example",
                lifecycle_stage="ready_for_review",
                review_status="pending",
                ready_for_execution=False,
                validation_passed=True,
                wrote=False,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "InitiativePackageService", FakeService)

    result = plan_handlers._run_plan_confirm_inputs(_plan_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan confirm-inputs"
    assert payload["initiative_id"] == "initiative.plan_example"
    assert payload["trace_id"] == "trace.plan_example"
    assert payload["ready_for_execution"] is False


def test_plan_approve_uses_project_scoped_service_and_prints_summary(
    monkeypatch,
    capsys,
) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def approve_project_scoped(
            self,
            project_slug: str,
            initiative_slug: str,
            actor_id: str,
            *,
            write: bool,
        ) -> SimpleNamespace:
            assert project_slug == "watchtower"
            assert initiative_slug == "example_project_initiative"
            assert actor_id == "actor.repository_maintainer"
            assert write is True
            return SimpleNamespace(
                initiative_id="initiative.example_project_initiative",
                trace_id="trace.example_project_initiative",
                initiative_root="plan/projects/watchtower/initiatives/example_project_initiative",
                lifecycle_stage="ready_for_execution",
                review_status="approved",
                ready_for_execution=True,
                validation_passed=True,
                wrote=True,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "InitiativePackageService", FakeService)

    result = plan_handlers._run_plan_approve(
        _plan_args(
            initiative_slug="example_project_initiative",
            project_slug="watchtower",
            write=True,
        )
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Approved live initiative trace.example_project_initiative." in captured.out
    assert "Lifecycle Stage: ready_for_execution" in captured.out
    assert "Ready For Execution: True" in captured.out


def test_task_create_prints_dry_run_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def create(self, params: object, *, write: bool) -> SimpleNamespace:
            return SimpleNamespace(
                task_id="task.example.001",
                title="Example task",
                summary="Task summary.",
                trace_id="trace.example",
                task_status="planned",
                task_kind="feature",
                priority="high",
                owner="repository_maintainer",
                updated_at="2026-03-10T23:59:59Z",
                doc_path="plan/initiatives/example/.wt/tasks/example/task.json",
                previous_doc_path=None,
                moved=False,
                changed=True,
                wrote=False,
                coordination_refreshed=False,
                closeout_recommended=False,
            )

    monkeypatch.setattr(task_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(task_handlers, "TaskLifecycleService", FakeService)

    result = task_handlers._run_task_create(_task_args())

    captured = capsys.readouterr()
    assert result == 0
    assert (
        "Prepared task task.example.001 at plan/initiatives/example/.wt/tasks/example/task.json."
        in captured.out
    )
    assert (
        "Dry-run only. Use --write to persist the task change and refresh coordination."
        in captured.out
    )


def test_task_transition_prints_move_and_closeout_guidance(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def transition(self, params: object, *, write: bool) -> SimpleNamespace:
            return SimpleNamespace(
                task_id="task.example.001",
                title="Example task",
                summary="Task summary.",
                trace_id="trace.example",
                task_status="completed",
                task_kind="feature",
                priority="high",
                owner="repository_maintainer",
                updated_at="2026-03-10T23:59:59Z",
                doc_path="plan/initiatives/example/.wt/tasks/example/task.json",
                previous_doc_path=None,
                moved=False,
                changed=True,
                wrote=True,
                coordination_refreshed=True,
                closeout_recommended=True,
            )

    monkeypatch.setattr(task_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(task_handlers, "TaskLifecycleService", FakeService)

    result = task_handlers._run_task_transition(_task_args(task_status="completed", write=True))

    captured = capsys.readouterr()
    assert result == 0
    assert "Closeout Recommended: trace.example" in captured.out
    assert "Coordination surfaces were refreshed." in captured.out


def test_task_update_prints_no_change_message(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def update(self, params: object, *, write: bool) -> SimpleNamespace:
            return SimpleNamespace(
                task_id="task.example.001",
                title="Example task",
                summary="Task summary.",
                trace_id="trace.example",
                task_status="planned",
                task_kind="feature",
                priority="high",
                owner="repository_maintainer",
                updated_at="2026-03-10T23:59:59Z",
                doc_path="plan/initiatives/example/.wt/tasks/example/task.json",
                previous_doc_path=None,
                moved=False,
                changed=False,
                wrote=False,
                coordination_refreshed=False,
                closeout_recommended=False,
            )

    monkeypatch.setattr(task_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(task_handlers, "TaskLifecycleService", FakeService)

    result = task_handlers._run_task_update(_task_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "No task changes detected for task.example.001." in captured.out


def test_task_transition_supports_json_error_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def transition(self, params: object, *, write: bool) -> SimpleNamespace:
            raise ValueError("unknown task")

    monkeypatch.setattr(task_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(task_handlers, "TaskLifecycleService", FakeService)

    result = task_handlers._run_task_transition(
        _task_args(task_status="completed", format="json")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core plan task transition",
        "message": "unknown task",
        "status": "error",
    }


def test_task_create_reports_errors(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def create(self, params: object, *, write: bool) -> SimpleNamespace:
            raise ValueError("duplicate task")

    monkeypatch.setattr(task_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(task_handlers, "TaskLifecycleService", FakeService)

    result = task_handlers._run_task_create(_task_args())

    captured = capsys.readouterr()
    assert result == 1
    assert "Task create error: duplicate task" in captured.out
