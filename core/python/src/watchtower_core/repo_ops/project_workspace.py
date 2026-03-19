"""Project-container bootstrap, validation, rendered views, and query helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane import TerminologyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.path_ids import PlanPathIdHelper
from watchtower_core.control_plane.project_surface_policy import ProjectSurfacePolicyHelper
from watchtower_core.rebuild import (
    MarkdownReconciliationHelper,
    RebuildHarness,
    RebuildOutput,
    RebuildTargetSpec,
    RenderedViewBuilder,
    RenderedViewSpec,
)
from watchtower_core.repo_ops.artifact_index import (
    PLAN_ARTIFACT_INDEX_PATH,
    ArtifactIndexService,
)
from watchtower_core.repo_ops.project_context import (
    PLAN_PACK_SETTINGS_PATH,
    ProjectContext,
    load_project_context,
    validate_project_machine_state,
)
from watchtower_core.repo_ops.query.common import (
    normalize_optional_text,
    normalize_text,
    query_score,
)
from watchtower_core.utils.timestamps import utc_timestamp_now
from watchtower_core.validation import ValidationResult

PLAN_PROJECT_INDEX_PATH = "plan/.wt/indexes/project_index.json"
PROJECT_SURFACE_ID = "rendered.project.project"
PROJECT_REPOSITORIES_SURFACE_ID = "rendered.project.repositories"
PROJECT_SUMMARY_SURFACE_ID = "rendered.project.summary"

_ACTIVE_PROJECT_STATUSES = frozenset({"active", "planned"})


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
        self._vocabulary = TerminologyHelper.from_loader(
            loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._project_surface_policy = ProjectSurfacePolicyHelper.from_loader(
            loader,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._rendered_views = RenderedViewBuilder(loader)
        self._markdown_reconciliation = MarkdownReconciliationHelper(loader)

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
        project_id = params.project_id or PlanPathIdHelper.canonical_project_id(project_slug)
        if project_id != PlanPathIdHelper.canonical_project_id(project_slug):
            raise ValueError("project_id must use the canonical project.<slug> form.")

        project_root = self._project_root(project_slug)
        if project_root.exists():
            raise ValueError(
                f"Project root already exists: {project_root.relative_to(self._loader.repo_root)}"
            )

        repository_entries = []
        repository_refs = []
        for spec in params.repository_links:
            repository_id = spec.repository_id or PlanPathIdHelper.canonical_repository_id(
                project_slug,
                spec.repository_role,
            )
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
            "initiative_root": PlanPathIdHelper.project_initiatives_root_relative(
                project_slug
            ),
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

        validation = validate_project_machine_state(self._loader, project_slug)
        issues = list(validation.issue_messages)

        if not issues:
            derived_issues = self.expected_surface_issues(project_slug)
            issues.extend(issue.message for issue in derived_issues)

        return ProjectValidationResult(
            project_id=validation.project_id,
            project_root=validation.project_root,
            passed=not issues and all(result.passed for result in validation.artifact_results),
            issue_messages=tuple(issues),
            artifact_results=validation.artifact_results,
            wrote=write,
        )

    def load_project_context(self, project_slug: str) -> ProjectContext:
        """Load project-specific context on top of the always-loaded pack context."""

        return load_project_context(self._loader, project_slug)

    def sync(self, *, write: bool) -> ProjectWorkspaceSyncResult:
        """Rebuild the project index and project-local rendered views."""

        snapshots = self._load_project_snapshots()
        documents = self._build_documents(snapshots)
        artifact_index_document = ArtifactIndexService(self._loader).build_document(
            aggregate_overrides={
                PLAN_PROJECT_INDEX_PATH: documents["project_index"],
            }
        )
        rebuild_outputs = self._build_rebuild_outputs(documents, artifact_index_document)
        rebuild_result = RebuildHarness(self._loader).run_specs(
            (
                RebuildTargetSpec(
                    target="project-workspace",
                    build_outputs=lambda _loader: rebuild_outputs,
                ),
            ),
            write=write,
        )
        return ProjectWorkspaceSyncResult(
            project_count=len(snapshots),
            initiative_count=sum(len(snapshot.child_initiatives) for snapshot in snapshots),
            wrote=rebuild_result.wrote,
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
        required_rendered_paths = self._project_surface_policy.required_relative_paths(
            project_root,
            surface_kind="rendered_view",
        )
        expected_markdown = {
            relative_path: documents["project_views"].get(relative_path, "")
            for relative_path in required_rendered_paths
        }
        expected_json = {
            PLAN_PROJECT_INDEX_PATH: documents["project_index"],
            PLAN_ARTIFACT_INDEX_PATH: ArtifactIndexService(self._loader).build_document(
                aggregate_overrides={
                    PLAN_PROJECT_INDEX_PATH: documents["project_index"],
                }
            ),
        }

        issues: list[DerivedProjectSurfaceIssue] = []
        for issue in self._markdown_reconciliation.expected_issues(expected_markdown):
            issues.append(
                DerivedProjectSurfaceIssue(
                    category="stale_rendered_surface",
                    relative_path=issue.relative_output_path,
                    message=_project_markdown_issue_message(
                        issue.issue_code,
                        issue.relative_output_path,
                    ),
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
            if not self._vocabulary.is_terminal_lifecycle(str(initiative["lifecycle_stage"]))
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
                if not self._vocabulary.is_terminal_lifecycle(str(initiative["lifecycle_stage"]))
            )
            blocked_initiative_count = sum(
                1
                for initiative in snapshot.child_initiatives
                if str(initiative["lifecycle_stage"]) == "blocked"
                or bool(initiative.get("gate_state", {}).get("blocking_reasons"))
            )
            rendered_views = self._rendered_views.build_views(
                (
                    RenderedViewSpec(
                        surface_id=PROJECT_SURFACE_ID,
                        path_params={"project_slug": str(project["slug"])},
                        title=f"{project['title']} Project",
                        data={
                            "summary": (
                                "## Summary",
                                str(project["summary"]),
                            ),
                            "identity": (
                                "## Identity",
                                f"- `project_id`: `{project['project_id']}`",
                                f"- `slug`: `{project['slug']}`",
                                f"- `status`: `{project['status']}`",
                                f"- `initiative_root`: `{snapshot.initiative_root}`",
                            ),
                            "linked_repositories": (
                                "## Linked Repositories",
                                repository_lines,
                            ),
                        },
                    ),
                    RenderedViewSpec(
                        surface_id=PROJECT_REPOSITORIES_SURFACE_ID,
                        path_params={"project_slug": str(project["slug"])},
                        title=f"{project['title']} Repositories",
                        data={
                            "repository_map": (
                                "## Repository Map",
                                repository_lines,
                            ),
                        },
                    ),
                    RenderedViewSpec(
                        surface_id=PROJECT_SUMMARY_SURFACE_ID,
                        path_params={"project_slug": str(project["slug"])},
                        title=f"{project['title']} Summary",
                        data={
                            "status": (
                                "## Status",
                                f"- `status`: `{project['status']}`",
                                f"- `repository_count`: `{len(repositories)}`",
                                f"- `active_initiative_count`: `{active_initiative_count}`",
                                f"- `blocked_initiative_count`: `{blocked_initiative_count}`",
                                f"- `updated_at`: `{_snapshot_updated_at(snapshot)}`",
                            ),
                            "child_initiatives": (
                                "## Child Initiatives",
                                initiative_lines,
                            ),
                        },
                    ),
                )
            )
            for result in rendered_views:
                documents[result.relative_output_path] = result.content
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
        return self._loader.derive(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)

    def _build_rebuild_outputs(
        self,
        documents: dict[str, object],
        artifact_index_document: dict[str, object],
    ) -> tuple[RebuildOutput, ...]:
        project_views = documents["project_views"]
        assert isinstance(project_views, dict)
        outputs = (
            RebuildOutput(
                relative_output_path=PLAN_PROJECT_INDEX_PATH,
                artifact_kind="index",
                output_format="json",
                content=_json_document(documents["project_index"]),
                validated=True,
            ),
            RebuildOutput(
                relative_output_path=PLAN_ARTIFACT_INDEX_PATH,
                artifact_kind="index",
                output_format="json",
                content=artifact_index_document,
                validated=True,
            ),
        )
        return outputs + tuple(
            RebuildOutput(
                relative_output_path=relative_path,
                artifact_kind="rendered_view",
                output_format="markdown",
                content=_markdown_content(content),
            )
            for relative_path, content in sorted(project_views.items())
        )

    def _project_root(self, project_slug: str) -> Path:
        return self._loader.repo_root / "plan" / "projects" / project_slug

    def _project_root_relative(self, project_slug: str) -> str:
        return PlanPathIdHelper.project_root_relative(project_slug)

    def _project_initiative_root_relative(self, project_slug: str) -> str:
        return PlanPathIdHelper.project_initiatives_root_relative(project_slug)

    def _project_path(self, project_slug: str, suffix: str) -> str:
        return PlanPathIdHelper.join_relative(
            self._project_root_relative(project_slug),
            suffix,
        )


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


def _json_document(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return value


def _project_markdown_issue_message(issue_code: str, relative_path: str) -> str:
    if issue_code == "missing_expected_content":
        return (
            "Required project rendered surface is missing from the expected build: "
            f"{relative_path}."
        )
    if issue_code == "missing_output":
        return f"Required project rendered surface is missing: {relative_path}."
    return f"Project rendered surface drift detected for {relative_path}."


def _markdown_content(value: object) -> str:
    assert isinstance(value, str)
    return value


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
