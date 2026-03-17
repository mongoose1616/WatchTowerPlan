"""Project-scoped runtime context loading layered on top of pack context."""

from __future__ import annotations

import json
from dataclasses import dataclass

from watchtower_core.control_plane.human_surface_policy import HumanSurfacePolicyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_context import PackContext
from watchtower_core.control_plane.project_surface_policy import ProjectSurfacePolicyHelper
from watchtower_core.validation import ArtifactValidationService, ValidationResult

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


@dataclass(frozen=True, slots=True)
class ProjectRepositoryLink:
    """Loaded repository-link record for one project context."""

    repository_id: str
    repository_role: str
    repository_locator: str
    repository_kind: str
    owner: str
    access: str
    active: bool


@dataclass(frozen=True, slots=True)
class ProjectContext:
    """Project-specific runtime context layered on top of the pack context."""

    pack_context: PackContext
    project_id: str
    slug: str
    title: str
    summary: str
    status: str
    project_root: str
    initiative_root: str
    repository_links: tuple[ProjectRepositoryLink, ...]


@dataclass(frozen=True, slots=True)
class ProjectMachineValidationResult:
    """Machine-only validation result for one project container."""

    project_id: str
    project_root: str
    passed: bool
    issue_messages: tuple[str, ...]
    artifact_results: tuple[ValidationResult, ...]
    project_document: dict[str, object] | None
    repository_map_document: dict[str, object] | None


def load_project_context(
    loader: ControlPlaneLoader,
    project_slug: str,
    *,
    pack_settings_path: str = PLAN_PACK_SETTINGS_PATH,
) -> ProjectContext:
    """Load one project context from machine-authoritative project artifacts."""

    validation = validate_project_machine_state(
        loader,
        project_slug,
        pack_settings_path=pack_settings_path,
    )
    if not validation.passed:
        raise ValueError(
            "Project context cannot load from an invalid project container: "
            + "; ".join(validation.issue_messages)
        )

    assert validation.project_document is not None
    assert validation.repository_map_document is not None
    pack_loader = _pack_loader(loader, pack_settings_path)
    project_document = validation.project_document
    repository_map_document = validation.repository_map_document
    return ProjectContext(
        pack_context=pack_loader.load_pack_context(pack_settings_path),
        project_id=str(project_document["project_id"]),
        slug=str(project_document["slug"]),
        title=str(project_document["title"]),
        summary=str(project_document["summary"]),
        status=str(project_document["status"]),
        project_root=validation.project_root,
        initiative_root=str(project_document["initiative_root"]),
        repository_links=tuple(
            ProjectRepositoryLink(
                repository_id=str(entry["repository_id"]),
                repository_role=str(entry["repository_role"]),
                repository_locator=str(entry["repository_locator"]),
                repository_kind=str(entry["repository_kind"]),
                owner=str(entry["owner"]),
                access=str(entry["access"]),
                active=bool(entry["active"]),
            )
            for entry in repository_map_document["repositories"]
        ),
    )


def validate_project_machine_state(
    loader: ControlPlaneLoader,
    project_slug: str,
    *,
    pack_settings_path: str = PLAN_PACK_SETTINGS_PATH,
) -> ProjectMachineValidationResult:
    """Validate the machine-authoritative project surfaces needed for context load."""

    project_root = loader.repo_root / "plan" / "projects" / project_slug
    project_root_relative = f"plan/projects/{project_slug}"
    project_id = f"project.{project_slug}"
    issues: list[str] = []
    project_document: dict[str, object] | None = None
    repository_map_document: dict[str, object] | None = None
    project_surface_helper = ProjectSurfacePolicyHelper.from_loader(
        _pack_loader(loader, pack_settings_path),
        pack_settings_path=pack_settings_path,
    )

    if not project_root.exists():
        issues.append(f"Project root is missing: {project_root_relative}.")
        return ProjectMachineValidationResult(
            project_id=project_id,
            project_root=project_root_relative,
            passed=False,
            issue_messages=tuple(issues),
            artifact_results=(),
            project_document=None,
            repository_map_document=None,
        )

    required_paths = project_surface_helper.required_relative_paths(
        project_root_relative,
        surface_kind="machine_artifact",
    )
    validator = ArtifactValidationService(_pack_loader(loader, pack_settings_path))
    artifact_results: list[ValidationResult] = []
    for relative_path in required_paths:
        if not (loader.repo_root / relative_path).exists():
            issues.append(f"Required project artifact is missing: {relative_path}.")
            continue
        artifact_results.append(validator.validate(relative_path))
    policy_issues = project_surface_helper.validate_root(
        loader.repo_root,
        project_root_relative,
        surface_kinds=("machine_root", "machine_artifact", "initiative_container"),
    )
    issues.extend(issue.message for issue in policy_issues)
    initiative_root = f"{project_root_relative}/initiatives"

    if not issues:
        project_document = _load_json(loader, f"{project_root_relative}/.wt/project.json")
        repository_map_document = _load_json(
            loader,
            f"{project_root_relative}/.wt/project_repository_map.json",
        )
        if str(project_document["initiative_root"]) != initiative_root:
            issues.append(
                "Project record initiative_root does not match the canonical project initiatives path."
            )
        repository_refs = tuple(project_document.get("linked_repository_refs", ()))
        map_ids = tuple(
            entry["repository_id"] for entry in repository_map_document.get("repositories", ())
        )
        if tuple(repository_refs) != map_ids:
            issues.append(
                "Project record linked_repository_refs do not match project_repository_map repositories."
            )

    for result in artifact_results:
        if not result.passed:
            issues.append(
                f"{result.target_path} failed {result.validator_id} with {result.issue_count} issue(s)."
            )

    machine_root_issues = HumanSurfacePolicyHelper.from_loader(
        _pack_loader(loader, pack_settings_path),
        pack_settings_path=pack_settings_path,
    ).validate_root(loader.repo_root, f"{project_root_relative}/.wt")
    issues.extend(issue.message for issue in machine_root_issues)

    return ProjectMachineValidationResult(
        project_id=project_id,
        project_root=project_root_relative,
        passed=not issues and all(result.passed for result in artifact_results),
        issue_messages=tuple(issues),
        artifact_results=tuple(artifact_results),
        project_document=project_document,
        repository_map_document=repository_map_document,
    )


def _pack_loader(loader: ControlPlaneLoader, pack_settings_path: str) -> ControlPlaneLoader:
    return ControlPlaneLoader(
        loader.repo_root,
        active_pack_settings_path=pack_settings_path,
    )


def _load_json(loader: ControlPlaneLoader, relative_path: str) -> dict[str, object]:
    path = loader.repo_root / relative_path
    return json.loads(path.read_text(encoding="utf-8"))
