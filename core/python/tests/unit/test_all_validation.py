from __future__ import annotations

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.validation import (
    VALIDATION_FAMILY_SPECS,
    ValidationAllService,
)
from watchtower_core.validation.errors import ValidationSelectionError


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
