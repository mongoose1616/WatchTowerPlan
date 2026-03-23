from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane import ControlPlaneLoader, TerminologyHelper

REPO_ROOT = Path(__file__).resolve().parents[4]
PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"


def _helper() -> TerminologyHelper:
    return TerminologyHelper.from_loader(
        ControlPlaneLoader(REPO_ROOT),
        pack_settings_path=PLAN_PACK_SETTINGS_PATH,
    )


def test_terminology_helper_resolves_registry_backed_terms() -> None:
    helper = _helper()

    assert helper.current_phase_for_lifecycle("capture_incomplete") == "capture"
    assert helper.is_terminal_lifecycle("completed") is True
    assert helper.allows_execution("approved") is True
    assert helper.source_class_for("external_reference") == "external_reference"


def test_terminology_helper_rejects_removed_plan_task_status_aliases() -> None:
    helper = _helper()

    with pytest.raises(KeyError, match="plan_task_status:done"):
        helper.resolve("plan_task_status", "done")
    with pytest.raises(KeyError, match="plan_task_status:backlog"):
        helper.resolve("plan_task_status", "backlog")


def test_terminology_helper_exposes_canonical_plan_task_term_metadata() -> None:
    helper = _helper()

    term = helper.term("plan_task_status", "planned")

    assert term.deprecated_aliases == ()
    assert term.summary == "The initiative-local task is captured but not yet execution-ready."
