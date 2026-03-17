from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree, rmtree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.initiative_packages import (
    InitiativeBootstrapParams,
    InitiativePackageService,
    InitiativeTaskSpec,
)
from watchtower_core.repo_ops.project_context import load_project_context
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
    for path in (repo_root / "plan" / "initiatives").iterdir():
        if path.name == "README.md":
            continue
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()
    for path in (repo_root / "plan" / "projects").iterdir():
        if path.name == "README.md":
            continue
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()
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


def _initiative_params() -> InitiativeBootstrapParams:
    return InitiativeBootstrapParams(
        trace_id="trace.watchtower_scope_flow",
        title="WatchTower Scope Flow",
        summary="Bootstraps one project-scoped initiative for project workspace tests.",
        initiative_slug="watchtower_scope_flow",
        task_specs=(
            InitiativeTaskSpec(
                title="Seed WatchTower scope flow",
                summary="Creates one project-scoped initiative package.",
                slug="seed_watchtower_scope_flow",
            ),
        ),
        updated_at="2026-03-17T17:05:00Z",
    )


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


def test_project_context_load_uses_machine_state_even_when_rendered_surfaces_drift(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    service = ProjectWorkspaceService(loader)
    service.bootstrap(_bootstrap_params(), write=True)

    project_md = repo_root / "plan" / "projects" / "watchtower" / "project.md"
    project_md.write_text(
        project_md.read_text(encoding="utf-8")
        + "\n## Drift\nThis manual edit should not block machine context loading.\n",
        encoding="utf-8",
    )

    context = load_project_context(loader, "watchtower")

    assert context.pack_context.pack_settings.pack_id == "pack.plan"
    assert context.project_id == "project.watchtower"
    assert context.initiative_root == "plan/projects/watchtower/initiatives"
    assert len(context.repository_links) == 2

    validation = service.validate("watchtower", write=False)
    assert validation.passed is False
    assert any("Project rendered surface drift detected" in message for message in validation.issue_messages)


def test_project_workspace_sync_uses_latest_child_initiative_timestamp(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    project_service = ProjectWorkspaceService(loader)
    initiative_service = InitiativePackageService(loader)

    project_service.bootstrap(_bootstrap_params(), write=True)
    initiative_service.bootstrap_project_scoped(
        "watchtower",
        _initiative_params(),
        write=True,
    )

    initiative_path = (
        repo_root
        / "plan/projects/watchtower/initiatives/watchtower_scope_flow/.wt/initiative.json"
    )
    initiative_document = _load_json(initiative_path)
    initiative_document["updated_at"] = "2026-03-17T17:30:00Z"
    initiative_document["lifecycle_stage"] = "in_progress"
    initiative_path.write_text(
        f"{json.dumps(initiative_document, indent=2)}\n",
        encoding="utf-8",
    )

    project_service.sync(write=True)

    project_index = _load_json(repo_root / PLAN_PROJECT_INDEX_PATH)
    project_entry = next(
        entry
        for entry in project_index["entries"]
        if entry["project_id"] == "project.watchtower"
    )
    assert project_entry["updated_at"] == "2026-03-17T17:30:00Z"

    summary_view = (repo_root / "plan/projects/watchtower/summary.md").read_text(
        encoding="utf-8"
    )
    assert "`updated_at`: `2026-03-17T17:30:00Z`" in summary_view


def test_project_workspace_validation_blocks_stray_machine_root_agents_file(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    service = ProjectWorkspaceService(ControlPlaneLoader(repo_root))
    service.bootstrap(_bootstrap_params(), write=True)

    machine_root = repo_root / "plan" / "projects" / "watchtower" / ".wt"
    (machine_root / "AGENTS.md").write_text(
        "This file should not exist inside a machine-only root.\n",
        encoding="utf-8",
    )

    validation = service.validate("watchtower", write=False)

    assert validation.passed is False
    assert any("Forbidden human surface is present" in message for message in validation.issue_messages)
