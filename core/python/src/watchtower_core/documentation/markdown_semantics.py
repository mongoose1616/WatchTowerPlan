"""Repo-shared Markdown semantic helpers."""

from __future__ import annotations

import re
from pathlib import Path

from watchtower_core.adapters import extract_markdown_links

HEADING_PATTERN = re.compile(r"^#{2,6} ")
LIST_ITEM_PATTERN = re.compile(r"^\s{0,3}(?:[-*+] |\d+[.)] )")
_URI_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


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


def validate_repo_local_markdown_links(
    relative_path: str,
    markdown: str,
    *,
    repo_root: Path,
    source_path: Path | None = None,
) -> None:
    """Fail closed on missing, escaping, or filesystem-absolute repo-local Markdown links."""

    resolved_repo_root = repo_root.resolve()
    top_level_names = {child.name for child in resolved_repo_root.iterdir()}
    for target in extract_markdown_links(markdown):
        _validate_markdown_link_target(
            relative_path,
            target,
            repo_root=resolved_repo_root,
            top_level_names=top_level_names,
            source_path=source_path,
        )


def _validate_markdown_link_target(
    relative_path: str,
    target: str,
    *,
    repo_root: Path,
    top_level_names: set[str],
    source_path: Path | None,
) -> None:
    stripped = target.strip()
    if not stripped or stripped.startswith("#"):
        return

    without_fragment = stripped.split("#", 1)[0].split("?", 1)[0].strip()
    if not without_fragment or _URI_SCHEME_PATTERN.match(without_fragment):
        return

    candidate = Path(without_fragment)
    if candidate.is_absolute():
        repo_relative_candidate = without_fragment.lstrip("/")
        if not repo_relative_candidate:
            raise ValueError(
                f"{relative_path} repo-local Markdown link does not name a repository target: "
                f"{target}"
            )
        if ".." in Path(repo_relative_candidate).parts:
            raise ValueError(
                f"{relative_path} repo-local Markdown link escapes the repository root: {target}"
            )
        first_segment = repo_relative_candidate.split("/", 1)[0]
        if first_segment not in top_level_names:
            raise ValueError(
                f"{relative_path} repo-local Markdown link uses a filesystem-absolute path "
                f"instead of a repository-root-relative path: {target}"
            )
        resolved_candidate = (repo_root / repo_relative_candidate).resolve()
    else:
        base_directory = source_path.parent if source_path is not None else repo_root
        resolved_candidate = (base_directory / candidate).resolve()

    try:
        resolved_candidate.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(
            f"{relative_path} repo-local Markdown link escapes the repository root: {target}"
        ) from exc

    if not resolved_candidate.exists():
        raise ValueError(
            f"{relative_path} repo-local Markdown link does not exist in the repository: {target}"
        )
