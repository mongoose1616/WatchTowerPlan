from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

REPO_ROOT = Path(__file__).resolve().parents[4]


def load_json(relative_path: str) -> dict[str, object]:
    with (REPO_ROOT / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def materialize_additional_schema_catalog(pack_root: Path) -> dict[str, str]:
    repo_root = discover_repo_root(pack_root)
    control_plane_root = pack_root / ".wt"
    relative_root = control_plane_root.relative_to(repo_root).as_posix()
    schema_id = "urn:watchtower:schema:interfaces:packs:schema-store-note:v1"
    schema_relative_path = f"{relative_root}/schemas/interfaces/packs/schema_store_note.schema.json"
    catalog_path = f"{relative_root}/registries/schema_catalog.json"
    write_json(
        repo_root / schema_relative_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Schema Store Note",
            "description": "Schema discovered through an additional schema catalog.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "schema_store_note"},
            },
            "required": ["$schema", "kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        repo_root / catalog_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:schema-catalog:v1",
            "id": "registry.schema_catalog",
            "title": "Additional Schema Catalog",
            "status": "active",
            "schemas": [
                {
                    "schema_id": schema_id,
                    "title": "Schema Store Note",
                    "description": "Pack-local schema catalog record.",
                    "status": "active",
                    "schema_family": "interface",
                    "subject_kind": "schema_store_note",
                    "version": "v1",
                    "canonical_path": schema_relative_path,
                }
            ],
        },
    )
    return {
        "catalog_path": catalog_path,
        "schema_id": schema_id,
        "schema_relative_path": schema_relative_path,
    }


def documentation_and_pack_interface_examples() -> list[
    tuple[dict[str, object], dict[str, object], str]
]:
    return [
        (
            {
                "id": "ref.example.inline_payload",
                "title": "Inline Reference",
                "summary": "Inline reference front matter payload.",
                "type": "reference",
                "status": "active",
                "tags": ["inline"],
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
            },
            {
                "id": "ref.example.inline_payload",
                "title": "Inline Reference",
                "summary": "Missing tags should fail.",
                "type": "reference",
                "status": "active",
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
            },
            "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
        ),
        (
            {
                "id": "std.example.inline_payload",
                "title": "Inline Standard",
                "summary": "Inline standard front matter payload.",
                "type": "standard",
                "status": "active",
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
                "authority": "authoritative",
            },
            {
                "id": "std.example.inline_payload",
                "title": "Inline Standard",
                "summary": "Missing authority should fail for governed standards.",
                "type": "standard",
                "status": "active",
                "owner": "repository_maintainer",
                "updated_at": "2026-03-16T07:15:00Z",
                "audience": "shared",
            },
            "urn:watchtower:schema:interfaces:documentation:standard-front-matter:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
                "id": "note.example.inline_payload",
                "title": "Inline Work Item Note",
                "summary": "Inline pack-facing note.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_id": "task.example.inline_payload",
                "work_item_type": "task",
                "lifecycle_stage": "active",
                "updated_at": "2026-03-16T07:15:00Z",
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
                "id": "note.example.inline_payload",
                "title": "Inline Work Item Note",
                "summary": "Missing work_item_id should fail.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_type": "task",
                "lifecycle_stage": "active",
                "updated_at": "2026-03-16T07:15:00Z",
            },
            "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
                "id": "envelope.example.inline_payload",
                "title": "Inline Extraction Envelope",
                "summary": "Inline extraction payload.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_id": "task.example.inline_payload",
                "trace_id": "trace.example.inline_payload",
                "source_note_id": "note.example.inline_payload",
                "workflow_run_id": "run.example.inline_payload",
                "extraction_method": "manual",
                "created_at": "2026-03-16T07:15:00Z",
                "observations": [
                    {
                        "observation_id": "observation.example.inline_payload",
                        "summary": "Observed one durable fact.",
                    }
                ],
                "candidate_knowledge": [
                    {
                        "candidate_id": "candidate.example.inline_payload",
                        "title": "Inline Candidate",
                        "summary": "Candidate knowledge extracted from the note.",
                        "knowledge_family": "reference",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
                "id": "envelope.example.inline_payload",
                "title": "Inline Extraction Envelope",
                "summary": "Missing trace_id should fail.",
                "status": "active",
                "pack_id": "pack.example",
                "work_item_id": "task.example.inline_payload",
                "source_note_id": "note.example.inline_payload",
                "workflow_run_id": "run.example.inline_payload",
                "extraction_method": "manual",
                "created_at": "2026-03-16T07:15:00Z",
                "observations": [
                    {
                        "observation_id": "observation.example.inline_payload",
                        "summary": "Observed one durable fact.",
                    }
                ],
                "candidate_knowledge": [
                    {
                        "candidate_id": "candidate.example.inline_payload",
                        "title": "Inline Candidate",
                        "summary": "Candidate knowledge extracted from the note.",
                        "knowledge_family": "reference",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:extraction-output-envelope:v1",
        ),
    ]


def pack_contract_examples() -> list[tuple[dict[str, object], dict[str, object], str]]:
    return [
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
                "surface_name": "pack_settings",
                "contract_version": "v1",
                "description": "Inline pack settings payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "pack_id": "pack.example",
                "workspace_roots": {
                    "workspace_root": "packs/example",
                    "machine_root": "packs/example/.wt",
                    "docs_root": "packs/example/docs",
                    "workflows_root": "packs/example/workflows",
                    "tracking_root": "packs/example/tracking",
                    "initiatives_root": "packs/example/initiatives",
                    "projects_root": "packs/example/projects",
                    "overview_path": "packs/example/overview.md",
                },
                "default_validation_suite_id": "suite.example.validation_baseline",
                "surfaces": [
                    {
                        "surface_name": "schema_catalog",
                        "surface_kind": "schema_collection",
                        "path": "core/control_plane/registries/schema_catalog.json",
                        "authority": "authoritative",
                        "visibility": "hidden",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
                "surface_name": "pack_settings",
                "contract_version": "v1",
                "description": "Invalid pack settings payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "pack_id": "pack.example",
                "workspace_roots": {
                    "workspace_root": "packs/example",
                    "machine_root": "packs/example/.wt",
                    "docs_root": "packs/example/docs",
                    "workflows_root": "packs/example/workflows",
                    "tracking_root": "packs/example/tracking",
                    "initiatives_root": "packs/example/initiatives",
                    "projects_root": "packs/example/projects",
                    "overview_path": "packs/example/overview.md",
                },
                "default_validation_suite_id": "suite.example.validation_baseline",
                "surfaces": [
                    {
                        "surface_name": "schema_catalog",
                        "surface_kind": "wrong_kind",
                        "path": "core/control_plane/registries/schema_catalog.json",
                        "authority": "authoritative",
                        "visibility": "hidden",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:status-registry:v1",
                "surface_name": "status_registry",
                "contract_version": "v1",
                "description": "Inline status registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "statuses": [
                    {
                        "value": "active",
                        "entry_status": "active",
                        "summary": "Currently open.",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:status-registry:v1",
                "surface_name": "status_registry",
                "contract_version": "v1",
                "description": "Invalid status registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "statuses": [
                    {
                        "value": "active",
                        "entry_status": "unsupported",
                        "summary": "Currently open.",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:status-registry:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:actor-registry:v1",
                "surface_name": "actor_registry",
                "contract_version": "v1",
                "description": "Inline actor registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "actors": [
                    {
                        "actor_id": "actor.example",
                        "actor_type": "agent",
                        "label": "Example Agent",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:actor-registry:v1",
                "surface_name": "actor_registry",
                "contract_version": "v1",
                "description": "Invalid actor registry payload.",
                "updated_at": "2026-03-16T05:15:00Z",
                "actors": [
                    {
                        "actor_id": "example",
                        "actor_type": "agent",
                        "label": "Example Agent",
                    }
                ],
            },
            "urn:watchtower:schema:interfaces:packs:actor-registry:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:artifacts:registries:pack-registry:v1",
                "id": "registry.packs",
                "title": "Inline Pack Registry",
                "status": "active",
                "packs": [
                    {
                        "pack_id": "pack.example",
                        "pack_slug": "example",
                        "command_namespace": "example",
                        "pack_settings_path": "packs/example/.wt/manifests/pack_settings.json",
                        "pack_runtime_manifest_path": (
                            "packs/example/.wt/manifests/pack_runtime_manifest.json"
                        ),
                        "python_distribution": "watchtower-example",
                        "python_package": "watchtower_example",
                    }
                ],
            },
            {
                "$schema": "urn:watchtower:schema:artifacts:registries:pack-registry:v1",
                "id": "registry.packs",
                "title": "Invalid Pack Registry",
                "status": "active",
                "packs": [
                    {
                        "pack_id": "example",
                        "pack_slug": "example",
                        "command_namespace": "example",
                        "pack_settings_path": "packs/example/.wt/manifests/pack_settings.json",
                        "pack_runtime_manifest_path": (
                            "packs/example/.wt/manifests/pack_runtime_manifest.json"
                        ),
                        "python_distribution": "watchtower-example",
                        "python_package": "watchtower_example",
                    }
                ],
            },
            "urn:watchtower:schema:artifacts:registries:pack-registry:v1",
        ),
        (
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
                "surface_name": "pack_runtime_manifest",
                "contract_version": "v1",
                "description": "Inline runtime manifest payload.",
                "updated_at": "2026-03-20T22:10:00Z",
                "pack_id": "pack.example",
                "pack_slug": "example",
                "command_namespace": "example",
                "python_distribution": "watchtower-example",
                "python_package": "watchtower_example",
                "integration_module": "watchtower_example.integration",
                "declared_capabilities": [
                    "command_registration",
                    "query_runtime",
                    "sync_targets",
                    "validation_provider",
                ],
                "required_validation_suite_ids": ["suite.example.validation_baseline"],
                "owned_roots": {
                    "workspace_root": "packs/example",
                    "machine_root": "packs/example/.wt",
                    "docs_root": "packs/example/docs",
                    "workflows_root": "packs/example/workflows",
                    "tracking_root": "packs/example/tracking",
                    "python_root": "packs/example/python",
                },
            },
            {
                "$schema": "urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
                "surface_name": "pack_runtime_manifest",
                "contract_version": "v1",
                "description": "Invalid runtime manifest payload.",
                "updated_at": "2026-03-20T22:10:00Z",
                "pack_id": "pack.example",
                "pack_slug": "Example",
                "command_namespace": "example",
                "python_distribution": "watchtower-example",
                "python_package": "watchtower_example",
                "integration_module": "watchtower_example.integration",
                "declared_capabilities": [
                    "command_registration",
                    "query_runtime",
                    "sync_targets",
                    "validation_provider",
                ],
                "required_validation_suite_ids": ["suite.example.validation_baseline"],
                "owned_roots": {
                    "workspace_root": "packs/example",
                    "machine_root": "packs/example/.wt",
                    "docs_root": "packs/example/docs",
                    "workflows_root": "packs/example/workflows",
                    "tracking_root": "packs/example/tracking",
                    "python_root": "packs/example/python",
                },
            },
            "urn:watchtower:schema:interfaces:packs:pack-runtime-manifest:v1",
        ),
    ]
