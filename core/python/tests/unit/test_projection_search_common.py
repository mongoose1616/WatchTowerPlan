from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.repo_ops.query.common import (
    ProjectionSearchFilters,
    search_projection_entries,
)


@dataclass(frozen=True, slots=True)
class _FakeProjectionEntry:
    trace_id: str
    title: str
    initiative_status: str = "active"
    current_phase: str = "execution"
    primary_owner: str | None = "repository_maintainer"
    active_owners: tuple[str, ...] = ("repository_maintainer",)
    blocked_task_count: int = 0


def test_projection_search_applies_shared_structured_filters() -> None:
    entries = (
        _FakeProjectionEntry(trace_id="trace.alpha", title="Alpha planning trace"),
        _FakeProjectionEntry(
            trace_id="trace.beta",
            title="Beta planning trace",
            current_phase="validation",
        ),
        _FakeProjectionEntry(
            trace_id="trace.gamma",
            title="Gamma planning trace",
            initiative_status="completed",
        ),
    )

    results = search_projection_entries(
        entries,
        ProjectionSearchFilters(
            initiative_status="active",
            current_phase="execution",
            owner="repository_maintainer",
        ),
        query_fields=lambda entry: (entry.trace_id, entry.title),
        sort_key=lambda entry: entry.trace_id,
        trace_id=lambda entry: entry.trace_id,
        initiative_status=lambda entry: entry.initiative_status,
        current_phase=lambda entry: entry.current_phase,
        primary_owner=lambda entry: entry.primary_owner,
        active_owners=lambda entry: entry.active_owners,
        blocked_task_count=lambda entry: entry.blocked_task_count,
    )

    assert tuple(entry.trace_id for entry in results) == ("trace.alpha",)


def test_projection_search_preserves_service_specific_tie_break_order() -> None:
    entries = (
        _FakeProjectionEntry(
            trace_id="trace.third",
            title="Shared blocker trace",
            blocked_task_count=1,
        ),
        _FakeProjectionEntry(
            trace_id="trace.first",
            title="Shared blocker trace",
            blocked_task_count=1,
        ),
        _FakeProjectionEntry(
            trace_id="trace.second",
            title="Shared blocker trace",
            blocked_task_count=1,
        ),
    )
    entry_rank = {entry.trace_id: idx for idx, entry in enumerate(entries)}

    results = search_projection_entries(
        entries,
        ProjectionSearchFilters(query="shared blocker", blocked_only=True),
        query_fields=lambda entry: (entry.trace_id, entry.title),
        sort_key=lambda entry: (entry_rank[entry.trace_id], entry.trace_id),
        trace_id=lambda entry: entry.trace_id,
        initiative_status=lambda entry: entry.initiative_status,
        current_phase=lambda entry: entry.current_phase,
        primary_owner=lambda entry: entry.primary_owner,
        active_owners=lambda entry: entry.active_owners,
        blocked_task_count=lambda entry: entry.blocked_task_count,
    )

    assert tuple(entry.trace_id for entry in results) == (
        "trace.third",
        "trace.first",
        "trace.second",
    )


def test_projection_search_enforces_owner_filter_across_primary_and_active_owners() -> None:
    entries = (
        _FakeProjectionEntry(
            trace_id="trace.primary",
            title="Primary owner match",
            primary_owner="Repository_Maintainer",
            active_owners=(),
        ),
        _FakeProjectionEntry(
            trace_id="trace.active",
            title="Active owner match",
            primary_owner=None,
            active_owners=("repository_maintainer", "reviewer"),
        ),
        _FakeProjectionEntry(
            trace_id="trace.other",
            title="Other owner",
            primary_owner="reviewer",
            active_owners=("reviewer",),
        ),
    )

    results = search_projection_entries(
        entries,
        ProjectionSearchFilters(owner="repository_maintainer"),
        query_fields=lambda entry: (entry.trace_id, entry.title),
        sort_key=lambda entry: entry.trace_id,
        trace_id=lambda entry: entry.trace_id,
        initiative_status=lambda entry: entry.initiative_status,
        current_phase=lambda entry: entry.current_phase,
        primary_owner=lambda entry: entry.primary_owner,
        active_owners=lambda entry: entry.active_owners,
    )

    assert tuple(entry.trace_id for entry in results) == ("trace.active", "trace.primary")
