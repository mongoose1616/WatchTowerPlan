"""Markdown parsing helpers for governed planning and command documents."""

from __future__ import annotations

import re
from pathlib import Path

from watchtower_core.adapters.front_matter import FRONT_MATTER_PATTERN

H1_PATTERN = re.compile(r"^# (?P<title>.+)$", re.MULTILINE)
SECTION_HEADING_PATTERN = re.compile(r"^## (?P<title>.+)$", re.MULTILINE)
CODE_SPAN_PATTERN = re.compile(r"`([^`]+)`")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?P<target>[^)]+)\)")
METADATA_BULLET_PATTERN = re.compile(r"^- `(?P<label>[^`]+)`: (?P<value>.+)$")


def load_markdown_body(path: Path) -> str:
    """Return Markdown content with any leading YAML front matter removed."""
    text = path.read_text(encoding="utf-8")
    return FRONT_MATTER_PATTERN.sub("", text, count=1)


def extract_title(markdown: str) -> str:
    """Return the first H1 title from a Markdown document."""
    match = H1_PATTERN.search(markdown)
    if match is None:
        raise ValueError("Markdown document is missing its expected H1 title.")
    return match.group("title").strip()


def extract_sections(markdown: str) -> dict[str, str]:
    """Return a mapping of H2 section title to its raw body content."""
    sections: dict[str, list[str]] = {}
    current_title: str | None = None
    for line in markdown.splitlines():
        match = SECTION_HEADING_PATTERN.match(line)
        if match is not None:
            current_title = match.group("title").strip()
            sections[current_title] = []
            continue
        if current_title is not None:
            sections[current_title].append(line)
    return {title: "\n".join(lines).strip() for title, lines in sections.items()}


def extract_first_paragraph(section: str) -> str:
    """Return the first non-empty paragraph from a section body."""
    for block in section.split("\n\n"):
        candidate = block.strip()
        if candidate:
            return candidate.replace("\n", " ").strip()
    raise ValueError("Section is missing its expected paragraph content.")


def extract_code_spans(text: str) -> tuple[str, ...]:
    """Return inline code-span values in order."""
    return tuple(match.group(1).strip() for match in CODE_SPAN_PATTERN.finditer(text))


def extract_markdown_links(text: str) -> tuple[str, ...]:
    """Return Markdown link targets in order."""
    return tuple(match.group("target").strip() for match in MARKDOWN_LINK_PATTERN.finditer(text))


def extract_external_urls(text: str) -> tuple[str, ...]:
    """Return unique external URLs referenced in Markdown links or code spans."""
    candidates = [*extract_markdown_links(text), *extract_code_spans(text)]
    seen: set[str] = set()
    ordered: list[str] = []
    for value in candidates:
        if not value.startswith(("http://", "https://")):
            continue
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def extract_metadata_bullets(section: str) -> dict[str, str]:
    """Return a mapping of Record Metadata bullet labels to their raw values."""
    metadata: dict[str, str] = {}
    for line in section.splitlines():
        match = METADATA_BULLET_PATTERN.match(line.strip())
        if match is None:
            continue
        metadata[match.group("label").strip()] = match.group("value").strip()
    return metadata


def extract_prefixed_ids(section: str, prefix: str) -> tuple[str, ...]:
    """Return unique inline code IDs from a section that start with the given prefix."""
    seen: set[str] = set()
    ordered: list[str] = []
    for value in extract_code_spans(section):
        if not value.startswith(prefix) or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def extract_updated_at_from_section(section: str) -> str:
    """Return the RFC 3339 UTC timestamp published in an Updated At section."""
    values = extract_code_spans(section)
    if not values:
        raise ValueError("Updated At section is missing its expected timestamp code span.")
    return values[0]


def parse_markdown_table(section: str) -> list[dict[str, str]]:
    """Parse a simple Markdown table into a list of row dictionaries."""
    rows: list[dict[str, str]] = []
    lines = [line for line in section.splitlines() if line.strip()]
    header: list[str] | None = None

    for line in lines:
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.split("|")[1:-1]]
        if header is None:
            header = parts
            continue
        if all(part.startswith("---") for part in parts):
            continue
        if header is None or len(parts) != len(header):
            continue
        rows.append(
            {
                key: value.strip().strip("`")
                for key, value in zip(header, parts, strict=True)
            }
        )
    return rows


def split_semicolon_list(raw_value: str) -> tuple[str, ...]:
    """Split one semicolon-delimited metadata or tracker cell into cleaned items."""
    values: list[str] = []
    for part in raw_value.split(";"):
        cleaned = part.strip().strip("`").strip()
        if cleaned:
            values.append(cleaned)
    return tuple(values)


def extract_path_like_references(text: str) -> tuple[str, ...]:
    """Return inline code spans and Markdown link targets that look like repo paths."""
    candidates = [*extract_code_spans(text), *extract_markdown_links(text)]
    seen: set[str] = set()
    ordered: list[str] = []
    for value in candidates:
        if "/" not in value:
            continue
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def normalize_repo_path_reference(value: str, repo_root: Path) -> str | None:
    """Normalize an internal path-like reference to a repo-relative path when possible."""
    stripped = value.strip()
    if not stripped or stripped.startswith(("http://", "https://", "mailto:")):
        return None

    without_fragment = stripped.split("#", 1)[0].strip()
    if not without_fragment:
        return None

    repo_root = repo_root.resolve()
    if without_fragment.startswith(str(repo_root)):
        try:
            return Path(without_fragment).resolve().relative_to(repo_root).as_posix()
        except ValueError:
            return None

    candidate = without_fragment.lstrip("/")
    if not candidate:
        return None

    path = repo_root / candidate
    if path.exists():
        return candidate
    return None


def extract_repo_path_references(text: str, repo_root: Path) -> tuple[str, ...]:
    """Return unique repo-relative paths referenced in one Markdown block."""
    seen: set[str] = set()
    ordered: list[str] = []
    for value in extract_path_like_references(text):
        normalized = normalize_repo_path_reference(value, repo_root)
        if normalized is None or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return tuple(ordered)
