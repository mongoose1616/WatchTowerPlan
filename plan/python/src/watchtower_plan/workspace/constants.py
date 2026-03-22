"""Shared constants for the plan workspace package."""

from __future__ import annotations

PLAN_PACK_SETTINGS_PATH = "plan/.wt/manifests/pack_settings.json"
PLAN_INITIATIVE_INDEX_PATH = "plan/.wt/indexes/initiative_index.json"
PLAN_TASK_INDEX_PATH = "plan/.wt/indexes/task_index.json"
PLAN_READINESS_INDEX_PATH = "plan/.wt/indexes/readiness_index.json"
PLAN_DISCREPANCY_INDEX_PATH = "plan/.wt/indexes/discrepancy_index.json"
PLAN_EVIDENCE_INDEX_PATH = "plan/.wt/indexes/evidence_index.json"
PLAN_CLOSEOUT_INDEX_PATH = "plan/.wt/indexes/closeout_index.json"
PLAN_REVIEW_INDEX_PATH = "plan/.wt/indexes/review_index.json"
PLAN_PROMOTION_INDEX_PATH = "plan/.wt/indexes/promotion_index.json"
PLAN_GUIDANCE_INDEX_PATH = "plan/.wt/indexes/guidance_index.json"
PLAN_COORDINATION_INDEX_PATH = "plan/.wt/indexes/coordination_index.json"
PLAN_OVERVIEW_PATH = "plan/plan_overview.md"
PLAN_OVERVIEW_SURFACE_ID = "rendered.plan.overview"
INITIATIVE_PLAN_SURFACE_ID = "rendered.initiative.plan"
INITIATIVE_PROGRESS_SURFACE_ID = "rendered.initiative.progress"
INITIATIVE_SUMMARY_SURFACE_ID = "rendered.initiative.summary"

TERMINAL_TASK_STATUSES = frozenset({"completed", "cancelled"})
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
PHASE_ORDER = {
    "capture": 0,
    "execution": 1,
    "closeout": 2,
    "closed": 3,
}
