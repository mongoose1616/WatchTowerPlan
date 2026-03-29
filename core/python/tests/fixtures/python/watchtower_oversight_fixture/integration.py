"""Synthetic hosted-pack integration used by pack-contract tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from watchtower_core.control_plane.paths import discover_repo_root
from watchtower_core.pack_integration import (
    PackIntegration,
    PackQueryRuntime,
    PackSyncRuntime,
    PackValidationRuntime,
)
from watchtower_core.validation.pack_targets import resolve_pack_validation_suite_targets


class OversightFixtureDocumentSemanticsValidationService:
    """Trivial callable factory target for synthetic pack-validation tests."""

    def __init__(self, loader: object) -> None:
        self.loader = loader


def _fixture_sync_relative_output_path() -> str:
    repo_root = discover_repo_root(Path(__file__).resolve())
    pack_root = Path(__file__).resolve().parents[3]
    return (
        f"{pack_root.relative_to(repo_root).as_posix()}/.wt/indexes/fixture_sync_index.json"
    )


def _run_sync_all(args: argparse.Namespace) -> int:
    relative_output_path = _fixture_sync_relative_output_path()
    repo_root = discover_repo_root(Path(__file__).resolve())
    destination = repo_root / relative_output_path
    payload = {
        "command": "watchtower-core oversight sync all",
        "status": "ok",
        "result_count": 1,
        "wrote": bool(args.write),
        "output_dir": None,
        "results": [
            {
                "target": "fixture-index",
                "artifact_kind": "index",
                "relative_output_path": relative_output_path,
                "output_path": str(destination) if args.write else None,
                "wrote": bool(args.write),
                "record_count": 1,
                "details": {},
            }
        ],
    }
    if args.write:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(
                {
                    "id": "index.fixture_sync",
                    "title": "Fixture Sync Index",
                    "status": "active",
                    "entries": [{"id": "fixture", "status": "active"}],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    if args.format == "json":
        print(json.dumps(payload, sort_keys=True))
        return 0
    if args.write:
        print(f"Fixture sync wrote {destination}.")
        return 0
    print("Fixture sync ran in dry-run mode.")
    return 0


def _register_oversight_namespace(*args: Any, **kwargs: Any) -> None:
    subparsers = args[0]
    parser = subparsers.add_parser(
        "oversight",
        help="Synthetic oversight namespace used to prove hosted-pack extensibility.",
    )
    oversight_subparsers = parser.add_subparsers(dest="oversight_command")
    parser.set_defaults(handler=lambda _parsed_args: 0)

    sync_parser = oversight_subparsers.add_parser(
        "sync",
        help="Synthetic oversight sync commands used by bootstrap tests.",
    )
    sync_subparsers = sync_parser.add_subparsers(dest="oversight_sync_command")
    sync_parser.set_defaults(handler=lambda _parsed_args: 0)

    all_parser = sync_subparsers.add_parser(
        "all",
        help="Rebuild the synthetic fixture sync slice.",
    )
    all_parser.add_argument("--write", action="store_true")
    all_parser.add_argument("--format", choices=("human", "json"), default="human")
    all_parser.set_defaults(handler=_run_sync_all)


def _query_runtime(*args: Any, **kwargs: Any) -> PackQueryRuntime:
    return PackQueryRuntime(commands=("assessments", "reviews"))


def _sync_targets(*args: Any, **kwargs: Any) -> PackSyncRuntime:
    return PackSyncRuntime(targets=("all",))


def _validation_provider(*args: Any, **kwargs: Any) -> PackValidationRuntime:
    return PackValidationRuntime(
        document_semantics_factory=OversightFixtureDocumentSemanticsValidationService,
        suite_target_resolver=resolve_pack_validation_suite_targets,
    )


PACK_INTEGRATION = PackIntegration(
    pack_id="pack.oversight",
    pack_slug="oversight",
    command_namespace="oversight",
    python_package="watchtower_oversight_fixture",
    declared_capabilities=(
        "command_registration",
        "query_runtime",
        "sync_targets",
        "validation_provider",
    ),
    command_implementation_path=(
        "core/python/tests/fixtures/python/watchtower_oversight_fixture/integration.py"
    ),
    command_registration=_register_oversight_namespace,
    query_runtime=_query_runtime,
    sync_targets=_sync_targets,
    validation_provider=_validation_provider,
)
