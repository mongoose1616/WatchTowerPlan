"""Reusable CLI namespace registration helpers for hosted packs."""

from __future__ import annotations


def selected_subcommand(
    selected: str | None,
    valid_subcommands: frozenset[str],
) -> str | None:
    """Return *selected* if it belongs to *valid_subcommands*, else ``None``."""

    if selected in valid_subcommands:
        return selected
    return None


def should_register_command(
    selected_subcommand: str | None,
    command_name: str,
) -> bool:
    """True when no subcommand filter is active or *command_name* matches."""

    return selected_subcommand is None or selected_subcommand == command_name
