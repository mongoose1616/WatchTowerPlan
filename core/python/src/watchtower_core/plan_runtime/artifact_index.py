"""Build and load the live plan artifact index."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from watchtower_core.control_plane.artifact_family import ArtifactFamilyHelper
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.models import ArtifactIndex, ArtifactIndexEntry
from watchtower_core.utils.timestamps import utc_timestamp_now

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"
PLAN_ARTIFACT_INDEX_PATH = "plan/.wt/indexes/artifact_index.json"


@dataclass(frozen=True, slots=True)
class ArtifactIndexSyncResult:
    """Summary of one artifact-index rebuild run."""

    artifact_count: int
    wrote: bool


class ArtifactIndexService:
    """Build and load the pack-wide artifact index for live plan artifacts."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._pack_loader_instance = loader.derive(
            active_pack_settings_path=PLAN_PACK_SETTINGS_PATH
        )
        self._workspace_paths = PackWorkspacePaths.from_loader(
            self._pack_loader_instance,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )
        self._artifact_index_path = self._workspace_paths.index_path("artifact_index.json")
        self._workspace_subdomain = Path(self._workspace_paths.workspace_root).name
        self._artifact_family = ArtifactFamilyHelper.from_loader(
            self._pack_loader_instance,
            pack_settings_path=PLAN_PACK_SETTINGS_PATH,
        )

    def sync(
        self,
        *,
        write: bool,
        aggregate_overrides: dict[str, dict[str, object]] | None = None,
    ) -> ArtifactIndexSyncResult:
        """Build the live artifact index and optionally persist it."""

        document = self.build_document(aggregate_overrides=aggregate_overrides)
        if write:
            self._loader.artifact_store.write_json_object(self._artifact_index_path, document)
        return ArtifactIndexSyncResult(
            artifact_count=len(document["artifacts"]),
            wrote=write,
        )

    def build_document(
        self,
        *,
        aggregate_overrides: dict[str, dict[str, object]] | None = None,
    ) -> dict[str, object]:
        """Return the current artifact-index document."""

        overrides = aggregate_overrides or {}
        records = self._load_records(overrides)
        initiative_by_id = {
            str(document["initiative_id"]): document
            for _, family_id, document in records
            if family_id == "initiative_state"
        }
        project_by_id = {
            str(document["project_id"]): document
            for _, family_id, document in records
            if family_id == "project_record"
        }
        existing_entries_by_artifact_id = self._existing_entries_by_artifact_id()

        artifacts = []
        for relative_path, family_id, document in records:
            artifact_id = _artifact_id(relative_path, document)
            artifacts.append(
                self._build_entry(
                relative_path,
                family_id,
                document,
                artifact_id=artifact_id,
                existing_entry=existing_entries_by_artifact_id.get(artifact_id),
                initiative_by_id=initiative_by_id,
                project_by_id=project_by_id,
            )
            )
        updated_at_candidates = [
            str(entry["updated_at"]) for entry in artifacts if entry.get("updated_at")
        ]
        updated_at = _latest_timestamp(updated_at_candidates or [utc_timestamp_now()])
        existing_index_entry = existing_entries_by_artifact_id.get("index.artifacts")
        artifacts.append(
            {
                "artifact_id": "index.artifacts",
                "artifact_family": "artifact_index",
                "path": self._artifact_index_path,
                "pack": self._workspace_paths.pack_id,
                "subdomain": self._workspace_subdomain,
                "context_ids": [self._workspace_paths.pack_id],
                "status": "active",
                "authoritative": True,
                "hidden": True,
                "derived": True,
                "created_at": _entry_timestamp(existing_index_entry, "created_at") or updated_at,
                "updated_at": _entry_timestamp(existing_index_entry, "updated_at") or updated_at,
                "title": f"{self._workspace_subdomain.title()} Artifact Index",
                "summary": (
                    f"Cross-family artifact lookup for the live {self._workspace_subdomain} "
                    "workspace."
                ),
                "source_context": self._workspace_paths.pack_id,
                "source_channel": "aggregate_index",
                "source_type": "artifact_index",
            }
        )

        document = {
            "$schema": "urn:watchtower:schema:interfaces:packs:artifact-index:v1",
            "surface_name": "artifact_index",
            "contract_version": "v1",
            "description": (
                f"Cross-family artifact lookup for the live {self._workspace_subdomain} "
                "workspace."
            ),
            "updated_at": updated_at,
            "artifacts": sorted(artifacts, key=lambda entry: str(entry["artifact_id"])),
        }
        self._pack_loader().schema_store.validate_instance(document)
        return document

    def load_index(self) -> ArtifactIndex:
        """Load the typed artifact index from the live plan workspace."""

        return self._pack_loader().load_artifact_index(self._artifact_index_path)

    def _load_records(
        self,
        overrides: dict[str, dict[str, object]],
    ) -> list[tuple[str, str, dict[str, object]]]:
        candidate_paths = set(overrides)
        candidate_paths.update(self._iter_relative_json_paths(self._workspace_paths.initiatives_root))
        candidate_paths.update(self._iter_relative_json_paths(self._workspace_paths.projects_root))
        candidate_paths.update(
            self._iter_relative_json_paths(self._workspace_paths.machine_path("work_items"))
        )
        candidate_paths.update(
            self._iter_relative_json_paths(self._workspace_paths.machine_path("indexes"))
        )
        records: list[tuple[str, str, dict[str, object]]] = []
        for relative_path in sorted(candidate_paths):
            if relative_path == self._artifact_index_path:
                continue
            try:
                family_entry = self._artifact_family.family_for_path(relative_path)
            except KeyError:
                continue
            if family_entry.family_id == "artifact_index":
                continue
            document = overrides.get(relative_path)
            if document is None:
                document = json.loads(
                    (self._loader.repo_root / relative_path).read_text(encoding="utf-8")
                )
            records.append((relative_path, family_entry.family_id, document))
        return records

    def _iter_relative_json_paths(self, relative_root: str) -> tuple[str, ...]:
        root = self._loader.repo_root / relative_root
        if not root.exists():
            return ()
        return tuple(
            sorted(
                path.relative_to(self._loader.repo_root).as_posix()
                for path in root.rglob("*.json")
                if path.is_file()
            )
        )

    def _build_entry(
        self,
        relative_path: str,
        family_id: str,
        document: dict[str, object],
        *,
        artifact_id: str,
        existing_entry: dict[str, object] | None,
        initiative_by_id: dict[str, dict[str, object]],
        project_by_id: dict[str, dict[str, object]],
    ) -> dict[str, object]:
        initiative_document = _linked_initiative_document(document, initiative_by_id)
        project_document = _linked_project_document(
            document,
            initiative_document=initiative_document,
            project_by_id=project_by_id,
        )
        context_ids = _context_ids(
            document,
            initiative_document=initiative_document,
            project_document=project_document,
            pack_context_id=self._workspace_paths.pack_id,
        )
        entry: dict[str, object] = {
            "artifact_id": artifact_id,
            "artifact_family": family_id,
            "path": relative_path,
            "pack": self._workspace_paths.pack_id,
            "subdomain": _subdomain(
                project_document,
                workspace_subdomain=self._workspace_subdomain,
            ),
            "context_ids": list(context_ids),
            "status": _artifact_status(family_id, document),
            "authoritative": True,
            "hidden": _is_hidden_artifact(
                relative_path,
                machine_root=self._workspace_paths.machine_root,
            ),
            "derived": _is_derived_artifact(
                relative_path,
                machine_root=self._workspace_paths.machine_root,
            ),
            "created_at": _artifact_created_at(document, existing_entry),
            "updated_at": _artifact_updated_at(document, existing_entry),
            "title": _artifact_title(family_id, document),
            "summary": _artifact_summary(family_id, document, self._artifact_family),
            "source_context": _source_context(
                document,
                initiative_document=initiative_document,
                project_document=project_document,
                pack_context_id=self._workspace_paths.pack_id,
            ),
            "source_channel": _source_channel(
                family_id,
                relative_path,
                machine_root=self._workspace_paths.machine_root,
            ),
            "source_type": family_id,
        }
        parent_artifact_id = _parent_artifact_id(family_id, document)
        if parent_artifact_id is not None:
            entry["parent_artifact_id"] = parent_artifact_id
        related_artifact_ids = _related_artifact_ids(family_id, document)
        if related_artifact_ids:
            entry["related_artifact_ids"] = list(related_artifact_ids)
        review_status = _string_value(document.get("review_status"))
        if review_status is None and initiative_document is not None:
            review_status = _string_value(initiative_document.get("review_status"))
        if review_status is not None:
            entry["review_status"] = review_status
        rendered_view_path = _rendered_view_path(
            relative_path,
            family_id=family_id,
            document=document,
            initiative_document=initiative_document,
            project_document=project_document,
            overview_path=self._workspace_paths.overview_path,
        )
        if rendered_view_path is not None:
            entry["rendered_view_path"] = rendered_view_path
        source_summary = _string_value(document.get("summary"))
        if source_summary is not None:
            entry["source_summary"] = source_summary
        return entry

    def _pack_loader(self) -> ControlPlaneLoader:
        return self._pack_loader_instance

    def _existing_entries_by_artifact_id(self) -> dict[str, dict[str, object]]:
        path = self._loader.repo_root / self._artifact_index_path
        if not path.exists():
            return {}
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        if not isinstance(document, dict):
            return {}
        artifacts = document.get("artifacts")
        if not isinstance(artifacts, list):
            return {}
        entries: dict[str, dict[str, object]] = {}
        for entry in artifacts:
            if not isinstance(entry, dict):
                continue
            artifact_id = _string_value(entry.get("artifact_id"))
            if artifact_id is None:
                continue
            entries[artifact_id] = entry
        return entries


def search_artifact_entries(
    entries: tuple[ArtifactIndexEntry, ...],
    *,
    query: str | None = None,
    artifact_id: str | None = None,
    artifact_family: str | None = None,
    context_id: str | None = None,
    source_context: str | None = None,
    source_channel: str | None = None,
    status: str | None = None,
    authoritative: bool | None = None,
    derived: bool | None = None,
    hidden: bool | None = None,
    limit: int | None = None,
) -> tuple[ArtifactIndexEntry, ...]:
    """Search artifact-index entries with deterministic ranking."""

    normalized_query = _normalize(query)
    normalized_artifact_id = _normalize(artifact_id)
    normalized_artifact_family = _normalize(artifact_family)
    normalized_context_id = _normalize(context_id)
    normalized_source_context = _normalize(source_context)
    normalized_source_channel = _normalize(source_channel)
    normalized_status = _normalize(status)

    matches: list[tuple[int, tuple[str, str], ArtifactIndexEntry]] = []
    for entry in entries:
        if normalized_artifact_id is not None and _normalize(entry.artifact_id) != normalized_artifact_id:
            continue
        if normalized_artifact_family is not None and _normalize(entry.artifact_family) != normalized_artifact_family:
            continue
        if normalized_context_id is not None and normalized_context_id not in {
            _normalize(value) for value in entry.context_ids
        }:
            continue
        if normalized_source_context is not None and _normalize(entry.source_context) != normalized_source_context:
            continue
        if normalized_source_channel is not None and _normalize(entry.source_channel) != normalized_source_channel:
            continue
        if normalized_status is not None and _normalize(entry.status) != normalized_status:
            continue
        if authoritative is not None and entry.authoritative is not authoritative:
            continue
        if derived is not None and entry.derived is not derived:
            continue
        if hidden is not None and entry.hidden is not hidden:
            continue

        score = _query_score(
            normalized_query,
            (
                entry.artifact_id,
                entry.artifact_family,
                entry.path,
                entry.subdomain or "",
                entry.title or "",
                entry.summary or "",
                entry.parent_artifact_id or "",
                entry.rendered_view_path or "",
                entry.review_status or "",
                entry.source_context or "",
                entry.source_channel or "",
                entry.source_summary or "",
                entry.source_ref or "",
                entry.source_type or "",
                *entry.context_ids,
                *entry.related_artifact_ids,
            ),
        )
        if score is None:
            continue
        matches.append((score, (entry.artifact_family, entry.artifact_id), entry))

    matches.sort(key=lambda item: (-item[0], item[1]))
    ordered = [entry for _, _, entry in matches]
    if limit is not None:
        ordered = ordered[:limit]
    return tuple(ordered)


def _artifact_id(relative_path: str, document: dict[str, object]) -> str:
    for field_name in (
        "initiative_id",
        "task_id",
        "event_id",
        "deferred_item_id",
        "discrepancy_id",
        "project_id",
        "id",
    ):
        value = _string_value(document.get(field_name))
        if value is not None:
            return value
    return "artifact." + relative_path.removesuffix(".json").replace("/", ".").replace("-", "_")


def _artifact_status(family_id: str, document: dict[str, object]) -> str:
    if family_id in {"initiative_event_stream", "task_event_stream"}:
        return _string_value(document.get("event_type")) or "recorded"
    return (
        _string_value(document.get("lifecycle_stage"))
        or _string_value(document.get("status"))
        or "active"
    )


def _artifact_created_at(
    document: dict[str, object],
    existing_entry: dict[str, object] | None,
) -> str:
    return (
        _string_value(document.get("created_at"))
        or _nested_updated_at(document)
        or _string_value(document.get("recorded_at"))
        or _string_value(document.get("updated_at"))
        or _entry_timestamp(existing_entry, "created_at")
        or _entry_timestamp(existing_entry, "updated_at")
        or utc_timestamp_now()
    )


def _artifact_updated_at(
    document: dict[str, object],
    existing_entry: dict[str, object] | None,
) -> str:
    return (
        _string_value(document.get("updated_at"))
        or _nested_updated_at(document)
        or _string_value(document.get("recorded_at"))
        or _string_value(document.get("created_at"))
        or _entry_timestamp(existing_entry, "updated_at")
        or _entry_timestamp(existing_entry, "created_at")
        or utc_timestamp_now()
    )


def _artifact_title(family_id: str, document: dict[str, object]) -> str:
    title = _string_value(document.get("title"))
    if title is not None:
        return title
    event_type = _string_value(document.get("event_type"))
    if event_type is not None:
        return event_type.replace("_", " ").title()
    return family_id.replace("_", " ").title()


def _artifact_summary(
    family_id: str,
    document: dict[str, object],
    helper: ArtifactFamilyHelper,
) -> str:
    return (
        _string_value(document.get("summary"))
        or _string_value(document.get("description"))
        or _string_value(document.get("expected_outcome"))
        or helper.family(family_id).summary
    )


def _parent_artifact_id(family_id: str, document: dict[str, object]) -> str | None:
    if family_id == "task_state":
        return _string_value(document.get("initiative_id"))
    if family_id == "task_event_stream":
        return _string_value(document.get("task_id"))
    if family_id in {
        "initiative_event_stream",
        "deferred_item_record",
        "validation_bundle",
        "closeout_recap",
        "discrepancy_record",
        "guidance_promotion_record",
    }:
        return _string_value(document.get("initiative_id"))
    if family_id == "project_repository_map":
        return _string_value(document.get("project_id"))
    return None


def _related_artifact_ids(family_id: str, document: dict[str, object]) -> tuple[str, ...]:
    if family_id == "initiative_state":
        return tuple(
            _unique_strings(
                (
                    *_string_list(document.get("task_ids")),
                    *_string_list(document.get("deferred_item_ids")),
                    *_string_list(document.get("discrepancy_ids")),
                    *_string_list(document.get("evidence_ids")),
                    *_string_list(document.get("promotion_ids")),
                    *_string_list(document.get("closeout_ids")),
                )
            )
        )
    if family_id == "task_state":
        return tuple(
            _unique_strings(
                (
                    *_string_list(document.get("dependency_task_ids")),
                    *_string_list(document.get("blocker_task_ids")),
                    *_string_list(document.get("related_ids")),
                )
            )
        )
    if family_id == "project_record":
        return tuple(_unique_strings(_string_list(document.get("linked_repository_refs"))))
    if family_id == "closeout_recap":
        return tuple(
            _unique_strings(
                (
                    *_string_list(document.get("acceptance_ids")),
                    *_string_list(document.get("evidence_ids")),
                )
            )
        )
    return ()


def _context_ids(
    document: dict[str, object],
    *,
    initiative_document: dict[str, object] | None,
    project_document: dict[str, object] | None,
    pack_context_id: str,
) -> tuple[str, ...]:
    values = list(
        _unique_strings(
            (
                _string_value(document.get("initiative_id")),
                _string_value(document.get("trace_id")),
                _string_value(document.get("task_id")),
                _string_value(document.get("work_item_id")),
                _string_value(document.get("project_id")),
                _string_value(initiative_document.get("initiative_id")) if initiative_document else None,
                _string_value(initiative_document.get("trace_id")) if initiative_document else None,
                _string_value(initiative_document.get("project_id")) if initiative_document else None,
                _string_value(project_document.get("project_id")) if project_document else None,
                pack_context_id,
            )
        )
    )
    return tuple(values)


def _source_context(
    document: dict[str, object],
    *,
    initiative_document: dict[str, object] | None,
    project_document: dict[str, object] | None,
    pack_context_id: str,
) -> str:
    if initiative_document is not None:
        return _string_value(initiative_document.get("initiative_id")) or pack_context_id
    if project_document is not None:
        return _string_value(project_document.get("project_id")) or pack_context_id
    work_item_id = _string_value(document.get("work_item_id"))
    if work_item_id is not None:
        return work_item_id
    return pack_context_id


def _source_channel(family_id: str, relative_path: str, *, machine_root: str) -> str:
    if relative_path.startswith(f"{machine_root}/indexes/"):
        return "aggregate_index"
    if family_id == "pack_work_item_note":
        return "pack_work_item"
    if family_id in {"project_record", "project_repository_map"}:
        return "project_container"
    if family_id in {"initiative_event_stream", "task_event_stream"}:
        return "event_stream"
    return "initiative_package"


def _rendered_view_path(
    relative_path: str,
    *,
    family_id: str,
    document: dict[str, object],
    initiative_document: dict[str, object] | None,
    project_document: dict[str, object] | None,
    overview_path: str,
) -> str | None:
    if family_id == "initiative_state":
        return f"{Path(relative_path).parents[1].as_posix()}/plan.md"
    if family_id == "project_record":
        return f"{Path(relative_path).parents[1].as_posix()}/project.md"
    if family_id == "coordination_index":
        return overview_path
    if family_id == "closeout_recap" and initiative_document is not None:
        initiative_root = Path(relative_path).parents[2].as_posix()
        return f"{initiative_root}/summary.md"
    return None


def _linked_initiative_document(
    document: dict[str, object],
    initiative_by_id: dict[str, dict[str, object]],
) -> dict[str, object] | None:
    initiative_id = _string_value(document.get("initiative_id"))
    if initiative_id is None:
        return None
    return initiative_by_id.get(initiative_id)


def _linked_project_document(
    document: dict[str, object],
    *,
    initiative_document: dict[str, object] | None,
    project_by_id: dict[str, dict[str, object]],
) -> dict[str, object] | None:
    project_id = _string_value(document.get("project_id"))
    if project_id is None and initiative_document is not None:
        project_id = _string_value(initiative_document.get("project_id"))
    if project_id is None:
        return None
    return project_by_id.get(project_id)


def _subdomain(project_document: dict[str, object] | None, *, workspace_subdomain: str) -> str:
    if project_document is None:
        return workspace_subdomain
    return _string_value(project_document.get("project_id")) or workspace_subdomain


def _is_hidden_artifact(relative_path: str, *, machine_root: str) -> bool:
    return relative_path.startswith(f"{machine_root}/") or "/.wt/" in relative_path


def _is_derived_artifact(relative_path: str, *, machine_root: str) -> bool:
    return relative_path.startswith(f"{machine_root}/indexes/")


def _string_value(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _entry_timestamp(entry: dict[str, object] | None, field_name: str) -> str | None:
    if entry is None:
        return None
    return _string_value(entry.get(field_name))


def _string_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value if isinstance(item, str) and item)


def _nested_updated_at(document: dict[str, object]) -> str | None:
    entries = document.get("entries")
    if not isinstance(entries, list):
        return None
    timestamps = [
        str(value)
        for entry in entries
        if isinstance(entry, dict)
        for value in (entry.get("updated_at"),)
        if isinstance(value, str) and value
    ]
    if not timestamps:
        return None
    return max(timestamps)


def _unique_strings(values: tuple[str | None, ...] | tuple[str, ...] | list[str | None]) -> tuple[str, ...]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str) or not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def _latest_timestamp(values: list[str]) -> str:
    cleaned = [value for value in values if value]
    if not cleaned:
        return utc_timestamp_now()
    return max(cleaned)


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.casefold().strip()
    return normalized or None


def _query_score(query: str | None, fields: tuple[str, ...]) -> int | None:
    normalized_query = _normalize(query)
    if normalized_query is None:
        return 0
    tokens = [token for token in normalized_query.split() if token]
    if not tokens:
        return 0
    haystacks = [_normalize(field) for field in fields if field]
    haystacks = [field for field in haystacks if field is not None]
    score = 0
    for token in tokens:
        token_score = 0
        for haystack in haystacks:
            if haystack == token:
                token_score = max(token_score, 12)
            elif haystack.startswith(token):
                token_score = max(token_score, 8)
            elif token in haystack:
                token_score = max(token_score, 4)
        if token_score == 0:
            return None
        score += token_score
    return score


__all__ = [
    "ArtifactIndexService",
    "ArtifactIndexSyncResult",
    "PLAN_ARTIFACT_INDEX_PATH",
    "search_artifact_entries",
]
