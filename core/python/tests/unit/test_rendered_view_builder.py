from __future__ import annotations

from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.rebuild import (
    MarkdownReconciliationHelper,
    RenderedViewBuilder,
    RenderedViewSpec,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    (repo_root / "plan").mkdir(parents=True)
    return repo_root


def test_rendered_view_builder_uses_registry_definitions_with_overrides(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    builder = RenderedViewBuilder(ControlPlaneLoader(repo_root))

    result = builder.build_view(
        RenderedViewSpec(
            surface_id="rendered.initiative.plan",
            relative_output_path="plan/projects/watchtower/initiatives/example/plan.md",
            title="Example Initiative Plan",
            data={
                "initiative_identity": ("- `initiative_id`: `initiative.example`",),
                "objectives": ("- Deliver the example initiative.",),
                "planned_slices_or_workstreams": (
                    {
                        "task_id": "task.example.bootstrap",
                        "doc_path": "plan/projects/watchtower/initiatives/example/.wt/tasks/bootstrap/task.json",
                        "task_status": "planned",
                        "priority": "high",
                        "owner": "repository_maintainer",
                        "summary": "Bootstrap the example initiative.",
                    },
                ),
            },
        )
    )

    assert result.relative_output_path == "plan/projects/watchtower/initiatives/example/plan.md"
    assert result.content.startswith("# Example Initiative Plan\n")
    assert "## Planned Slices or Workstreams" in result.content


def test_markdown_reconciliation_helper_detects_missing_and_drifted_outputs(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    builder = RenderedViewBuilder(loader)
    reconciler = MarkdownReconciliationHelper(loader)
    rendered = builder.build_view(
        RenderedViewSpec(
            surface_id="rendered.plan.overview",
            data={
                "current_state": ("## Current State", "- `coordination_mode`: `ready_for_bootstrap`"),
                "active_initiatives": ("## Active Initiatives", "- None."),
                "actionable_tasks": ("## Actionable Tasks", "- None."),
                "recent_closeouts": ("## Recent Closeouts", "- None."),
            },
        )
    )

    missing_issues = reconciler.expected_issues({rendered.relative_output_path: rendered.content})
    assert missing_issues == (
        type(missing_issues[0])(
            relative_output_path="plan/plan_overview.md",
            issue_code="missing_output",
        ),
    )

    output_path = repo_root / rendered.relative_output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered.content, encoding="utf-8")
    assert reconciler.expected_issues({rendered.relative_output_path: rendered.content}) == ()

    output_path.write_text("# Drifted Overview\n", encoding="utf-8")
    drift_issues = reconciler.expected_issues({rendered.relative_output_path: rendered.content})
    assert drift_issues == (
        type(drift_issues[0])(
            relative_output_path="plan/plan_overview.md",
            issue_code="content_drift",
        ),
    )
