"""Typed registry for top-level CLI command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass

from watchtower_core.cli.closeout_family import register_closeout_family
from watchtower_core.cli.doctor_family import register_doctor_family
from watchtower_core.cli.plan_family import register_plan_family
from watchtower_core.cli.query_family import register_query_family
from watchtower_core.cli.route_family import register_route_family
from watchtower_core.cli.sync_family import register_sync_family
from watchtower_core.cli.task_family import register_task_family
from watchtower_core.cli.validate_family import register_validate_family

CommandRegistrar = Callable[[argparse._SubParsersAction], None]


@dataclass(frozen=True, slots=True)
class CommandGroupSpec:
    """Registry metadata for one top-level CLI command family."""

    name: str
    registrar: CommandRegistrar
    implementation_path: str
    subcommand_implementation_paths: tuple[tuple[str, str], ...] = ()


QUERY_DISCOVERY_FAMILY_PATH = "core/python/src/watchtower_core/cli/query_discovery_family.py"
QUERY_KNOWLEDGE_FAMILY_PATH = "core/python/src/watchtower_core/cli/query_knowledge_family.py"
QUERY_RECORDS_FAMILY_PATH = "core/python/src/watchtower_core/cli/query_records_family.py"
QUERY_COORDINATION_FAMILY_PATH = (
    "core/python/src/watchtower_core/cli/query_coordination_family.py"
)


COMMAND_GROUP_SPECS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(
        name="doctor",
        registrar=register_doctor_family,
        implementation_path="core/python/src/watchtower_core/cli/doctor_family.py",
    ),
    CommandGroupSpec(
        name="route",
        registrar=register_route_family,
        implementation_path="core/python/src/watchtower_core/cli/route_family.py",
    ),
    CommandGroupSpec(
        name="plan",
        registrar=register_plan_family,
        implementation_path="core/python/src/watchtower_core/cli/plan_family.py",
    ),
    CommandGroupSpec(
        name="query",
        registrar=register_query_family,
        implementation_path="core/python/src/watchtower_core/cli/query_family.py",
        subcommand_implementation_paths=(
            ("paths", QUERY_DISCOVERY_FAMILY_PATH),
            ("commands", QUERY_DISCOVERY_FAMILY_PATH),
            ("foundations", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("workflows", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("references", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("standards", QUERY_KNOWLEDGE_FAMILY_PATH),
            ("prds", QUERY_RECORDS_FAMILY_PATH),
            ("decisions", QUERY_RECORDS_FAMILY_PATH),
            ("designs", QUERY_RECORDS_FAMILY_PATH),
            ("acceptance", QUERY_RECORDS_FAMILY_PATH),
            ("evidence", QUERY_RECORDS_FAMILY_PATH),
            ("tasks", QUERY_COORDINATION_FAMILY_PATH),
            ("coordination", QUERY_COORDINATION_FAMILY_PATH),
            ("authority", QUERY_COORDINATION_FAMILY_PATH),
            ("planning", QUERY_COORDINATION_FAMILY_PATH),
            ("initiatives", QUERY_COORDINATION_FAMILY_PATH),
            ("trace", QUERY_COORDINATION_FAMILY_PATH),
        ),
    ),
    CommandGroupSpec(
        name="task",
        registrar=register_task_family,
        implementation_path="core/python/src/watchtower_core/cli/task_family.py",
    ),
    CommandGroupSpec(
        name="sync",
        registrar=register_sync_family,
        implementation_path="core/python/src/watchtower_core/cli/sync_family.py",
    ),
    CommandGroupSpec(
        name="closeout",
        registrar=register_closeout_family,
        implementation_path="core/python/src/watchtower_core/cli/closeout_family.py",
    ),
    CommandGroupSpec(
        name="validate",
        registrar=register_validate_family,
        implementation_path="core/python/src/watchtower_core/cli/validate_family.py",
    ),
)
