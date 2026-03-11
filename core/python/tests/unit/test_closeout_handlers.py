from __future__ import annotations

import argparse
import json
from types import SimpleNamespace

from watchtower_core.cli import closeout_handlers


def _args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "trace_id": "trace.example",
        "initiative_status": "completed",
        "closure_reason": "Closed for tests.",
        "superseded_by_trace_id": None,
        "closed_at": "2026-03-10T23:59:59Z",
        "write": True,
        "allow_open_tasks": False,
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
            return SimpleNamespace(
                trace_id="trace.example",
                initiative_status="completed",
                closed_at="2026-03-10T23:59:59Z",
                closure_reason="Closed for tests.",
                superseded_by_trace_id="trace.next",
                open_task_ids=("task.example.001",),
                wrote=True,
                traceability_output_path="core/control_plane/indexes/traceability/traceability_index.v1.json",
                initiative_index_output_path="core/control_plane/indexes/initiatives/initiative_index.v1.json",
                coordination_index_output_path="core/control_plane/indexes/coordination/coordination_index.v1.json",
                initiative_tracking_output_path="docs/planning/initiatives/initiative_tracking.md",
                coordination_tracking_output_path="docs/planning/coordination_tracking.md",
                prd_tracking_output_path="docs/planning/prds/prd_tracking.md",
                decision_tracking_output_path="docs/planning/decisions/decision_tracking.md",
                design_tracking_output_path="docs/planning/design/design_tracking.md",
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
    assert (
        "Canonical traceability, initiative, coordination, and planning trackers "
        "were updated."
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
