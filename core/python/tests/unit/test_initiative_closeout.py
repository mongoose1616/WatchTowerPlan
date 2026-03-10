from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.closeout import InitiativeCloseoutService
from watchtower_core.control_plane.loader import (
    COORDINATION_INDEX_PATH,
    INITIATIVE_INDEX_PATH,
    TRACEABILITY_INDEX_PATH,
    ControlPlaneLoader,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_closeout_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    for relative_path in (
        "docs/planning",
        "docs/planning/prds",
        "docs/planning/decisions",
        "docs/planning/design",
        "docs/planning/initiatives",
    ):
        (repo_root / relative_path).mkdir(parents=True, exist_ok=True)
    return repo_root


def _load_json(repo_root: Path, relative_path: str) -> dict[str, object]:
    return json.loads((repo_root / relative_path).read_text(encoding="utf-8"))


def test_initiative_closeout_updates_effective_timestamps_and_coordination_outputs(
    tmp_path: Path,
) -> None:
    repo_root = _build_closeout_fixture_repo(tmp_path)
    traceability_document = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    entries = traceability_document["entries"]
    assert isinstance(entries, list)
    target = next(
        entry
        for entry in entries
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    target["initiative_status"] = "active"
    target["updated_at"] = "2026-03-10T19:43:34Z"
    target.pop("closed_at", None)
    target.pop("closure_reason", None)
    (repo_root / TRACEABILITY_INDEX_PATH).write_text(
        f"{json.dumps(traceability_document, indent=2)}\n",
        encoding="utf-8",
    )

    closed_at = "2026-03-10T23:59:59Z"
    service = InitiativeCloseoutService(ControlPlaneLoader(repo_root))
    result = service.close(
        trace_id="trace.end_to_end_repo_review_and_rationalization",
        initiative_status="completed",
        closure_reason="Closed for regression coverage.",
        closed_at=closed_at,
        write=True,
        allow_open_tasks=True,
    )

    assert result.traceability_output_path is not None
    assert result.initiative_index_output_path is not None
    assert result.coordination_index_output_path is not None
    assert result.initiative_tracking_output_path is not None
    assert result.coordination_tracking_output_path is not None

    written_traceability = _load_json(repo_root, TRACEABILITY_INDEX_PATH)
    written_trace_entry = next(
        entry
        for entry in written_traceability["entries"]
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    assert written_trace_entry["updated_at"] == closed_at
    assert written_trace_entry["closed_at"] == closed_at

    written_initiative_index = _load_json(repo_root, INITIATIVE_INDEX_PATH)
    initiative_entry = next(
        entry
        for entry in written_initiative_index["entries"]
        if entry["trace_id"] == "trace.end_to_end_repo_review_and_rationalization"
    )
    assert initiative_entry["updated_at"] == closed_at
    assert initiative_entry["closed_at"] == closed_at

    written_coordination_index = _load_json(repo_root, COORDINATION_INDEX_PATH)
    assert written_coordination_index["updated_at"] == closed_at

    coordination_tracking = (repo_root / "docs/planning/coordination_tracking.md").read_text(
        encoding="utf-8"
    )
    assert f"_Updated At: `{closed_at}`_" in coordination_tracking
