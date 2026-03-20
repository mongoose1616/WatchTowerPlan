from __future__ import annotations

import argparse
import json
from types import SimpleNamespace

from watchtower_core.cli import closeout_handlers


def _args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "trace_id": "trace.example",
        "initiative_slug": "example_initiative",
        "project_slug": None,
        "initiative_status": "completed",
        "closure_reason": "Closed for tests.",
        "superseded_by_trace_id": None,
        "closed_at": "2026-03-10T23:59:59Z",
        "retained_authority_path": [],
        "purged_at": "2026-03-10T23:59:59Z",
        "write": True,
        "allow_open_tasks": False,
        "allow_acceptance_issues": False,
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def test_closeout_initiative_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def close(self, **kwargs: object) -> SimpleNamespace:
            assert kwargs["trace_id"] == "trace.example"
            assert kwargs["write"] is True
            assert kwargs["allow_acceptance_issues"] is False
            return SimpleNamespace(
                trace_id="trace.example",
                initiative_status="completed",
                closed_at="2026-03-10T23:59:59Z",
                closure_reason="Closed for tests.",
                superseded_by_trace_id="trace.next",
                open_task_ids=("task.example.001",),
                acceptance_issue_count=2,
                acceptance_issues_allowed=True,
                wrote=True,
                traceability_output_path="core/control_plane/indexes/traceability/traceability_index.json",
                initiative_index_output_path="plan/.wt/indexes/initiative_index.json",
                coordination_index_output_path="plan/.wt/indexes/coordination_index.json",
                initiative_tracking_output_path="plan/tracking/initiative_tracking.md",
                coordination_tracking_output_path="plan/tracking/coordination_tracking.md",
            )

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "InitiativeCloseoutService", FakeService)

    result = closeout_handlers._run_closeout_initiative(
        _args(superseded_by_trace_id="trace.next", allow_open_tasks=True)
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Closed initiative trace.example as completed." in captured.out
    assert "Superseded By: trace.next" in captured.out
    assert "Open Tasks Left In Place: task.example.001" in captured.out
    assert "Acceptance Issues Left In Place: 2" in captured.out
    assert (
        "Canonical traceability, initiative, coordination, and live trackers were updated."
        in captured.out
    )


def test_closeout_initiative_supports_json_errors(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def close(self, **kwargs: object) -> SimpleNamespace:
            raise ValueError("open tasks remain")

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "InitiativeCloseoutService", FakeService)

    result = closeout_handlers._run_closeout_initiative(_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core closeout initiative",
        "message": "open tasks remain",
        "status": "error",
    }


def test_closeout_initiative_supports_json_success(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def close(self, **kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(
                trace_id="trace.example",
                initiative_status="completed",
                closed_at="2026-03-10T23:59:59Z",
                closure_reason="Closed for tests.",
                superseded_by_trace_id=None,
                open_task_ids=(),
                acceptance_issue_count=0,
                acceptance_issues_allowed=False,
                wrote=True,
                traceability_output_path="core/control_plane/indexes/traceability/traceability_index.json",
                initiative_index_output_path="plan/.wt/indexes/initiative_index.json",
                coordination_index_output_path="plan/.wt/indexes/coordination_index.json",
                initiative_tracking_output_path="plan/tracking/initiative_tracking.md",
                coordination_tracking_output_path="plan/tracking/coordination_tracking.md",
            )

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "InitiativeCloseoutService", FakeService)

    result = closeout_handlers._run_closeout_initiative(_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core closeout initiative"
    assert payload["acceptance_issue_count"] == 0
    assert payload["acceptance_issues_allowed"] is False
    assert ("planning" + "_catalog_output_path") not in payload


def test_closeout_plan_initiative_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def close_packwide(self, initiative_slug: str, **kwargs: object) -> SimpleNamespace:
            assert initiative_slug == "example_initiative"
            assert kwargs["write"] is True
            return SimpleNamespace(
                initiative_id="initiative.example_initiative",
                trace_id="trace.example_initiative",
                initiative_root="plan/initiatives/example_initiative",
                scope_type="pack_wide",
                initiative_status="completed",
                closed_at="2026-03-10T23:59:59Z",
                closure_reason="Closed for tests.",
                superseded_by_trace_id=None,
                wrote=True,
            )

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "InitiativePackageService", FakeService)

    result = closeout_handlers._run_closeout_plan_initiative(_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Closed live plan initiative trace.example_initiative as completed." in captured.out
    assert "Initiative Root: plan/initiatives/example_initiative" in captured.out
    assert "Initiative state, local artifacts, and derived plan surfaces were updated." in captured.out


def test_closeout_plan_initiative_supports_json_success(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def close_project_scoped(
            self,
            project_slug: str,
            initiative_slug: str,
            **kwargs: object,
        ) -> SimpleNamespace:
            assert project_slug == "watchtower"
            assert initiative_slug == "example_initiative"
            return SimpleNamespace(
                initiative_id="initiative.example_initiative",
                trace_id="trace.example_initiative",
                initiative_root="plan/projects/watchtower/initiatives/example_initiative",
                scope_type="project_scoped",
                initiative_status="completed",
                closed_at="2026-03-10T23:59:59Z",
                closure_reason="Closed for tests.",
                superseded_by_trace_id=None,
                wrote=False,
            )

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "InitiativePackageService", FakeService)

    result = closeout_handlers._run_closeout_plan_initiative(
        _args(format="json", write=False, project_slug="watchtower")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core closeout plan-initiative"
    assert payload["scope_type"] == "project_scoped"
    assert payload["initiative_root"] == "plan/projects/watchtower/initiatives/example_initiative"
    assert payload["wrote"] is False


def test_closeout_plan_initiative_supports_json_errors(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def close_packwide(self, initiative_slug: str, **kwargs: object) -> SimpleNamespace:
            raise ValueError("open local tasks remain")

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "InitiativePackageService", FakeService)

    result = closeout_handlers._run_closeout_plan_initiative(_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core closeout plan-initiative",
        "message": "open local tasks remain",
        "status": "error",
    }


def test_closeout_purge_trace_prints_human_summary(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def purge(self, **kwargs: object) -> SimpleNamespace:
            assert kwargs["trace_id"] == "trace.example"
            assert kwargs["retained_authority_paths"] == ()
            assert kwargs["write"] is True
            return SimpleNamespace(
                trace_id="trace.example",
                title="Example Trace",
                initiative_status="completed",
                closed_at="2026-03-10T21:00:00Z",
                closure_reason="Closed for tests.",
                purged_at="2026-03-10T23:59:59Z",
                wrote=True,
                removed_paths=(
                    "plan/initiatives/example/initiative_brief.md",
                    "plan/initiatives/example/.wt/tasks/example/task.json",
                ),
                retained_authority_paths=(
                    "plan/docs/standards/governance/example.md",
                    "plan/python/src/watchtower_plan/closeout/purge_trace.py",
                ),
                purge_ledger_relative_path="core/control_plane/ledgers/purges/example_purge_record.json",
                purge_ledger_output_path="core/control_plane/ledgers/purges/example_purge_record.json",
                refreshed_targets=("repository-paths", "traceability-index", "coordination"),
            )

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "TracePurgeService", FakeService)

    result = closeout_handlers._run_closeout_purge_trace(_args())

    captured = capsys.readouterr()
    assert result == 0
    assert "Prepared purge for trace.example." in captured.out
    assert "Removed Paths: 2" in captured.out
    assert (
        "Purge Ledger: "
        "core/control_plane/ledgers/purges/example_purge_record.json"
        in captured.out
    )
    assert "Trace package was deleted and derived surfaces were refreshed." in captured.out


def test_closeout_purge_trace_supports_json_errors(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def purge(self, **kwargs: object) -> SimpleNamespace:
            raise ValueError("surviving references remain")

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "TracePurgeService", FakeService)

    result = closeout_handlers._run_closeout_purge_trace(_args(format="json"))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core closeout purge-trace",
        "message": "surviving references remain",
        "status": "error",
    }


def test_closeout_purge_trace_supports_json_success(monkeypatch, capsys) -> None:
    class FakeService:
        def __init__(self, loader: object) -> None:
            self.loader = loader

        def purge(self, **kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(
                trace_id="trace.example",
                title="Example Trace",
                initiative_status="completed",
                closed_at="2026-03-10T21:00:00Z",
                closure_reason="Closed for tests.",
                purged_at="2026-03-10T23:59:59Z",
                wrote=False,
                removed_paths=("plan/initiatives/example/initiative_brief.md",),
                retained_authority_paths=("plan/docs/standards/governance/example.md",),
                purge_ledger_relative_path="core/control_plane/ledgers/purges/example_purge_record.json",
                purge_ledger_output_path=None,
                refreshed_targets=(),
            )

    monkeypatch.setattr(closeout_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(closeout_handlers, "TracePurgeService", FakeService)

    result = closeout_handlers._run_closeout_purge_trace(_args(format="json", write=False))

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 0
    assert payload["command"] == "watchtower-core closeout purge-trace"
    assert payload["purge_ledger_relative_path"].endswith("example_purge_record.json")
    assert payload["wrote"] is False
