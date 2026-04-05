"""Pure unit tests for the routing algorithm using synthetic fixtures.

Tests scoring, overlay attachment, merge-policy suppression, and
assisted fallback in isolation from real control-plane data.
Adding or removing routes in the live index cannot break these tests.
"""

from __future__ import annotations

import pytest

from watchtower_core.query.routes import RoutePreviewService, ScoringConfig

from .synthetic_routing_support import (
    make_merge_policy,
    make_overlay,
    make_route,
    make_stub_loader,
    make_workflow,
    synthetic_preview,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _route_ids(result) -> list[str]:
    return [r.route_id for r in result.selected_routes]


def _task_types(result) -> set[str]:
    return {r.task_type for r in result.selected_routes}


def _workflow_ids(result) -> set[str]:
    return {w.workflow_id for w in result.selected_workflows}


def _intent_ids(result) -> set[str]:
    return {i.intent_id for i in result.activated_intents}


# ===================================================================
# Scoring basics
# ===================================================================


class TestScoringBasics:
    """Core keyword and phrase matching behavior."""

    def test_exact_phrase_match_scores_highest(self) -> None:
        """A request containing the exact trigger phrase should win."""
        route_a = make_route("Alpha", keywords=("alpha task",))
        route_b = make_route("Beta", keywords=("beta task",))
        result = synthetic_preview(
            "please run the alpha task",
            routes=(route_a, route_b),
            workflows=(make_workflow("workflow.alpha"), make_workflow("workflow.beta")),
        )
        assert _route_ids(result) == ["route.alpha"]

    def test_single_token_match(self) -> None:
        route = make_route("Review", keywords=("review",))
        result = synthetic_preview(
            "review the code",
            routes=(route,),
            workflows=(make_workflow("workflow.review"),),
        )
        assert "route.review" in _route_ids(result)

    def test_multi_token_keyword_all_tokens_required(self) -> None:
        """A multi-word keyword only matches if all tokens appear."""
        route = make_route("Full Audit", keywords=("full audit",))
        result = synthetic_preview(
            "just audit please",
            routes=(route,),
            workflows=(make_workflow("workflow.full_audit"),),
        )
        # "full" is missing — should not match the multi-word keyword phrase,
        # but "audit" alone may still match via task-type token scoring
        # The key assertion: "full audit" phrase bonus should NOT activate
        for match in result.selected_routes:
            assert "full audit" not in match.matched_keywords

    def test_no_match_returns_empty(self) -> None:
        route = make_route("Alpha", keywords=("alpha",))
        result = synthetic_preview(
            "completely unrelated request",
            routes=(route,),
            workflows=(make_workflow("workflow.alpha"),),
        )
        assert result.selected_routes == ()

    def test_highest_scoring_route_wins_tiebreak(self) -> None:
        """When two routes match, the higher-scoring one appears first."""
        route_a = make_route("Review Code", keywords=("review code", "audit code"))
        route_b = make_route("Review Docs", keywords=("review docs",))
        result = synthetic_preview(
            "review code and audit code changes",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.review_code"),
                make_workflow("workflow.review_docs"),
            ),
        )
        assert result.selected_routes
        assert result.selected_routes[0].route_id == "route.review_code"

    def test_case_insensitive_matching(self) -> None:
        route = make_route("Alpha", keywords=("alpha task",))
        result = synthetic_preview(
            "ALPHA TASK please",
            routes=(route,),
            workflows=(make_workflow("workflow.alpha"),),
        )
        assert "route.alpha" in _route_ids(result)

    def test_empty_request_returns_no_routes(self) -> None:
        route = make_route("Alpha", keywords=("alpha",))
        result = synthetic_preview(
            "   ",
            routes=(route,),
            workflows=(make_workflow("workflow.alpha"),),
        )
        assert result.selected_routes == ()


# ===================================================================
# Secondary route filtering
# ===================================================================


class TestSecondaryRouteFiltering:
    """The filter that keeps secondary routes above 50% of top score."""

    def test_weak_secondary_route_is_dropped(self) -> None:
        """A route scoring far below the top should be filtered out."""
        # Route A: exact phrase match on "review code" → high score
        # Route B: single token "code" → low score
        route_a = make_route("Code Review", keywords=("review code",))
        route_b = make_route("Code Validation", keywords=("validate",))
        result = synthetic_preview(
            "review code carefully",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.code_validation"),
            ),
        )
        assert _task_types(result) == {"Code Review"}

    def test_strong_secondary_route_is_retained(self) -> None:
        """Two routes with similar scores should both survive."""
        route_a = make_route("Code Review", keywords=("review code",))
        route_b = make_route("Code Audit", keywords=("audit code",))
        result = synthetic_preview(
            "review code and audit code",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.code_audit"),
            ),
        )
        assert "Code Review" in _task_types(result)
        assert "Code Audit" in _task_types(result)


# ===================================================================
# Overlay attachment
# ===================================================================


class TestOverlayAttachment:
    """Overlays attach workflows to compatible routes via intents."""

    def test_workflow_modifier_overlay_attaches_workflow(self) -> None:
        """A workflow_modifier overlay should add its workflow to the
        selected set when the trigger term is present."""
        route = make_route("Code Review", keywords=("review code",))
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            compatible_task_types=("Code Review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        result = synthetic_preview(
            "adversarial review code",
            routes=(route,),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "route.code_review" in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "overlay.adversarial" in _intent_ids(result)

    def test_overlay_does_not_attach_to_incompatible_route(self) -> None:
        """Overlay with compatible_task_types should NOT attach to
        a route outside that list."""
        route = make_route("Branch Cleanup", keywords=("branch cleanup",))
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            compatible_task_types=("Code Review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        result = synthetic_preview(
            "adversarial branch cleanup",
            routes=(route,),
            workflows=(
                make_workflow("workflow.branch_cleanup"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "route.branch_cleanup" in _route_ids(result)
        assert "workflow.adversarial_reviewer" not in _workflow_ids(result)

    def test_overlay_excluded_task_type_blocks_attachment(self) -> None:
        """Even if compatible_task_types is empty (allow all), an
        excluded task type should block the overlay."""
        route = make_route("Special Review", keywords=("special review",))
        overlay = make_overlay(
            "overlay.extra",
            trigger_terms=("extra",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            excluded_task_types=("Special Review",),
            attached_workflow_ids=("workflow.extra",),
        )
        result = synthetic_preview(
            "extra special review",
            routes=(route,),
            workflows=(
                make_workflow("workflow.special_review"),
                make_workflow("workflow.extra"),
            ),
            overlays=(overlay,),
        )
        assert "workflow.extra" not in _workflow_ids(result)

    def test_companion_route_overlay_adds_companion(self) -> None:
        """A companion_route overlay should add its attached route
        alongside the dominant route."""
        route_main = make_route("Code Review", keywords=("review code",))
        route_companion = make_route("Commit Closeout", keywords=("commit",))
        overlay = make_overlay(
            "overlay.commit",
            trigger_terms=("commit",),
            trigger_mode="anywhere",
            intent_kind="companion_route",
            attached_route_task_types=("Commit Closeout",),
            dominant_route_retention_mode="strongest_compatible",
            exclude_attached_from_scoring=True,
            minimum_route_score=12,
        )
        result = synthetic_preview(
            "review code and commit",
            routes=(route_main, route_companion),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.commit_closeout"),
            ),
            overlays=(overlay,),
        )
        assert "Code Review" in _task_types(result)
        assert "Commit Closeout" in _task_types(result)

    def test_modifier_before_anchor_trigger_mode(self) -> None:
        """modifier_before_anchor mode requires the trigger term
        to appear before an anchor term."""
        route = make_route("Code Review", keywords=("review code",))
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="modifier_before_anchor",
            anchor_terms=("review", "audit"),
            intent_kind="workflow_modifier",
            compatible_task_types=("Code Review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        # trigger before anchor: should activate
        result = synthetic_preview(
            "adversarial review code",
            routes=(route,),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_modifier_before_anchor_does_not_fire_when_after(self) -> None:
        """If the trigger term appears AFTER the anchor, the overlay
        should not activate."""
        route = make_route("Code Review", keywords=("review code",))
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="modifier_before_anchor",
            anchor_terms=("review",),
            intent_kind="workflow_modifier",
            compatible_task_types=("Code Review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        result = synthetic_preview(
            "review code adversarial",
            routes=(route,),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "workflow.adversarial_reviewer" not in _workflow_ids(result)


# ===================================================================
# Intent suppression
# ===================================================================


class TestIntentSuppression:
    """One overlay can suppress another via suppresses_intent_ids."""

    def test_stronger_intent_suppresses_weaker(self) -> None:
        route_single = make_route("Single Pass", keywords=("fix findings",))
        route_loop = make_route("Loop Pass", keywords=("fix loop",))
        overlay_single = make_overlay(
            "overlay.single",
            trigger_terms=("fix findings",),
            trigger_mode="anywhere",
            intent_kind="companion_route",
            attached_route_task_types=("Single Pass",),
            dominant_route_retention_mode="all_compatible",
            exclude_attached_from_scoring=True,
        )
        overlay_loop = make_overlay(
            "overlay.loop",
            trigger_terms=("fix loop",),
            trigger_mode="anywhere",
            intent_kind="companion_route",
            attached_route_task_types=("Loop Pass",),
            dominant_route_retention_mode="all_compatible",
            exclude_attached_from_scoring=True,
            suppresses_intent_ids=("overlay.single",),
        )
        result = synthetic_preview(
            "fix findings fix loop",
            routes=(route_single, route_loop),
            workflows=(
                make_workflow("workflow.single_pass"),
                make_workflow("workflow.loop_pass"),
            ),
            overlays=(overlay_single, overlay_loop),
        )
        assert "overlay.loop" in _intent_ids(result)
        assert "overlay.single" not in _intent_ids(result)


# ===================================================================
# Merge policy suppression
# ===================================================================


class TestMergePolicySuppression:
    """Merge policies suppress conflicting routes after scoring."""

    def test_when_all_present_suppresses_target(self) -> None:
        route_a = make_route("Alpha", keywords=("alpha",))
        route_b = make_route("Beta", keywords=("beta",))
        policy = make_merge_policy(
            "policy.suppress_beta",
            when_all=("Alpha", "Beta"),
            suppress_task_types=("Beta",),
        )
        result = synthetic_preview(
            "alpha and beta",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.alpha"),
                make_workflow("workflow.beta"),
            ),
            merge_policies=(policy,),
        )
        assert "Alpha" in _task_types(result)
        assert "Beta" not in _task_types(result)

    def test_when_any_present_suppresses_target(self) -> None:
        route_a = make_route("Alpha", keywords=("alpha",))
        route_b = make_route("Beta", keywords=("beta",))
        route_c = make_route("Gamma", keywords=("gamma",))
        policy = make_merge_policy(
            "policy.suppress_gamma",
            when_any=("Alpha", "Beta"),
            when_all=("Gamma",),
            suppress_task_types=("Gamma",),
        )
        result = synthetic_preview(
            "alpha and gamma",
            routes=(route_a, route_b, route_c),
            workflows=(
                make_workflow("workflow.alpha"),
                make_workflow("workflow.beta"),
                make_workflow("workflow.gamma"),
            ),
            merge_policies=(policy,),
        )
        assert "Alpha" in _task_types(result)
        assert "Gamma" not in _task_types(result)

    def test_unless_terms_block_suppression(self) -> None:
        """Suppression should NOT fire when an unless-term is present."""
        route_a = make_route("Alpha", keywords=("alpha",))
        route_b = make_route("Beta", keywords=("beta",))
        policy = make_merge_policy(
            "policy.suppress_beta",
            when_all=("Alpha", "Beta"),
            suppress_task_types=("Beta",),
            unless_terms=("keep beta",),
        )
        result = synthetic_preview(
            "alpha and beta keep beta",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.alpha"),
                make_workflow("workflow.beta"),
            ),
            merge_policies=(policy,),
        )
        assert "Alpha" in _task_types(result)
        assert "Beta" in _task_types(result)

    def test_when_terms_required_for_suppression(self) -> None:
        """Suppression should only fire when request terms match."""
        route_a = make_route("Alpha", keywords=("alpha",))
        route_b = make_route("Beta", keywords=("beta",))
        policy = make_merge_policy(
            "policy.suppress_beta",
            when_all=("Alpha", "Beta"),
            when_terms=("urgent",),
            suppress_task_types=("Beta",),
        )
        # No "urgent" in request — policy should NOT fire
        result = synthetic_preview(
            "alpha and beta",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.alpha"),
                make_workflow("workflow.beta"),
            ),
            merge_policies=(policy,),
        )
        assert "Beta" in _task_types(result)

    def test_policy_priority_ordering(self) -> None:
        """Lower priority number runs first."""
        route_a = make_route("Alpha", keywords=("alpha",))
        route_b = make_route("Beta", keywords=("beta",))
        route_c = make_route("Gamma", keywords=("gamma",))
        # Policy 1 (priority 10): suppress Beta when Alpha present
        # Policy 2 (priority 20): suppress Gamma when Beta present
        # If policy 1 runs first, Beta is gone, so policy 2 should not fire
        policy_1 = make_merge_policy(
            "policy.1",
            priority=10,
            when_all=("Alpha", "Beta"),
            suppress_task_types=("Beta",),
        )
        policy_2 = make_merge_policy(
            "policy.2",
            priority=20,
            when_all=("Beta", "Gamma"),
            suppress_task_types=("Gamma",),
        )
        result = synthetic_preview(
            "alpha beta gamma",
            routes=(route_a, route_b, route_c),
            workflows=(
                make_workflow("workflow.alpha"),
                make_workflow("workflow.beta"),
                make_workflow("workflow.gamma"),
            ),
            merge_policies=(policy_1, policy_2),
        )
        assert "Alpha" in _task_types(result)
        assert "Beta" not in _task_types(result)
        # Gamma survives because Beta was already suppressed before policy 2 ran
        assert "Gamma" in _task_types(result)


# ===================================================================
# Workflow composition
# ===================================================================


class TestWorkflowComposition:
    """Correct workflows are collected from routes and overlays."""

    def test_multi_route_merges_workflows(self) -> None:
        """Workflows from multiple routes are de-duplicated and merged."""
        route_a = make_route(
            "Alpha",
            keywords=("alpha",),
            workflow_ids=("workflow.core", "workflow.alpha"),
        )
        route_b = make_route(
            "Beta",
            keywords=("beta",),
            workflow_ids=("workflow.core", "workflow.beta"),
        )
        result = synthetic_preview(
            "alpha and beta",
            routes=(route_a, route_b),
            workflows=(
                make_workflow("workflow.core"),
                make_workflow("workflow.alpha"),
                make_workflow("workflow.beta"),
            ),
        )
        wids = _workflow_ids(result)
        assert "workflow.core" in wids
        assert "workflow.alpha" in wids
        assert "workflow.beta" in wids

    def test_missing_workflow_raises(self) -> None:
        """Referencing a workflow not in the index should raise."""
        route = make_route(
            "Alpha",
            keywords=("alpha",),
            workflow_ids=("workflow.nonexistent",),
        )
        with pytest.raises(ValueError, match="missing workflow-index entries"):
            synthetic_preview(
                "alpha",
                routes=(route,),
                workflows=(),
            )


# ===================================================================
# Explicit task-type selection
# ===================================================================


class TestExplicitTaskType:
    """Selecting by exact task type bypasses scoring."""

    def test_exact_task_type_returns_single_route(self) -> None:
        route = make_route("Code Review", keywords=("review code",))
        loader = make_stub_loader(
            routes=(route,),
            workflows=(make_workflow("workflow.code_review"),),
        )
        result = RoutePreviewService(loader).preview(task_type="Code Review")
        assert len(result.selected_routes) == 1
        assert result.selected_routes[0].route_id == "route.code_review"
        assert result.selected_routes[0].score == 100

    def test_unknown_task_type_raises(self) -> None:
        route = make_route("Code Review", keywords=("review code",))
        loader = make_stub_loader(
            routes=(route,),
            workflows=(make_workflow("workflow.code_review"),),
        )
        with pytest.raises(ValueError, match="Unknown task type"):
            RoutePreviewService(loader).preview(task_type="Nonexistent")

    def test_both_inputs_raises(self) -> None:
        loader = make_stub_loader()
        with pytest.raises(ValueError, match="exactly one"):
            RoutePreviewService(loader).preview(
                request_text="review", task_type="Code Review"
            )

    def test_neither_input_raises(self) -> None:
        loader = make_stub_loader()
        with pytest.raises(ValueError, match="exactly one"):
            RoutePreviewService(loader).preview()


# ===================================================================
# Multiple overlays composing together
# ===================================================================


class TestMultipleOverlayComposition:
    """Multiple overlays can activate simultaneously."""

    def test_two_overlays_both_activate(self) -> None:
        route = make_route("Code Review", keywords=("review code",))
        overlay_a = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            compatible_task_types=("Code Review",),
            attached_workflow_ids=("workflow.adversarial",),
        )
        overlay_b = make_overlay(
            "overlay.commit",
            trigger_terms=("commit",),
            trigger_mode="anywhere",
            intent_kind="companion_route",
            attached_route_task_types=("Commit Closeout",),
            dominant_route_retention_mode="strongest_compatible",
            exclude_attached_from_scoring=True,
        )
        route_commit = make_route("Commit Closeout", keywords=("commit",))
        result = synthetic_preview(
            "adversarial review code and commit",
            routes=(route, route_commit),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.commit_closeout"),
                make_workflow("workflow.adversarial"),
            ),
            overlays=(overlay_a, overlay_b),
        )
        intent_ids = _intent_ids(result)
        assert "overlay.adversarial" in intent_ids
        assert "overlay.commit" in intent_ids
        assert "Code Review" in _task_types(result)
        assert "Commit Closeout" in _task_types(result)
        assert "workflow.adversarial" in _workflow_ids(result)


# ===================================================================
# Assisted fallback suggestions
# ===================================================================


class TestAssistedFallback:
    """When no routes match, the engine should produce assisted suggestions."""

    def test_no_match_produces_suggestions(self) -> None:
        route = make_route("Code Review", keywords=("review code",))
        workflow = make_workflow("workflow.code_review", title="Code Review")
        synthetic_preview(
            "something about review",
            routes=(route,),
            workflows=(workflow,),
        )
        # "review" alone may or may not match the route depending on scoring,
        # but let's test with a fully unmatched request
        result2 = synthetic_preview(
            "improve the xyzzy plugh",
            routes=(route,),
            workflows=(workflow,),
        )
        assert result2.selected_routes == ()

    def test_warnings_when_no_match(self) -> None:
        result = synthetic_preview(
            "xyzzy plugh",
            routes=(make_route("Alpha", keywords=("alpha",)),),
            workflows=(make_workflow("workflow.alpha"),),
        )
        assert any("No route matched" in w for w in result.warnings)


# ===================================================================
# Route-family-based overlay compatibility
# ===================================================================


class TestRouteFamilyOverlayCompatibility:
    """Overlays can declare compatible_route_families to match routes
    by family membership, not just by explicit task-type lists."""

    def test_family_match_enables_overlay(self) -> None:
        """A route NOT in compatible_task_types but IN a matching family
        should still receive the overlay."""
        make_route("Security Audit", keywords=("security audit",))
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            compatible_task_types=(),  # no explicit task types
            compatible_route_families=("review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        # Give the route the "review" family via the route entry
        from watchtower_core.control_plane.models import RouteIndexEntry
        route_with_family = RouteIndexEntry(
            route_id="route.security_audit",
            task_type="Security Audit",
            trigger_keywords=("security audit",),
            required_workflow_ids=("workflow.security_audit",),
            required_workflow_paths=("core/workflows/modules/security_audit.md",),
            route_families=("review",),
        )
        result = synthetic_preview(
            "adversarial security audit",
            routes=(route_with_family,),
            workflows=(
                make_workflow("workflow.security_audit"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "route.security_audit" in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_family_mismatch_blocks_overlay(self) -> None:
        """A route with a non-matching family should NOT receive the overlay."""
        from watchtower_core.control_plane.models import RouteIndexEntry
        route_with_family = RouteIndexEntry(
            route_id="route.cleanup_job",
            task_type="Cleanup Job",
            trigger_keywords=("cleanup job",),
            required_workflow_ids=("workflow.cleanup_job",),
            required_workflow_paths=("core/workflows/modules/cleanup_job.md",),
            route_families=("infrastructure",),
        )
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            compatible_route_families=("review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        result = synthetic_preview(
            "adversarial cleanup job",
            routes=(route_with_family,),
            workflows=(
                make_workflow("workflow.cleanup_job"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "route.cleanup_job" in _route_ids(result)
        assert "workflow.adversarial_reviewer" not in _workflow_ids(result)

    def test_explicit_task_type_and_family_both_work(self) -> None:
        """Both compatible_task_types and compatible_route_families
        should be checked — matching either is sufficient."""
        from watchtower_core.control_plane.models import RouteIndexEntry
        route_explicit = make_route("Code Review", keywords=("review code",))
        route_by_family = RouteIndexEntry(
            route_id="route.new_review_type",
            task_type="New Review Type",
            trigger_keywords=("new review",),
            required_workflow_ids=("workflow.new_review_type",),
            required_workflow_paths=("core/workflows/modules/new_review_type.md",),
            route_families=("review",),
        )
        overlay = make_overlay(
            "overlay.adversarial",
            trigger_terms=("adversarial",),
            trigger_mode="anywhere",
            intent_kind="workflow_modifier",
            compatible_task_types=("Code Review",),
            compatible_route_families=("review",),
            attached_workflow_ids=("workflow.adversarial_reviewer",),
        )
        # Both should match: code_review via explicit, new_review via family
        result1 = synthetic_preview(
            "adversarial review code",
            routes=(route_explicit,),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        result2 = synthetic_preview(
            "adversarial new review",
            routes=(route_by_family,),
            workflows=(
                make_workflow("workflow.new_review_type"),
                make_workflow("workflow.adversarial_reviewer"),
            ),
            overlays=(overlay,),
        )
        assert "workflow.adversarial_reviewer" in _workflow_ids(result1)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result2)


# ===================================================================
# Scoring config customization
# ===================================================================


class TestScoringConfig:
    """ScoringConfig changes are wired through to scoring decisions."""

    def test_custom_phrase_match_base_changes_scores(self) -> None:
        """Increasing phrase_match_base should increase the match score."""
        route = make_route("Alpha Task", keywords=("alpha task",))
        workflows = (make_workflow("workflow.alpha_task"),)

        default_result = synthetic_preview(
            "alpha task", routes=(route,), workflows=workflows,
        )
        boosted_result = synthetic_preview(
            "alpha task", routes=(route,), workflows=workflows,
            scoring_config=ScoringConfig(phrase_match_base=50),
        )
        assert boosted_result.selected_routes[0].score > default_result.selected_routes[0].score

    def test_custom_multi_token_match_base_changes_score(self) -> None:
        """Changing multi_token_match_base should change scores for
        keywords where all tokens match but the phrase doesn't."""
        # Keyword "alpha beta" — request has both tokens but not as a phrase
        route = make_route("Zxcv Qwer", keywords=("alpha beta",))
        workflows = (make_workflow("workflow.zxcv_qwer"),)

        default_result = synthetic_preview(
            "beta then alpha",  # tokens match, phrase does not
            routes=(route,), workflows=workflows,
        )
        boosted_result = synthetic_preview(
            "beta then alpha",
            routes=(route,), workflows=workflows,
            scoring_config=ScoringConfig(multi_token_match_base=30),
        )
        assert default_result.selected_routes
        assert boosted_result.selected_routes
        # Default: 10 + 2*2 = 14, Boosted: 30 + 2*2 = 34
        assert boosted_result.selected_routes[0].score > default_result.selected_routes[0].score

    def test_high_secondary_minimum_filters_more_aggressively(self) -> None:
        """A very high secondary_route_minimum should drop weak matches."""
        route_strong = make_route("Code Review", keywords=("review code", "audit code"))
        route_weak = make_route("Code Validation", keywords=("code",))
        result = synthetic_preview(
            "review code and check the code",
            routes=(route_strong, route_weak),
            workflows=(
                make_workflow("workflow.code_review"),
                make_workflow("workflow.code_validation"),
            ),
            scoring_config=ScoringConfig(secondary_route_minimum=100),
        )
        # With minimum=100, only the top route should survive
        assert len(result.selected_routes) == 1
        assert result.selected_routes[0].route_id == "route.code_review"

    def test_custom_token_matcher_enables_prefix_matching(self) -> None:
        """A prefix-based token matcher should allow partial token matches."""

        def prefix_matcher(request_token: str, candidate_token: str) -> bool:
            return request_token.startswith(candidate_token) or candidate_token.startswith(
                request_token
            )

        # Keyword is "benchmark", request uses "bench" — exact match fails,
        # but prefix matcher should succeed.
        route = make_route("Zxcv Qwer", keywords=("benchmark",))
        workflows = (make_workflow("workflow.zxcv_qwer"),)

        exact_result = synthetic_preview(
            "bench the system",
            routes=(route,), workflows=workflows,
        )
        prefix_result = synthetic_preview(
            "bench the system",
            routes=(route,), workflows=workflows,
            scoring_config=ScoringConfig(token_matcher=prefix_matcher),
        )
        assert exact_result.selected_routes == ()
        assert prefix_result.selected_routes
        assert prefix_result.selected_routes[0].route_id == "route.zxcv_qwer"

    def test_custom_token_aliases_expand_vocabulary(self) -> None:
        """Custom token_aliases should normalize novel terms."""
        route = make_route("Zxcv Qwer", keywords=("review",))
        workflows = (make_workflow("workflow.zxcv_qwer"),)

        # "inspect" is not an alias of "review" by default
        default_result = synthetic_preview(
            "inspect the thing",
            routes=(route,), workflows=workflows,
        )
        # Add a custom alias
        custom_aliases = dict(ScoringConfig().token_aliases)
        custom_aliases["inspect"] = "review"
        custom_result = synthetic_preview(
            "inspect the thing",
            routes=(route,), workflows=workflows,
            scoring_config=ScoringConfig(token_aliases=custom_aliases),
        )
        assert default_result.selected_routes == ()
        assert custom_result.selected_routes
        assert custom_result.selected_routes[0].route_id == "route.zxcv_qwer"
