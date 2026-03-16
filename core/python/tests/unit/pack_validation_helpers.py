from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def materialize_pack_validation_suite(
    pack_root: Path,
    *,
    include_validation_suite_registry: bool = True,
    suite_step_validator_id: str | None = None,
) -> dict[str, str]:
    control_plane_root = pack_root / ".wt"
    relative_root = control_plane_root.relative_to(REPO_ROOT).as_posix()
    schema_id = "urn:watchtower:schema:interfaces:domain-packs:plan-note:v1"
    schema_relative_path = f"{relative_root}/schemas/interfaces/domain_packs/plan_note.schema.json"
    validator_id = "validator.domain_packs.plan_note"
    suite_id = "suite.plan.validation_baseline"
    artifact_relative_path = f"{relative_root}/work_items/plan_note.json"
    validation_suite_registry_path = f"{relative_root}/registries/validation_suite_registry.json"

    write_json(
        REPO_ROOT / schema_relative_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Plan Note",
            "description": "Pack-local schema used by validation suite tests.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "plan_note"},
                "title": {"type": "string"},
            },
            "required": ["$schema", "kind", "title"],
            "additionalProperties": False,
        },
    )
    write_json(
        REPO_ROOT / f"{relative_root}/registries/schema_catalog.json",
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:schema-catalog:v1",
            "id": "registry.schema_catalog",
            "title": "Plan Pack Schema Catalog",
            "status": "active",
            "schemas": [
                {
                    "schema_id": schema_id,
                    "title": "Plan Note",
                    "description": "Pack-local schema for plan note artifacts.",
                    "status": "active",
                    "schema_family": "interface",
                    "subject_kind": "plan_note",
                    "version": "v1",
                    "canonical_path": schema_relative_path,
                }
            ],
        },
    )
    write_json(
        REPO_ROOT / f"{relative_root}/registries/validator_registry.json",
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:validator-registry:v1",
            "id": "registry.validators",
            "title": "Plan Pack Validators",
            "status": "active",
            "validators": [
                {
                    "id": validator_id,
                    "title": "Plan Note Validator",
                    "description": "Pack-local validator for plan note artifacts.",
                    "status": "active",
                    "engine": "json_schema",
                    "artifact_kind": "plan_note",
                    "applies_to": [artifact_relative_path],
                    "schema_ids": [schema_id],
                },
                {
                    "id": "validator.domain_packs.validation_suite_registry",
                    "title": "Plan Validation Suite Registry Validator",
                    "description": "Pack-local validator for the validation suite registry artifact.",
                    "status": "active",
                    "engine": "json_schema",
                    "artifact_kind": "validation_suite_registry",
                    "applies_to": [validation_suite_registry_path],
                    "schema_ids": [
                        "urn:watchtower:schema:artifacts:registries:validation-suite-registry:v1"
                    ],
                },
            ],
        },
    )
    write_json(
        REPO_ROOT / artifact_relative_path,
        {
            "$schema": schema_id,
            "kind": "plan_note",
            "title": "Plan Validation Note",
        },
    )
    if include_validation_suite_registry:
        write_json(
            REPO_ROOT / validation_suite_registry_path,
            {
                "$schema": (
                    "urn:watchtower:schema:artifacts:registries:"
                    "validation-suite-registry:v1"
                ),
                "id": "registry.validation_suites",
                "title": "Plan Validation Suites",
                "status": "active",
                "suites": [
                    {
                        "id": suite_id,
                        "title": "Plan Validation Baseline",
                        "description": "Pack-contract plus schema-backed plan note validation.",
                        "status": "active",
                        "steps": [
                            {
                                "id": "step.plan.pack_contract",
                                "title": "Validate plan pack contract",
                                "description": "Ensure the pack publishes the governed surfaces reusable core expects.",
                                "step_kind": "pack_contract"
                            },
                            {
                                "id": "step.plan.artifacts",
                                "title": "Validate plan note artifacts",
                                "description": "Validate the pack-local plan note artifacts.",
                                "step_kind": "artifact",
                                "paths": [artifact_relative_path],
                                "validator_id": suite_step_validator_id or validator_id
                            }
                        ]
                    }
                ]
            },
        )
    pack_settings_path = f"{relative_root}/pack_settings.json"
    surfaces = [
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
            "path": f"{relative_root}/registries/validator_registry.json",
            "authority": "authoritative",
            "visibility": "hidden",
        },
    ]
    if include_validation_suite_registry:
        surfaces.append(
            {
                "surface_name": "validation_suite_registry",
                "surface_kind": "registry",
                "path": validation_suite_registry_path,
                "authority": "authoritative",
                "visibility": "hidden",
            }
        )
    write_json(
        REPO_ROOT / pack_settings_path,
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
            "surface_name": "pack_settings",
            "contract_version": "v1",
            "description": "Pack settings for validation suite tests.",
            "updated_at": "2026-03-16T21:40:00Z",
            "pack_id": "pack.plan",
            "surfaces": surfaces,
        },
    )
    return {
        "artifact_relative_path": artifact_relative_path,
        "pack_settings_path": pack_settings_path,
        "schema_id": schema_id,
        "schema_relative_path": schema_relative_path,
        "suite_id": suite_id,
        "validation_suite_registry_path": validation_suite_registry_path,
        "validator_id": validator_id,
    }
