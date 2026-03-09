"""Markdown front-matter parsing helpers for governed document validation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


class FrontMatterParseError(ValueError):
    """Raised when a Markdown document front-matter block cannot be parsed."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def load_front_matter(path: Path) -> dict[str, Any]:
    """Parse and return the YAML front matter from a Markdown document."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_PATTERN.search(text)
    if match is None:
        raise FrontMatterParseError(
            "front_matter_missing",
            "Missing YAML front matter block at the top of the Markdown document.",
        )

    try:
        loaded = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise FrontMatterParseError(
            "front_matter_yaml_invalid",
            f"Invalid YAML front matter: {exc}",
        ) from exc

    if not isinstance(loaded, dict):
        raise FrontMatterParseError(
            "front_matter_not_mapping",
            "Parsed front matter must be a YAML mapping object.",
        )
    return loaded
