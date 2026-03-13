"""Rendering helpers shared by planning scaffold services."""

from __future__ import annotations


def render_document_content(title: object, sections: dict[str, str]) -> str:
    """Render a document body from ordered sections."""

    lines = [f"# {title}", ""]
    for section_title, section_body in sections.items():
        lines.extend((f"## {section_title}", section_body.strip(), ""))
    return "\n".join(lines).rstrip() + "\n"


def format_code_values(values: tuple[str, ...]) -> str:
    """Render metadata values using the planning-document code style."""

    if not values:
        return "`None`"
    return "; ".join(f"`{value}`" for value in values)


def render_metadata(label: str, values: tuple[str, ...]) -> str:
    """Render one Record Metadata bullet."""

    return f"- `{label}`: {format_code_values(values)}"


def render_bullets(values: tuple[str, ...], *, placeholder: str) -> str:
    """Render a bullet list or one placeholder bullet."""

    if values:
        return "\n".join(f"- {value}" for value in values)
    return f"- {placeholder}"


def render_numbered(values: tuple[str, ...], *, placeholders: tuple[str, ...]) -> str:
    """Render a numbered list or placeholder steps."""

    if values:
        return "\n".join(f"{index}. {value}" for index, value in enumerate(values, start=1))
    return "\n".join(f"{index}. {value}" for index, value in enumerate(placeholders, start=1))


def render_references(values: tuple[str, ...]) -> str:
    """Render references for a scaffolded planning document."""

    if values:
        return "\n".join(f"- {value}" for value in values)
    return "- <Companion document or source>"


def split_metadata_values(raw_value: str) -> tuple[str, ...]:
    """Split metadata values rendered with code formatting back into scalars."""

    cleaned = raw_value.replace("`", "")
    values = tuple(value.strip() for value in cleaned.split(";") if value.strip())
    if values == ("None",):
        return ()
    return values
