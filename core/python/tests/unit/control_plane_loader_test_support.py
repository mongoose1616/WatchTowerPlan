from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from watchtower_core.control_plane.errors import ArtifactLoadError
from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def copy_validation_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def discover_repo_root(start: Path) -> Path:
    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    raise ValueError(f"Could not discover repo root for fixture destination: {start}")


def require_default_pack(loader: ControlPlaneLoader):
    try:
        return loader.load_pack_registry().default_pack()
    except (ArtifactLoadError, ValueError):
        pytest.skip("Repository does not declare a default hosted pack.")


def require_pack_runtime_manifest(loader: ControlPlaneLoader):
    try:
        return loader.load_pack_runtime_manifest()
    except ArtifactLoadError:
        pytest.skip("Repository does not publish a default pack runtime manifest.")


def materialize_pack_validation_surfaces(pack_root: Path) -> dict[str, str]:
    repo_root = discover_repo_root(pack_root)
    control_plane_root = pack_root / ".wt"
    workspace_relative_root = pack_root.relative_to(repo_root).as_posix()
    relative_root = control_plane_root.relative_to(repo_root).as_posix()
    schema_id = "urn:watchtower:schema:interfaces:packs:loader-pack-note:v1"
    schema_relative_path = f"{relative_root}/schemas/interfaces/packs/loader_pack_note.schema.json"
    validator_id = "validator.packs.loader_pack_note"
    validator_registry_path = f"{relative_root}/registries/validator_registry.json"
    validation_suite_registry_path = f"{relative_root}/registries/validation_suite_registry.json"
    suite_id = "suite.loader_test.validation_baseline"
    artifact_relative_path = f"{relative_root}/work_items/loader_pack_note.json"
    write_json(
        repo_root / schema_relative_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Loader Pack Note",
            "description": "Schema published by a pack-local schema catalog.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "loader_pack_note"},
                "title": {"type": "string"},
            },
            "required": ["$schema", "kind", "title"],
            "additionalProperties": False,
        },
    )
    write_json(
        repo_root / f"{relative_root}/registries/schema_catalog.json",
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:schema-catalog:v1",
            "id": "registry.schema_catalog",
            "title": "Pack Schema Catalog",
            "status": "active",
            "schemas": [
                {
                    "schema_id": schema_id,
                    "title": "Loader Pack Note",
                    "description": "Pack-local schema for loader tests.",
                    "status": "active",
                    "schema_family": "interface",
                    "subject_kind": "loader_pack_note",
                    "version": "v1",
                    "canonical_path": schema_relative_path,
                }
            ],
        },
    )
    write_json(
        repo_root / validator_registry_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:validator-registry:v1",
            "id": "registry.validators",
            "title": "Pack Validator Registry",
            "status": "active",
            "validators": [
                {
                    "id": validator_id,
                    "title": "Loader Pack Note Validator",
                    "description": "Schema-backed validator declared by a pack.",
                    "status": "active",
                    "engine": "json_schema",
                    "artifact_kind": "loader_pack_note",
                    "applies_to": [artifact_relative_path],
                    "schema_ids": [schema_id],
                }
            ],
        },
    )
    write_json(
        repo_root / validation_suite_registry_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:validation-suite-registry:v1",
            "id": "registry.validation_suites",
            "title": "Loader Pack Validation Suites",
            "status": "active",
            "suites": [
                {
                    "id": suite_id,
                    "title": "Loader Pack Validation Baseline",
                    "description": "Pack-local validation baseline for loader tests.",
                    "status": "active",
                    "steps": [
                        {
                            "id": "step.loader_test.artifacts",
                            "title": "Validate loader-test artifacts",
                            "description": "Validate the pack-local loader artifact.",
                            "step_kind": "artifact",
                        }
                    ],
                }
            ],
        },
    )
    write_json(
        repo_root / artifact_relative_path,
        {
            "$schema": schema_id,
            "kind": "loader_pack_note",
            "title": "Loader Pack Note",
        },
    )
    pack_settings_path = f"{relative_root}/manifests/pack_settings.json"
    write_json(
        repo_root / pack_settings_path,
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
            "surface_name": "pack_settings",
            "contract_version": "v1",
            "description": "Pack settings for active loader validation tests.",
            "updated_at": "2026-03-16T21:10:00Z",
            "pack_id": "pack.loader_test",
            "surfaces": [
                {
                    "surface_name": "schema_catalog",
                    "surface_kind": "schema_collection",
                    "path": f"{relative_root}/registries/schema_catalog.json",
                    "authority": "authoritative",
                    "visibility": "hidden",
                },
                {
                    "surface_name": "validator_registry",
                    "surface_kind": "registry",
                    "path": validator_registry_path,
                    "authority": "authoritative",
                    "visibility": "hidden",
                },
                {
                    "surface_name": "validation_suite_registry",
                    "surface_kind": "registry",
                    "path": validation_suite_registry_path,
                    "authority": "authoritative",
                    "visibility": "hidden",
                },
            ],
            "workspace_roots": {
                "workspace_root": workspace_relative_root,
                "machine_root": relative_root,
                "docs_root": f"{workspace_relative_root}/docs",
                "workflows_root": f"{workspace_relative_root}/workflows",
                "tracking_root": f"{workspace_relative_root}/tracking",
                "initiatives_root": f"{workspace_relative_root}/initiatives",
                "projects_root": f"{workspace_relative_root}/projects",
                "overview_path": f"{workspace_relative_root}/overview.md",
            },
            "default_validation_suite_id": suite_id,
        },
    )
    return {
        "artifact_relative_path": artifact_relative_path,
        "pack_settings_path": pack_settings_path,
        "schema_id": schema_id,
        "schema_relative_path": schema_relative_path,
        "suite_id": suite_id,
        "validator_id": validator_id,
        "validation_suite_registry_path": validation_suite_registry_path,
        "validator_registry_path": validator_registry_path,
    }
