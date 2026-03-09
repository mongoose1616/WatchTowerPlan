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

    assert doctor.parent_command_id == "command.watchtower_core"
    assert doctor.doc_path == "docs/commands/core_python/watchtower_core_doctor.md"
