"""Deterministic rebuild helpers for the workflow index."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from watchtower_core.adapters import (
    extract_external_urls,
    extract_first_paragraph,
    extract_repo_path_references,
    extract_sections,
    extract_title,
    load_markdown_body,
)
from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.models import WorkflowMetadataDefinition
from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.documentation.governed_documents import (
    ordered_unique,
    validate_explained_bullet_section,
    validate_required_section_order,
)
from watchtower_core.documentation.markdown_semantics import (
    validate_blank_line_before_heading_after_list,
)
from watchtower_core.pack_integration.roots import (
    discover_pack_workspace_roots,
    pack_routing_table_paths,
    pack_workflow_module_roots,
    pack_workflow_role_roots,
)
from watchtower_core.sync.reference_resolution import build_reference_urls_by_path

WORKFLOW_INDEX_ARTIFACT_PATH = "core/control_plane/indexes/workflows/workflow_index.json"
CORE_WORKFLOW_MODULE_ROOT = "core/workflows/modules"
CORE_WORKFLOW_ROLE_ROOT = "core/workflows/roles"
WORKFLOW_EXCLUDED_NAMES = {"README.md"}
WORKFLOW_REQUIRED_SECTIONS = (
    "Purpose",
    "Use When",
    "Inputs",
    "Workflow",
    "Data Structure",
    "Outputs",
    "Done When",
)
WORKFLOW_ROLE_REQUIRED_SECTIONS = (
    "Purpose",
    "Use When",
    "Inputs",
    "Composes Modules",
    "Workflow",
    "Data Structure",
    "Outputs",
    "Done When",
)
WORKFLOW_ADDITIONAL_LOAD_SECTION = "Additional Files to Load"
WORKFLOW_COMPOSES_MODULES_SECTION = "Composes Modules"
WORKFLOW_MAX_ADDITIONAL_LOAD_BULLETS = 5
WORKFLOW_STATIC_DISALLOWED_ADDITIONAL_LOAD_PATHS = {
    "AGENTS.md",
    "core/workflows/ROUTING_TABLE.md",
    "core/workflows/modules/core.md",
    "core/docs/standards/workflows/workflow_design_standard.md",
    "core/docs/standards/workflows/routing_and_context_loading_standard.md",
    "core/docs/standards/documentation/workflow_md_standard.md",
}
WORKFLOW_TRIGGER_TAG_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "for",
    "from",
    "in",
    "into",
    "of",
    "or",
    "the",
    "this",
    "to",
    "use",
    "when",
    "workflow",
}
WORKFLOW_REFERENCE_DOC_PATH_PATTERN = re.compile(
    r"^(?:core|[^/]+|packs/[^/]+)/docs/references/.+\.md$"
)
CORE_SHARED_WORKFLOW_ROOTS = (
    CORE_WORKFLOW_MODULE_ROOT,
    CORE_WORKFLOW_ROLE_ROOT,
)
CORE_SHARED_WORKFLOW_ALLOWED_REFERENCE_PREFIX = "core/"
CORE_SHARED_ROLE_ALLOWED_MODULE_ROOT = CORE_WORKFLOW_MODULE_ROOT
CORE_SHARED_WORKFLOW_DISALLOWED_LANGUAGE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\btrace_id\b", re.IGNORECASE), "trace_id"),
    (re.compile(r"\binitiative\b", re.IGNORECASE), "initiative"),
    (
        re.compile(r"\bcoordination (?:index|tracker)\b", re.IGNORECASE),
        "coordination index or coordination tracker",
    ),
    (
        re.compile(r"\btraceability (?:state|view)\b", re.IGNORECASE),
        "traceability state or traceability view",
    ),
)


@dataclass(frozen=True, slots=True)
class WorkflowDocument:
    """Parsed and validated workflow document used for indexing and validation."""

    workflow_id: str
    workflow_kind: str
    title: str
    summary: str
    relative_path: str
    phase_type: str
    task_family: str
    uses_internal_references: bool
    uses_external_references: bool
    primary_risks: tuple[str, ...]
    trigger_tags: tuple[str, ...]
    companion_workflow_ids: tuple[str, ...]
    composes_module_paths: tuple[str, ...]
    related_paths: tuple[str, ...]
    reference_doc_paths: tuple[str, ...]
    internal_reference_paths: tuple[str, ...]
    external_reference_urls: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class WorkflowDocumentContext:
    """Precomputed metadata and reference-resolution context for workflow loading."""

    metadata_by_workflow_id: dict[str, WorkflowMetadataDefinition]
    reference_urls_by_path: dict[str, tuple[str, ...]]
    routing_table_paths: tuple[str, ...]
    workflow_module_roots: tuple[str, ...]
    shared_core_disallowed_pack_root_tokens: tuple[str, ...]


def _workflow_kind_for_path(relative_path: str) -> str:
    if "/workflows/modules/" in relative_path:
        return "module"
    if "/workflows/roles/" in relative_path:
        return "role"
    raise ValueError(f"{relative_path} is not under a governed workflow root.")


def _workflow_title_suffix(workflow_kind: str) -> str:
    if workflow_kind == "module":
        return " Workflow"
    if workflow_kind == "role":
        return " Role"
    raise ValueError(f"Unsupported workflow kind: {workflow_kind}")


def _is_core_shared_workflow_path(relative_path: str) -> bool:
    return any(relative_path.startswith(f"{root}/") for root in CORE_SHARED_WORKFLOW_ROOTS)


def _is_reference_doc_path(path: str) -> bool:
    return bool(WORKFLOW_REFERENCE_DOC_PATH_PATTERN.match(path))


def _derive_trigger_tags(
    workflow_id: str,
    title: str,
    summary: str,
    related_paths: tuple[str, ...],
    reference_doc_paths: tuple[str, ...],
    extra_tags: tuple[str, ...],
) -> tuple[str, ...]:
    tokens: list[str] = []
    for source in (workflow_id, title, summary, *related_paths, *reference_doc_paths, *extra_tags):
        tokens.extend(re.findall(r"[a-z0-9]+", source.casefold()))
    filtered_tokens = tuple(
        token for token in tokens if len(token) > 2 and token not in WORKFLOW_TRIGGER_TAG_STOPWORDS
    )
    return ordered_unique(filtered_tokens)


def validate_workflow_additional_load_section(
    relative_path: str,
    section: str | None,
    *,
    repo_root: Path,
    source_path: Path | None = None,
    routing_table_paths: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    """Validate and return task-specific extra files to load for one workflow."""
    if section is None:
        return ()

    validate_explained_bullet_section(relative_path, WORKFLOW_ADDITIONAL_LOAD_SECTION, section)

    bullets = [line.strip() for line in section.splitlines() if line.strip().startswith("- ")]
    if len(bullets) > WORKFLOW_MAX_ADDITIONAL_LOAD_BULLETS:
        raise ValueError(
            f"{relative_path} section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} must not contain "
            f"more than {WORKFLOW_MAX_ADDITIONAL_LOAD_BULLETS} bullets."
        )
    if extract_external_urls(section):
        raise ValueError(
            f"{relative_path} section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} must point to "
            "repo-local files, not raw external URLs."
        )

    resolved_paths: list[str] = []
    for bullet in bullets:
        bullet_paths = extract_repo_path_references(
            bullet,
            repo_root,
            source_path=source_path,
        )
        if len(bullet_paths) != 1:
            raise ValueError(
                f"{relative_path} section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} must give "
                "exactly one repo-local file reference per bullet."
            )
        resolved_paths.extend(bullet_paths)

    additional_paths = ordered_unique(tuple(resolved_paths))
    if len(additional_paths) != len(resolved_paths):
        raise ValueError(
            f"{relative_path} section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} must not repeat the "
            "same repo-local file in multiple bullets."
        )

    disallowed_paths = [
        path
        for path in additional_paths
        if path
        in (
            WORKFLOW_STATIC_DISALLOWED_ADDITIONAL_LOAD_PATHS
            | set(
                routing_table_paths
                if routing_table_paths is not None
                else pack_routing_table_paths(repo_root)
            )
        )
    ]
    if disallowed_paths:
        joined = ", ".join(disallowed_paths)
        raise ValueError(
            f"{relative_path} section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} repeats "
            f"routing-baseline files that should stay implicit: {joined}"
        )
    return additional_paths


def validate_workflow_section_order(
    relative_path: str,
    sections: dict[str, str],
    workflow_kind: str,
) -> None:
    """Validate required workflow section order plus optional additional-load placement."""
    if workflow_kind == "role":
        validate_required_section_order(relative_path, sections, WORKFLOW_ROLE_REQUIRED_SECTIONS)
    else:
        validate_required_section_order(relative_path, sections, WORKFLOW_REQUIRED_SECTIONS)
        if WORKFLOW_COMPOSES_MODULES_SECTION in sections:
            raise ValueError(
                f"{relative_path} must not define section "
                f"{WORKFLOW_COMPOSES_MODULES_SECTION!r} outside workflow role roots."
            )
    if WORKFLOW_ADDITIONAL_LOAD_SECTION not in sections:
        return

    section_order = list(sections.keys())
    additional_index = section_order.index(WORKFLOW_ADDITIONAL_LOAD_SECTION)
    workflow_index = section_order.index("Workflow")
    if workflow_kind == "role":
        composition_index = section_order.index(WORKFLOW_COMPOSES_MODULES_SECTION)
        if not composition_index < additional_index < workflow_index:
            raise ValueError(
                f"{relative_path} places optional section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} "
                "outside the allowed position between 'Composes Modules' and 'Workflow'."
            )
        return

    inputs_index = section_order.index("Inputs")
    if not inputs_index < additional_index < workflow_index:
        raise ValueError(
            f"{relative_path} places optional section {WORKFLOW_ADDITIONAL_LOAD_SECTION!r} "
            "outside the allowed position between 'Inputs' and 'Workflow'."
        )


def validate_core_shared_workflow_boundary(
    relative_path: str,
    markdown: str,
    *,
    loader: ControlPlaneLoader,
    internal_reference_paths: tuple[str, ...],
    composes_module_paths: tuple[str, ...],
    disallowed_pack_root_tokens: tuple[str, ...] | None = None,
) -> None:
    """Fail closed when shared core workflow docs depend on pack-owned surfaces."""

    if not _is_core_shared_workflow_path(relative_path):
        return

    disallowed_reference_paths = tuple(
        path
        for path in internal_reference_paths
        if not path.startswith(CORE_SHARED_WORKFLOW_ALLOWED_REFERENCE_PREFIX)
    )
    if disallowed_reference_paths:
        joined = ", ".join(disallowed_reference_paths)
        raise ValueError(
            f"{relative_path} shared core workflow docs must keep "
            f"{WORKFLOW_ADDITIONAL_LOAD_SECTION!r} under "
            f"{CORE_SHARED_WORKFLOW_ALLOWED_REFERENCE_PREFIX} "
            f"and out of pack-owned roots: {joined}"
        )

    disallowed_composed_paths = tuple(
        path
        for path in composes_module_paths
        if not path.startswith(f"{CORE_SHARED_ROLE_ALLOWED_MODULE_ROOT}/")
    )
    if disallowed_composed_paths:
        joined = ", ".join(disallowed_composed_paths)
        raise ValueError(
            f"{relative_path} shared core workflow roles must compose only modules under "
            f"{CORE_SHARED_ROLE_ALLOWED_MODULE_ROOT}/: {joined}"
        )

    for token in (
        disallowed_pack_root_tokens
        if disallowed_pack_root_tokens is not None
        else _shared_core_disallowed_pack_root_tokens(loader.repo_root, loader=loader)
    ):
        if token not in markdown:
            continue
        raise ValueError(
            f"{relative_path} shared core workflow docs must not reference pack-owned roots "
            f"such as {token!r}; move that repository-local logic into the "
            "owning pack workflow root."
        )

    for pattern, label in CORE_SHARED_WORKFLOW_DISALLOWED_LANGUAGE_PATTERNS:
        if pattern.search(markdown) is None:
            continue
        raise ValueError(
            f"{relative_path} shared core workflow docs must not require pack-specific "
            f"coordination language such as {label!r}; move that tracked-work logic into "
            "the owning pack workflow root."
        )


def validate_workflow_composes_modules_section(
    relative_path: str,
    section: str | None,
    *,
    workflow_kind: str,
    loader: ControlPlaneLoader,
    source_path: Path | None = None,
    workflow_module_roots: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    """Validate and return explicit role-to-module composition links."""
    if workflow_kind != "role":
        if section is not None:
            raise ValueError(
                f"{relative_path} must not define section "
                f"{WORKFLOW_COMPOSES_MODULES_SECTION!r} outside workflow role roots."
            )
        return ()

    validate_explained_bullet_section(relative_path, WORKFLOW_COMPOSES_MODULES_SECTION, section)
    if extract_external_urls(section or ""):
        raise ValueError(
            f"{relative_path} section {WORKFLOW_COMPOSES_MODULES_SECTION!r} must point to "
            "repo-local workflow modules, not raw external URLs."
        )

    bullets = [
        line.strip()
        for line in (section or "").splitlines()
        if line.strip().startswith("- ")
    ]
    resolved_paths: list[str] = []
    for bullet in bullets:
        module_paths = extract_repo_path_references(
            bullet,
            loader.repo_root,
            source_path=source_path,
        )
        if len(module_paths) != 1:
            raise ValueError(
                f"{relative_path} section {WORKFLOW_COMPOSES_MODULES_SECTION!r} must give "
                "exactly one workflow-module path per bullet."
            )
        resolved_paths.extend(module_paths)

    composed_module_paths = ordered_unique(tuple(resolved_paths))
    if len(composed_module_paths) != len(resolved_paths):
        raise ValueError(
            f"{relative_path} section {WORKFLOW_COMPOSES_MODULES_SECTION!r} must not repeat "
            "the same workflow-module path in multiple bullets."
        )

    module_roots = (
        workflow_module_roots
        if workflow_module_roots is not None
        else (
            CORE_WORKFLOW_MODULE_ROOT,
            *pack_workflow_module_roots(loader.repo_root, loader=loader),
        )
    )
    invalid_paths = [
        path
        for path in composed_module_paths
        if not any(path == root or path.startswith(f"{root}/") for root in module_roots)
        or path.endswith("/README.md")
    ]
    if invalid_paths:
        joined = ", ".join(invalid_paths)
        raise ValueError(
            f"{relative_path} section {WORKFLOW_COMPOSES_MODULES_SECTION!r} must cite only "
            f"workflow-module documents under governed module roots: {joined}"
        )
    return composed_module_paths


def build_workflow_document_context(
    loader: ControlPlaneLoader,
    *,
    reference_urls_by_path: dict[str, tuple[str, ...]] | None = None,
) -> WorkflowDocumentContext:
    """Build the reusable context needed to load workflow documents."""

    metadata_registry = loader.load_workflow_metadata_registry()
    return WorkflowDocumentContext(
        metadata_by_workflow_id={entry.workflow_id: entry for entry in metadata_registry.entries},
        reference_urls_by_path=(
            build_reference_urls_by_path(loader)
            if reference_urls_by_path is None
            else reference_urls_by_path
        ),
        routing_table_paths=pack_routing_table_paths(loader.repo_root, loader=loader),
        workflow_module_roots=(
            CORE_WORKFLOW_MODULE_ROOT,
            *pack_workflow_module_roots(loader.repo_root, loader=loader),
        ),
        shared_core_disallowed_pack_root_tokens=_shared_core_disallowed_pack_root_tokens(
            loader.repo_root,
            loader=loader,
        ),
    )


def _shared_core_disallowed_pack_root_tokens(
    repo_root: Path,
    *,
    loader: ControlPlaneLoader,
) -> tuple[str, ...]:
    tokens = {
        f"{roots.workspace_root.rstrip('/')}/"
        for roots in discover_pack_workspace_roots(repo_root, loader=loader)
        if roots.workspace_root
    }
    if any(token.startswith("packs/") for token in tokens):
        tokens.add("packs/")
    return tuple(sorted(tokens))


def load_workflow_document(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    context: WorkflowDocumentContext | None = None,
) -> WorkflowDocument:
    """Load and validate one workflow document from its repository-relative path."""
    workflow_context = context or build_workflow_document_context(loader)
    return load_workflow_document_with_reference_map(
        loader,
        relative_path,
        metadata_by_workflow_id=workflow_context.metadata_by_workflow_id,
        reference_urls_by_path=workflow_context.reference_urls_by_path,
        routing_table_paths=workflow_context.routing_table_paths,
        workflow_module_roots=workflow_context.workflow_module_roots,
        shared_core_disallowed_pack_root_tokens=(
            workflow_context.shared_core_disallowed_pack_root_tokens
        ),
    )


def load_workflow_document_with_reference_map(
    loader: ControlPlaneLoader,
    relative_path: str,
    *,
    metadata_by_workflow_id: dict[str, WorkflowMetadataDefinition],
    reference_urls_by_path: dict[str, tuple[str, ...]],
    routing_table_paths: tuple[str, ...] | None = None,
    workflow_module_roots: tuple[str, ...] | None = None,
    shared_core_disallowed_pack_root_tokens: tuple[str, ...] | None = None,
) -> WorkflowDocument:
    """Load and validate one workflow document using a prebuilt reference-url map."""
    path = loader.repo_root / relative_path
    markdown = load_markdown_body(path)
    validate_blank_line_before_heading_after_list(relative_path, markdown)
    title = extract_title(markdown)
    sections = extract_sections(markdown)
    workflow_kind = _workflow_kind_for_path(relative_path)

    missing_sections = [
        section
        for section in (
            WORKFLOW_ROLE_REQUIRED_SECTIONS
            if workflow_kind == "role"
            else WORKFLOW_REQUIRED_SECTIONS
        )
        if section not in sections
    ]
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{relative_path} is missing required sections: {joined}")
    validate_workflow_section_order(relative_path, sections, workflow_kind)
    composes_module_paths = validate_workflow_composes_modules_section(
        relative_path,
        sections.get(WORKFLOW_COMPOSES_MODULES_SECTION),
        workflow_kind=workflow_kind,
        loader=loader,
        source_path=path,
        workflow_module_roots=workflow_module_roots,
    )
    internal_reference_paths = validate_workflow_additional_load_section(
        relative_path,
        sections.get(WORKFLOW_ADDITIONAL_LOAD_SECTION),
        repo_root=loader.repo_root,
        source_path=path,
        routing_table_paths=routing_table_paths,
    )
    title_suffix = _workflow_title_suffix(workflow_kind)
    if not title.endswith(title_suffix):
        raise ValueError(
            f"{relative_path} {workflow_kind} title must end with {title_suffix!r}."
        )

    validate_core_shared_workflow_boundary(
        relative_path,
        markdown,
        loader=loader,
        internal_reference_paths=internal_reference_paths,
        composes_module_paths=composes_module_paths,
        disallowed_pack_root_tokens=shared_core_disallowed_pack_root_tokens,
    )

    summary = extract_first_paragraph(sections["Purpose"])
    reference_doc_paths = tuple(
        value for value in internal_reference_paths if _is_reference_doc_path(value)
    )

    direct_external_urls: tuple[str, ...] = ()
    transitive_external_urls = ordered_unique(
        *(reference_urls_by_path.get(reference_path, ()) for reference_path in reference_doc_paths)
    )
    external_reference_urls = ordered_unique(direct_external_urls, transitive_external_urls)
    workflow_id = _resolve_workflow_id(relative_path, metadata_by_workflow_id)
    try:
        retrieval_metadata = metadata_by_workflow_id[workflow_id]
    except KeyError as exc:
        raise ValueError(f"Workflow retrieval metadata is missing for {workflow_id}.") from exc

    return WorkflowDocument(
        workflow_id=workflow_id,
        workflow_kind=workflow_kind,
        title=title,
        summary=summary,
        relative_path=relative_path,
        phase_type=retrieval_metadata.phase_type,
        task_family=retrieval_metadata.task_family,
        uses_internal_references=bool(internal_reference_paths),
        uses_external_references=bool(external_reference_urls),
        primary_risks=retrieval_metadata.primary_risks,
        trigger_tags=_derive_trigger_tags(
            workflow_id,
            title,
            summary,
            internal_reference_paths,
            reference_doc_paths,
            retrieval_metadata.extra_trigger_tags,
        ),
        companion_workflow_ids=retrieval_metadata.companion_workflow_ids,
        composes_module_paths=composes_module_paths,
        related_paths=internal_reference_paths,
        reference_doc_paths=reference_doc_paths,
        internal_reference_paths=internal_reference_paths,
        external_reference_urls=external_reference_urls,
    )


def _resolve_workflow_id(
    relative_path: str,
    metadata_by_workflow_id: dict[str, WorkflowMetadataDefinition],
) -> str:
    stem = Path(relative_path).stem
    default_workflow_id = f"workflow.{stem}"
    if default_workflow_id in metadata_by_workflow_id:
        return default_workflow_id

    suffix = f".{stem}"
    matches = sorted(
        workflow_id for workflow_id in metadata_by_workflow_id if workflow_id.endswith(suffix)
    )
    if len(matches) == 1:
        return matches[0]
    if not matches:
        return default_workflow_id
    raise ValueError(
        f"Workflow retrieval metadata is ambiguous for {relative_path}: "
        + ", ".join(matches)
    )


def _load_existing_entries(loader: ControlPlaneLoader) -> dict[str, dict[str, Any]]:
    try:
        document = loader.load_json_object(WORKFLOW_INDEX_ARTIFACT_PATH)
    except ArtifactLoadError:
        return {}

    entries = document.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{WORKFLOW_INDEX_ARTIFACT_PATH} is missing its entries list.")

    existing: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        workflow_id = entry.get("workflow_id")
        if isinstance(workflow_id, str):
            existing[workflow_id] = entry
    return existing


class WorkflowIndexSyncService:
    """Build and write the workflow index from workflow documents."""

    def __init__(self, loader: ControlPlaneLoader) -> None:
        self._loader = loader
        self._repo_root = loader.repo_root
        self._reference_urls_by_path: dict[str, tuple[str, ...]] | None = None

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> WorkflowIndexSyncService:
        return cls(ControlPlaneLoader(discover_repo_root(repo_root)))

    def set_reference_urls_by_path(
        self,
        reference_urls_by_path: dict[str, tuple[str, ...]],
    ) -> None:
        """Provide precomputed reference-resolution data for aggregate sync reuse."""

        self._reference_urls_by_path = reference_urls_by_path

    def build_document(self) -> dict[str, object]:
        existing_entries = _load_existing_entries(self._loader)
        workflow_context = build_workflow_document_context(
            self._loader,
            reference_urls_by_path=self._reference_urls_by_path,
        )
        entries: list[dict[str, object]] = []

        seen_workflow_ids: set[str] = set()
        workflow_roots = (
            CORE_WORKFLOW_MODULE_ROOT,
            CORE_WORKFLOW_ROLE_ROOT,
            *pack_workflow_module_roots(self._repo_root, loader=self._loader),
            *pack_workflow_role_roots(self._repo_root, loader=self._loader),
        )
        for workflow_root_relative in workflow_roots:
            workflow_root = self._repo_root / workflow_root_relative
            if not workflow_root.exists():
                continue

            for path in sorted(workflow_root.rglob("*.md")):
                if path.name in WORKFLOW_EXCLUDED_NAMES:
                    continue

                relative_path = path.relative_to(self._repo_root).as_posix()
                workflow = load_workflow_document_with_reference_map(
                    self._loader,
                    relative_path,
                    metadata_by_workflow_id=workflow_context.metadata_by_workflow_id,
                    reference_urls_by_path=workflow_context.reference_urls_by_path,
                    routing_table_paths=workflow_context.routing_table_paths,
                    workflow_module_roots=workflow_context.workflow_module_roots,
                    shared_core_disallowed_pack_root_tokens=(
                        workflow_context.shared_core_disallowed_pack_root_tokens
                    ),
                )
                if workflow.workflow_id in seen_workflow_ids:
                    raise ValueError(
                        "Duplicate workflow_id "
                        f"{workflow.workflow_id} detected across split workflow roots."
                    )
                seen_workflow_ids.add(workflow.workflow_id)

                current = existing_entries.get(workflow.workflow_id, {})
                aliases = ordered_unique(_tuple_of_strings(current.get("aliases")))
                tags = ordered_unique(_tuple_of_strings(current.get("tags")))
                notes = _optional_string(current.get("notes"))

                entry: dict[str, object] = {
                    "workflow_id": workflow.workflow_id,
                    "workflow_kind": workflow.workflow_kind,
                    "title": workflow.title,
                    "summary": workflow.summary,
                    "status": "active",
                    "doc_path": workflow.relative_path,
                    "phase_type": workflow.phase_type,
                    "task_family": workflow.task_family,
                    "uses_internal_references": workflow.uses_internal_references,
                    "uses_external_references": workflow.uses_external_references,
                    "primary_risks": list(workflow.primary_risks),
                    "trigger_tags": list(workflow.trigger_tags),
                }
                if workflow.companion_workflow_ids:
                    entry["companion_workflow_ids"] = list(workflow.companion_workflow_ids)
                if workflow.composes_module_paths:
                    entry["composes_module_paths"] = list(workflow.composes_module_paths)
                if workflow.related_paths:
                    entry["related_paths"] = list(workflow.related_paths)
                if workflow.reference_doc_paths:
                    entry["reference_doc_paths"] = list(workflow.reference_doc_paths)
                if workflow.internal_reference_paths:
                    entry["internal_reference_paths"] = list(workflow.internal_reference_paths)
                if workflow.external_reference_urls:
                    entry["external_reference_urls"] = list(workflow.external_reference_urls)
                if aliases:
                    entry["aliases"] = list(aliases)
                if tags:
                    entry["tags"] = list(tags)
                if notes is not None:
                    entry["notes"] = notes

                entries.append(entry)

        self._validate_workflow_links(entries)

        artifact: dict[str, object] = {
            "$schema": "urn:watchtower:schema:artifacts:indexes:workflow-index:v1",
            "id": "index.workflows",
            "title": "Workflow Index",
            "status": "active",
            "entries": entries,
        }
        self._loader.schema_store.validate_instance(artifact)
        return artifact

    def write_document(self, document: dict[str, object], destination: Path | None = None) -> Path:
        """Write the generated workflow index to disk."""
        target = destination or (self._repo_root / WORKFLOW_INDEX_ARTIFACT_PATH)
        target.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")
        return target

    def _validate_workflow_links(self, entries: list[dict[str, object]]) -> None:
        known_ids = {
            entry["workflow_id"] for entry in entries if isinstance(entry.get("workflow_id"), str)
        }
        workflow_kind_by_path = {
            entry["doc_path"]: entry.get("workflow_kind")
            for entry in entries
            if isinstance(entry.get("doc_path"), str)
        }
        for entry in entries:
            workflow_id = entry.get("workflow_id")
            companions = entry.get("companion_workflow_ids", ())
            if not isinstance(workflow_id, str) or not isinstance(companions, list):
                if not isinstance(workflow_id, str):
                    continue
            if isinstance(companions, list):
                missing = sorted(
                    companion
                    for companion in companions
                    if isinstance(companion, str) and companion not in known_ids
                )
                if missing:
                    joined = ", ".join(missing)
                    raise ValueError(
                        f"Workflow {workflow_id} points to missing companion workflows: {joined}"
                    )
            composes_module_paths = entry.get("composes_module_paths", ())
            if not isinstance(composes_module_paths, list):
                continue
            invalid_module_paths = sorted(
                module_path
                for module_path in composes_module_paths
                if isinstance(module_path, str)
                and workflow_kind_by_path.get(module_path) != "module"
            )
            if invalid_module_paths:
                joined = ", ".join(invalid_module_paths)
                raise ValueError(
                    f"Workflow {workflow_id} points to missing or non-module composed "
                    f"workflow documents: {joined}"
                )


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _optional_string(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None
