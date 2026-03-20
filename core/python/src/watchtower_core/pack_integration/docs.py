"""Helpers for pack-owned command documentation paths."""

from __future__ import annotations


def pack_command_docs_root(*, docs_root: str) -> str:
    """Return the canonical command-doc root for one pack-owned docs root."""

    return f"{docs_root}/commands/core_python"


def pack_command_entry_doc_path(*, command_namespace: str, docs_root: str) -> str:
    """Return the canonical entry page for one pack command namespace."""

    normalized_namespace = command_namespace.replace("-", "_")
    return f"{pack_command_docs_root(docs_root=docs_root)}/watchtower_core_{normalized_namespace}.md"


__all__ = [
    "pack_command_docs_root",
    "pack_command_entry_doc_path",
]
