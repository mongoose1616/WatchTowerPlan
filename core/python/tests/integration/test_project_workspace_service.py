from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.project_workspace import (
    PLAN_PROJECT_INDEX_PATH,
    PlanProjectSearchParams,
    ProjectBootstrapParams,
    ProjectRepositoryLinkSpec,
    ProjectWorkspaceService,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    copytree(REPO_ROOT / "plan", repo_root / "plan")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _bootstrap_params() -> ProjectBootstrapParams:
    return ProjectBootstrapParams(
        project_slug="watchtower",
        title="WatchTower",
        summary="Operator-facing implementation target for the first project-scoped flow.",
        repository_links=(
            ProjectRepositoryLinkSpec(
                repository_role="planning",
                repository_locator="/home/j/WatchTowerPlan",
                repository_kind="planning",
            ),
            ProjectRepositoryLinkSpec(
                repository_role="implementation",
                repository_locator="/home/j/WatchTower",
                repository_kind="implementation",
            ),
        ),
        updated_at="2026-03-17T17:00:00Z",
    )


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_project_workspace_bootstrap_writes_machine_package_views_index_and_context(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = ProjectWorkspaceService(ControlPlaneLoader(repo_root))

    result = service.bootstrap(_bootstrap_params(), write=True)

    assert result.wrote is True
    assert result.project_id == "project.watchtower"
    assert result.validation_passed is True

    project_root = repo_root / "plan" / "projects" / "watchtower"
    assert (project_root / ".wt" / "project.json").exists()
    assert (project_root / ".wt" / "project_repository_map.json").exists()
    assert (project_root / "project.md").exists()
    assert (project_root / "repositories.md").exists()
    assert (project_root / "summary.md").exists()
    assert (repo_root / PLAN_PROJECT_INDEX_PATH).exists()

    context = service.load_project_context("watchtower")
    assert context.pack_context.pack_settings.pack_id == "pack.plan"
    assert context.project_id == "project.watchtower"
    assert context.initiative_root == "plan/projects/watchtower/initiatives"
    assert len(context.repository_links) == 2
    assert {link.repository_role for link in context.repository_links} == {
        "planning",
        "implementation",
    }

    entries = service.search_projects(PlanProjectSearchParams(query="watchtower"))
    assert len(entries) == 1
    assert entries[0].project_id == "project.watchtower"
    assert entries[0].repository_count == 2


def test_project_workspace_validation_detects_stale_surfaces_until_rebuilt(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = ProjectWorkspaceService(ControlPlaneLoader(repo_root))
    service.bootstrap(_bootstrap_params(), write=True)

    project_md = repo_root / "plan" / "projects" / "watchtower" / "project.md"
    project_md.write_text(
        project_md.read_text(encoding="utf-8")
        + "\n## Drift\nThis manual edit should fail validation.\n",
        encoding="utf-8",
    )
    project_index = _load_json(repo_root / PLAN_PROJECT_INDEX_PATH)
    project_index["title"] = "Stale Project Index"
    (repo_root / PLAN_PROJECT_INDEX_PATH).write_text(
        f"{json.dumps(project_index, indent=2)}\n",
        encoding="utf-8",
    )

    validation = service.validate("watchtower", write=False)

    assert validation.passed is False
    assert any("Project rendered surface drift detected" in message for message in validation.issue_messages)
    assert any("Project aggregate index drift detected" in message for message in validation.issue_messages)

    service.sync(write=True)
    restored = service.validate("watchtower", write=False)
    assert restored.passed is True
