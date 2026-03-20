"""Shared repo-local Markdown semantic helpers."""

from __future__ import annotations

import re

HEADING_PATTERN = re.compile(r"^#{2,6} ")
LIST_ITEM_PATTERN = re.compile(r"^\s{0,3}(?:[-*+] |\d+[.)] )")


def validate_blank_line_before_heading_after_list(relative_path: str, markdown: str) -> None:
    """Fail when a heading immediately follows a Markdown list block."""
    in_fence = False
    list_block_active = False
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        stripped = line.strip()
        if not in_fence and HEADING_PATTERN.match(line) and list_block_active:
            raise ValueError(
                f"{relative_path} heading on line {line_number} must be separated "
                "from the preceding list by a blank line."
            )
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
        if in_fence:
            continue
        if not stripped:
            list_block_active = False
            continue
        if LIST_ITEM_PATTERN.match(line):
            list_block_active = True
            continue
        if list_block_active and (line.startswith("  ") or line.startswith("\t")):
            continue
        list_block_active = False
