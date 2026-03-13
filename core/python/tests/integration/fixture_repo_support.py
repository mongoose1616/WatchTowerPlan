from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

FRONT_MATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


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
