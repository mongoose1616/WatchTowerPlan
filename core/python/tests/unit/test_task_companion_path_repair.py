from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.task_companion_path_repair import (
    repair_governed_task_path_references,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core" / "python").mkdir(parents=True)
    return repo_root


def test_repair_governed_task_path_references_updates_matching_paths_only(
    tmp_path: Path,
) -> None:
    repo_root = _build_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)
    previous_doc_path = "docs/planning/tasks/open/example_task.md"
    current_doc_path = "docs/planning/tasks/closed/example_task.md"
    untouched_path = "docs/planning/tasks/open/other_task.md"

    contract_relative_path = (
        "core/control_plane/contracts/acceptance/"
        "unit_test_task_companion_path_repair_acceptance.v1.json"
    )
    evidence_relative_path = (
        "core/control_plane/ledgers/validation_evidence/"
        "unit_test_task_companion_path_repair_planning_baseline.v1.json"
    )
    loader.artifact_store.write_json_object(
        contract_relative_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:contracts:acceptance-contract:v1",
            "id": "contract.acceptance.unit_test_task_companion_path_repair",
            "title": "Unit Test Task Companion Path Repair Acceptance Contract",
            "status": "active",
            "trace_id": "trace.unit_test_task_companion_path_repair",
            "source_prd_id": "prd.unit_test_task_companion_path_repair",
            "entries": [
                {
                    "acceptance_id": "ac.unit_test_task_companion_path_repair.001",
                    "summary": "Repairs the moved task path in governed companions.",
                    "validation_targets": [previous_doc_path, untouched_path],
                    "related_paths": [previous_doc_path, untouched_path],
                }
            ],
        },
    )
    loader.artifact_store.write_json_object(
        evidence_relative_path,
        {
            "$schema": "urn:watchtower:schema:artifacts:ledgers:validation-evidence:v1",
            "id": "evidence.unit_test_task_companion_path_repair.planning_baseline",
            "title": "Unit Test Task Companion Path Repair Evidence",
            "status": "active",
            "trace_id": "trace.unit_test_task_companion_path_repair",
            "overall_result": "passed",
            "recorded_at": "2026-03-13T18:30:00Z",
            "source_acceptance_contract_ids": [
                "contract.acceptance.unit_test_task_companion_path_repair"
            ],
            "checks": [
                {
                    "check_id": "check.unit_test_task_companion_path_repair.001",
                    "title": "Repair the moved task path in evidence.",
                    "result": "passed",
                    "subject_paths": [previous_doc_path, untouched_path],
                }
            ],
            "related_paths": [previous_doc_path, untouched_path],
        },
    )

    repair_governed_task_path_references(
        loader,
        previous_doc_path=previous_doc_path,
        current_doc_path=current_doc_path,
    )

    contract_document = json.loads((repo_root / contract_relative_path).read_text(encoding="utf-8"))
    entry = contract_document["entries"][0]
    assert entry["validation_targets"] == [current_doc_path, untouched_path]
    assert entry["related_paths"] == [current_doc_path, untouched_path]

    evidence_document = json.loads((repo_root / evidence_relative_path).read_text(encoding="utf-8"))
    assert evidence_document["related_paths"] == [current_doc_path, untouched_path]
    assert evidence_document["checks"][0]["subject_paths"] == [
        current_doc_path,
        untouched_path,
    ]
