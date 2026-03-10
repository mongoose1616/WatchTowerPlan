"""Typed registry for top-level CLI command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass

from watchtower_core.cli.closeout_family import register_closeout_family
from watchtower_core.cli.doctor_family import register_doctor_family
from watchtower_core.cli.query_family import register_query_family
from watchtower_core.cli.route_family import register_route_family
from watchtower_core.cli.sync_family import register_sync_family
from watchtower_core.cli.validate_family import register_validate_family

CommandRegistrar = Callable[[argparse._SubParsersAction], None]


@dataclass(frozen=True, slots=True)
class CommandGroupSpec:
    """Registry metadata for one top-level CLI command family."""

    name: str
    registrar: CommandRegistrar
    implementation_path: str


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
        name="query",
        registrar=register_query_family,
        implementation_path="core/python/src/watchtower_core/cli/query_family.py",
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
