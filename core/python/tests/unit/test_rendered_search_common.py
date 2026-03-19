from __future__ import annotations

from dataclasses import dataclass

from watchtower_core.repo_ops.query.common import (
    RenderedSearchFilters,
    rendered_search_filters_from_params,
    search_rendered_entries,
)


@dataclass(frozen=True, slots=True)
class _FakeRenderedEntry:
    trace_id: str
    title: str
    initiative_status: str = "active"
    current_phase: str = "execution"
    primary_owner: str | None = "repository_maintainer"
    active_owners: tuple[str, ...] = ("repository_maintainer",)
    blocked_task_count: int = 0


@dataclass(frozen=True, slots=True)
class _FakeRenderedParams:
    query: str | None = None
    trace_id: str | None = None
    initiative_status: str | None = None
    current_phase: str | None = None
    owner: str | None = None
    limit: int | None = None


def test_rendered_search_filters_from_params_maps_shared_fields() -> None:
    params = _FakeRenderedParams(
        query="alpha",
        trace_id="trace.alpha",
        initiative_status="active",
        current_phase="execution",
        owner="repository_maintainer",
        limit=5,
    )

    assert rendered_search_filters_from_params(
        params,
        blocked_only=True,
    ) == RenderedSearchFilters(
        query="alpha",
        trace_id="trace.alpha",
        initiative_status="active",
        current_phase="execution",
        owner="repository_maintainer",
        blocked_only=True,
        limit=5,
    )


def test_rendered_search_applies_shared_structured_filters() -> None:
    entries = (
        _FakeRenderedEntry(trace_id="trace.alpha", title="Alpha planning trace"),
        _FakeRenderedEntry(
            trace_id="trace.beta",
            title="Beta planning trace",
            current_phase="validation",
        ),
        _FakeRenderedEntry(
            trace_id="trace.gamma",
            title="Gamma planning trace",
            initiative_status="completed",
        ),
    )

    results = search_rendered_entries(
        entries,
        RenderedSearchFilters(
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


def test_rendered_search_preserves_service_specific_tie_break_order() -> None:
    entries = (
        _FakeRenderedEntry(
            trace_id="trace.third",
            title="Shared blocker trace",
            blocked_task_count=1,
        ),
        _FakeRenderedEntry(
            trace_id="trace.first",
            title="Shared blocker trace",
            blocked_task_count=1,
        ),
        _FakeRenderedEntry(
            trace_id="trace.second",
            title="Shared blocker trace",
            blocked_task_count=1,
        ),
    )
    entry_rank = {entry.trace_id: idx for idx, entry in enumerate(entries)}

    results = search_rendered_entries(
        entries,
        RenderedSearchFilters(query="shared blocker", blocked_only=True),
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


def test_rendered_search_enforces_owner_filter_across_primary_and_active_owners() -> None:
    entries = (
        _FakeRenderedEntry(
            trace_id="trace.primary",
            title="Primary owner match",
            primary_owner="Repository_Maintainer",
            active_owners=(),
        ),
        _FakeRenderedEntry(
            trace_id="trace.active",
            title="Active owner match",
            primary_owner=None,
            active_owners=("repository_maintainer", "reviewer"),
        ),
        _FakeRenderedEntry(
            trace_id="trace.other",
            title="Other owner",
            primary_owner="reviewer",
            active_owners=("reviewer",),
        ),
    )

    results = search_rendered_entries(
        entries,
        RenderedSearchFilters(owner="repository_maintainer"),
        query_fields=lambda entry: (entry.trace_id, entry.title),
        sort_key=lambda entry: entry.trace_id,
        trace_id=lambda entry: entry.trace_id,
        initiative_status=lambda entry: entry.initiative_status,
        current_phase=lambda entry: entry.current_phase,
        primary_owner=lambda entry: entry.primary_owner,
        active_owners=lambda entry: entry.active_owners,
    )

    assert tuple(entry.trace_id for entry in results) == ("trace.active", "trace.primary")
