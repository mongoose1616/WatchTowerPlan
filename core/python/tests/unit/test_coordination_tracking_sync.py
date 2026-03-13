from __future__ import annotations

import json
from pathlib import Path
from shutil import copytree

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.repo_ops.sync.coordination_tracking import (
    ACTIONABLE_TASK_LIMIT,
    ACTIVE_INITIATIVE_LIMIT,
    RECENT_CLOSEOUT_LIMIT,
    CoordinationTrackingSyncService,
)

REPO_ROOT = Path(__file__).resolve().parents[4]


def _build_control_plane_fixture_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    copytree(REPO_ROOT / "core" / "control_plane", repo_root / "core" / "control_plane")
    (repo_root / "core/python").mkdir(parents=True)
    return repo_root


def _load_coordination_index(repo_root: Path) -> dict[str, object]:
    path = repo_root / "core/control_plane/indexes/coordination/coordination_index.v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _active_entry_template(document: dict[str, object]) -> dict[str, object]:
    entries = document.get("entries")
    if isinstance(entries, list) and entries:
        return dict(entries[0])
    return {
        "trace_id": "trace.example",
        "title": "Example Initiative",
        "summary": "Example summary.",
        "artifact_status": "active",
        "initiative_status": "active",
        "current_phase": "execution",
        "updated_at": "2026-03-10T19:00:00Z",
        "open_task_count": 1,
        "blocked_task_count": 0,
        "key_surface_path": "docs/planning/prds/example.md",
        "next_action": "Continue the example task set.",
        "next_surface_path": "docs/planning/tasks/open/example.md",
        "primary_owner": "repository_maintainer",
        "active_owners": ["repository_maintainer"],
        "active_task_ids": ["task.example.001"],
        "active_task_summaries": [
            {
                "task_id": "task.example.001",
                "title": "Example Task",
                "task_status": "ready",
                "priority": "high",
                "owner": "repository_maintainer",
                "doc_path": "docs/planning/tasks/open/example.md",
                "is_actionable": True,
            }
        ],
        "prd_ids": ["prd.example"],
        "task_ids": ["task.example.001"],
        "notes": "Synthetic active-entry template for coordination tracking tests.",
    }


def _write_coordination_index(repo_root: Path, document: dict[str, object]) -> None:
    path = repo_root / "core/control_plane/indexes/coordination/coordination_index.v1.json"
    path.write_text(f"{json.dumps(document, indent=2)}\n", encoding="utf-8")


def test_coordination_tracking_renders_required_sections_and_companion_links(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    loader = ControlPlaneLoader(repo_root)

    content = CoordinationTrackingSyncService(loader).build_document().content

    assert "# Coordination Tracking" in content
    assert "## Current State" in content
    assert "## Active Initiatives" in content
    assert "## Actionable Tasks" in content
    assert "## Recent Closeouts" in content
    assert "](" in content
    assert "initiative_tracking.md" in content
    assert "task_tracking.md" in content
    assert "_Updated At: `" in content


def test_coordination_tracking_caps_preview_sections_and_reports_full_counts(
    tmp_path: Path,
) -> None:
    repo_root = _build_control_plane_fixture_repo(tmp_path)
    document = _load_coordination_index(repo_root)

    entry_template = _active_entry_template(document)
    closeout_template = dict(document["recent_closed_initiatives"][0])

    active_entries = []
    for index in range(ACTIVE_INITIATIVE_LIMIT + 2):
        entry = dict(entry_template)
        entry["trace_id"] = f"trace.example_{index}"
        entry["initiative_status"] = "active"
        entry["current_phase"] = "execution"
        entry["next_action"] = f"Continue task set {index}."
        entry["next_surface_path"] = f"docs/planning/tasks/open/example_{index}.md"
        entry["open_task_count"] = 1
        entry["active_owners"] = ["repository_maintainer"]
        entry["active_task_ids"] = [f"task.example_{index}.001"]
        entry["active_task_summaries"] = [
            {
                "task_id": f"task.example_{index}.001",
                "title": f"Example Task {index}",
                "task_status": "ready",
                "priority": "high",
                "owner": "repository_maintainer",
                "doc_path": f"docs/planning/tasks/open/example_{index}.md",
                "is_actionable": True,
            }
        ]
        active_entries.append(entry)
    document["entries"] = active_entries
    document["active_initiative_count"] = len(active_entries)

    actionable_tasks = []
    for index in range(ACTIONABLE_TASK_LIMIT + 2):
        task = {
            "trace_id": f"trace.example_{index}",
            "initiative_title": f"Example Initiative {index}",
            "task_id": f"task.example_{index}.001",
            "title": f"Example Task {index}",
            "task_status": "ready",
            "priority": "high",
            "owner": "repository_maintainer",
            "doc_path": f"docs/planning/tasks/open/example_{index}.md",
            "is_actionable": True,
        }
        actionable_tasks.append(task)
    document["actionable_tasks"] = actionable_tasks
    document["actionable_task_count"] = len(actionable_tasks)

    recent_closeouts = []
    for index in range(RECENT_CLOSEOUT_LIMIT + 2):
        closeout = dict(closeout_template)
        closeout["trace_id"] = f"trace.closed_{index}"
        closeout["closed_at"] = f"2026-03-10T19:{index:02d}:00Z"
        recent_closeouts.append(closeout)
    document["recent_closed_initiatives"] = recent_closeouts

    _write_coordination_index(repo_root, document)

    loader = ControlPlaneLoader(repo_root)
    content = CoordinationTrackingSyncService(loader).build_document().content

    assert (
        f"Showing {ACTIVE_INITIATIVE_LIMIT} of {len(active_entries)} active initiatives"
        in content
    )
    assert (
        f"Showing {ACTIONABLE_TASK_LIMIT} of {len(actionable_tasks)} actionable tasks"
        in content
    )
    assert content.count("trace.closed_") == RECENT_CLOSEOUT_LIMIT
