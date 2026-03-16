"""Schema-driven Markdown rendering for governed rendered surfaces."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from watchtower_core.control_plane.models import (
    RenderedSurfaceColumnDefinition,
    RenderedSurfaceDefinition,
    RenderedSurfaceSectionDefinition,
)


def render_repo_link(relative_path: str, *, label: str) -> str:
    """Return one repository-local Markdown link."""

    normalized_path = relative_path.strip().lstrip("/")
    return f"[{label}](/{normalized_path})"


def render_rendered_surface(
    surface: RenderedSurfaceDefinition,
    data: Mapping[str, object],
) -> str:
    """Render one governed surface definition against shaped section data."""

    lines = [f"# {surface.title}"]
    for section in surface.sections:
        section_lines = _render_section(section, data)
        if not section_lines:
            continue
        lines.extend(["", *section_lines])
    lines.append("")
    return "\n".join(lines)


def _render_section(
    section: RenderedSurfaceSectionDefinition,
    data: Mapping[str, object],
) -> list[str]:
    if section.kind == "table":
        return _render_table_section(section, data)
    if section.kind == "bullet_summary":
        return _render_bullet_summary_section(section, data)
    if section.kind == "lines":
        return _render_lines_section(section, data)
    if section.kind == "updated_at":
        return _render_updated_at_section(section, data)
    raise ValueError(f"Unsupported rendered section kind: {section.kind}")


def _render_table_section(
    section: RenderedSurfaceSectionDefinition,
    data: Mapping[str, object],
) -> list[str]:
    rows = _sequence_of_mappings(data.get(section.source_key))
    rendered: list[str] = []
    if section.title is not None:
        rendered.append(f"## {section.title}")
    if not rows:
        rendered.append(section.empty_message or "_No entries._")
        return rendered

    columns = tuple(
        column
        for column in section.columns
        if column.enabled_when_key is None or bool(data.get(column.enabled_when_key))
    )
    headers = tuple(column.header for column in columns)
    separator = tuple("---" for _ in columns)
    rendered.append("| " + " | ".join(headers) + " |")
    rendered.append("| " + " | ".join(separator) + " |")
    for row in rows:
        rendered.append(
            "| "
            + " | ".join(_render_column_cell(column, row) for column in columns)
            + " |"
        )
    return rendered


def _render_bullet_summary_section(
    section: RenderedSurfaceSectionDefinition,
    data: Mapping[str, object],
) -> list[str]:
    items = _sequence_of_mappings(data.get(section.source_key))
    rendered: list[str] = []
    if section.title is not None:
        rendered.append(f"## {section.title}")
    if not items:
        rendered.append(section.empty_message or "_No entries._")
        return rendered

    assert section.label_field is not None
    assert section.count_field is not None
    for item in items:
        label = _string_value(item.get(section.label_field), empty_value="-")
        count = _string_value(item.get(section.count_field), empty_value="0")
        rendered.append(f"- `{label}`: {count}")
    return rendered


def _render_lines_section(
    section: RenderedSurfaceSectionDefinition,
    data: Mapping[str, object],
) -> list[str]:
    values = _string_sequence(data.get(section.source_key))
    if not values:
        return []
    rendered: list[str] = []
    if section.title is not None:
        rendered.append(f"## {section.title}")
    rendered.extend(values)
    return rendered


def _render_updated_at_section(
    section: RenderedSurfaceSectionDefinition,
    data: Mapping[str, object],
) -> list[str]:
    value = _string_value(data.get(section.source_key), empty_value="None")
    return [f"_Updated At: `{value}`_"]


def _render_column_cell(
    column: RenderedSurfaceColumnDefinition,
    row: Mapping[str, object],
) -> str:
    empty_value = column.empty_value or "-"
    value = row.get(column.field)
    if column.formatter == "plain":
        return _string_value(value, empty_value=empty_value)
    if column.formatter == "markdown":
        return _string_value(value, empty_value=empty_value)
    if column.formatter == "code":
        if value is None or value == "":
            return empty_value
        return f"`{value}`"
    if column.formatter == "repo_link":
        path_field = column.path_field
        if path_field is None:
            raise ValueError(f"Rendered repo_link column missing path_field: {column.header}")
        path = row.get(path_field)
        if path is None or path == "":
            return empty_value
        label_value = (
            row.get(column.label_field)
            if column.label_field is not None
            else value
        )
        label = _string_value(label_value, empty_value=empty_value)
        return render_repo_link(str(path), label=label)
    raise ValueError(f"Unsupported rendered column formatter: {column.formatter}")


def _sequence_of_mappings(value: object) -> tuple[Mapping[str, object], ...]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise TypeError("Rendered table and bullet sections require a sequence of row mappings.")
    rows: list[Mapping[str, object]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise TypeError("Rendered section rows must be mappings.")
        rows.append(item)
    return tuple(rows)


def _string_sequence(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, Sequence) or isinstance(value, bytes):
        raise TypeError("Rendered lines sections require a string or a sequence of strings.")
    return tuple(str(item) for item in value)


def _string_value(value: object, *, empty_value: str) -> str:
    if value is None or value == "":
        return empty_value
    return str(value)
