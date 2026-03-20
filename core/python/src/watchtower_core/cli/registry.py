"""Compatibility wrapper around the host-owned command registry."""

from __future__ import annotations

from watchtower_host.cli.registry import (
    COMMAND_GROUP_SPECS,
    CORE_COMMAND_GROUP_SPECS,
    QUERY_COORDINATION_FAMILY_PATH,
    QUERY_DISCOVERY_FAMILY_PATH,
    QUERY_KNOWLEDGE_FAMILY_PATH,
    QUERY_RECORDS_FAMILY_PATH,
    CommandGroupSpec,
    CommandRegistrar,
    load_command_group_specs,
)
