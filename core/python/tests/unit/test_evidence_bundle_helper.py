from __future__ import annotations

from pathlib import Path

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


def test_evidence_bundle_helper_loads_typed_artifact_from_live_plan_bundle() -> None:
    helper = EvidenceBundleHelper(
        ControlPlaneLoader(
            REPO_ROOT,
            active_pack_settings_path="plan/.wt/manifests/pack_settings.json",
        )
    )

    artifact = helper.load_artifact(
        "plan/initiatives/plan_evidence_bundle_helper_foundation/.wt/evidence/validation_bundle.bootstrap.json"
    )

    assert artifact.evidence_id == "evidence.plan_evidence_bundle_helper_foundation.bootstrap_validation_bundle"
    assert artifact.entry_count == 2
    assert artifact.acceptance_labels == (
        "package_contracts_valid",
        "ready_for_execution_gate",
    )
    assert artifact.target_phases == ("readiness",)
