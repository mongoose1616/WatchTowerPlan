from __future__ import annotations

import json
from types import SimpleNamespace

from watchtower_plan.cli import query_lookup_handlers

from tests.unit.route_query_handler_test_support import query_args


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
                repository_locator="repos/watchtower-plan",
                repository_kind="planning",
                owner="repository_maintainer",
                access="local_write",
                active=True,
            ),
        ),
    )

    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_lookup_handlers,
        "load_project_context",
        lambda loader, project_slug: project_context,
    )

    result = query_lookup_handlers._run_query_project_context(query_args(project_slug="watchtower"))

    captured = capsys.readouterr()
    assert result == 0
    assert "project.watchtower: WatchTower [active]" in captured.out
    assert "Pack Context: pack.plan via plan/.wt/manifests/pack_settings.json" in captured.out
    assert "Initiative Root: plan/projects/watchtower/initiatives" in captured.out
    assert "- planning: repos/watchtower-plan [planning, active]" in captured.out


def test_query_project_context_supports_json_errors(monkeypatch, capsys) -> None:
    monkeypatch.setattr(query_lookup_handlers, "ControlPlaneLoader", lambda: object())
    monkeypatch.setattr(
        query_lookup_handlers,
        "load_project_context",
        lambda loader, project_slug: (_ for _ in ()).throw(
            ValueError("Project root is missing: plan/projects/watchtower.")
        ),
    )

    result = query_lookup_handlers._run_query_project_context(
        query_args(project_slug="watchtower", format="json")
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert result == 1
    assert payload == {
        "command": "watchtower-core plan query project-context",
        "message": "Project root is missing: plan/projects/watchtower.",
        "status": "error",
    }
