from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

import pytest

from tests.unit.control_plane_loader_test_support import require_default_pack
from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import ArtifactValidationService, ValidationSelectionError

REPO_ROOT = Path(__file__).resolve().parents[4]


def write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def _copy_validation_repo_subset(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def _discover_repo_root(start: Path) -> Path:
    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if (parent / "core/control_plane").is_dir() and (parent / "core/python").is_dir():
            return parent
    raise ValueError(f"Could not discover repo root for fixture destination: {start}")


def materialize_pack_validation_surfaces(pack_root: Path) -> dict[str, str]:
    repo_root = _discover_repo_root(pack_root)
    control_plane_root = pack_root / ".wt"
    workspace_relative_root = pack_root.relative_to(repo_root).as_posix()
    relative_root = control_plane_root.relative_to(repo_root).as_posix()
    schema_id = "urn:watchtower:schema:interfaces:packs:artifact-pack-note:v1"
    schema_relative_path = (
        f"{relative_root}/schemas/interfaces/packs/artifact_pack_note.schema.json"
    )
    validator_id = "validator.packs.artifact_pack_note"
    validation_suite_registry_path = f"{relative_root}/registries/validation_suite_registry.json"
    suite_id = "suite.artifact_test.validation_baseline"
    artifact_relative_path = f"{relative_root}/work_items/artifact_pack_note.json"
    write_json(
        repo_root / schema_relative_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Artifact Pack Note",
            "description": "Pack-local schema used by artifact validation tests.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "artifact_pack_note"},
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
            "title": "Artifact Validation Pack Schema Catalog",
            "status": "active",
            "schemas": [
                {
                    "schema_id": schema_id,
                    "title": "Artifact Pack Note",
                    "description": "Schema record for pack-local artifact validation tests.",
                    "status": "active",
                    "schema_family": "interface",
                    "subject_kind": "artifact_pack_note",
                    "version": "v1",
                    "canonical_path": schema_relative_path,
                }
            ],
        },
    )
    write_json(
        repo_root / f"{relative_root}/registries/validator_registry.json",
        {
            "$schema": "urn:watchtower:schema:artifacts:registries:validator-registry:v1",
            "id": "registry.validators",
            "title": "Artifact Validation Pack Validators",
            "status": "active",
            "validators": [
                {
                    "id": validator_id,
                    "title": "Artifact Pack Note Validator",
                    "description": (
                        "Validator selected from pack settings rather than "
                        "the repo default registry."
                    ),
                    "status": "active",
                    "engine": "json_schema",
                    "artifact_kind": "artifact_pack_note",
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
            "title": "Artifact Validation Pack Suites",
            "status": "active",
            "suites": [
                {
                    "id": suite_id,
                    "title": "Artifact Validation Pack Baseline",
                    "description": "Minimal validation suite for artifact pack tests.",
                    "status": "active",
                    "steps": [
                        {
                            "id": "step.artifact_test.artifacts",
                            "title": "Validate artifact-test note artifacts",
                            "description": "Validate pack-local artifact note JSON.",
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
            "kind": "artifact_pack_note",
            "title": "Artifact Pack Note",
        },
    )
    pack_settings_path = f"{relative_root}/manifests/pack_settings.json"
    write_json(
        repo_root / pack_settings_path,
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-settings:v1",
            "surface_name": "pack_settings",
            "contract_version": "v1",
            "description": "Pack settings for artifact validation tests.",
            "updated_at": "2026-03-16T21:10:00Z",
            "pack_id": "pack.artifact_test",
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
                    "path": f"{relative_root}/registries/validator_registry.json",
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
        "suite_id": suite_id,
        "validator_id": validator_id,
    }


def test_artifact_validation_auto_selects_acceptance_contract_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        "core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json"
    )

    assert result.passed is True
    assert result.validator_id == "validator.control_plane.acceptance_contract"
    assert result.issue_count == 0


def test_artifact_validation_allows_empty_traceability_index_after_export_scrub(
    tmp_path: Path,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    traceability_path = (
        repo_root / "core" / "control_plane" / "indexes" / "traceability"
        / "traceability_index.json"
    )
    document = json.loads(traceability_path.read_text(encoding="utf-8"))
    document["entries"] = []
    write_json(traceability_path, document)

    service = ArtifactValidationService(ControlPlaneLoader(repo_root))
    result = service.validate("core/control_plane/indexes/traceability/traceability_index.json")

    assert result.passed is True
    assert result.validator_id == "validator.control_plane.traceability_index"
    assert result.issue_count == 0


def test_artifact_validation_supports_explicit_pack_work_item_note_validator(
    tmp_path: Path,
) -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))
    artifact_path = tmp_path / "pack_work_item_note.json"
    write_json(
        artifact_path,
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
            "id": "note.example.work_item",
            "title": "Example Work Item Note",
            "summary": "Valid pack-facing work item note.",
            "status": "active",
            "pack_id": "pack.example",
            "work_item_id": "task.example.work_item",
            "work_item_type": "task",
            "lifecycle_stage": "active",
            "updated_at": "2026-03-16T07:15:00Z",
        },
    )

    result = service.validate(artifact_path, validator_id="validator.interface.pack_work_item_note")

    assert result.passed is True
    assert result.validator_id == "validator.interface.pack_work_item_note"
    assert result.issue_count == 0


def test_artifact_validation_auto_selects_benchmark_record_validator_for_retained_record(
    tmp_path: Path,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    service = ArtifactValidationService(ControlPlaneLoader(repo_root))
    artifact_path = (
        repo_root / "core" / "control_plane" / "records" / "benchmarks" / "benchmark_fixture.json"
    )
    write_json(
        artifact_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:records:benchmark-record:v1",
            "id": "benchmark.fixture.current",
            "title": "Benchmark Fixture",
            "status": "active",
            "benchmark_kind": "baseline",
            "suite_id": "suite.benchmark.fixture",
            "suite_title": "Fixture Benchmark Suite",
            "recorded_at": "2026-03-29T12:30:00Z",
            "working_directory": "core/python",
            "benchmark_contract": {
                "working_directory": "core/python",
                "warmup_runs": 1,
                "measured_runs": 2,
                "execution_mode": "serialized_subprocess",
                "failure_posture": "fail_closed",
                "telemetry_environment": {
                    "telemetry_on": {
                        "WATCHTOWER_TELEMETRY": "on",
                        "WATCHTOWER_TELEMETRY_STDERR": "off",
                        "WATCHTOWER_TELEMETRY_DIR": "<temp benchmark dir>"
                    },
                    "telemetry_off": {
                        "WATCHTOWER_TELEMETRY": "off",
                        "WATCHTOWER_TELEMETRY_STDERR": "off"
                    }
                }
            },
            "environment_context": {
                "python_version": "3.12.0",
                "python_executable": "python",
                "platform": "linux-test"
            },
            "commands": [
                {
                    "command_id": "step.benchmark.fixture",
                    "title": "Fixture Command",
                    "description": "Fixture benchmark command.",
                    "command": "watchtower-core doctor",
                    "argv": ["watchtower-core", "doctor"],
                    "warmup_runs": 1,
                    "measured_runs": 2,
                    "telemetry_on_runs_ms": [12.4, 11.8],
                    "telemetry_off_runs_ms": [11.0, 10.9],
                    "median_ms_telemetry_on": 12.1,
                    "median_ms_telemetry_off": 10.95,
                    "delta_ms": 1.15,
                    "ratio_on_over_off": 1.105,
                    "top_nested_operations": []
                }
            ]
        },
    )

    result = service.validate(artifact_path)

    assert result.passed is True
    assert result.validator_id == "validator.control_plane.benchmark_record"
    assert result.issue_count == 0


def test_artifact_validation_prefers_more_specific_pack_owned_validator() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)
    service = ArtifactValidationService(loader)
    pack = require_default_pack(loader)
    machine_root = loader.load_pack_settings().workspace_roots.machine_root
    work_item_root = loader.resolve_path(f"{machine_root}/work_items")
    artifact_candidates = sorted(work_item_root.glob("pack_work_item_note*.json"))
    if not artifact_candidates:
        pytest.skip(
            "Active pack does not publish a pack_work_item_note artifact that overlaps "
            "the generic interface validator."
        )
    artifact_path = loader.workspace_config.logical_path_for(artifact_candidates[0])

    result = service.validate(artifact_path)

    assert result.passed is True
    assert result.validator_id == f"validator.{pack.pack_slug}.pack_work_item_note"
    assert result.issue_count == 0


def test_artifact_validation_rejects_schema_definition_without_explicit_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError):
        service.validate("core/control_plane/schemas/artifacts/benchmark_record.schema.json")


def test_artifact_validation_auto_selects_pack_settings_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate("core/control_plane/manifests/pack_settings.json")

    assert result.passed is True
    assert result.validator_id == "validator.control_plane.pack_settings"
    assert result.issue_count == 0


def test_artifact_validation_rejects_unsupported_path_without_validator() -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(ValidationSelectionError):
        service.validate("core/docs/commands/core_python/watchtower_core.md")


def test_artifact_validation_reports_invalid_json(tmp_path: Path) -> None:
    document_path = tmp_path / "invalid.json"
    document_path.write_text("{ invalid json", encoding="utf-8")
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    result = service.validate(
        document_path,
        validator_id="validator.control_plane.acceptance_contract",
    )

    assert result.passed is False
    assert result.issue_count == 1
    assert result.issues[0].code == "json_parse_invalid"


def test_artifact_validation_reports_invalid_pack_interface_artifact(tmp_path: Path) -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))
    artifact_path = tmp_path / "pack_work_item_note_invalid.json"
    write_json(
        artifact_path,
        {
            "$schema": "urn:watchtower:schema:interfaces:packs:pack-work-item-note:v1",
            "id": "note.example.work_item",
            "title": "Invalid Work Item Note",
            "summary": "Missing work item provenance.",
            "status": "active",
            "pack_id": "pack.example",
            "work_item_type": "task",
            "lifecycle_stage": "active",
            "updated_at": "2026-03-16T07:15:00Z",
        },
    )

    result = service.validate(
        artifact_path,
        validator_id="validator.interface.pack_work_item_note",
    )

    assert result.passed is False
    assert result.validator_id == "validator.interface.pack_work_item_note"
    assert result.issue_count >= 1
    assert any("work_item_id" in issue.message for issue in result.issues)


def test_artifact_validation_reports_invalid_benchmark_record(tmp_path: Path) -> None:
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))
    artifact_path = tmp_path / "benchmark_invalid.json"
    write_json(
        artifact_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:records:benchmark-record:v1",
            "id": "benchmark.example.invalid",
            "title": "Invalid Benchmark Record",
            "status": "active",
            "benchmark_kind": "task_slice",
            "suite_id": "suite.benchmark.invalid",
            "suite_title": "Invalid Benchmark Suite",
            "recorded_at": "2026-03-29T12:30:00Z",
            "working_directory": "core/python",
            "benchmark_contract": {
                "working_directory": "core/python",
                "warmup_runs": 1,
                "measured_runs": 2,
                "execution_mode": "serialized_subprocess",
                "failure_posture": "fail_closed",
                "telemetry_environment": {
                    "telemetry_on": {
                        "WATCHTOWER_TELEMETRY": "on"
                    },
                    "telemetry_off": {
                        "WATCHTOWER_TELEMETRY": "off"
                    }
                }
            },
            "environment_context": {
                "python_version": "3.12.0",
                "python_executable": "python",
                "platform": "linux-test"
            },
            "commands": [],
        },
    )

    result = service.validate(
        artifact_path,
        validator_id="validator.control_plane.benchmark_record",
    )

    assert result.passed is False
    assert result.validator_id == "validator.control_plane.benchmark_record"
    assert result.issue_count >= 1
    assert any(
        issue.location == "commands" or "commands" in issue.message
        for issue in result.issues
    )


def test_artifact_validation_uses_pack_declared_registry_when_loader_is_pack_aware(
    tmp_path: Path,
) -> None:
    repo_root = _copy_validation_repo_subset(tmp_path)
    surfaces = materialize_pack_validation_surfaces(repo_root / "packs" / "plan")
    service = ArtifactValidationService(
        ControlPlaneLoader(
            repo_root,
            active_pack_settings_path=surfaces["pack_settings_path"],
        )
    )

    result = service.validate(surfaces["artifact_relative_path"])

    assert result.passed is True
    assert result.validator_id == surfaces["validator_id"]
    assert result.schema_ids == (surfaces["schema_id"],)


def test_artifact_validation_supports_external_schema_id_with_supplemental_schema_path(
    tmp_path: Path,
) -> None:
    schema_path = tmp_path / "schemas" / "external_note.schema.json"
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    schema_id = "urn:watchtower:schema:external:artifact-validation-note:v1"
    write_json(
        schema_path,
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "External Artifact Validation Note",
            "description": "Schema used to validate an external artifact without a registry entry.",
            "type": "object",
            "properties": {"kind": {"const": "external_validation_note"}},
            "required": ["kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        artifact_path,
        {
            "kind": "external_validation_note",
        },
    )

    service = ArtifactValidationService(
        ControlPlaneLoader(
            REPO_ROOT,
            supplemental_schema_paths=(schema_path,),
        )
    )

    result = service.validate(artifact_path, schema_id=schema_id)

    assert result.passed is True
    assert result.validator_id == f"schema:{schema_id}"
    assert result.schema_ids == (schema_id,)


def test_artifact_validation_supports_external_document_schema_with_supplemental_schema_path(
    tmp_path: Path,
) -> None:
    schema_dir = tmp_path / "schemas"
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    schema_id = "urn:watchtower:schema:external:artifact-validation-note-auto:v1"
    write_json(
        schema_dir / "external_note_auto.schema.json",
        {
            "$id": schema_id,
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "External Artifact Validation Note Auto",
            "description": "Schema discovered through a document $schema field.",
            "type": "object",
            "properties": {
                "$schema": {"const": schema_id},
                "kind": {"const": "external_validation_note_auto"},
            },
            "required": ["$schema", "kind"],
            "additionalProperties": False,
        },
    )
    write_json(
        artifact_path,
        {
            "$schema": schema_id,
            "kind": "external_validation_note_auto",
        },
    )

    service = ArtifactValidationService(
        ControlPlaneLoader(
            REPO_ROOT,
            supplemental_schema_paths=(schema_dir,),
        )
    )

    result = service.validate(artifact_path)

    assert result.passed is True
    assert result.validator_id == f"schema:{schema_id}"
    assert result.schema_ids == (schema_id,)


def test_artifact_validation_rejects_external_file_without_validator_or_schema(
    tmp_path: Path,
) -> None:
    artifact_path = tmp_path / "artifacts" / "external_note.json"
    write_json(
        artifact_path,
        {
            "kind": "external_validation_note",
        },
    )
    service = ArtifactValidationService(ControlPlaneLoader(REPO_ROOT))

    with pytest.raises(
        ValidationSelectionError,
        match="External files require --validator-id, --schema-id, or a document \\$schema",
    ):
        service.validate(artifact_path)
