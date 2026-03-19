"""Runtime handlers for the doctor command family."""

from __future__ import annotations

import argparse

from watchtower_core.cli.handler_common import _emit_detail_result
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.plan_runtime.plan_workspace import PlanWorkspaceService


def _run_doctor(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    plan_workspace = PlanWorkspaceService(loader)
    schema_catalog = loader.load_schema_catalog()
    validator_registry = loader.load_validator_registry()
    command_index = loader.load_command_index()
    foundation_index = loader.load_foundation_index()
    reference_index = loader.load_reference_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    task_entries = plan_workspace.load_task_entries()
    initiative_index = plan_workspace.load_initiative_index()
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
            "tasks": len(task_entries),
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

    def _render_human() -> None:
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

    return _emit_detail_result(
        args,
        payload_factory=lambda: payload,
        render_human=_render_human,
    )
