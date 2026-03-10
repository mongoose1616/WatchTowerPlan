"""Typed registry for top-level CLI command families."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass

from watchtower_core.cli.closeout_family import register_closeout_family
from watchtower_core.cli.doctor_family import register_doctor_family
from watchtower_core.cli.query_family import register_query_family
from watchtower_core.cli.sync_family import register_sync_family
from watchtower_core.cli.validate_family import register_validate_family

CommandRegistrar = Callable[[argparse._SubParsersAction], None]


@dataclass(frozen=True, slots=True)
class CommandGroupSpec:
    """Registry metadata for one top-level CLI command family."""

    name: str
    registrar: CommandRegistrar


COMMAND_GROUP_SPECS: tuple[CommandGroupSpec, ...] = (
    CommandGroupSpec(name="doctor", registrar=register_doctor_family),
    CommandGroupSpec(name="query", registrar=register_query_family),
    CommandGroupSpec(name="sync", registrar=register_sync_family),
    CommandGroupSpec(name="closeout", registrar=register_closeout_family),
    CommandGroupSpec(name="validate", registrar=register_validate_family),
)
