from __future__ import annotations

import argparse
import json
from types import SimpleNamespace

from watchtower_core.cli import plan_handlers, task_handlers


def _plan_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "kind": "prd",
        "trace_id": "trace.plan_example",
        "document_id": "prd.plan_example",
        "title": "Plan Example",
        "summary": "Plan summary.",
        "owner": "repository_maintainer",
        "status": None,
        "applies_to": [],
        "alias": [],
        "file_stem": None,
        "linked_prd": [],
        "linked_decision": [],
        "linked_design": [],
        "linked_plan": [],
        "linked_acceptance": [],
        "source_request": [],
        "reference": [],
        "updated_at": "2026-03-10T23:59:59Z",
        "write": False,
        "include_document": False,
        "include_documents": False,
        "include_decision": False,
        "decision_id": None,
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
        "task_status": "backlog",
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


def test_plan_scaffold_prints_document_when_requested(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def scaffold(self, params: object, *, write: bool) -> SimpleNamespace:
            assert write is False
            return SimpleNamespace(
                kind="prd",
                document_id="prd.plan_example",
                trace_id="trace.plan_example",
                title="Plan Example",
                summary="Plan summary.",
                status="active",
                doc_path="docs/planning/prds/plan_example.md",
                content="# Body\n",
                wrote=False,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "PlanningScaffoldService", FakeService)

    result = plan_handlers._run_plan_scaffold(_plan_args(include_document=True))

    captured = capsys.readouterr()
    assert result == 0
    assert "Prepared prd scaffold at docs/planning/prds/plan_example.md." in captured.out
    assert "# Body" in captured.out


def test_plan_bootstrap_requires_include_decision_for_decision_id(capsys) -> None:
    result = plan_handlers._run_plan_bootstrap(
        _plan_args(decision_id="decision.example", include_decision=False)
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "Plan bootstrap error: --decision-id requires --include-decision." in captured.out


def test_plan_bootstrap_supports_json_output(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def bootstrap(self, params: object, *, write: bool) -> SimpleNamespace:
            return SimpleNamespace(
                documents=(
                    SimpleNamespace(
                        kind="prd",
                        document_id="prd.plan_example",
                        trace_id="trace.plan_example",
                        title="Plan Example PRD",
                        summary="Plan summary.",
                        status="active",
                        doc_path="docs/planning/prds/plan_example.md",
                        content="# PRD\n",
                    ),
                ),
                task_result=SimpleNamespace(
                    task_id="task.plan_example.bootstrap.001",
                    title="Bootstrap planning chain",
                    summary="Bootstrap summary.",
                    task_status="backlog",
                    task_kind="governance",
                    priority="medium",
                    owner="repository_maintainer",
                    doc_path="docs/planning/tasks/open/plan_bootstrap.md",
                    wrote=False,
                ),
                wrote=False,
                sync_refreshed=False,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "PlanningScaffoldService", FakeService)

    result = plan_handlers._run_plan_bootstrap(_plan_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core plan bootstrap"
    assert payload["document_count"] == 1
    assert payload["task"]["task_id"] == "task.plan_example.bootstrap.001"


def test_plan_bootstrap_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def bootstrap(self, params: object, *, write: bool) -> SimpleNamespace:
            return SimpleNamespace(
                documents=(
                    SimpleNamespace(
                        kind="prd",
                        document_id="prd.plan_example",
                        trace_id="trace.plan_example",
                        title="Plan Example PRD",
                        summary="Plan summary.",
                        status="active",
                        doc_path="docs/planning/prds/plan_example.md",
                        content="# PRD\n",
                    ),
                ),
                task_result=SimpleNamespace(
                    task_id="task.plan_example.bootstrap.001",
                    title="Bootstrap planning chain",
                    summary="Bootstrap summary.",
                    task_status="backlog",
                    task_kind="governance",
                    priority="medium",
                    owner="repository_maintainer",
                    doc_path="docs/planning/tasks/open/plan_bootstrap.md",
                    wrote=True,
                ),
                wrote=True,
                sync_refreshed=True,
            )

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "PlanningScaffoldService", FakeService)

    result = plan_handlers._run_plan_bootstrap(_plan_args(include_documents=True, write=True))

    captured = capsys.readouterr()
    assert result == 0
    assert "Wrote bootstrap chain with 1 planning documents" in captured.out
    assert "- prd: docs/planning/prds/plan_example.md" in captured.out
    assert "# PRD" in captured.out
    assert "Derived planning surfaces were refreshed." in captured.out


def test_plan_scaffold_reports_errors(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def scaffold(self, params: object, *, write: bool) -> SimpleNamespace:
            raise ValueError("duplicate path")

    monkeypatch.setattr(plan_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(plan_handlers, "PlanningScaffoldService", FakeService)

    result = plan_handlers._run_plan_scaffold(_plan_args())

    captured = capsys.readouterr()
    assert result == 1
    assert "Plan scaffold error: duplicate path" in captured.out


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
                task_status="backlog",
                task_kind="feature",
                priority="high",
                owner="repository_maintainer",
                updated_at="2026-03-10T23:59:59Z",
                doc_path="docs/planning/tasks/open/example.md",
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
    assert "Prepared task task.example.001 at docs/planning/tasks/open/example.md." in captured.out
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
                task_status="done",
                task_kind="feature",
                priority="high",
                owner="repository_maintainer",
                updated_at="2026-03-10T23:59:59Z",
                doc_path="docs/planning/tasks/closed/example.md",
                previous_doc_path="docs/planning/tasks/open/example.md",
                moved=True,
                changed=True,
                wrote=True,
                coordination_refreshed=True,
                closeout_recommended=True,
            )

    monkeypatch.setattr(task_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(task_handlers, "TaskLifecycleService", FakeService)

    result = task_handlers._run_task_transition(_task_args(task_status="done", write=True))

    captured = capsys.readouterr()
    assert result == 0
    assert "Moved From: docs/planning/tasks/open/example.md" in captured.out
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
                task_status="backlog",
                task_kind="feature",
                priority="high",
                owner="repository_maintainer",
                updated_at="2026-03-10T23:59:59Z",
                doc_path="docs/planning/tasks/open/example.md",
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
        _task_args(task_status="done", format="json")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core task transition",
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
