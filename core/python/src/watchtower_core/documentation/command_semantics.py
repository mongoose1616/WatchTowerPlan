"""Shared structure helpers for repository-native command documents."""

from __future__ import annotations

import json
import re
import shlex
from datetime import datetime
from pathlib import Path, PurePosixPath

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
    validate_repo_local_markdown_links,
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
_PACK_NAMESPACE_PLACEHOLDER = "<pack-namespace>"
_PACK_NAMESPACE_META_FAMILIES = frozenset({"bootstrap", "query", "sync"})
_FENCED_CODE_BLOCK_PATTERN = re.compile(r"```(?:[^\n`]*)\n(?P<body>.*?)\n```", re.DOTALL)
_REPO_LOCAL_EXAMPLE_OPTIONS = frozenset({"--pack-settings-path"})


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
    validate_repo_local_markdown_links(
        relative_path,
        markdown,
        repo_root=repo_root,
        source_path=resolved_path,
    )
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

    table_source_surface, primary_source_surface = load_command_doc_source_surfaces(resolved_path)
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
    _validate_repo_local_example_paths(
        relative_path,
        sections["Examples"],
        repo_root=repo_root,
    )

    related_rows = parse_markdown_table(sections["Related Commands"])
    if not related_rows:
        raise ValueError(
            f"{relative_path} Related Commands section must publish at least one table row."
        )
    _validate_related_command_references(
        relative_path,
        related_rows,
        repo_root=repo_root,
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
        section_title
        for section_title in COMMAND_REQUIRED_SECTIONS
        if section_title not in sections
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
                f"{relative_path} Source Surface path escapes the repository root: {source_surface}"
            ) from exc
        if candidate.exists():
            continue
        raise ValueError(
            f"{relative_path} Source Surface path does not exist in the repository: "
            f"{source_surface}"
        )


def _validate_related_command_references(
    relative_path: str,
    related_rows: list[dict[str, str]],
    *,
    repo_root: Path,
) -> None:
    known_commands = tuple(
        sorted(
            _load_known_commands_from_index(repo_root),
            key=lambda command: len(command.split()),
            reverse=True,
        )
    )
    seen_surfaces: set[str] = set()
    for row in related_rows:
        command_cell = row.get("Command", "")
        for reference in _iter_related_command_references(command_cell):
            if "watchtower-core" not in reference:
                continue
            normalized_reference = reference[reference.index("watchtower-core") :].strip()
            matched_surface = _resolve_known_command_surface(
                normalized_reference,
                known_commands,
            )
            if matched_surface is None:
                raise ValueError(
                    f"{relative_path} Related Commands references an unknown command surface: "
                    f"{reference}"
                )
            if matched_surface in seen_surfaces:
                raise ValueError(
                    f"{relative_path} Related Commands repeats the same command surface more "
                    f"than once: {matched_surface}"
                )
            seen_surfaces.add(matched_surface)


def _validate_repo_local_example_paths(
    relative_path: str,
    examples_section: str,
    *,
    repo_root: Path,
) -> None:
    for code_block in _iter_fenced_code_blocks(examples_section):
        for line in code_block.splitlines():
            _validate_repo_local_example_line(
                relative_path,
                line,
                repo_root=repo_root,
            )


def _iter_fenced_code_blocks(section: str) -> tuple[str, ...]:
    return tuple(
        match.group("body").strip()
        for match in _FENCED_CODE_BLOCK_PATTERN.finditer(section)
    )


def _validate_repo_local_example_line(
    relative_path: str,
    line: str,
    *,
    repo_root: Path,
) -> None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped.startswith("cd "):
        return
    try:
        tokens = shlex.split(stripped)
    except ValueError as exc:
        raise ValueError(
            f"{relative_path} Examples contains an invalid shell example line: {stripped}"
        ) from exc
    for index, token in enumerate(tokens):
        option, inline_value = _split_cli_option(token)
        if option not in _REPO_LOCAL_EXAMPLE_OPTIONS:
            continue
        value = inline_value
        if value is None:
            if index + 1 >= len(tokens):
                raise ValueError(
                    f"{relative_path} Examples option {option} is missing its value."
                )
            value = tokens[index + 1].strip()
        if _is_illustrative_cli_value(value) or Path(value).is_absolute():
            continue
        normalized = PurePosixPath(value.rstrip("/"))
        if not normalized.parts or normalized.is_absolute() or ".." in normalized.parts:
            raise ValueError(
                f"{relative_path} Examples uses an invalid repo-local path for {option}: {value}"
            )
        if not (repo_root / normalized.as_posix()).exists():
            raise ValueError(
                f"{relative_path} Examples uses missing repo-local path for {option}: {value}"
            )


def _split_cli_option(token: str) -> tuple[str, str | None]:
    if "=" not in token:
        return token, None
    option, value = token.split("=", 1)
    return option, value


def _is_illustrative_cli_value(value: str) -> bool:
    return (
        "<" in value
        or ">" in value
        or "${" in value
        or value.startswith("$")
        or value.startswith("~")
        or value == "..."
    )


def _iter_related_command_references(command_cell: str) -> tuple[str, ...]:
    references = tuple(reference.strip() for reference in extract_code_spans(command_cell))
    if references:
        return references
    normalized_cell = command_cell.strip()
    if "watchtower-core" not in normalized_cell:
        return ()
    return (normalized_cell,)


def _reference_matches_known_command_surface(
    normalized_reference: str,
    known_commands: tuple[str, ...],
) -> bool:
    return _resolve_known_command_surface(normalized_reference, known_commands) is not None


def _resolve_known_command_surface(
    normalized_reference: str,
    known_commands: tuple[str, ...],
) -> str | None:
    tokens = _split_cli_tokens(normalized_reference)
    if not tokens or tokens[0] != "watchtower-core":
        return None
    if _is_pack_namespace_meta_reference(tokens):
        canonical_tokens = list(tokens[: min(len(tokens), 3)])
        if len(tokens) > 3 and not tokens[3].startswith("-"):
            canonical_tokens.append(tokens[3])
        return " ".join(canonical_tokens)

    for command in known_commands:
        command_tokens = tuple(command.split())
        if tokens[: len(command_tokens)] != command_tokens:
            continue
        remainder = tokens[len(command_tokens) :]
        if not remainder:
            return command
        if remainder[0].startswith("-"):
            return command
    return None


def _is_pack_namespace_meta_reference(tokens: tuple[str, ...]) -> bool:
    if len(tokens) < 2 or tokens[1] != _PACK_NAMESPACE_PLACEHOLDER:
        return False
    if len(tokens) == 2:
        return True
    return tokens[2] in _PACK_NAMESPACE_META_FAMILIES


def _split_cli_tokens(invocation: str) -> tuple[str, ...]:
    try:
        return tuple(shlex.split(invocation))
    except ValueError:
        return tuple(invocation.split())


def _load_known_commands_from_index(repo_root: Path) -> frozenset[str]:
    command_index_path = (
        repo_root / "core" / "control_plane" / "indexes" / "commands" / "command_index.json"
    )
    try:
        document = json.loads(command_index_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(
            "Command semantics validation requires a readable command index at "
            f"{command_index_path.relative_to(repo_root).as_posix()}."
        ) from exc
    entries = document.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("Command index is missing its entries list.")
    return frozenset(
        command
        for entry in entries
        if isinstance(entry, dict)
        for command in (entry.get("command"),)
        if isinstance(command, str) and command
    )


__all__ = [
    "COMMAND_REQUIRED_SECTIONS",
    "load_command_doc_source_surfaces",
    "validate_command_document",
]
