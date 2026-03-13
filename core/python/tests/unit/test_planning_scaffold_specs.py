from __future__ import annotations

from watchtower_core.repo_ops.planning_documents import (
    DECISION_REQUIRED_EXPLAINED_SECTIONS,
    DECISION_REQUIRED_SECTIONS,
    FEATURE_DESIGN_REQUIRED_EXPLAINED_SECTIONS,
    FEATURE_DESIGN_REQUIRED_SECTIONS,
    IMPLEMENTATION_PLAN_REQUIRED_EXPLAINED_SECTIONS,
    IMPLEMENTATION_PLAN_REQUIRED_SECTIONS,
    PRD_REQUIRED_SECTIONS,
)
from watchtower_core.repo_ops.planning_scaffold_specs import scaffold_spec_for_kind


def test_scaffold_specs_align_with_planning_document_requirements() -> None:
    prd_spec = scaffold_spec_for_kind("prd")
    assert prd_spec.required_sections == ("Record Metadata", *PRD_REQUIRED_SECTIONS)
    assert prd_spec.required_explained_sections == ()

    feature_spec = scaffold_spec_for_kind("feature-design")
    assert feature_spec.required_sections == (
        "Record Metadata",
        *FEATURE_DESIGN_REQUIRED_SECTIONS,
    )
    assert feature_spec.required_explained_sections == FEATURE_DESIGN_REQUIRED_EXPLAINED_SECTIONS

    implementation_spec = scaffold_spec_for_kind("implementation-plan")
    assert implementation_spec.required_sections == (
        "Record Metadata",
        *IMPLEMENTATION_PLAN_REQUIRED_SECTIONS,
    )
    assert (
        implementation_spec.required_explained_sections
        == IMPLEMENTATION_PLAN_REQUIRED_EXPLAINED_SECTIONS
    )

    decision_spec = scaffold_spec_for_kind("decision")
    assert decision_spec.required_sections == ("Record Metadata", *DECISION_REQUIRED_SECTIONS)
    assert decision_spec.required_explained_sections == DECISION_REQUIRED_EXPLAINED_SECTIONS
    assert decision_spec.constant_metadata_values == (("Decision Status", "proposed"),)
