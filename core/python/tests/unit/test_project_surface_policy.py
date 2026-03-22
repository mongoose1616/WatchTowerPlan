from __future__ import annotations

import json
from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.project_surface_policy import ProjectSurfacePolicyHelper

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> ProjectSurfacePolicyHelper:
    return ProjectSurfacePolicyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_project_surface_policy_helper_exposes_required_project_surfaces() -> None:
    helper = _helper()

    required_paths = helper.required_relative_paths(
        "plan/projects/watchtower",
        surface_kind="rendered_view",
    )

    assert required_paths == (
        "plan/projects/watchtower/project.md",
        "plan/projects/watchtower/repositories.md",
        "plan/projects/watchtower/summary.md",
    )


def test_project_surface_policy_helper_reports_missing_required_metadata(tmp_path: Path) -> None:
    helper = _helper()
    repo_root = tmp_path / "repo"
    project_root = repo_root / "plan" / "projects" / "example"
    (project_root / ".wt").mkdir(parents=True)
    (project_root / "initiatives").mkdir(parents=True)
    (project_root / "project.md").write_text("# Example\n", encoding="utf-8")
    (project_root / "repositories.md").write_text("# Repositories\n", encoding="utf-8")
    (project_root / "summary.md").write_text("# Summary\n", encoding="utf-8")
    (project_root / ".wt" / "project.json").write_text(
        json.dumps(
            {
                "$schema": "urn:watchtower:schema:artifacts:plan:project-record:v1",
                "project_id": "project.example",
                "title": "Example",
                "summary": "Example project.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (project_root / ".wt" / "project_repository_map.json").write_text(
        json.dumps(
            {
                "$schema": "urn:watchtower:schema:artifacts:plan:project-repository-map:v1",
                "project_id": "project.example",
                "repositories": [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    issues = helper.validate_root(
        repo_root,
        "plan/projects/example",
        surface_kinds=("machine_artifact", "initiative_container", "rendered_view", "machine_root"),
    )

    assert any(issue.issue_code == "required_metadata_missing" for issue in issues)
