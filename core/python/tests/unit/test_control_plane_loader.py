from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane.loader import ControlPlaneLoader

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_control_plane_loader_reads_validator_registry() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    registry = loader.load_validator_registry()
    validator = registry.get("validator.documentation.reference_front_matter")

    assert registry.artifact_id == "registry.validators"
    assert validator.engine == "json_schema"
    assert validator.schema_ids == (
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1",
    )


def test_control_plane_loader_reads_repository_path_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    index = loader.load_repository_path_index()
    entry = index.get("core/python/")

    assert index.coverage_mode == "entrypoints"
    assert entry.surface_kind == "python_workspace"
    assert "core/python/AGENTS.md" in entry.related_paths


def test_control_plane_loader_reads_command_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    command_index = loader.load_command_index()
    doctor = command_index.get("command.watchtower_core.doctor")
    query_paths = command_index.get("command.watchtower_core.query.paths")
    validate_front_matter = command_index.get("command.watchtower_core.validate.front_matter")
    validate_artifact = command_index.get("command.watchtower_core.validate.artifact")

    assert doctor.parent_command_id == "command.watchtower_core"
    assert doctor.doc_path == "docs/commands/core_python/watchtower_core_doctor.md"
    assert query_paths.default_output_format == "human"
    assert query_paths.doc_path == "docs/commands/core_python/watchtower_core_query_paths.md"
    assert validate_front_matter.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_front_matter.doc_path
        == "docs/commands/core_python/watchtower_core_validate_front_matter.md"
    )
    assert validate_artifact.parent_command_id == "command.watchtower_core.validate"
    assert (
        validate_artifact.doc_path
        == "docs/commands/core_python/watchtower_core_validate_artifact.md"
    )


def test_control_plane_loader_reads_traceability_index() -> None:
    loader = ControlPlaneLoader(REPO_ROOT)

    traceability_index = loader.load_traceability_index()
    trace = traceability_index.get("trace.core_python_foundation")

    assert trace.trace_id == "trace.core_python_foundation"
    assert "design.features.schema_resolution_and_index_search" in trace.design_ids
