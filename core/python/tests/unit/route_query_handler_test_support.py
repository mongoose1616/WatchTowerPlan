from __future__ import annotations

import argparse
from types import SimpleNamespace


def route_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "request": "review code and commit",
        "task_type": None,
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def query_args(**overrides: object) -> argparse.Namespace:
    defaults: dict[str, object] = {
        "query": None,
        "project_slug": None,
        "project_id": None,
        "slug": None,
        "artifact_id": None,
        "artifact_family": None,
        "context_id": None,
        "source_context": None,
        "source_channel": None,
        "task_id": [],
        "trace_id": None,
        "initiative_id": None,
        "task_status": None,
        "priority": None,
        "owner": None,
        "task_kind": None,
        "blocked_only": False,
        "ready_for_execution": None,
        "lifecycle_stage": None,
        "review_status": None,
        "category": None,
        "severity": None,
        "status": None,
        "repository_role": None,
        "authoritative": None,
        "derived": None,
        "hidden": None,
        "blocking_only": False,
        "blocked_by": None,
        "depends_on": None,
        "limit": 20,
        "include_dependency_details": False,
        "initiative_status": None,
        "current_phase": None,
        "format": "text",
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def task_entry(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "task_id": "task.example.001",
        "trace_id": "trace.example",
        "title": "Example task",
        "summary": "Task summary.",
        "status": "active",
        "task_status": "planned",
        "task_kind": "feature",
        "priority": "high",
        "owner": "repository_maintainer",
        "doc_path": "plan/initiatives/example/.wt/tasks/example/task.json",
        "updated_at": "2026-03-10T23:59:59Z",
        "blocked_by": ("task.blocker.001",),
        "depends_on": ("task.depends.001",),
        "related_ids": (),
        "applies_to": (),
        "github_repository": None,
        "github_issue_number": None,
        "github_issue_node_id": None,
        "github_project_owner": None,
        "github_project_owner_type": None,
        "github_project_number": None,
        "github_project_item_id": None,
        "github_synced_at": None,
        "tags": (),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def active_task_summary(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "trace_id": "trace.example",
        "initiative_title": "Example Initiative",
        "task_id": "task.example.001",
        "title": "Example task",
        "task_status": "planned",
        "priority": "high",
        "owner": "repository_maintainer",
        "doc_path": "plan/initiatives/example/.wt/tasks/example/task.json",
        "is_actionable": True,
        "blocked_by": (),
        "depends_on": (),
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def artifact_entry(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "artifact_id": "initiative.example",
        "artifact_family": "initiative_state",
        "path": "plan/initiatives/example/.wt/initiative.json",
        "pack": "pack.plan",
        "subdomain": "plan",
        "status": "ready_for_execution",
        "authoritative": True,
        "hidden": True,
        "derived": False,
        "created_at": "2026-03-10T23:59:59Z",
        "updated_at": "2026-03-10T23:59:59Z",
        "context_ids": ("initiative.example", "trace.example", "pack.plan"),
        "title": "Example Initiative",
        "summary": "Example initiative artifact.",
        "parent_artifact_id": None,
        "related_artifact_ids": (),
        "route_id": None,
        "rendered_view_path": "plan/initiatives/example/plan.md",
        "workflow_surface": None,
        "review_status": "approved",
        "source_context": "initiative.example",
        "source_channel": "initiative_package",
        "source_summary": "Example initiative artifact.",
        "source_url": None,
        "source_ref": None,
        "source_type": "initiative_state",
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def initiative_entry(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "initiative_id": "initiative.example",
        "trace_id": "trace.example",
        "slug": "example",
        "title": "Example Initiative",
        "summary": "Initiative summary.",
        "artifact_status": "active",
        "initiative_status": "active",
        "scope_type": "pack_wide",
        "project_id": None,
        "current_phase": "execution",
        "updated_at": "2026-03-10T23:59:59Z",
        "open_task_count": 1,
        "blocked_task_count": 0,
        "key_surface_path": "plan/initiatives/example/initiative_brief.md",
        "next_action": "Start execution.",
        "next_surface_path": "plan/initiatives/example/implementation_slice.md",
        "primary_owner": "repository_maintainer",
        "active_owners": ("repository_maintainer",),
        "active_task_ids": ("task.example.001",),
        "active_task_summaries": (active_task_summary(),),
        "blocked_by_task_ids": (),
        "source_surface_paths": (
            "plan/initiatives/example/initiative_brief.md",
            "plan/initiatives/example/design_record.md",
            "plan/initiatives/example/implementation_slice.md",
        ),
        "task_ids": ("task.example.001",),
        "acceptance_ids": ("ac.example.001",),
        "acceptance_contract_ids": ("contract.acceptance.example",),
        "evidence_ids": ("evidence.example",),
        "closed_at": None,
        "closure_reason": None,
        "superseded_by_trace_id": None,
        "related_paths": ("plan/initiatives/example/initiative_brief.md",),
        "tags": ("traceability",),
        "notes": "Example notes.",
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)
