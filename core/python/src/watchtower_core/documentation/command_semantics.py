"""Shared structure helpers for repository-native command documents."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from watchtower_core.adapters.markdown import (
    extract_code_spans,
    extract_sections,
    extract_title,
    extract_updated_at_from_section,
    load_markdown_body,
    parse_markdown_table,
)
from watchtower_core.documentation.governed_documents import validate_required_section_order
from watchtower_core.documentation.markdown_semantics import (
    validate_blank_line_before_heading_after_list,
)

COMMAND_REQUIRED_SECTIONS = (
    "Summary",
    "Use When",
    "Command",
    "Synopsis",
    "Arguments and Options",
    "Examples",
    "Behavior and Outputs",
    "Related Commands",
    "Source Surface",
    "Updated At",
)
_COMMAND_TABLE_REQUIRED_FIELDS = (
    "Invocation",
    "Kind",
    "Workspace",
    "Source Surface",
)
_UTC_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def load_command_doc_source_surfaces(doc_path: Path) -> tuple[str, str]:
    """Return the command-table and primary source-surface values from one command doc."""

    sections = extract_sections(load_markdown_body(doc_path))
    try:
        command_section = sections["Command"]
        source_surface_section = sections["Source Surface"]
    except KeyError as exc:
        raise ValueError(f"Command doc is missing a required section: {doc_path}") from exc

    command_rows = parse_markdown_table(command_section)
    table_source_surface = next(
        (row["Value"] for row in command_rows if row.get("Field") == "Source Surface"),
        None,
    )
    if table_source_surface is None:
        raise ValueError(f"Command doc Command table is missing its Source Surface row: {doc_path}")

    source_surfaces = extract_code_spans(source_surface_section)
    if not source_surfaces:
        raise ValueError(
            f"Command doc Source Surface section is missing its primary code path: {doc_path}"
        )

    return table_source_surface, source_surfaces[0]


def validate_command_document(
    *,
    relative_path: str,
    resolved_path: Path,
    repo_root: Path,
) -> None:
    """Validate one command document against the shared command-doc contract."""

    markdown = load_markdown_body(resolved_path)
    sections = extract_sections(markdown)
    validate_blank_line_before_heading_after_list(relative_path, markdown)
    _validate_required_sections(relative_path, sections)
    title = extract_title(markdown)
    if not title.startswith("`") or not title.endswith("`"):
        raise ValueError(
            f"{relative_path} H1 title must wrap the literal command name in backticks."
        )
    visible_command = title.strip("`").strip()

    command_rows = parse_markdown_table(sections["Command"])
    if not command_rows:
        raise ValueError(f"{relative_path} Command section is missing its command table rows.")
    command_fields = {row.get("Field", ""): row.get("Value", "") for row in command_rows}
    missing_fields = [
        field_name
        for field_name in _COMMAND_TABLE_REQUIRED_FIELDS
        if not command_fields.get(field_name)
    ]
    if missing_fields:
        joined = ", ".join(missing_fields)
        raise ValueError(f"{relative_path} Command table is missing required fields: {joined}")

    invocation = command_fields["Invocation"].strip()
    if invocation != visible_command:
        raise ValueError(
            f"{relative_path} H1 title does not match the Invocation row: "
            f"{visible_command!r} != {invocation!r}"
        )

    table_source_surface, primary_source_surface = load_command_doc_source_surfaces(
        resolved_path
    )
    if table_source_surface != primary_source_surface:
        raise ValueError(
            f"{relative_path} Source Surface section must lead with the same path published "
            "in the Command table Source Surface row."
        )
    _validate_source_surface_paths(relative_path, sections["Source Surface"], repo_root=repo_root)

    if "```" not in sections["Synopsis"]:
        raise ValueError(f"{relative_path} Synopsis section must include a fenced code block.")
    if "```" not in sections["Examples"]:
        raise ValueError(f"{relative_path} Examples section must include at least one code block.")

    related_rows = parse_markdown_table(sections["Related Commands"])
    if not related_rows:
        raise ValueError(
            f"{relative_path} Related Commands section must publish at least one table row."
        )

    try:
        datetime.strptime(
            extract_updated_at_from_section(sections["Updated At"]),
            _UTC_TIMESTAMP_FORMAT,
        )
    except ValueError as exc:
        raise ValueError(
            f"{relative_path} Updated At section must publish one RFC 3339 UTC timestamp."
        ) from exc


def _validate_required_sections(
    relative_path: str,
    sections: dict[str, str],
) -> None:
    missing_sections = [
        section_title for section_title in COMMAND_REQUIRED_SECTIONS if section_title not in sections
    ]
    if missing_sections:
        joined = ", ".join(missing_sections)
        raise ValueError(f"{relative_path} is missing required sections: {joined}")
    validate_required_section_order(relative_path, sections, COMMAND_REQUIRED_SECTIONS)


def _validate_source_surface_paths(
    relative_path: str,
    source_surface_section: str,
    *,
    repo_root: Path,
) -> None:
    source_surfaces = extract_code_spans(source_surface_section)
    for source_surface in source_surfaces:
        candidate = (repo_root / source_surface).resolve()
        try:
            candidate.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError(
                f"{relative_path} Source Surface path escapes the repository root: "
                f"{source_surface}"
            ) from exc
        if candidate.exists():
            continue
        raise ValueError(
            f"{relative_path} Source Surface path does not exist in the repository: "
            f"{source_surface}"
        )


__all__ = [
    "COMMAND_REQUIRED_SECTIONS",
    "load_command_doc_source_surfaces",
    "validate_command_document",
]
