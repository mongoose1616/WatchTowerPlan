from __future__ import annotations

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.validation import ValidationAllService


def test_validate_all_can_pass_when_acceptance_is_skipped() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    result = service.run(include_acceptance=False)

    assert result.passed is True
    assert result.total_count >= 1
    assert result.failed_count == 0
    assert result.included_families == ("front_matter", "document_semantics", "artifacts")
    assert any(summary.family == "front_matter" for summary in result.family_summaries)
    assert any(summary.family == "document_semantics" for summary in result.family_summaries)
    assert any(summary.family == "artifacts" for summary in result.family_summaries)


def test_validate_all_passes_when_all_governed_families_are_aligned() -> None:
    service = ValidationAllService(ControlPlaneLoader())

    result = service.run()

    assert result.passed is True
    assert result.total_count >= 1
    assert result.failed_count == 0
    acceptance_summary = next(
        summary for summary in result.family_summaries if summary.family == "acceptance"
    )
    assert acceptance_summary.total_count >= 1
    assert acceptance_summary.failed_count == 0
