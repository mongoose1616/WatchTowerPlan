"""Shared helpers for focused control-plane artifact integration suites."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[4]
FRONT_MATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def load_json_object(path: Path) -> dict[str, object]:
    """Load one JSON object fixture from disk."""

    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def load_front_matter(path: Path) -> dict[str, object]:
    """Load one Markdown front-matter block from disk."""

    match = FRONT_MATTER_PATTERN.search(path.read_text(encoding="utf-8"))
    assert match is not None, f"missing front matter: {path}"
    loaded = yaml.safe_load(match.group(1))
    assert isinstance(loaded, dict)
    return loaded
