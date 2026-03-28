from __future__ import annotations

import json
import re
from pathlib import Path
from shutil import copy2, copytree

import yaml

from watchtower_core.adapters import split_semicolon_list
from watchtower_core.adapters.markdown import extract_code_spans, extract_sections, load_markdown_body
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.operationalization_paths import (
    expand_pack_placeholder_operationalization_paths,
    operationalization_path_is_glob,
)
from watchtower_core.documentation.standards import (
    STANDARD_OPERATIONALIZATION_PATHS_LABEL,
    STANDARD_OPERATIONALIZATION_SECTION,
)
from watchtower_core.adapters import extract_metadata_bullets
from watchtower_core.control_plane.path_ids import PlanPathIdHelper
from watchtower_plan.initiatives import (
    InitiativeBootstrapParams,
    InitiativePackageResult,
    InitiativePackageService,
    InitiativeTaskSpec,
)

FRONT_MATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def materialize_plan_pack(repo_root: Path, source_repo_root: Path) -> None:
    source_plan_root = source_repo_root / "plan"
    if not source_plan_root.exists():
        return
    copytree(source_plan_root, repo_root / "plan")


def materialize_minimal_plan_pack(repo_root: Path, source_repo_root: Path) -> None:
    """Copy only the minimum live plan pack surfaces required by loaders and syncs."""

    source_plan_root = source_repo_root / "plan"
    source_runtime_root = source_plan_root / ".wt"
    if not source_runtime_root.exists():
        return
    target_plan_root = repo_root / "plan"
    target_plan_root.mkdir(parents=True, exist_ok=True)
    copytree(source_runtime_root, target_plan_root / ".wt")
    (target_plan_root / "initiatives").mkdir(parents=True, exist_ok=True)
    (target_plan_root / "projects").mkdir(parents=True, exist_ok=True)


def materialize_governed_applies_to_targets(
    repo_root: Path,
    source_repo_root: Path | None = None,
) -> None:
    for docs_root in (repo_root / "core" / "docs", repo_root / "plan" / "docs"):
        if not docs_root.exists():
            continue
        for path in docs_root.rglob("*.md"):
            match = FRONT_MATTER_PATTERN.search(path.read_text(encoding="utf-8"))
            if match is None:
                continue
            front_matter = yaml.safe_load(match.group(1))
            if not isinstance(front_matter, dict):
                continue
            applies_to = front_matter.get("applies_to")
            if not isinstance(applies_to, list):
                continue
            for value in applies_to:
                if not isinstance(value, str):
                    continue
                candidate = value.strip()
                if "/" not in candidate:
                    continue
                target = repo_root / candidate.rstrip("/")
                if candidate.endswith("/"):
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if target.suffix:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if source_repo_root is not None:
                        source = source_repo_root / candidate
                        if source.exists() and source.is_file():
                            copy2(source, target)
                            continue
                    target.touch(exist_ok=True)
                    continue
                target.mkdir(parents=True, exist_ok=True)


def materialize_standard_operationalization_targets(
    repo_root: Path,
    source_repo_root: Path | None = None,
) -> None:
    for docs_root in (repo_root / "core" / "docs" / "standards", repo_root / "plan" / "docs" / "standards"):
        if not docs_root.exists():
            continue
        for path in docs_root.rglob("*.md"):
            sections = extract_sections(load_markdown_body(path))
            section = sections.get(STANDARD_OPERATIONALIZATION_SECTION)
            if section is None:
                continue
            metadata = extract_metadata_bullets(section)
            raw_values = metadata.get(STANDARD_OPERATIONALIZATION_PATHS_LABEL)
            if raw_values is None:
                continue
            for value in split_semicolon_list(raw_values):
                _materialize_semantic_repo_path_reference(
                    repo_root,
                    value,
                    source_repo_root,
                )


def materialize_command_doc_source_surfaces(
    repo_root: Path,
    source_repo_root: Path | None = None,
) -> None:
    for docs_root in (repo_root / "core" / "docs" / "commands", repo_root / "plan" / "docs" / "commands"):
        if not docs_root.exists():
            continue
        for path in docs_root.rglob("*.md"):
            sections = extract_sections(load_markdown_body(path))
            if "Source Surface" not in sections:
                continue
            for value in extract_code_spans(sections["Source Surface"]):
                _materialize_semantic_repo_path_reference(
                    repo_root,
                    value,
                    source_repo_root,
                )


def materialize_acceptance_and_evidence_paths(
    repo_root: Path,
    source_repo_root: Path | None = None,
) -> None:
    for relative_root in (
        "core/control_plane/contracts/acceptance",
        "core/control_plane/records/validation_evidence",
    ):
        root = repo_root / relative_root
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            document = json.loads(path.read_text(encoding="utf-8"))
            _materialize_document_paths(repo_root, document, source_repo_root)


def _materialize_document_paths(
    repo_root: Path,
    document: object,
    source_repo_root: Path | None,
) -> None:
    if isinstance(document, dict):
        for key, value in document.items():
            if key in {"validation_targets", "related_paths", "subject_paths"}:
                _materialize_paths(repo_root, value, source_repo_root)
            else:
                _materialize_document_paths(repo_root, value, source_repo_root)
        return
    if isinstance(document, list):
        for item in document:
            _materialize_document_paths(repo_root, item, source_repo_root)


def _materialize_paths(
    repo_root: Path,
    values: object,
    source_repo_root: Path | None,
) -> None:
    if not isinstance(values, list):
        return
    for value in values:
        if not isinstance(value, str):
            continue
        candidate = value.strip()
        if "/" not in candidate:
            continue
        target = repo_root / candidate.rstrip("/")
        if candidate.endswith("/"):
            target.mkdir(parents=True, exist_ok=True)
            continue
        if target.suffix:
            target.parent.mkdir(parents=True, exist_ok=True)
            if source_repo_root is not None:
                source = source_repo_root / candidate
                if source.exists() and source.is_file():
                    copy2(source, target)
                    continue
            target.touch(exist_ok=True)
            continue
        target.mkdir(parents=True, exist_ok=True)


def _materialize_semantic_repo_path_reference(
    repo_root: Path,
    value: str,
    source_repo_root: Path | None,
) -> None:
    stripped = value.strip().split("#", 1)[0].split("?", 1)[0].strip()
    if not stripped:
        return
    if "/" not in stripped and "<pack>" not in stripped:
        if source_repo_root is None:
            return
        if not (source_repo_root / stripped.rstrip("/")).exists():
            return

    candidates = (
        expand_pack_placeholder_operationalization_paths(stripped, repo_root)
        if "<pack>" in stripped
        else (stripped,)
    )
    for candidate in candidates:
        if operationalization_path_is_glob(candidate):
            _materialize_glob_matches(repo_root, candidate, source_repo_root)
            continue
        _materialize_repo_path(repo_root, candidate, source_repo_root)


def _materialize_glob_matches(
    repo_root: Path,
    pattern: str,
    source_repo_root: Path | None,
) -> None:
    if source_repo_root is None:
        return
    for source in source_repo_root.glob(pattern):
        if source.is_dir():
            continue
        relative_path = source.relative_to(source_repo_root).as_posix()
        _materialize_repo_path(repo_root, relative_path, source_repo_root)


def _materialize_repo_path(
    repo_root: Path,
    candidate: str,
    source_repo_root: Path | None,
) -> None:
    target = repo_root / candidate.rstrip("/")
    source = source_repo_root / candidate.rstrip("/") if source_repo_root is not None else None
    if candidate.endswith("/"):
        target.mkdir(parents=True, exist_ok=True)
        return
    if source is not None and source.exists():
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        return
    if target.suffix:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.touch(exist_ok=True)
        return
    target.mkdir(parents=True, exist_ok=True)


def packwide_initiative_root(repo_root: Path, trace_id: str) -> Path:
    """Return the pack-wide initiative root for one trace identifier."""

    return repo_root / "plan" / "initiatives" / PlanPathIdHelper.trace_suffix(trace_id)


def bootstrap_packwide_initiative(
    repo_root: Path,
    *,
    trace_id: str,
    title: str,
    summary: str,
    task_specs: tuple[InitiativeTaskSpec, ...] = (),
    include_decision_notes: bool = False,
    approve: bool = False,
    updated_at: str = "2026-03-18T12:00:00Z",
) -> InitiativePackageResult:
    """Bootstrap one live pack-wide initiative package for integration scenarios."""

    initiative_slug = PlanPathIdHelper.trace_suffix(trace_id)
    effective_task_specs = task_specs or (
        InitiativeTaskSpec(
            title=f"Seed {title}",
            summary="Seeds the live initiative-local task state for integration coverage.",
            slug="seed_bootstrap",
            task_id=f"task.{initiative_slug}.seed_bootstrap",
        ),
    )
    service = InitiativePackageService(ControlPlaneLoader(repo_root))
    result = service.bootstrap_packwide(
        InitiativeBootstrapParams(
            trace_id=trace_id,
            title=title,
            summary=summary,
            task_specs=effective_task_specs,
            include_decision_notes=include_decision_notes,
            updated_at=updated_at,
        ),
        write=True,
    )
    if approve:
        service.approve_packwide(
            initiative_slug,
            "actor.repository_maintainer",
            write=True,
        )
    return result
