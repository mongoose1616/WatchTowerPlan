"""Rendered overview and initiative-surface helpers for the plan workspace."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from watchtower_core.adapters import extract_sections, load_markdown_body, render_repo_link
from watchtower_core.control_plane.pack_workspace import PackWorkspacePaths
from watchtower_core.control_plane.terminology import TerminologyHelper
from watchtower_core.rebuild import RenderedViewBuilder, RenderedViewSpec

from watchtower_plan.governing_documents import (
    effective_initiative_governing_document_paths,
)
from watchtower_plan.workspace.constants import (
    INITIATIVE_PLAN_SURFACE_ID,
    INITIATIVE_PROGRESS_SURFACE_ID,
    INITIATIVE_SUMMARY_SURFACE_ID,
    PHASE_ORDER,
    PLAN_OVERVIEW_SURFACE_ID,
    PRIORITY_ORDER,
    TERMINAL_TASK_STATUSES,
)
from watchtower_plan.workspace.models import PlanReadinessIndexEntry
from watchtower_plan.workspace.snapshots import (
    PlanInitiativeSnapshot,
    snapshot_updated_at,
)
from watchtower_plan.workspace.support import (
    joined_or_dash,
    next_action,
    next_surface_path,
    task_status_order,
)


class PlanWorkspaceRenderer:
    """Render pack-wide overview and initiative-local markdown views."""

    def __init__(
        self,
        *,
        repo_root: Path,
        workspace_paths: PackWorkspacePaths,
        rendered_views: RenderedViewBuilder,
        vocabulary: TerminologyHelper,
        overview_path: str,
    ) -> None:
        self._repo_root = repo_root
        self._workspace_paths = workspace_paths
        self._rendered_views = rendered_views
        self._vocabulary = vocabulary
        self._overview_path = overview_path

    def render_plan_overview(self, coordination_document: dict[str, Any]) -> str:
        entries = coordination_document["entries"]
        assert isinstance(entries, list)
        pack_wide_entries = tuple(
            entry
            for entry in entries
            if isinstance(entry, dict)
            and entry.get("scope_type", "pack_wide") == "pack_wide"
        )
        project_entries = tuple(
            entry
            for entry in entries
            if isinstance(entry, dict)
            and entry.get("scope_type", "pack_wide") != "pack_wide"
        )
        actionable_tasks = coordination_document["actionable_tasks"]
        assert isinstance(actionable_tasks, list)
        blocked_or_attention_items = [
            (
                f"- Blocked initiative `{entry['trace_id']}`: {entry['title']}"
                if entry.get("blocked_task_count", 0)
                else ""
            )
            for entry in pack_wide_entries + project_entries
        ]
        blocked_or_attention_items.extend(
            f"- Actionable task `{entry['task_id']}` ({entry['priority']}) in "
            f"`{entry['trace_id']}` -> `{entry['doc_path']}`"
            for entry in actionable_tasks
            if isinstance(entry, dict)
        )
        navigation_links = (
            f"- [initiative_tracking.md](/{self._workspace_paths.tracking_path('initiative_tracking.md')})",
            f"- [task_tracking.md](/{self._workspace_paths.tracking_path('task_tracking.md')})",
            f"- [coordination_tracking.md](/{self._workspace_paths.tracking_path('coordination_tracking.md')})",
            f"- [README.md](/{self._workspace_paths.docs_path('README.md')})",
            "- [README.md](/core/docs/README.md)",
            f"- [ROUTING_TABLE.md](/{self._workspace_paths.workflows_path('ROUTING_TABLE.md')})",
        )
        result = self._rendered_views.build_view(
            RenderedViewSpec(
                surface_id=PLAN_OVERVIEW_SURFACE_ID,
                data={
                    "plan_domain_summary": (
                        f"- `coordination_mode`: `{coordination_document['coordination_mode']}`",
                        f"- `summary`: {coordination_document['summary']}",
                        f"- `recommended_next_action`: {coordination_document['recommended_next_action']}",
                        f"- `recommended_surface_path`: `{coordination_document['recommended_surface_path']}`",
                    ),
                    "active_pack_wide_initiatives": (
                        (
                            "\n".join(
                                (
                                    f"- `{entry['trace_id']}`: {entry['title']} "
                                    f"(`{entry['current_phase']}` / "
                                    f"`{entry.get('scope_type', 'pack_wide')}`)"
                                )
                                for entry in pack_wide_entries
                            )
                            or "- None."
                        ),
                    ),
                    "active_project_initiatives": (
                        (
                            "\n".join(
                                (
                                    f"- `{entry['trace_id']}`: {entry['title']} "
                                    f"(`{entry['current_phase']}` / "
                                    f"`{entry.get('scope_type', 'project_scoped')}`)"
                                )
                                for entry in project_entries
                            )
                            or "- None."
                        ),
                    ),
                    "blocked_or_attention_needed_items": (
                        tuple(item for item in blocked_or_attention_items if item)
                        or ("- None.",)
                    ),
                    "recent_completions_or_changes": (
                        (
                            "\n".join(
                                (
                                    f"- `{entry['trace_id']}`: {entry['title']} "
                                    f"(`{entry['initiative_status']}` at `{entry['closed_at']}`)"
                                    + (
                                        f" - {entry['closure_reason']}"
                                        if entry.get("closure_reason")
                                        else ""
                                    )
                                )
                                for entry in coordination_document.get(
                                    "recent_closed_initiatives",
                                    (),
                                )
                                if isinstance(entry, dict)
                            )
                            or "- None."
                        ),
                    ),
                    "navigation_links": navigation_links,
                },
            )
        )
        assert result.relative_output_path == self._overview_path
        return result.content

    def render_initiative_views(
        self,
        snapshots: tuple[PlanInitiativeSnapshot, ...],
        readiness_by_initiative_id: dict[str, PlanReadinessIndexEntry],
    ) -> dict[str, str]:
        documents: dict[str, str] = {}
        for snapshot in snapshots:
            initiative = snapshot.initiative_document
            initiative_id = str(initiative["initiative_id"])
            readiness = readiness_by_initiative_id[initiative_id]
            task_rows = initiative_task_rows(snapshot, self._vocabulary)
            active_task_rows = tuple(
                row
                for row in task_rows
                if row["task_status"] not in TERMINAL_TASK_STATUSES
            )
            include_planned_task_blocked_by = any(
                row["blocked_by"] not in {None, "-"} for row in task_rows
            )
            include_planned_task_depends_on = any(
                row["depends_on"] not in {None, "-"} for row in task_rows
            )
            include_active_task_blocked_by = any(
                row["blocked_by"] not in {None, "-"} for row in active_task_rows
            )
            include_active_task_depends_on = any(
                row["depends_on"] not in {None, "-"} for row in active_task_rows
            )
            dependency_and_risk_lines = initiative_dependency_and_risk_lines(
                snapshot,
                readiness=readiness,
            )
            blocker_lines = initiative_blocker_lines(
                snapshot,
                readiness=readiness,
            )
            resolved_next_surface_path = next_surface_path(snapshot, readiness)
            root = snapshot.initiative_root
            rendered_views = self._rendered_views.build_views(
                (
                    RenderedViewSpec(
                        surface_id=INITIATIVE_PLAN_SURFACE_ID,
                        relative_output_path=f"{root}/plan.md",
                        title=f"{initiative['title']} Plan",
                        data={
                            "initiative_identity": (
                                f"- `initiative_id`: `{initiative['initiative_id']}`",
                                f"- `trace_id`: `{initiative['trace_id']}`",
                                f"- `scope_type`: `{initiative['scope_type']}`",
                                *(
                                    (f"- `project_id`: `{initiative['project_id']}`",)
                                    if initiative.get("project_id") is not None
                                    else ()
                                ),
                                f"- `owner`: `{initiative['owner']}`",
                                f"- `lifecycle_stage`: `{initiative['lifecycle_stage']}`",
                                f"- `review_status`: `{initiative['review_status']}`",
                                f"- `updated_at`: `{snapshot_updated_at(snapshot)}`",
                            ),
                            "scope_and_non_goals": initiative_scope_lines(
                                snapshot,
                                repo_root=self._repo_root,
                            ),
                            "objectives": initiative_objective_lines(snapshot),
                            "planned_slices_or_workstreams": task_rows,
                            "include_planned_slice_blocked_by": include_planned_task_blocked_by,
                            "include_planned_slice_depends_on": include_planned_task_depends_on,
                            "dependencies_and_risks": dependency_and_risk_lines,
                            "validation_or_completion_gates": initiative_gate_lines(
                                snapshot,
                                readiness=readiness,
                            ),
                            "linked_outputs": initiative_linked_output_lines(snapshot),
                        },
                    ),
                    RenderedViewSpec(
                        surface_id=INITIATIVE_PROGRESS_SURFACE_ID,
                        relative_output_path=f"{root}/progress.md",
                        title=f"{initiative['title']} Progress",
                        data={
                            "current_status": (
                                f"- `lifecycle_stage`: `{initiative['lifecycle_stage']}`",
                                f"- `review_status`: `{initiative['review_status']}`",
                                f"- `approval_status`: `{readiness.approval_status}`",
                                f"- `ready_for_execution`: `{readiness.ready_for_execution}`",
                                f"- `updated_at`: `{snapshot_updated_at(snapshot)}`",
                            ),
                            "recent_events_or_changes": initiative_event_rows(snapshot),
                            "active_tasks": active_task_rows,
                            "include_active_task_blocked_by": include_active_task_blocked_by,
                            "include_active_task_depends_on": include_active_task_depends_on,
                            "blockers": blocker_lines,
                            "next_actions": (
                                f"- {next_action(snapshot, readiness, self._vocabulary)}",
                                f"- Next surface: {render_repo_link(resolved_next_surface_path, label=Path(resolved_next_surface_path).name)}",
                            ),
                            "evidence_or_validation_state": initiative_evidence_validation_lines(
                                snapshot,
                                readiness=readiness,
                            ),
                        },
                    ),
                    RenderedViewSpec(
                        surface_id=INITIATIVE_SUMMARY_SURFACE_ID,
                        relative_output_path=f"{root}/summary.md",
                        title=f"{initiative['title']} Summary",
                        data={
                            "outcome_summary": (
                                str(initiative["summary"]),
                                f"- `lifecycle_stage`: `{initiative['lifecycle_stage']}`",
                                *(
                                    (f"- `closed_at`: `{initiative['closed_at']}`",)
                                    if initiative.get("closed_at") is not None
                                    else ()
                                ),
                                *(
                                    (
                                        f"- `closure_reason`: {initiative['closure_reason']}",
                                    )
                                    if initiative.get("closure_reason") is not None
                                    else ()
                                ),
                                *(
                                    (
                                        f"- `superseded_by_trace_id`: "
                                        f"`{initiative['superseded_by_trace_id']}`",
                                    )
                                    if initiative.get("superseded_by_trace_id")
                                    is not None
                                    else ()
                                ),
                            ),
                            "delivered_outputs": initiative_delivered_output_lines(
                                snapshot
                            ),
                            "promoted_guidance": initiative_promotion_lines(
                                snapshot,
                                repo_root=self._repo_root,
                            ),
                            "evidence_references": initiative_evidence_reference_lines(
                                snapshot
                            ),
                            "unresolved_follow_ups": initiative_unresolved_follow_up_lines(
                                snapshot
                            ),
                            "closeout_state": initiative_closeout_lines(snapshot),
                        },
                    ),
                )
            )
            for result in rendered_views:
                documents[result.relative_output_path] = result.content
        return documents


def _initiative_section_text(
    repo_root: Path,
    snapshot: PlanInitiativeSnapshot,
    *,
    filename: str,
    section_title: str,
) -> str | None:
    document_path = repo_root / snapshot.initiative_root / filename
    if not document_path.exists():
        return None
    sections = extract_sections(load_markdown_body(document_path))
    return sections.get(section_title)


def _section_bullet_items(section_text: str | None) -> tuple[str, ...]:
    if section_text is None:
        return ()
    items: list[str] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return tuple(items)


def initiative_scope_lines(
    snapshot: PlanInitiativeSnapshot,
    *,
    repo_root: Path,
) -> tuple[str, ...]:
    initiative = snapshot.initiative_document
    lines = [
        str(initiative["summary"]),
        f"- Scope type: `{initiative['scope_type']}`.",
    ]
    non_goal_items = _section_bullet_items(
        _initiative_section_text(
            repo_root,
            snapshot,
            filename="initiative_brief.md",
            section_title="Non-Goals",
        )
    )
    if non_goal_items:
        lines.extend(f"- Non-goal: {item}" for item in non_goal_items)

    deferred_lines = [
        f"- Deferred item `{document['deferred_item_id']}`: {document['summary']} "
        f"(`{document['status']}`)"
        for document in snapshot.deferred_documents
    ]
    if not deferred_lines:
        deferred_lines.extend(
            f"- Locked post-v1 deferral: {item}"
            for item in _section_bullet_items(
                _initiative_section_text(
                    repo_root,
                    snapshot,
                    filename="decision_notes.md",
                    section_title="Locked Post-V1 Deferrals",
                )
            )
        )
    if deferred_lines:
        lines.extend(deferred_lines)
    elif not non_goal_items:
        lines.append("- No explicit non-goals or deferred scope items are recorded.")
    return tuple(lines)


def initiative_task_rows(
    snapshot: PlanInitiativeSnapshot,
    vocabulary: TerminologyHelper,
) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    sorted_tasks = sorted(
        snapshot.task_documents,
        key=lambda task_document: (
            task_status_order(str(task_document["task_status"])),
            PRIORITY_ORDER.get(str(task_document["priority"]), 99),
            str(task_document["task_id"]),
        ),
    )
    for task_document in sorted_tasks:
        rows.append(
            {
                "task_id": str(task_document["task_id"]),
                "doc_path": (
                    f"{snapshot.initiative_root}/.wt/tasks/{task_document['slug']}/task.json"
                ),
                "task_status": vocabulary.surface_task_status(
                    str(task_document["task_status"])
                ),
                "priority": str(task_document["priority"]),
                "owner": str(task_document["owner"]),
                "summary": str(task_document["summary"]),
                "blocked_by": joined_or_dash(task_document.get("blocker_task_ids", ())),
                "depends_on": joined_or_dash(
                    task_document.get("dependency_task_ids", ())
                ),
            }
        )
    return tuple(rows)


def initiative_objective_lines(
    snapshot: PlanInitiativeSnapshot,
) -> tuple[str, ...]:
    objectives = tuple(
        dict.fromkeys(
            f"{task_document['title']}: {task_document['summary']}"
            for task_document in snapshot.task_documents
            if str(task_document.get("task_status", "")) != "cancelled"
        )
    )
    if not objectives:
        return ("- No explicit objectives are currently recorded.",)
    return tuple(f"- {objective}" for objective in objectives)


def initiative_dependency_and_risk_lines(
    snapshot: PlanInitiativeSnapshot,
    *,
    readiness: PlanReadinessIndexEntry,
) -> tuple[str, ...]:
    lines: list[str] = []
    for reason in readiness.blocking_reasons:
        lines.append(f"- Readiness blocker: `{reason}`.")
    for document in snapshot.discrepancy_documents:
        status = str(document.get("status", ""))
        if status in {"resolved", "closed", "completed", "cancelled"}:
            continue
        lines.append(
            f"- Discrepancy `{document['discrepancy_id']}`: `{document['severity']}` "
            f"`{document['category']}` / `{status}`. {document['summary']}"
        )
    for task_document in snapshot.task_documents:
        blocked_by = tuple(
            str(value) for value in task_document.get("blocker_task_ids", ())
        )
        depends_on = tuple(
            str(value) for value in task_document.get("dependency_task_ids", ())
        )
        if not blocked_by and not depends_on:
            continue
        relation_bits: list[str] = []
        if blocked_by:
            relation_bits.append(
                "blocked by " + ", ".join(f"`{value}`" for value in blocked_by)
            )
        if depends_on:
            relation_bits.append(
                "depends on " + ", ".join(f"`{value}`" for value in depends_on)
            )
        lines.append(
            f"- Task `{task_document['task_id']}` " + " and ".join(relation_bits) + "."
        )
    if not lines:
        return (
            "- No current blockers, dependencies, or open discrepancy risks are recorded.",
        )
    return tuple(lines)


def initiative_blocker_lines(
    snapshot: PlanInitiativeSnapshot,
    *,
    readiness: PlanReadinessIndexEntry,
) -> tuple[str, ...]:
    lines: list[str] = []
    for reason in readiness.blocking_reasons:
        lines.append(f"- Readiness blocker: `{reason}`.")
    for document in snapshot.discrepancy_documents:
        status = str(document["status"])
        if status in {"resolved", "closed", "completed", "cancelled"}:
            continue
        lines.append(
            f"- Discrepancy `{document['discrepancy_id']}`: `{document['severity']}` "
            f"`{document['category']}` / `{status}`. {document['summary']}"
        )
    for task_document in snapshot.task_documents:
        task_status = str(task_document.get("task_status", ""))
        if task_status in TERMINAL_TASK_STATUSES:
            continue
        blocked_by = tuple(
            str(value) for value in task_document.get("blocker_task_ids", ())
        )
        depends_on = tuple(
            str(value) for value in task_document.get("dependency_task_ids", ())
        )
        if not blocked_by and not depends_on:
            continue
        relation_bits: list[str] = []
        if blocked_by:
            relation_bits.append(
                "blocked by " + ", ".join(f"`{value}`" for value in blocked_by)
            )
        if depends_on:
            relation_bits.append(
                "depends on " + ", ".join(f"`{value}`" for value in depends_on)
            )
        lines.append(
            f"- Task `{task_document['task_id']}` " + " and ".join(relation_bits) + "."
        )
    if not lines:
        return (
            "- No active blockers, unresolved dependencies, or open discrepancy risks are recorded.",
        )
    return tuple(lines)


def initiative_gate_lines(
    snapshot: PlanInitiativeSnapshot,
    *,
    readiness: PlanReadinessIndexEntry,
) -> tuple[str, ...]:
    return (
        f"- `capture_complete`: `{readiness.capture_complete}`",
        f"- `machine_valid`: `{readiness.machine_valid}`",
        f"- `approval_status`: `{readiness.approval_status}`",
        f"- `ready_for_execution`: `{readiness.ready_for_execution}`",
        "- `blocking_reasons`: `"
        + (
            ", ".join(readiness.blocking_reasons)
            if readiness.blocking_reasons
            else "none"
        )
        + "`",
        f"- Task count: `{len(snapshot.task_documents)}`",
        f"- Evidence bundle count: `{len(snapshot.evidence_documents)}`",
        f"- Closeout shell count: `{len(snapshot.closeout_documents)}`",
        f"- Promotion shell count: `{len(snapshot.promotion_documents)}`",
        f"- Acceptance contract refs: `{len(snapshot.acceptance_contract_ids)}`",
    )


def initiative_linked_output_lines(
    snapshot: PlanInitiativeSnapshot,
) -> tuple[str, ...]:
    initiative = snapshot.initiative_document
    lines: list[str] = []
    authored_input_paths = {
        str(record.get("path"))
        for record in initiative.get("authored_inputs", ())
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }
    for path in effective_initiative_governing_document_paths(initiative):
        label = (
            "Authored input" if path in authored_input_paths else "Governing document"
        )
        lines.append(f"- {label}: {render_repo_link(path, label=Path(path).name)}")
    lines.extend(
        (
            f"- Rendered plan: {render_repo_link(f'{snapshot.initiative_root}/plan.md', label='plan.md')}",
            f"- Rendered progress: {render_repo_link(f'{snapshot.initiative_root}/progress.md', label='progress.md')}",
            f"- Rendered summary: {render_repo_link(f'{snapshot.initiative_root}/summary.md', label='summary.md')}",
        )
    )
    if snapshot.project_root is not None:
        lines.extend(
            (
                f"- Project surface: {render_repo_link(f'{snapshot.project_root}/project.md', label='project.md')}",
                f"- Project repositories: {render_repo_link(f'{snapshot.project_root}/repositories.md', label='repositories.md')}",
                f"- Project summary: {render_repo_link(f'{snapshot.project_root}/summary.md', label='summary.md')}",
            )
        )
    if not lines:
        return ("- No linked outputs are currently recorded.",)
    return tuple(lines)


def initiative_event_rows(
    snapshot: PlanInitiativeSnapshot,
    *,
    limit: int = 5,
) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    sorted_events = sorted(
        snapshot.event_documents,
        key=lambda document: (
            int(document.get("sequence", 0)),
            str(document.get("recorded_at", "")),
        ),
        reverse=True,
    )
    for document in sorted_events[:limit]:
        rows.append(
            {
                "recorded_at": str(document.get("recorded_at", "-")),
                "event_type": str(document.get("event_type", "-")),
                "actor_id": str(document.get("actor_id", "-")),
                "summary": str(document.get("summary", "-")),
            }
        )
    return tuple(rows)


def initiative_evidence_validation_lines(
    snapshot: PlanInitiativeSnapshot,
    *,
    readiness: PlanReadinessIndexEntry,
) -> tuple[str, ...]:
    lines = [
        f"- `machine_valid`: `{readiness.machine_valid}`",
        f"- Evidence bundles: `{len(snapshot.evidence_documents)}`",
        f"- Acceptance contract refs: `{len(snapshot.acceptance_contract_ids)}`",
        f"- Trace-linked evidence refs: `{len(snapshot.trace_evidence_ids)}`",
    ]
    for document in snapshot.evidence_documents:
        lines.append(f"- `{document['id']}`: `{document['status']}`")
    return tuple(lines)


def initiative_delivered_output_lines(
    snapshot: PlanInitiativeSnapshot,
) -> tuple[str, ...]:
    lines = list(initiative_linked_output_lines(snapshot))
    completed_tasks = [
        task_document
        for task_document in snapshot.task_documents
        if str(task_document["task_status"]) in TERMINAL_TASK_STATUSES
    ]
    if completed_tasks:
        lines.extend(
            f"- Terminal task `{task_document['task_id']}`: `{task_document['task_status']}`"
            for task_document in completed_tasks
        )
    else:
        lines.append("- No terminal task outputs are recorded yet.")
    return tuple(lines)


def initiative_promotion_lines(
    snapshot: PlanInitiativeSnapshot,
    *,
    repo_root: Path,
) -> tuple[str, ...]:
    if not snapshot.promotion_documents:
        return ("- No promotion candidates are currently recorded.",)
    lines: list[str] = []
    for document in snapshot.promotion_documents:
        lines.append(
            f"- `{document['id']}`: `{document['status']}` / approval `{document.get('approval_state', 'pending')}`"
        )
        for candidate in document.get("candidates", ()):
            if not isinstance(candidate, dict):
                continue
            target_path = candidate.get("target_path")
            if isinstance(target_path, str) and target_path:
                target_repo_path = repo_root / target_path
                if target_repo_path.exists():
                    lines.append(
                        f"- Candidate target: {render_repo_link(target_path, label=Path(target_path).name)}"
                    )
                else:
                    lines.append(
                        f"- Candidate target path (planned, not yet promoted): `{target_path}`"
                    )
    return tuple(lines)


def initiative_evidence_reference_lines(
    snapshot: PlanInitiativeSnapshot,
) -> tuple[str, ...]:
    lines: list[str] = []
    for document in snapshot.evidence_documents:
        lines.append(f"- `{document['id']}`: `{document['status']}`")
    for evidence_id in snapshot.trace_evidence_ids:
        lines.append(f"- Trace evidence ref: `{evidence_id}`")
    for acceptance_id in snapshot.acceptance_contract_ids:
        lines.append(f"- Acceptance contract ref: `{acceptance_id}`")
    if not lines:
        return ("- No evidence or acceptance references are currently recorded.",)
    return tuple(lines)


def initiative_unresolved_follow_up_lines(
    snapshot: PlanInitiativeSnapshot,
) -> tuple[str, ...]:
    lines: list[str] = []
    for task_document in snapshot.task_documents:
        if str(task_document["task_status"]) in TERMINAL_TASK_STATUSES:
            continue
        lines.append(
            f"- Open task `{task_document['task_id']}`: `{task_document['task_status']}`"
        )
    for document in snapshot.deferred_documents:
        lines.append(
            f"- Deferred item `{document['deferred_item_id']}`: `{document['status']}`"
        )
    for document in snapshot.discrepancy_documents:
        if str(document.get("status")) == "resolved":
            continue
        lines.append(
            f"- Open discrepancy `{document['discrepancy_id']}`: `{document['severity']}` `{document['category']}`"
        )
    if not lines:
        return ("- No unresolved follow-up items remain.",)
    return tuple(lines)


def initiative_closeout_lines(
    snapshot: PlanInitiativeSnapshot,
) -> tuple[str, ...]:
    initiative = snapshot.initiative_document
    lines: list[str] = [
        f"- `lifecycle_stage`: `{initiative['lifecycle_stage']}`",
        f"- `updated_at`: `{snapshot_updated_at(snapshot)}`",
    ]
    for document in snapshot.closeout_documents:
        lines.append(f"- `{document['id']}`: `{document['status']}`")
    if initiative.get("closed_at") is not None:
        lines.append(f"- `closed_at`: `{initiative['closed_at']}`")
    if initiative.get("closure_reason") is not None:
        lines.append(f"- `closure_reason`: {initiative['closure_reason']}")
    if initiative.get("superseded_by_trace_id") is not None:
        lines.append(
            f"- `superseded_by_trace_id`: `{initiative['superseded_by_trace_id']}`"
        )
    return tuple(lines)


__all__ = [
    "PHASE_ORDER",
    "PRIORITY_ORDER",
    "PlanWorkspaceRenderer",
    "initiative_blocker_lines",
    "initiative_closeout_lines",
    "initiative_delivered_output_lines",
    "initiative_dependency_and_risk_lines",
    "initiative_evidence_reference_lines",
    "initiative_evidence_validation_lines",
    "initiative_event_rows",
    "initiative_gate_lines",
    "initiative_linked_output_lines",
    "initiative_objective_lines",
    "initiative_promotion_lines",
    "initiative_scope_lines",
    "initiative_task_rows",
    "initiative_unresolved_follow_up_lines",
]
