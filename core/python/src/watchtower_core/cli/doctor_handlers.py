"""Runtime handlers for the doctor command family."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _print_payload
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _run_doctor(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    schema_catalog = loader.load_schema_catalog()
    validator_registry = loader.load_validator_registry()
    command_index = loader.load_command_index()
    foundation_index = loader.load_foundation_index()
    reference_index = loader.load_reference_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    task_index = loader.load_task_index()
    initiative_index = loader.load_initiative_index()
    traceability_index = loader.load_traceability_index()
    payload = {
        "command": "watchtower-core doctor",
        "workspace": "core_python",
        "repo_root": str(loader.repo_root),
        "status": "ok",
        "message": (
            "watchtower-core workspace is available and core governed surfaces "
            "loaded successfully."
        ),
        "counts": {
            "schemas": len(schema_catalog.records),
            "validators": len(validator_registry.validators),
            "commands": len(command_index.entries),
            "foundations": len(foundation_index.entries),
            "references": len(reference_index.entries),
            "standards": len(standard_index.entries),
            "workflows": len(workflow_index.entries),
            "initiatives": len(initiative_index.entries),
            "tasks": len(task_index.entries),
            "traces": len(traceability_index.entries),
        },
        "recommended_baseline": [
            "watchtower-core sync all --write",
            "watchtower-core validate all",
            "./.venv/bin/python -m mypy src",
            "./.venv/bin/ruff check src tests/unit tests/integration",
            "./.venv/bin/python -m pytest",
        ],
    }
    if _print_payload(args, payload) == 0:
        return 0

    print(payload["message"])
    print(f"Repo Root: {payload['repo_root']}")
    counts = payload["counts"]
    if isinstance(counts, dict):
        print(
            "Loaded: "
            f"{counts['schemas']} schemas, "
            f"{counts['validators']} validators, "
            f"{counts['commands']} commands, "
            f"{counts['foundations']} foundations, "
            f"{counts['references']} references, "
            f"{counts['standards']} standards, "
            f"{counts['workflows']} workflows, "
            f"{counts['initiatives']} initiatives, "
            f"{counts['tasks']} tasks, "
            f"{counts['traces']} traces"
        )
    print("Recommended baseline:")
    for command in payload["recommended_baseline"]:
        print(f"- {command}")
    return 0
