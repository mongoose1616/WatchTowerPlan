"""Runtime handlers for the doctor command family."""

from __future__ import annotations

import argparse
from collections.abc import Callable

from watchtower_core.cli.handler_common import _emit_detail_result
from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader import ControlPlaneLoader


def _declared_pack_surface_names(loader: ControlPlaneLoader) -> frozenset[str]:
    pack_settings_path = loader.activate_pack_settings()
    pack_settings = loader.load_pack_settings(pack_settings_path)
    return frozenset(declaration.surface_name for declaration in pack_settings.surfaces)


def _optional_entry_count(
    loader: ControlPlaneLoader,
    *,
    declared_surface_names: frozenset[str],
    surface_name: str,
    load_index: Callable[[], object],
) -> int:
    if surface_name not in declared_surface_names:
        return 0
    index = load_index()
    entries = getattr(index, "entries", None)
    if not isinstance(entries, tuple):
        return 0
    return len(entries)


def _default_pack_command_namespace(loader: ControlPlaneLoader) -> str | None:
    try:
        pack_settings_path = loader.activate_pack_settings()
        runtime_manifest = loader.load_pack_runtime_manifest(
            pack_settings_path=pack_settings_path
        )
    except (ArtifactLoadError, KeyError, ValueError):
        runtime_manifest = None
    if runtime_manifest is not None:
        return runtime_manifest.command_namespace
    try:
        return loader.load_pack_registry().default_pack().command_namespace
    except ValueError:
        return None


def _run_doctor(args: argparse.Namespace) -> int:
    loader = ControlPlaneLoader()
    schema_catalog = loader.load_schema_catalog()
    validator_registry = loader.load_validator_registry()
    command_index = loader.load_command_index()
    foundation_index = loader.load_foundation_index()
    reference_index = loader.load_reference_index()
    standard_index = loader.load_standard_index()
    workflow_index = loader.load_workflow_index()
    traceability_index = loader.load_traceability_index()
    declared_surface_names = _declared_pack_surface_names(loader)
    task_count = _optional_entry_count(
        loader,
        declared_surface_names=declared_surface_names,
        surface_name="task_index",
        load_index=loader.load_task_index,
    )
    initiative_count = _optional_entry_count(
        loader,
        declared_surface_names=declared_surface_names,
        surface_name="initiative_index",
        load_index=loader.load_initiative_index,
    )
    recommended_baseline = [
        "watchtower-core sync command-index --write",
        "watchtower-core sync route-index --write",
        "watchtower-core sync repository-paths --write",
        "watchtower-core validate all",
        "./.venv/bin/python -m mypy src",
        "./.venv/bin/ruff check src tests/unit tests/integration",
        "./.venv/bin/python -m pytest tests/unit tests/integration -q",
    ]
    default_namespace = _default_pack_command_namespace(loader)
    if default_namespace:
        recommended_baseline.insert(3, f"watchtower-core {default_namespace} sync all --write")
    payload = {
        "command": "watchtower-core doctor",
        "workspace": "core_python",
        "repo_root": str(loader.repo_root),
        "status": "ok",
        "message": (
            "watchtower-core workspace is available and core governed surfaces loaded successfully."
        ),
        "counts": {
            "schemas": len(schema_catalog.records),
            "validators": len(validator_registry.validators),
            "commands": len(command_index.entries),
            "foundations": len(foundation_index.entries),
            "references": len(reference_index.entries),
            "standards": len(standard_index.entries),
            "workflows": len(workflow_index.entries),
            "initiatives": initiative_count,
            "tasks": task_count,
            "traces": len(traceability_index.entries),
        },
        "recommended_baseline": recommended_baseline,
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
