from __future__ import annotations

from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import materialize_governed_applies_to_targets
from watchtower_core.control_plane import ControlPlaneLoader, SchemaStore, WorkspaceConfig
from watchtower_core.evidence import ValidationEvidenceRecorder
from watchtower_core.validation import ArtifactValidationService, ValidationResult

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_custom_workspace(tmp_path: Path) -> WorkspaceConfig:
    repo_root = tmp_path / "repo"
    control_plane_root = repo_root / "machine_artifacts"
    python_workspace_root = repo_root / "runtime" / "python"

    copytree(REPO_ROOT / "core" / "control_plane", control_plane_root)
    copytree(REPO_ROOT / "docs", repo_root / "docs")
    python_workspace_root.mkdir(parents=True)
    materialize_governed_applies_to_targets(repo_root)

    return WorkspaceConfig(
        repo_root=repo_root,
        control_plane_root=control_plane_root,
        python_workspace_root=python_workspace_root,
    )


def test_schema_store_loads_from_injected_workspace(tmp_path: Path) -> None:
    workspace_config = _build_custom_workspace(tmp_path)

    store = SchemaStore.from_workspace(workspace_config)
    record = store.get_record(
        "urn:watchtower:schema:interfaces:documentation:reference-front-matter:v1"
    )

    assert record.canonical_relative_path == (
        "core/control_plane/schemas/interfaces/documentation/reference_front_matter.v1.schema.json"
    )
    assert record.canonical_path == (
        workspace_config.control_plane_root
        / "schemas/interfaces/documentation/reference_front_matter.v1.schema.json"
    )


def test_control_plane_loader_validates_logical_control_plane_path_in_custom_workspace(
    tmp_path: Path,
) -> None:
    workspace_config = _build_custom_workspace(tmp_path)
    loader = ControlPlaneLoader(workspace_config=workspace_config)

    registry = loader.load_validator_registry()
    index = loader.load_repository_path_index()
    result = ArtifactValidationService(loader).validate(
        "core/control_plane/indexes/traceability/traceability_index.v1.json"
    )

    assert registry.artifact_id == "registry.validators"
    assert index.get("core/python/").surface_kind == "python_workspace"
    assert result.passed is True


def test_validation_evidence_recorder_writes_default_outputs_to_injected_workspace(
    tmp_path: Path,
) -> None:
    workspace_config = _build_custom_workspace(tmp_path)
    loader = ControlPlaneLoader(workspace_config=workspace_config)
    recorder = ValidationEvidenceRecorder(loader)
    result = ValidationResult(
        validator_id="validator.control_plane.traceability_index",
        target_path="core/control_plane/indexes/traceability/traceability_index.v1.json",
        engine="json_schema",
        schema_ids=(
            "urn:watchtower:schema:artifacts:indexes:traceability-index:v1",
        ),
        passed=True,
        issues=(),
    )

    write_result = recorder.record(
        result,
        trace_id="trace.core_export_readiness_and_optimization",
    )

    evidence_output = Path(write_result.evidence_output_path)
    traceability_output = Path(write_result.traceability_output_path)
    assert evidence_output.exists()
    assert traceability_output.exists()
    assert evidence_output.is_relative_to(workspace_config.control_plane_root)
    assert traceability_output == (
        workspace_config.control_plane_root / "indexes/traceability/traceability_index.v1.json"
    )
