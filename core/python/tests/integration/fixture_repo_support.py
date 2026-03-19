from __future__ import annotations

import json
import re
from pathlib import Path
from shutil import copytree

import yaml

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.control_plane.path_ids import PlanPathIdHelper
from watchtower_core.plan_runtime.initiative_packages import (
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


def materialize_plan_runtime_pack(repo_root: Path, source_repo_root: Path) -> None:
    """Copy only the minimum live plan runtime package required by loaders and syncs."""

    source_plan_root = source_repo_root / "plan"
    source_runtime_root = source_plan_root / ".wt"
    if not source_runtime_root.exists():
        return
    target_plan_root = repo_root / "plan"
    target_plan_root.mkdir(parents=True, exist_ok=True)
    copytree(source_runtime_root, target_plan_root / ".wt")
    (target_plan_root / "initiatives").mkdir(parents=True, exist_ok=True)
    (target_plan_root / "projects").mkdir(parents=True, exist_ok=True)


def materialize_governed_applies_to_targets(repo_root: Path) -> None:
    docs_root = repo_root / "docs"
    if not docs_root.exists():
        return

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
                target.touch(exist_ok=True)
                continue
            target.mkdir(parents=True, exist_ok=True)


def materialize_acceptance_and_evidence_paths(repo_root: Path) -> None:
    for relative_root in (
        "core/control_plane/contracts/acceptance",
        "core/control_plane/ledgers/validation_evidence",
    ):
        root = repo_root / relative_root
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            document = json.loads(path.read_text(encoding="utf-8"))
            _materialize_document_paths(repo_root, document)


def _materialize_document_paths(repo_root: Path, document: object) -> None:
    if isinstance(document, dict):
        for key, value in document.items():
            if key in {"validation_targets", "related_paths", "subject_paths"}:
                _materialize_paths(repo_root, value)
            else:
                _materialize_document_paths(repo_root, value)
        return
    if isinstance(document, list):
        for item in document:
            _materialize_document_paths(repo_root, item)


def _materialize_paths(repo_root: Path, values: object) -> None:
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
            target.touch(exist_ok=True)
            continue
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
