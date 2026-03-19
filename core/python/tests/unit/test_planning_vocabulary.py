from __future__ import annotations

from pathlib import Path

from watchtower_core.control_plane import ControlPlaneLoader, PlanningVocabularyHelper

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> PlanningVocabularyHelper:
    return PlanningVocabularyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_planning_vocabulary_helper_resolves_lifecycle_phases_and_terminals() -> None:
    helper = _helper()

    assert helper.current_phase_for_lifecycle("capture_incomplete") == "capture"
    assert helper.current_phase_for_lifecycle("closing") == "closeout"
    assert helper.is_terminal_lifecycle("completed") is True
    assert helper.is_terminal_lifecycle("blocked") is False


def test_planning_vocabulary_helper_resolves_review_and_source_semantics() -> None:
    helper = _helper()

    assert helper.allows_execution("approved") is True
    assert helper.allows_execution("pending") is False
    assert helper.source_class_for("authored_input") == "authored_input"
    assert helper.source_class_for("external_reference") == "external_reference"
