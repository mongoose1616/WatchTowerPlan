from __future__ import annotations

from pathlib import Path
from shutil import copytree
from textwrap import dedent

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.reference_index import ReferenceIndexSyncService
from watchtower_core.repo_ops.validation import (
    VALIDATION_FAMILY_SPECS,
    ValidationAllService,
)
from watchtower_core.validation.errors import ValidationSelectionError

REPO_ROOT = Path(__file__).resolve().parents[4]


def _copy_control_plane_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def _write_invalid_decision_fixture(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        dedent(
            """\
            ---
            trace_id: trace.validate_all_decision_semantics
            id: decision.validate_all_decision_semantics
            title: Validate All Decision Semantics
            summary: Exercises aggregate validation for governed decision semantics.
            type: decision_record
            status: active
            owner: repository_maintainer
            updated_at: '2026-03-11T17:05:00Z'
            audience: shared
            authority: supporting
            ---

            # Validate All Decision Semantics

            ## Record Metadata
            - `Trace ID`: `trace.validate_all_decision_semantics`
            - `Decision ID`: `decision.validate_all_decision_semantics`
            - `Record Status`: `active`
            - `Decision Status`: `accepted`
            - `Linked PRDs`: `None`
            - `Linked Designs`: `None`
            - `Linked Implementation Plans`: `None`
            - `Updated At`: `2026-03-11T17:05:00Z`

            ## Summary
            Exercises aggregate validation for governed decision semantics.

            ## Decision Statement
            Keep the aggregate validator aligned with decision semantics.

            ## Trigger or Source Request
            - Added to pin validate-all coverage.

            ## Current Context and Constraints
            - The fixture should fail only for the missing applied-reference section.

            ## Affected Surfaces
            - `docs/planning/decisions/validate_all_decision_semantics.md`

            ## Options Considered
            ### Option 1
            - Keep the fixture minimal.
            - Strength.
            - Tradeoff.

            ### Option 2
            - Expand the fixture further.
            - Strength.
            - Tradeoff.

            ## Chosen Outcome
            Use the minimal invalid fixture.

            ## Rationale and Tradeoffs
            - Small fixture: isolates the aggregate validation regression.

            ## Consequences and Follow-Up Impacts
            - Validate-all should surface the decision-semantic failure directly.

            ## Risks, Dependencies, and Assumptions
            - The validator remains aligned with the governed decision rules.

            ## References
            - docs/standards/governance/decision_capture_standard.md
            """
        ),
        encoding="utf-8",
    )


def test_validate_all_can_pass_when_acceptance_is_skipped() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    result = service.run(
        included_families=tuple(
            spec.family for spec in VALIDATION_FAMILY_SPECS if spec.family != "acceptance"
        )
    )

    assert result.passed is True
    assert result.total_count >= 1
    assert result.failed_count == 0
    assert result.included_families == tuple(
        spec.family for spec in VALIDATION_FAMILY_SPECS if spec.family != "acceptance"
    )
    assert any(summary.family == "front_matter" for summary in result.family_summaries)
    assert any(summary.family == "document_semantics" for summary in result.family_summaries)
    assert any(summary.family == "artifacts" for summary in result.family_summaries)


def test_validate_all_passes_when_all_governed_families_are_aligned() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    result = service.run()

    assert result.passed is True
    assert result.total_count >= 1
    assert result.failed_count == 0
    assert result.included_families == tuple(spec.family for spec in VALIDATION_FAMILY_SPECS)
    acceptance_summary = next(
        summary for summary in result.family_summaries if summary.family == "acceptance"
    )
    assert acceptance_summary.total_count >= 1
    assert acceptance_summary.failed_count == 0


def test_validation_family_registry_is_unique() -> None:
    assert len({spec.family for spec in VALIDATION_FAMILY_SPECS}) == len(
        VALIDATION_FAMILY_SPECS
    )


def test_validate_all_rejects_unknown_family() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    with pytest.raises(ValueError, match="unknown validation families: imaginary"):
        service.run(included_families=("imaginary",))


def test_validate_all_requires_at_least_one_selected_family() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    with pytest.raises(ValueError, match="requires at least one validation family"):
        service.run(included_families=())


def test_validate_all_records_selection_errors_as_failed_results(monkeypatch) -> None:
    service = ValidationAllService(ControlPlaneLoader())
    target = "docs/references/example_reference.md"

    monkeypatch.setattr(service, "_front_matter_targets", lambda: (target,))

    def raise_selection_error(relative_path: str) -> object:
        raise ValidationSelectionError(f"No validator matched {relative_path}")

    monkeypatch.setattr(service._front_matter, "validate", raise_selection_error)

    result = service.run(included_families=("front_matter",))

    assert result.passed is False
    assert result.failed_count == 1
    assert result.records[0].family == "front_matter"
    assert result.records[0].target == target
    assert result.records[0].result.validator_id == "validator.front_matter.aggregate_selection"
    assert result.records[0].result.issue_count == 1
    assert result.records[0].result.issues[0].code == "validation_target_resolution_error"


def test_validate_all_reports_missing_decision_applied_reference_section(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = _copy_control_plane_repo(tmp_path)
    relative_path = "docs/planning/decisions/validate_all_decision_semantics.md"
    _write_invalid_decision_fixture(repo_root / relative_path)
    service = ValidationAllService(ControlPlaneLoader(repo_root))

    monkeypatch.setattr(service, "_document_semantics_targets", lambda: (relative_path,))

    result = service.run(included_families=("document_semantics",))

    assert result.passed is False
    assert result.failed_count == 1
    assert result.records[0].family == "document_semantics"
    assert result.records[0].target == relative_path
    assert (
        result.records[0].result.validator_id
        == "validator.documentation.decision_record_semantics"
    )
    assert "missing required sections: Applied References and Implications" in (
        result.records[0].result.issues[0].message
    )


def test_validate_all_artifacts_include_valid_control_plane_examples() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    result = service.run(included_families=("artifacts",))

    target_paths = {record.target for record in result.records}
    assert "core/control_plane/examples/valid/indexes/foundation_index.v1.example.json" in (
        target_paths
    )
    assert "core/control_plane/examples/valid/indexes/traceability_index.v1.example.json" in (
        target_paths
    )
    assert result.passed is True


def test_validate_all_reuses_reference_index_build_across_workflow_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = ValidationAllService(ControlPlaneLoader())
    reference_build_count = 0
    original_build_document = ReferenceIndexSyncService.build_document

    monkeypatch.setattr(
        service,
        "_document_semantics_targets",
        lambda: (
            "workflows/modules/code_validation.md",
            "workflows/modules/code_review.md",
        ),
    )

    def wrapped_build_document(
        self: ReferenceIndexSyncService,
    ) -> dict[str, object]:
        nonlocal reference_build_count
        reference_build_count += 1
        return original_build_document(self)

    monkeypatch.setattr(
        ReferenceIndexSyncService,
        "build_document",
        wrapped_build_document,
    )

    result = service.run(included_families=("document_semantics",))

    assert result.passed is True
    assert reference_build_count == 1
