from __future__ import annotations

from pathlib import Path
from shutil import copytree

from tests.integration.fixture_repo_support import materialize_plan_runtime_pack
from watchtower_core.control_plane import ControlPlaneLoader
from watchtower_core.evidence import EvidenceBundleEntrySpec, EvidenceBundleHelper

REPO_ROOT = Path(__file__).resolve().parents[4]


def test_evidence_bundle_helper_builds_schema_valid_document() -> None:
    loader = ControlPlaneLoader(
        REPO_ROOT,
        active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
    )
    helper = EvidenceBundleHelper(loader)

    document = helper.build_document(
        evidence_id="evidence.plan_example.bootstrap_validation_bundle",
        initiative_id="initiative.plan_example",
        trace_id="trace.plan_example",
        title="Bootstrap Validation Bundle",
        status="planned",
        updated_at="2026-03-18T01:31:00Z",
        entries=(
            EvidenceBundleEntrySpec(
                entry_id="entry.plan_example.schema_validation",
                acceptance_label="package_contracts_valid",
                validation_type="schema_validation",
                owner="repository_maintainer",
                target_phase="readiness",
                expected_output_paths=("plan/initiatives/plan_example/.wt/initiative.json",),
            ),
        ),
    )

    loader.schema_store.validate_instance(document)
    assert document["id"] == "evidence.plan_example.bootstrap_validation_bundle"


def test_evidence_bundle_helper_loads_typed_artifact_from_live_plan_bundle(
    tmp_path: Path,
) -> None:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    materialize_plan_runtime_pack(repo_root, REPO_ROOT)
    helper = EvidenceBundleHelper(
        ControlPlaneLoader(
            repo_root,
            active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
        )
    )
    relative_path = "plan/initiatives/example_live_bundle/.wt/evidence/validation_bundle.bootstrap.json"
    document = helper.build_document(
        evidence_id="evidence.example_live_bundle.bootstrap_validation_bundle",
        initiative_id="initiative.example_live_bundle",
        trace_id="trace.example_live_bundle",
        title="Example Live Bundle",
        status="planned",
        updated_at="2026-03-19T12:00:00Z",
        entries=(
            EvidenceBundleEntrySpec(
                entry_id="entry.example_live_bundle.schema_validation",
                acceptance_label="package_contracts_valid",
                validation_type="schema_validation",
                owner="repository_maintainer",
                target_phase="readiness",
                expected_output_paths=("plan/initiatives/example_live_bundle/.wt/initiative.json",),
            ),
        ),
    )
    helper.write_document(document, evidence_relative_path=relative_path)

    artifact = helper.load_artifact(relative_path)

    assert artifact.evidence_id == (
        "evidence.example_live_bundle.bootstrap_validation_bundle"
    )
    assert artifact.entry_count >= 1
    assert "package_contracts_valid" in artifact.acceptance_labels
    assert artifact.target_phases == ("readiness",)
