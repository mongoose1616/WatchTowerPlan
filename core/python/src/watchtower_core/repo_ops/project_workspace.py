"""Project-container bootstrap, validation, rendered views, and query helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.human_surface_policy import HumanSurfacePolicyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_context import PackContext
from watchtower_core.repo_ops.query.common import (
    normalize_optional_text,
    normalize_text,
    query_score,
)
from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_core.validation import ArtifactValidationService, ValidationResult

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"
PLAN_PROJECT_INDEX_PATH = "plan/.wt/indexes/project_index.json"

_ACTIVE_PROJECT_STATUSES = frozenset({"active", "planned"})
_TERMINAL_INITIATIVE_STAGES = frozenset({"completed", "superseded", "cancelled"})


@dataclass(frozen=True, slots=True)
class ProjectRepositoryLinkSpec:
    """Bootstrap-time specification for one linked project repository."""

    repository_role: str
    repository_locator: str
    repository_kind: str
    repository_id: str | None = None
    owner: str = "repository_maintainer"
    access: str = "local_write"
    active: bool = True


@dataclass(frozen=True, slots=True)
class ProjectBootstrapParams:
    """Inputs for bootstrapping one project container."""

    project_slug: str
    title: str
    summary: str
    repository_links: tuple[ProjectRepositoryLinkSpec, ...]
    project_id: str | None = None
    status: str = "active"
    updated_at: str | None = None


@dataclass(frozen=True, slots=True)
class ProjectBootstrapResult:
    """Summary of one project-bootstrap mutation."""

    project_id: str
    project_root: str
    validation_passed: bool
    wrote: bool


@dataclass(frozen=True, slots=True)
class ProjectValidationResult:
    """Structured validation result for one project container."""

    project_id: str
    project_root: str
    passed: bool
    issue_messages: tuple[str, ...]
    artifact_results: tuple[ValidationResult, ...]
    wrote: bool


@dataclass(frozen=True, slots=True)
class ProjectRepositoryLink:
    """Loaded repository-link record for a project context."""

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
class PlanProjectIndexEntry:
    """Machine-readable project summary entry for the plan workspace."""

    project_id: str
    slug: str
    title: str
    summary: str
    status: str
    project_root: str
    initiative_root: str
    repository_count: int
    active_initiative_count: int
    blocked_initiative_count: int
    linked_repository_roles: tuple[str, ...]
    repository_locators: tuple[str, ...]
    updated_at: str

    @classmethod
    def from_document(cls, document: dict[str, object]) -> PlanProjectIndexEntry:
        return cls(
            project_id=str(document["project_id"]),
            slug=str(document["slug"]),
            title=str(document["title"]),
            summary=str(document["summary"]),
            status=str(document["status"]),
            project_root=str(document["project_root"]),
            initiative_root=str(document["initiative_root"]),
            repository_count=int(document["repository_count"]),
            active_initiative_count=int(document["active_initiative_count"]),
            blocked_initiative_count=int(document["blocked_initiative_count"]),
            linked_repository_roles=tuple(document.get("linked_repository_roles", ())),
            repository_locators=tuple(document.get("repository_locators", ())),
            updated_at=str(document["updated_at"]),
        )


@dataclass(frozen=True, slots=True)
class PlanProjectSearchParams:
    """Structured lookup filters for plan-workspace project entries."""

    query: str | None = None
    project_id: str | None = None
    slug: str | None = None
    status: str | None = None
    repository_role: str | None = None
    limit: int | None = None


@dataclass(frozen=True, slots=True)
class DerivedProjectSurfaceIssue:
    """One stale or missing rendered or index surface tied to a project container."""

    category: str
    relative_path: str
    message: str


@dataclass(frozen=True, slots=True)
class ProjectWorkspaceSyncResult:
    """Summary of one project-workspace rebuild run."""

    project_count: int
    initiative_count: int
    wrote: bool


@dataclass(frozen=True, slots=True)
class _ProjectSnapshot:
    project_document: dict[str, object]
    repository_map_document: dict[str, object]
    child_initiatives: tuple[dict[str, object], ...]
    project_root: str
    initiative_root: str


class ProjectWorkspaceService:
    """Manage project containers and project-local rendered/query surfaces."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader

    def bootstrap(
        self,
        params: ProjectBootstrapParams,
        *,
        write: bool,
    ) -> ProjectBootstrapResult:
        """Create one project container with its required machine package."""

        if not params.repository_links:
            raise ValueError("Project bootstrap requires at least one linked repository.")

        updated_at = params.updated_at or utc_timestamp_now()
        project_slug = params.project_slug
        project_id = params.project_id or f"project.{project_slug}"
        if project_id != f"project.{project_slug}":
            raise ValueError("project_id must use the canonical project.<slug> form.")

        project_root = self._project_root(project_slug)
        if project_root.exists():
            raise ValueError(
                f"Project root already exists: {project_root.relative_to(self._loader.repo_root)}"
            )

        repository_entries = []
        repository_refs = []
        for spec in params.repository_links:
            repository_id = spec.repository_id or f"repository.{project_slug}.{spec.repository_role}"
            repository_refs.append(repository_id)
            repository_entries.append(
                {
                    "repository_id": repository_id,
                    "repository_role": spec.repository_role,
                    "repository_locator": spec.repository_locator,
                    "repository_kind": spec.repository_kind,
                    "owner": spec.owner,
                    "access": spec.access,
                    "active": spec.active,
                }
            )

        project_document = {
            "$schema": "urn:watchtower:schema:artifacts:plan:project-record:v1",
            "project_id": project_id,
            "slug": project_slug,
            "title": params.title,
            "summary": params.summary,
            "status": params.status,
            "linked_repository_refs": repository_refs,
            "initiative_root": self._project_initiative_root_relative(project_slug),
            "updated_at": updated_at,
        }
        repository_map_document = {
            "$schema": "urn:watchtower:schema:artifacts:plan:project-repository-map:v1",
            "id": f"projectmap.{project_slug}",
            "project_id": project_id,
            "updated_at": updated_at,
            "repositories": repository_entries,
        }

        if not write:
            return ProjectBootstrapResult(
                project_id=project_id,
                project_root=str(project_root.relative_to(self._loader.repo_root)),
                validation_passed=False,
                wrote=False,
            )

        (project_root / "initiatives").mkdir(parents=True, exist_ok=True)
        self._loader.artifact_store.write_json_object(
            self._project_path(project_slug, ".wt/project.json"),
            project_document,
        )
        self._loader.artifact_store.write_json_object(
            self._project_path(project_slug, ".wt/project_repository_map.json"),
            repository_map_document,
        )
        self.sync(write=True)

        validation = self.validate(project_slug, write=False)
        return ProjectBootstrapResult(
            project_id=project_id,
            project_root=str(project_root.relative_to(self._loader.repo_root)),
            validation_passed=validation.passed,
            wrote=True,
        )

    def validate(
        self,
        project_slug: str,
        *,
        write: bool,
    ) -> ProjectValidationResult:
        """Validate one project container and its derived project surfaces."""

        project_root = self._project_root(project_slug)
        project_root_relative = self._project_root_relative(project_slug)
        project_id = f"project.{project_slug}"
        issues: list[str] = []

        if not project_root.exists():
            issues.append(f"Project root is missing: {project_root_relative}.")
            return ProjectValidationResult(
                project_id=project_id,
                project_root=project_root_relative,
                passed=False,
                issue_messages=tuple(issues),
                artifact_results=(),
                wrote=write,
            )

        required_paths = (
            self._project_path(project_slug, ".wt/project.json"),
            self._project_path(project_slug, ".wt/project_repository_map.json"),
        )
        validator = ArtifactValidationService(self._pack_loader())
        artifact_results: list[ValidationResult] = []
        for relative_path in required_paths:
            if not (self._loader.repo_root / relative_path).exists():
                issues.append(f"Required project artifact is missing: {relative_path}.")
                continue
            artifact_results.append(validator.validate(relative_path))

        initiatives_dir = project_root / "initiatives"
        if not initiatives_dir.exists():
            issues.append(
                f"Project initiative root is missing: {self._project_path(project_slug, 'initiatives')}."
            )

        if not issues:
            project_document = self._load_json(self._project_path(project_slug, ".wt/project.json"))
            repository_map_document = self._load_json(
                self._project_path(project_slug, ".wt/project_repository_map.json")
            )
            if str(project_document["initiative_root"]) != self._project_initiative_root_relative(
                project_slug
            ):
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

        if not issues:
            derived_issues = self.expected_surface_issues(project_slug)
            issues.extend(issue.message for issue in derived_issues)

        machine_root_issues = HumanSurfacePolicyHelper.from_loader(
            self._pack_loader(),
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        ).validate_root(self._loader.repo_root, self._project_path(project_slug, ".wt"))
        issues.extend(issue.message for issue in machine_root_issues)

        return ProjectValidationResult(
            project_id=project_id,
            project_root=project_root_relative,
            passed=not issues and all(result.passed for result in artifact_results),
            issue_messages=tuple(issues),
            artifact_results=tuple(artifact_results),
            wrote=write,
        )

    def load_project_context(self, project_slug: str) -> ProjectContext:
        """Load project-specific context on top of the always-loaded pack context."""

        validation = self.validate(project_slug, write=False)
        if not validation.passed:
            raise ValueError(
                "Project context cannot load from an invalid project container: "
                + "; ".join(validation.issue_messages)
            )

        project_document = self._load_json(self._project_path(project_slug, ".wt/project.json"))
        repository_map_document = self._load_json(
            self._project_path(project_slug, ".wt/project_repository_map.json")
        )
        return ProjectContext(
            pack_context=self._loader.load_pack_context(PLAN_PACK_SETTINGS_PATH),
            project_id=str(project_document["project_id"]),
            slug=str(project_document["slug"]),
            title=str(project_document["title"]),
            summary=str(project_document["summary"]),
            status=str(project_document["status"]),
            project_root=self._project_root_relative(project_slug),
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

    def sync(self, *, write: bool) -> ProjectWorkspaceSyncResult:
        """Rebuild the project index and project-local rendered views."""

        snapshots = self._load_project_snapshots()
        documents = self._build_documents(snapshots)
        if write:
            self._loader.artifact_store.write_json_object(
                PLAN_PROJECT_INDEX_PATH,
                documents["project_index"],
            )
            for relative_path, content in documents["project_views"].items():
                self._write_markdown(relative_path, content)
        return ProjectWorkspaceSyncResult(
            project_count=len(snapshots),
            initiative_count=sum(len(snapshot.child_initiatives) for snapshot in snapshots),
            wrote=write,
        )

    def load_project_entries(self) -> tuple[PlanProjectIndexEntry, ...]:
        """Load typed project-index entries for plan-local search."""

        document = self._pack_loader().load_validated_document(PLAN_PROJECT_INDEX_PATH)
        assert isinstance(document, dict)
        return tuple(PlanProjectIndexEntry.from_document(entry) for entry in document["entries"])

    def search_projects(
        self,
        params: PlanProjectSearchParams,
    ) -> tuple[PlanProjectIndexEntry, ...]:
        """Search pack-level project entries."""

        return _search_project_entries(self.load_project_entries(), params)

    def expected_surface_issues(
        self,
        project_slug: str,
    ) -> tuple[DerivedProjectSurfaceIssue, ...]:
        """Return stale or missing derived surfaces for one project container."""

        snapshots = self._load_project_snapshots()
        documents = self._build_documents(snapshots)
        project_root = self._project_root_relative(project_slug)
        expected_markdown = {
            f"{project_root}/project.md": documents["project_views"].get(
                f"{project_root}/project.md",
                "",
            ),
            f"{project_root}/repositories.md": documents["project_views"].get(
                f"{project_root}/repositories.md",
                "",
            ),
            f"{project_root}/summary.md": documents["project_views"].get(
                f"{project_root}/summary.md",
                "",
            ),
        }
        expected_json = {
            PLAN_PROJECT_INDEX_PATH: documents["project_index"],
        }

        issues: list[DerivedProjectSurfaceIssue] = []
        for relative_path, expected in expected_markdown.items():
            if not expected:
                issues.append(
                    DerivedProjectSurfaceIssue(
                        category="stale_rendered_surface",
                        relative_path=relative_path,
                        message=f"Required project rendered surface is missing from the expected build: {relative_path}.",
                    )
                )
                continue
            candidate = self._loader.repo_root / relative_path
            if not candidate.exists():
                issues.append(
                    DerivedProjectSurfaceIssue(
                        category="stale_rendered_surface",
                        relative_path=relative_path,
                        message=f"Required project rendered surface is missing: {relative_path}.",
                    )
                )
                continue
            if candidate.read_text(encoding="utf-8") != expected:
                issues.append(
                    DerivedProjectSurfaceIssue(
                        category="stale_rendered_surface",
                        relative_path=relative_path,
                        message=f"Project rendered surface drift detected for {relative_path}.",
                    )
                )

        for relative_path, expected in expected_json.items():
            candidate = self._loader.repo_root / relative_path
            if not candidate.exists():
                issues.append(
                    DerivedProjectSurfaceIssue(
                        category="stale_aggregate_index",
                        relative_path=relative_path,
                        message=f"Required project aggregate index is missing: {relative_path}.",
                    )
                )
                continue
            try:
                current = json.loads(candidate.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                issues.append(
                    DerivedProjectSurfaceIssue(
                        category="stale_aggregate_index",
                        relative_path=relative_path,
                        message=f"Project aggregate index is not valid JSON: {relative_path}.",
                    )
                )
                continue
            if current != expected:
                issues.append(
                    DerivedProjectSurfaceIssue(
                        category="stale_aggregate_index",
                        relative_path=relative_path,
                        message=f"Project aggregate index drift detected for {relative_path}.",
                    )
                )
        return tuple(sorted(issues, key=lambda issue: (issue.category, issue.relative_path)))

    def _build_documents(
        self,
        snapshots: tuple[_ProjectSnapshot, ...],
    ) -> dict[str, object]:
        updated_at = _latest_timestamp(_snapshot_updated_at(snapshot) for snapshot in snapshots)
        project_entries = tuple(
            sorted(
                (self._build_project_entry(snapshot) for snapshot in snapshots),
                key=lambda entry: entry.project_id,
            )
        )
        project_index = {
            "$schema": "urn:watchtower:schema:artifacts:plan:project-index:v1",
            "id": "index.projects",
            "title": "Plan Workspace Project Index",
            "status": "active",
            "updated_at": _latest_timestamp(
                [*(entry.updated_at for entry in project_entries), updated_at]
            ),
            "entries": [self._serialize_project_entry(entry) for entry in project_entries],
        }
        self._pack_loader().schema_store.validate_instance(project_index)
        return {
            "project_index": project_index,
            "project_views": self._render_project_views(snapshots),
        }

    def _build_project_entry(self, snapshot: _ProjectSnapshot) -> PlanProjectIndexEntry:
        project = snapshot.project_document
        child_initiatives = snapshot.child_initiatives
        active_initiatives = tuple(
            initiative
            for initiative in child_initiatives
            if str(initiative["lifecycle_stage"]) not in _TERMINAL_INITIATIVE_STAGES
        )
        blocked_initiatives = tuple(
            initiative
            for initiative in active_initiatives
            if str(initiative["lifecycle_stage"]) == "blocked"
            or bool(initiative.get("gate_state", {}).get("blocking_reasons"))
        )
        repositories = tuple(snapshot.repository_map_document["repositories"])
        return PlanProjectIndexEntry(
            project_id=str(project["project_id"]),
            slug=str(project["slug"]),
            title=str(project["title"]),
            summary=str(project["summary"]),
            status=str(project["status"]),
            project_root=snapshot.project_root,
            initiative_root=snapshot.initiative_root,
            repository_count=len(repositories),
            active_initiative_count=len(active_initiatives),
            blocked_initiative_count=len(blocked_initiatives),
            linked_repository_roles=tuple(
                str(entry["repository_role"]) for entry in repositories
            ),
            repository_locators=tuple(
                str(entry["repository_locator"]) for entry in repositories
            ),
            updated_at=_snapshot_updated_at(snapshot),
        )

    def _render_project_views(
        self,
        snapshots: tuple[_ProjectSnapshot, ...],
    ) -> dict[str, str]:
        documents: dict[str, str] = {}
        for snapshot in snapshots:
            project = snapshot.project_document
            repositories = tuple(snapshot.repository_map_document["repositories"])
            initiative_lines = "\n".join(
                f"- `{initiative['initiative_id']}`: `{initiative['lifecycle_stage']}` / `{initiative['review_status']}`"
                for initiative in snapshot.child_initiatives
            ) or "- None."
            repository_lines = "\n".join(
                (
                    f"- `{entry['repository_role']}` / `{entry['repository_kind']}`:"
                    f" `{entry['repository_locator']}` (`active={entry['active']}`)"
                )
                for entry in repositories
            ) or "- None."
            active_initiative_count = sum(
                1
                for initiative in snapshot.child_initiatives
                if str(initiative["lifecycle_stage"]) not in _TERMINAL_INITIATIVE_STAGES
            )
            blocked_initiative_count = sum(
                1
                for initiative in snapshot.child_initiatives
                if str(initiative["lifecycle_stage"]) == "blocked"
                or bool(initiative.get("gate_state", {}).get("blocking_reasons"))
            )
            root = snapshot.project_root
            documents[f"{root}/project.md"] = "\n".join(
                (
                    f"# {project['title']} Project",
                    "",
                    "## Summary",
                    str(project["summary"]),
                    "",
                    "## Identity",
                    f"- `project_id`: `{project['project_id']}`",
                    f"- `slug`: `{project['slug']}`",
                    f"- `status`: `{project['status']}`",
                    f"- `initiative_root`: `{snapshot.initiative_root}`",
                    "",
                    "## Linked Repositories",
                    repository_lines,
                    "",
                )
            )
            documents[f"{root}/repositories.md"] = "\n".join(
                (
                    f"# {project['title']} Repositories",
                    "",
                    "## Repository Map",
                    repository_lines,
                    "",
                )
            )
            documents[f"{root}/summary.md"] = "\n".join(
                (
                    f"# {project['title']} Summary",
                    "",
                    "## Status",
                    f"- `status`: `{project['status']}`",
                    f"- `repository_count`: `{len(repositories)}`",
                    f"- `active_initiative_count`: `{active_initiative_count}`",
                    f"- `blocked_initiative_count`: `{blocked_initiative_count}`",
                    f"- `updated_at`: `{_snapshot_updated_at(snapshot)}`",
                    "",
                    "## Child Initiatives",
                    initiative_lines,
                    "",
                )
            )
        return documents

    def _load_project_snapshots(self) -> tuple[_ProjectSnapshot, ...]:
        projects_root = self._loader.repo_root / "plan" / "projects"
        if not projects_root.exists():
            return ()
        snapshots: list[_ProjectSnapshot] = []
        for project_path in sorted(projects_root.iterdir()):
            if not project_path.is_dir():
                continue
            project_state_path = project_path / ".wt" / "project.json"
            repository_map_path = project_path / ".wt" / "project_repository_map.json"
            if not project_state_path.exists() or not repository_map_path.exists():
                continue
            child_initiatives = tuple(
                json.loads(path.read_text(encoding="utf-8"))
                for path in sorted(project_path.glob("initiatives/*/.wt/initiative.json"))
            )
            snapshots.append(
                _ProjectSnapshot(
                    project_document=json.loads(project_state_path.read_text(encoding="utf-8")),
                    repository_map_document=json.loads(
                        repository_map_path.read_text(encoding="utf-8")
                    ),
                    child_initiatives=child_initiatives,
                    project_root=str(project_path.relative_to(self._loader.repo_root)),
                    initiative_root=str(
                        (project_path / "initiatives").relative_to(self._loader.repo_root)
                    ),
                )
            )
        return tuple(snapshots)

    def _serialize_project_entry(self, entry: PlanProjectIndexEntry) -> dict[str, object]:
        payload: dict[str, object] = {
            "project_id": entry.project_id,
            "slug": entry.slug,
            "title": entry.title,
            "summary": entry.summary,
            "status": entry.status,
            "project_root": entry.project_root,
            "initiative_root": entry.initiative_root,
            "repository_count": entry.repository_count,
            "active_initiative_count": entry.active_initiative_count,
            "blocked_initiative_count": entry.blocked_initiative_count,
            "linked_repository_roles": list(entry.linked_repository_roles),
            "updated_at": entry.updated_at,
        }
        if entry.repository_locators:
            payload["repository_locators"] = list(entry.repository_locators)
        return payload

    def _pack_loader(self) -> ControlPlaneLoader:
        return ControlPlaneLoader(
            self._loader.repo_root,
            active_pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def _load_json(self, relative_path: str) -> dict[str, object]:
        path = self._loader.repo_root / relative_path
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_markdown(self, relative_path: str, content: str) -> None:
        path = self._loader.repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{content.rstrip()}\n", encoding="utf-8")

    def _project_root(self, project_slug: str) -> Path:
        return self._loader.repo_root / "plan" / "projects" / project_slug

    def _project_root_relative(self, project_slug: str) -> str:
        return f"plan/projects/{project_slug}"

    def _project_initiative_root_relative(self, project_slug: str) -> str:
        return f"{self._project_root_relative(project_slug)}/initiatives"

    def _project_path(self, project_slug: str, suffix: str) -> str:
        return f"{self._project_root_relative(project_slug)}/{suffix}"


def _latest_timestamp(values: object) -> str:
    normalized = [value for value in values if isinstance(value, str) and value]
    return max(normalized, default=utc_timestamp_now())


def _snapshot_updated_at(snapshot: _ProjectSnapshot) -> str:
    documents = (snapshot.project_document, *snapshot.child_initiatives)
    return _latest_timestamp(_document_updated_at(document) for document in documents)


def _document_updated_at(document: dict[str, object]) -> str:
    updated_at = document.get("updated_at")
    if isinstance(updated_at, str) and updated_at:
        return updated_at
    created_at = document.get("created_at")
    if isinstance(created_at, str) and created_at:
        return created_at
    return ""


def _search_project_entries(
    entries: tuple[PlanProjectIndexEntry, ...],
    params: PlanProjectSearchParams,
) -> tuple[PlanProjectIndexEntry, ...]:
    project_id = normalize_optional_text(params.project_id)
    slug = normalize_optional_text(params.slug)
    status = normalize_optional_text(params.status)
    repository_role = normalize_optional_text(params.repository_role)
    matches: list[tuple[int, PlanProjectIndexEntry]] = []
    for entry in entries:
        if project_id is not None and normalize_text(entry.project_id) != project_id:
            continue
        if slug is not None and normalize_text(entry.slug) != slug:
            continue
        if status is not None and normalize_text(entry.status) != status:
            continue
        if repository_role is not None and repository_role not in {
            normalize_text(value) for value in entry.linked_repository_roles
        }:
            continue
        score = query_score(
            params.query,
            (
                entry.project_id,
                entry.slug,
                entry.title,
                entry.summary,
                entry.status,
                entry.project_root,
                entry.initiative_root,
                *entry.linked_repository_roles,
                *entry.repository_locators,
            ),
        )
        if score is None:
            continue
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1].project_id))
    selected = [entry for _, entry in matches]
    if params.limit is not None:
        selected = selected[: params.limit]
    return tuple(selected)
