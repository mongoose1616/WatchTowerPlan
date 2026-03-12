from __future__ import annotations

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
