"""Helpers for initiative-local live task state under the plan workspace."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_plan.workspace.service import PLAN_PACK_SETTINGS_PATH

TASK_STATE_SCHEMA_ID = "urn:watchtower:schema:artifacts:plan:task-state:v1"


@dataclass(frozen=True, slots=True)
class PlanTaskStateDocument:
    """One validated live task-state document with initiative context."""

    relative_path: str
    initiative_root: str
    initiative_id: str
    trace_id: str
    project_id: str | None
    initiative_title: str
    slug: str
    task_id: str
    title: str
    summary: str
    status: str
    task_status: str
    task_kind: str
    priority: str
    owner: str
    created_at: str
    updated_at: str
    depends_on: tuple[str, ...] = ()
    blocked_by: tuple[str, ...] = ()
    related_ids: tuple[str, ...] = ()
    applies_to: tuple[str, ...] = ()
    scope_items: tuple[str, ...] = ()
    done_when_items: tuple[str, ...] = ()
    github_repository: str | None = None
    github_issue_number: int | None = None
    github_issue_node_id: str | None = None
    github_project_owner: str | None = None
    github_project_owner_type: str | None = None
    github_project_number: int | None = None
    github_project_item_id: str | None = None
    github_synced_at: str | None = None

    @classmethod
    def from_documents(
        cls,
        *,
        relative_path: str,
        initiative_root: str,
        initiative_document: dict[str, object],
        task_document: dict[str, object],
    ) -> PlanTaskStateDocument:
        return cls(
            relative_path=relative_path,
            initiative_root=initiative_root,
            initiative_id=str(initiative_document["initiative_id"]),
            trace_id=str(initiative_document["trace_id"]),
            project_id=(
                str(initiative_document["project_id"])
                if initiative_document.get("project_id") is not None
                else None
            ),
            initiative_title=str(initiative_document["title"]),
            slug=str(task_document["slug"]),
            task_id=str(task_document["task_id"]),
            title=str(task_document["title"]),
            summary=str(task_document["summary"]),
            status=str(task_document["status"]),
            task_status=str(task_document["task_status"]),
            task_kind=str(task_document.get("task_kind", "feature")),
            priority=str(task_document["priority"]),
            owner=str(task_document["owner"]),
            created_at=str(task_document["created_at"]),
            updated_at=str(task_document["updated_at"]),
            depends_on=tuple(str(value) for value in task_document.get("dependency_task_ids", ())),
            blocked_by=tuple(str(value) for value in task_document.get("blocker_task_ids", ())),
            related_ids=tuple(str(value) for value in task_document.get("related_ids", ())),
            applies_to=tuple(str(value) for value in task_document.get("applies_to", ())),
            scope_items=tuple(str(value) for value in task_document.get("scope_items", ())),
            done_when_items=tuple(str(value) for value in task_document.get("done_when_items", ())),
            github_repository=_optional_str(task_document.get("github_repository")),
            github_issue_number=_optional_int(task_document.get("github_issue_number")),
            github_issue_node_id=_optional_str(task_document.get("github_issue_node_id")),
            github_project_owner=_optional_str(task_document.get("github_project_owner")),
            github_project_owner_type=_optional_str(task_document.get("github_project_owner_type")),
            github_project_number=_optional_int(task_document.get("github_project_number")),
            github_project_item_id=_optional_str(task_document.get("github_project_item_id")),
            github_synced_at=_optional_str(task_document.get("github_synced_at")),
        )

    @property
    def doc_path(self) -> str:
        """Compatibility alias for consumers that expect `doc_path`."""

        return self.relative_path


@dataclass(frozen=True, slots=True)
class PlanInitiativeState:
    """One initiative package root plus its machine state."""

    relative_root: str
    document: dict[str, object]

    @property
    def initiative_id(self) -> str:
        return str(self.document["initiative_id"])

    @property
    def trace_id(self) -> str:
        return str(self.document["trace_id"])

    @property
    def title(self) -> str:
        return str(self.document["title"])

    @property
    def project_id(self) -> str | None:
        value = self.document.get("project_id")
        return str(value) if value is not None else None


def iter_initiative_states(loader: ControlPlaneLoader) -> tuple[PlanInitiativeState, ...]:
    """Return every initiative package state currently present under `plan/**`."""

    pack_loader = _plan_loader(loader)
    states: list[PlanInitiativeState] = []
    for root in _initiative_roots(loader.repo_root):
        initiative_path = root / ".wt" / "initiative.json"
        if not initiative_path.exists():
            continue
        relative_path = str(initiative_path.relative_to(loader.repo_root))
        document = pack_loader.load_validated_document(relative_path)
        states.append(
            PlanInitiativeState(
                relative_root=str(root.relative_to(loader.repo_root)),
                document=document,
            )
        )
    states.sort(key=lambda item: item.relative_root)
    return tuple(states)


def find_initiative_by_trace_id(
    loader: ControlPlaneLoader,
    trace_id: str,
) -> PlanInitiativeState:
    """Return one initiative state by trace identifier."""

    for state in iter_initiative_states(loader):
        if state.trace_id == trace_id:
            return state
    raise ValueError(f"Unknown live initiative trace_id: {trace_id}")


def find_initiative_by_slug(
    loader: ControlPlaneLoader,
    initiative_slug: str,
) -> PlanInitiativeState:
    """Return one initiative state by initiative-root slug."""

    for state in iter_initiative_states(loader):
        if Path(state.relative_root).name == initiative_slug:
            return state
    raise ValueError(f"Unknown live initiative slug: {initiative_slug}")


def iter_task_documents(loader: ControlPlaneLoader) -> tuple[PlanTaskStateDocument, ...]:
    """Return every validated live task-state document across the plan workspace."""

    documents: list[PlanTaskStateDocument] = []
    for state in iter_initiative_states(loader):
        tasks_root = loader.repo_root / state.relative_root / ".wt" / "tasks"
        if not tasks_root.exists():
            continue
        for path in sorted(tasks_root.glob("*/task.json")):
            relative_path = str(path.relative_to(loader.repo_root))
            try:
                documents.append(load_task_document(loader, relative_path))
            except FileNotFoundError:
                # Task lifecycle updates can remove or replace a sibling task between discovery
                # and load; skip only the vanished path and keep surviving task state strict.
                continue
    _assert_unique_task_ids(documents)
    return tuple(documents)


def load_task_documents_by_id(
    loader: ControlPlaneLoader,
) -> dict[str, PlanTaskStateDocument]:
    """Return live task-state documents keyed by stable task ID."""

    return {document.task_id: document for document in iter_task_documents(loader)}


def load_task_document(
    loader: ControlPlaneLoader,
    relative_path: str,
) -> PlanTaskStateDocument:
    """Load one live task-state document by relative path."""

    normalized_path = relative_path.strip().lstrip("/")
    state = _initiative_for_task_path(loader, normalized_path)
    task_document = _plan_loader(loader).load_validated_document(normalized_path)
    return PlanTaskStateDocument.from_documents(
        relative_path=normalized_path,
        initiative_root=state.relative_root,
        initiative_document=state.document,
        task_document=task_document,
    )


def task_event_directory(relative_path: str) -> str:
    """Return the sibling event-stream directory for one live task-state path."""

    task_path = Path(relative_path)
    return str(task_path.parent / "events")


def write_task_document(
    loader: ControlPlaneLoader,
    relative_path: str,
    document: dict[str, object],
) -> None:
    """Write one live task-state document under the active plan workspace."""

    _plan_loader(loader).schema_store.validate_instance(document, schema_id=TASK_STATE_SCHEMA_ID)
    loader.artifact_store.write_json_object(relative_path, document)


def update_task_document(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    updates: dict[str, Any],
) -> bool:
    """Apply field updates to one live task-state document if any values changed."""

    plan_loader = _plan_loader(loader)
    normalized_path = relative_path.strip().lstrip("/")
    current = dict(plan_loader.load_validated_document(normalized_path))
    changed = False
    for key, value in updates.items():
        if value is None:
            if key in current:
                del current[key]
                changed = True
            continue
        if current.get(key) != value:
            current[key] = value
            changed = True
    if not changed:
        return False
    write_task_document(loader, normalized_path, current)
    return True


def _initiative_roots(repo_root: Path) -> tuple[Path, ...]:
    roots: list[Path] = []
    workspace_paths = PackWorkspacePaths.from_loader(
        ControlPlaneLoader(repo_root, active_pack_settings_path=PLAN_PACK_SETTINGS_PATH),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )

    pack_root = repo_root / workspace_paths.initiatives_root
    if pack_root.exists():
        roots.extend(path for path in sorted(pack_root.iterdir()) if path.is_dir())

    projects_root = repo_root / workspace_paths.projects_root
    if projects_root.exists():
        for project_root in sorted(path for path in projects_root.iterdir() if path.is_dir()):
            initiatives_root = project_root / "initiatives"
            if not initiatives_root.exists():
                continue
            roots.extend(path for path in sorted(initiatives_root.iterdir()) if path.is_dir())

    return tuple(roots)


def _initiative_for_task_path(
    loader: ControlPlaneLoader,
    relative_path: str,
) -> PlanInitiativeState:
    prefix, separator, _suffix = relative_path.partition("/.wt/tasks/")
    if not separator:
        raise ValueError(f"Task path is not under an initiative-local task root: {relative_path}")
    for state in iter_initiative_states(loader):
        if state.relative_root == prefix:
            return state
    raise ValueError(f"Unknown initiative root for task path: {relative_path}")


def _assert_unique_task_ids(documents: list[PlanTaskStateDocument]) -> None:
    seen: dict[str, str] = {}
    for document in documents:
        existing = seen.get(document.task_id)
        if existing is not None:
            raise ValueError(
                "Duplicate live task ID detected: "
                f"{document.task_id} in {existing} and {document.relative_path}"
            )
        seen[document.task_id] = document.relative_path


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) else None


def _optional_str(value: object) -> str | None:
    return str(value) if value is not None else None


def _plan_loader(loader: ControlPlaneLoader) -> ControlPlaneLoader:
    return loader.derive(active_pack_settings_path=PLAN_PACK_SETTINGS_PATH)


__all__ = [
    "PlanInitiativeState",
    "PlanTaskStateDocument",
    "TASK_STATE_SCHEMA_ID",
    "find_initiative_by_slug",
    "find_initiative_by_trace_id",
    "iter_initiative_states",
    "iter_task_documents",
    "load_task_document",
    "load_task_documents_by_id",
    "task_event_directory",
    "update_task_document",
    "write_task_document",
]
