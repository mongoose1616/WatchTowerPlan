"""Adapters for parsing and normalizing governed input surfaces."""

from watchtower_core.adapters.front_matter import (
    FrontMatterParseError,
    load_front_matter,
    replace_front_matter,
)
from watchtower_core.adapters.markdown import (
    extract_first_paragraph,
    extract_metadata_bullets,
    extract_path_like_references,
    extract_prefixed_ids,
    extract_sections,
    extract_title,
    extract_updated_at_from_section,
    load_markdown_body,
    parse_markdown_table,
    split_semicolon_list,
)

__all__ = [
    "FrontMatterParseError",
    "extract_first_paragraph",
    "extract_metadata_bullets",
    "extract_path_like_references",
    "extract_prefixed_ids",
    "extract_sections",
    "extract_title",
    "extract_updated_at_from_section",
    "load_front_matter",
    "load_markdown_body",
    "parse_markdown_table",
    "replace_front_matter",
    "split_semicolon_list",
]
