"""Mock scenario tests for workflow routing.

Exercises the routing engine against realistic user requests to verify
that route selection, overlay activation, merge-policy suppression, and
assisted-module fallback behave correctly across the full surface of
task types, intents, and composite phrasing.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from watchtower_core.control_plane.loader import ControlPlaneLoader
from watchtower_core.routing import RoutingEngine

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(scope="module")
def engine() -> RoutingEngine:
    """Single shared engine for all scenario tests in this module."""
    return RoutingEngine(ControlPlaneLoader(REPO_ROOT))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _route_ids(result) -> list[str]:
    return [r.route_id for r in result.selected_routes]


def _task_types(result) -> list[str]:
    return [r.task_type for r in result.selected_routes]


def _workflow_ids(result) -> set[str]:
    return {w.workflow_id for w in result.selected_workflows}


def _intent_ids(result) -> set[str]:
    return {i.intent_id for i in result.activated_intents}


# ===================================================================
# SECTION 1 — Adversarial refactor & optimization review in fix loops
# ===================================================================


class TestAdversarialRefactorOptimizationLoops:
    """Adversarial-lens overlay applied to implementation and review routes
    within remediation-loop contexts."""

    def test_adversarial_refactor_review_routes_to_implementation_with_overlay(
        self, engine: RoutingEngine,
    ) -> None:
        """'adversarial refactor review' should land on Code Implementation
        (refactor is an implementation keyword) with the adversarial-lens
        overlay, NOT the dedicated repository audit."""
        result = engine.select_for_request("adversarial refactor review")

        assert "route.code_implementation" in _route_ids(result)
        assert "Adversarial Repository Review" not in _task_types(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.overlay_adversarial_lens" in _intent_ids(result)

    def test_adversarial_optimization_review_routes_to_adversarial_repo_review(
        self, engine: RoutingEngine,
    ) -> None:
        """'adversarial optimization review' — 'optimization' alone does not
        match a compatible overlay-capable route strongly enough, so the
        dedicated adversarial repository review route wins."""
        result = engine.select_for_request("adversarial optimization review")

        assert result.selected_routes
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.adversarial_repository_review" in _route_ids(result)

    def test_adversarial_review_fix_loop_activates_loop_and_overlay(
        self, engine: RoutingEngine,
    ) -> None:
        """'adversarial review fix loop' should produce:
        - A compatible review route
        - Review Remediation Loop (via loop intent)
        - Adversarial reviewer workflow (via overlay)
        - Loop intent suppresses single-pass remediation intent."""
        result = engine.select_for_request("adversarial review fix loop")

        task_types = _task_types(result)
        assert "Review Remediation Loop" in task_types
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.overlay_adversarial_lens" in _intent_ids(result)
        assert "route.overlay_review_remediation_loop_intent" in _intent_ids(result)
        # Single-pass remediation should not survive loop suppression
        assert "Review Remediation" not in task_types

    def test_adversarial_code_review_and_fix_loop(
        self, engine: RoutingEngine,
    ) -> None:
        """'adversarial code review and fix loop' combines:
        code_review route + loop companion + adversarial overlay."""
        result = engine.select_for_request(
            "adversarial code review and fix loop"
        )

        task_types = _task_types(result)
        assert "Code Review" in task_types
        assert "Review Remediation Loop" in task_types
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "workflow.review_remediation_loop" in _workflow_ids(result)

    def test_adversarial_fix_loop_without_repo_scope_suppresses_repo_audit(
        self, engine: RoutingEngine,
    ) -> None:
        """Generic 'adversarial fix loop' should NOT activate full repository
        audit — merge policy suppresses it when no repo-scope terms present."""
        result = engine.select_for_request("adversarial fix loop")

        assert "Adversarial Repository Review" not in _task_types(result)
        assert "Review Remediation Loop" in _task_types(result)

    def test_adversarial_implementation_review_and_fix(
        self, engine: RoutingEngine,
    ) -> None:
        """'adversarial review of implementation and fix findings' should
        activate the adversarial overlay and route to remediation."""
        result = engine.select_for_request(
            "adversarial review of implementation and fix findings"
        )

        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.overlay_adversarial_lens" in _intent_ids(result)
        # Should produce a remediation route (loop or single-pass)
        task_types = _task_types(result)
        has_remediation = (
            "Review Remediation" in task_types
            or "Review Remediation Loop" in task_types
        )
        assert has_remediation


# ===================================================================
# SECTION 2 — Documentation and standards adherence review
# ===================================================================


class TestDocumentationAndStandardsAdherenceReview:
    """Routes for documentation review, standards alignment, and their
    composition with overlays and remediation."""

    def test_documentation_review_routes_correctly(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("documentation review")

        assert "route.documentation_review" in _route_ids(result)
        assert "workflow.documentation_review" in _workflow_ids(result)

    def test_standards_adherence_review_routes_correctly(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("standards adherence review")

        assert "route.standards_alignment_review" in _route_ids(result)
        assert "workflow.standards_alignment_review" in _workflow_ids(result)

    def test_governance_audit_routes_to_standards_alignment(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("governance audit")

        assert "route.standards_alignment_review" in _route_ids(result)

    def test_docs_audit_routes_to_documentation_review(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("docs audit")

        assert "route.documentation_review" in _route_ids(result)

    def test_adversarial_documentation_review(
        self, engine: RoutingEngine,
    ) -> None:
        """Adversarial lens should compose with documentation review."""
        result = engine.select_for_request("adversarial documentation review")

        assert "route.documentation_review" in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.overlay_adversarial_lens" in _intent_ids(result)

    def test_adversarial_standards_alignment_review(
        self, engine: RoutingEngine,
    ) -> None:
        """Adversarial lens should compose with standards alignment review."""
        result = engine.select_for_request("adversarial standards alignment review")

        assert "route.standards_alignment_review" in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_documentation_review_and_fix_findings(
        self, engine: RoutingEngine,
    ) -> None:
        """'documentation review and fix findings' should pair doc review
        with remediation."""
        result = engine.select_for_request(
            "documentation review and fix findings"
        )

        task_types = _task_types(result)
        assert "Documentation Review" in task_types
        assert "Review Remediation" in task_types
        assert "route.overlay_review_remediation_intent" in _intent_ids(result)

    def test_standards_review_remediation_loop(
        self, engine: RoutingEngine,
    ) -> None:
        """'standards review and fix loop' should pair standards alignment
        with a remediation loop."""
        result = engine.select_for_request(
            "standards alignment review fix loop"
        )

        task_types = _task_types(result)
        assert "Standards Alignment Review" in task_types
        assert "Review Remediation Loop" in task_types

    def test_documentation_refresh_routes_correctly(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("refresh docs")

        assert "route.documentation_refresh" in _route_ids(result)

    def test_documentation_generation_routes_correctly(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("create doc for the new module")

        assert "route.documentation_generation" in _route_ids(result)

    def test_docs_vs_code_reconciliation(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("reconcile docs with code")

        assert "route.documentation_implementation_reconciliation" in _route_ids(result)


# ===================================================================
# SECTION 3 — Overlay composition: adversarial lens with base routes
# ===================================================================


class TestAdversarialLensOverlayComposition:
    """The adversarial-lens overlay must attach to every compatible
    task type without escalating to the dedicated repo audit."""

    @pytest.mark.parametrize(
        "request_text, expected_route_id",
        [
            ("adversarial code review", "route.code_review"),
            ("adversarial documentation review", "route.documentation_review"),
            ("adversarial workflow audit", "route.workflow_system_review"),
            ("adversarial standards audit", "route.standards_alignment_review"),
            ("adversarial benchmark review", "route.performance_benchmarking"),
        ],
        ids=[
            "code_review",
            "documentation_review",
            "workflow_system_review",
            "standards_alignment",
            "performance_benchmarking",
        ],
    )
    def test_adversarial_overlay_attaches_to_compatible_route(
        self, engine: RoutingEngine, request_text: str, expected_route_id: str
    ) -> None:
        result = engine.select_for_request(request_text)

        assert expected_route_id in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.overlay_adversarial_lens" in _intent_ids(result)
        # Should NOT promote to full repo audit
        assert "Adversarial Repository Review" not in _task_types(result)

    def test_full_spectrum_audit_without_repo_scope_uses_overlay(
        self, engine: RoutingEngine,
    ) -> None:
        """'full-spectrum code review' should use the overlay, not repo audit."""
        result = engine.select_for_request("full-spectrum code review")

        assert "route.code_review" in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "Adversarial Repository Review" not in _task_types(result)

    def test_false_green_audit_routes_correctly(
        self, engine: RoutingEngine,
    ) -> None:
        """'false-green audit' is a trigger for both adversarial lens
        and validation harness review — the overlay should compose."""
        result = engine.select_for_request("false-green audit")

        # Should activate the adversarial lens overlay
        assert "route.overlay_adversarial_lens" in _intent_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_contradiction_oriented_review(
        self, engine: RoutingEngine,
    ) -> None:
        """'contradiction-oriented review' activates overlay on review route."""
        result = engine.select_for_request("contradiction-oriented code review")

        assert "workflow.adversarial_reviewer" in _workflow_ids(result)
        assert "route.overlay_adversarial_lens" in _intent_ids(result)


# ===================================================================
# SECTION 4 — Merge policy suppression scenarios
# ===================================================================


class TestMergePolicySuppression:
    """Verify merge policies suppress conflicting routes correctly."""

    def test_loop_suppresses_single_pass_remediation(
        self, engine: RoutingEngine,
    ) -> None:
        """When both loop and single-pass remediation match,
        the loop suppresses single-pass."""
        result = engine.select_for_request(
            "code review and fix loop until clean"
        )

        task_types = _task_types(result)
        assert "Review Remediation Loop" in task_types
        assert "Review Remediation" not in task_types

    def test_remediation_focus_suppresses_repo_review(
        self, engine: RoutingEngine,
    ) -> None:
        """Remediation keywords ('fix', 'findings') suppress repository review
        unless explicit repo-scope terms present."""
        result = engine.select_for_request(
            "fix the findings from the review report"
        )

        assert "Repository Review" not in _task_types(result)

    def test_repo_review_retained_when_explicit_scope(
        self, engine: RoutingEngine,
    ) -> None:
        """'repository review and fix findings' keeps repo review because
        explicit repo-scope terms are present."""
        result = engine.select_for_request(
            "repository review and fix findings"
        )

        task_types = _task_types(result)
        assert "Repository Review" in task_types

    def test_adversarial_repo_review_suppresses_plain_repo_review(
        self, engine: RoutingEngine,
    ) -> None:
        """When both adversarial and plain repo review match,
        the adversarial variant wins."""
        result = engine.select_for_request(
            "adversarial repository review"
        )

        task_types = _task_types(result)
        assert "Adversarial Repository Review" in task_types
        assert "Repository Review" not in task_types

    def test_overlay_capable_suppresses_adversarial_repo_review(
        self, engine: RoutingEngine,
    ) -> None:
        """When a compatible route (e.g., code review) co-matches with
        adversarial repo review and no repo-scope terms, the repo audit
        is suppressed in favor of the overlay."""
        result = engine.select_for_request(
            "adversarial code review"
        )

        assert "route.code_review" in _route_ids(result)
        assert "Adversarial Repository Review" not in _task_types(result)


# ===================================================================
# SECTION 5 — Commit closeout companion intent
# ===================================================================


class TestCommitCloseoutCompanionIntent:
    """Commit closeout should attach as a companion, not displace
    the dominant substantive route."""

    def test_implement_and_commit_keeps_implementation_route(
        self, engine: RoutingEngine,
    ) -> None:
        """'implement feature and commit' should keep code implementation
        as the dominant route with commit closeout as companion."""
        result = engine.select_for_request(
            "implement the new feature and commit changes"
        )

        task_types = _task_types(result)
        assert "Code Implementation" in task_types
        assert "Commit Closeout" in task_types
        assert "route.overlay_commit_closeout_intent" in _intent_ids(result)

    def test_code_review_and_commit_keeps_review_dominant(
        self, engine: RoutingEngine,
    ) -> None:
        """'review code and create commit' should pair review + closeout."""
        result = engine.select_for_request(
            "review code and create commit"
        )

        task_types = _task_types(result)
        assert "Code Review" in task_types
        assert "Commit Closeout" in task_types

    def test_standalone_commit_routes_to_closeout(
        self, engine: RoutingEngine,
    ) -> None:
        """'git commit' alone should route to commit closeout."""
        result = engine.select_for_request("git commit")

        assert "route.commit_closeout" in _route_ids(result)

    def test_fix_bug_and_commit_pairs_implementation_with_closeout(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("fix bug and commit")

        task_types = _task_types(result)
        assert "Code Implementation" in task_types
        assert "Commit Closeout" in task_types


# ===================================================================
# SECTION 6 — Review remediation intent scenarios
# ===================================================================


class TestReviewRemediationIntents:
    """Single-pass and loop remediation intents compose correctly
    with review routes."""

    def test_review_and_fix_activates_remediation_intent(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("review code and fix findings")

        task_types = _task_types(result)
        assert "Code Review" in task_types
        assert "Review Remediation" in task_types
        assert "route.overlay_review_remediation_intent" in _intent_ids(result)

    def test_audit_and_remediate_activates_remediation_intent(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("audit code and remediate findings")

        assert "Review Remediation" in _task_types(result)

    def test_iterate_review_and_fix_activates_loop(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("iterate review and fix")

        assert "Review Remediation Loop" in _task_types(result)
        assert "route.overlay_review_remediation_loop_intent" in _intent_ids(result)

    def test_keep_fixing_until_clean_activates_loop(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("keep fixing until clean")

        assert "Review Remediation Loop" in _task_types(result)

    def test_loop_intent_suppresses_single_pass_intent(
        self, engine: RoutingEngine,
    ) -> None:
        """When the loop overlay triggers, it should suppress the
        single-pass remediation overlay via suppresses_intent_ids."""
        result = engine.select_for_request(
            "review and fix loop until clean"
        )

        intent_ids = _intent_ids(result)
        assert "route.overlay_review_remediation_loop_intent" in intent_ids
        # Single-pass intent should be suppressed by loop
        assert "route.overlay_review_remediation_intent" not in intent_ids


# ===================================================================
# SECTION 7 — Full route coverage: every task type by explicit name
# ===================================================================


class TestExplicitTaskTypeSelection:
    """Every task type in the route index must be selectable by name."""

    @pytest.mark.parametrize(
        "task_type, expected_route_id",
        [
            ("Code Implementation", "route.code_implementation"),
            ("Test Suite Optimization", "route.test_suite_optimization"),
            ("Performance Benchmarking", "route.performance_benchmarking"),
            ("Domain Pack Integration", "route.domain_pack_integration"),
            ("Shared Core Refresh", "route.shared_core_refresh"),
            ("Code Review", "route.code_review"),
            ("Review Remediation", "route.review_remediation"),
            ("Review Remediation Loop", "route.review_remediation_loop"),
            ("Code Validation", "route.code_validation"),
            ("Branch Hygiene Review", "route.branch_hygiene_review"),
            ("Clarification", "route.clarification"),
            ("Commit Closeout", "route.commit_closeout"),
            (
                "Documentation-Implementation Reconciliation",
                "route.documentation_implementation_reconciliation",
            ),
            ("Documentation Generation", "route.documentation_generation"),
            ("Documentation Review", "route.documentation_review"),
            ("Workflow System Review", "route.workflow_system_review"),
            ("Documentation Refresh", "route.documentation_refresh"),
            ("Foundations Alignment Review", "route.foundations_alignment_review"),
            (
                "Governed Artifact Reconciliation",
                "route.governed_artifact_reconciliation",
            ),
            ("Pack Interface Validation", "route.pack_interface_validation"),
            ("Reference Distillation", "route.reference_distillation"),
            (
                "Adversarial Repository Review",
                "route.adversarial_repository_review",
            ),
            ("Standards Alignment Review", "route.standards_alignment_review"),
            ("Validation Harness Review", "route.validation_harness_review"),
            ("Repository Review", "route.repository_review"),
        ],
        ids=lambda v: v.replace(" ", "_").replace("-", "_").lower()
        if " " in v
        else v,
    )
    def test_explicit_task_type_resolves(
        self, engine: RoutingEngine, task_type: str, expected_route_id: str
    ) -> None:
        result = engine.select_for_task_type(task_type)

        assert len(result.selected_routes) == 1
        assert result.selected_routes[0].route_id == expected_route_id
        assert result.selected_workflows  # must load at least one workflow


# ===================================================================
# SECTION 8 — Keyword-driven route coverage by request text
# ===================================================================


class TestKeywordDrivenRouteSelection:
    """Each route should be reachable via its trigger keywords."""

    @pytest.mark.parametrize(
        "request_text, expected_route_id",
        [
            ("implement the new parser", "route.code_implementation"),
            ("build feature for auth", "route.code_implementation"),
            ("fix bug in router", "route.code_implementation"),
            ("refactor and optimize the query layer", "route.code_implementation"),
            ("slow tests need cleanup", "route.test_suite_optimization"),
            ("optimize tests for CI", "route.test_suite_optimization"),
            ("benchmark the request handler", "route.performance_benchmarking"),
            ("performance baseline measurement", "route.performance_benchmarking"),
            ("pack integration for analytics", "route.domain_pack_integration"),
            ("sync core from donor repo", "route.shared_core_refresh"),
            ("review code and audit diff", "route.code_review"),
            ("PR review the latest changes", "route.code_review"),
            ("validate the build", "route.code_validation"),
            ("run lint and typecheck", "route.code_validation"),
            ("branch hygiene cleanup", "route.branch_hygiene_review"),
            ("stale branches review", "route.branch_hygiene_review"),
            ("clarify the ambiguous request", "route.clarification"),
            ("commit closeout", "route.commit_closeout"),
            ("reconcile docs with code", "route.documentation_implementation_reconciliation"),
            ("write doc for the new API", "route.documentation_generation"),
            ("documentation review pass", "route.documentation_review"),
            ("workflow system audit", "route.workflow_system_review"),
            ("route index review", "route.workflow_system_review"),
            ("refresh docs for latest changes", "route.documentation_refresh"),
            ("update docs to reflect new behavior", "route.documentation_refresh"),
            ("foundations alignment review", "route.foundations_alignment_review"),
            ("schema drift reconciliation", "route.governed_artifact_reconciliation"),
            ("registry drift check", "route.governed_artifact_reconciliation"),
            ("validate pack interface contract", "route.pack_interface_validation"),
            ("distill reference from external standard", "route.reference_distillation"),
            ("standards adherence audit", "route.standards_alignment_review"),
            ("enforcement gaps review", "route.standards_alignment_review"),
            ("validation harness hardening", "route.validation_harness_review"),
            ("test coverage audit", "route.validation_harness_review"),
            ("repository review full audit", "route.repository_review"),
            ("health check assessment", "route.repository_review"),
        ],
        ids=lambda v: v.replace(" ", "_")[:50] if " " in v else v,
    )
    def test_keyword_request_resolves(
        self, engine: RoutingEngine, request_text: str, expected_route_id: str
    ) -> None:
        result = engine.select_for_request(request_text)

        assert result.selected_routes, f"No routes matched for: {request_text!r}"
        assert expected_route_id in _route_ids(result), (
            f"Expected {expected_route_id} for {request_text!r}, "
            f"got {_route_ids(result)}"
        )


# ===================================================================
# SECTION 9 — Dedicated adversarial repository review
# ===================================================================


class TestAdversarialRepositoryReview:
    """The dedicated adversarial repository review route should activate
    only when explicit repo-scope terms are present."""

    def test_adversarial_repository_review_explicit(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("adversarial repository review")

        assert "route.adversarial_repository_review" in _route_ids(result)
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_full_spectrum_audit_standalone(
        self, engine: RoutingEngine,
    ) -> None:
        """'full-spectrum audit' alone should route to adversarial repo review."""
        result = engine.select_for_request("full-spectrum audit")

        assert result.selected_routes
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_contradiction_oriented_audit(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("contradiction-oriented audit")

        assert result.selected_routes
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)


# ===================================================================
# SECTION 10 — Edge cases and boundaries
# ===================================================================


class TestEdgeCasesAndBoundaries:
    """Boundary conditions, no-match fallbacks, and degenerate inputs."""

    def test_empty_request_returns_no_routes(
        self, engine: RoutingEngine,
    ) -> None:
        """Empty string should return no routes (no crash)."""
        result = engine.select_for_request("   ")

        assert result.selected_routes == ()

    def test_gibberish_returns_no_routes(
        self, engine: RoutingEngine,
    ) -> None:
        """Nonsense input should fall through to no match or assisted suggestions."""
        result = engine.select_for_request("xyzzy plugh foobarbaz")

        assert result.selected_routes == ()

    def test_both_request_and_task_type_raises(
        self, engine: RoutingEngine,
    ) -> None:
        with pytest.raises(ValueError, match="exactly one"):
            engine.select(request_text="review code", task_type="Code Review")

    def test_neither_request_nor_task_type_raises(
        self, engine: RoutingEngine,
    ) -> None:
        with pytest.raises(ValueError, match="exactly one"):
            engine.select()

    def test_case_insensitive_matching(
        self, engine: RoutingEngine,
    ) -> None:
        """Request text matching should be case-insensitive."""
        result = engine.select_for_request("CODE REVIEW AND AUDIT DIFF")

        assert "route.code_review" in _route_ids(result)

    def test_unknown_task_type_raises_value_error(
        self, engine: RoutingEngine,
    ) -> None:
        """An unrecognized explicit task type should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown task type"):
            engine.select_for_task_type("Nonexistent Task Type")

    def test_assisted_suggestions_for_vague_request(
        self, engine: RoutingEngine,
    ) -> None:
        """A vague request that partially matches workflow vocabulary
        should produce assisted suggestions, not routes."""
        result = engine.select_for_request("improve the workflow stuff")

        assert result.selected_routes == ()
        assert result.assisted_module_suggestions

    def test_multiple_overlays_can_coactivate(
        self, engine: RoutingEngine,
    ) -> None:
        """Adversarial lens + commit closeout can both activate."""
        result = engine.select_for_request(
            "adversarial code review and commit"
        )

        intent_ids = _intent_ids(result)
        assert "route.overlay_adversarial_lens" in intent_ids
        assert "route.overlay_commit_closeout_intent" in intent_ids

    def test_adversarial_plus_loop_plus_commit_triple_composition(
        self, engine: RoutingEngine,
    ) -> None:
        """Three overlays/intents can compose: adversarial lens +
        remediation loop + commit closeout."""
        result = engine.select_for_request(
            "adversarial code review fix loop and commit changes"
        )

        intent_ids = _intent_ids(result)
        assert "route.overlay_adversarial_lens" in intent_ids
        assert "route.overlay_review_remediation_loop_intent" in intent_ids
        assert "route.overlay_commit_closeout_intent" in intent_ids


# ===================================================================
# SECTION 11 — Workflow composition verification
# ===================================================================


class TestWorkflowCompositionVerification:
    """Verify that selected routes load the correct workflow modules."""

    def test_code_implementation_loads_full_pipeline(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Code Implementation")

        wids = _workflow_ids(result)
        assert "workflow.core" in wids
        assert "workflow.task_scope_definition" in wids
        assert "workflow.code_implementation" in wids
        assert "workflow.code_validation" in wids
        assert "workflow.task_handoff_review" in wids

    def test_review_remediation_loop_loads_both_remediation_modules(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Review Remediation Loop")

        wids = _workflow_ids(result)
        assert "workflow.review_remediation" in wids
        assert "workflow.review_remediation_loop" in wids
        assert "workflow.code_validation" in wids

    def test_adversarial_repo_review_loads_reviewer_role(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Adversarial Repository Review")

        wids = _workflow_ids(result)
        assert "workflow.adversarial_reviewer" in wids
        assert "workflow.repository_review" in wids
        assert "workflow.repository_assessment" in wids

    def test_workflow_system_review_loads_steward_role(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Workflow System Review")

        wids = _workflow_ids(result)
        assert "workflow.workflow_steward" in wids
        assert "workflow.workflow_system_review" in wids

    def test_repo_review_loads_inventory_and_assessment(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Repository Review")

        wids = _workflow_ids(result)
        assert "workflow.repository_inventory_review" in wids
        assert "workflow.repository_assessment" in wids
        assert "workflow.repository_review" in wids

    def test_domain_pack_integration_loads_reconciliation(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Domain Pack Integration")

        wids = _workflow_ids(result)
        assert "workflow.domain_pack_integration" in wids
        assert "workflow.governed_artifact_reconciliation" in wids
        assert "workflow.documentation_refresh" in wids

    def test_shared_core_refresh_loads_reconciliation(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_task_type("Shared Core Refresh")

        wids = _workflow_ids(result)
        assert "workflow.shared_core_refresh" in wids
        assert "workflow.governed_artifact_reconciliation" in wids
        assert "workflow.documentation_refresh" in wids


# ===================================================================
# SECTION 12 — Composite real-world phrasing
# ===================================================================


class TestCompositeRealWorldPhrasing:
    """Natural-language requests that combine multiple concerns,
    verifying the routing engine handles realistic phrasing."""

    def test_refactor_the_auth_module(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("refactor the auth module")

        assert "route.code_implementation" in _route_ids(result)

    def test_review_report_changes_and_remediate(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request(
            "review report changes and remediate findings"
        )

        task_types = _task_types(result)
        assert "Code Review" in task_types
        assert "Review Remediation" in task_types

    def test_fix_pasted_findings_from_review(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("fix pasted findings")

        assert "route.review_remediation" in _route_ids(result)

    def test_stale_test_cleanup(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("stale test cleanup")

        assert "route.test_suite_optimization" in _route_ids(result)

    def test_watchtower_report(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("watchtower report")

        assert "route.repository_review" in _route_ids(result)

    def test_project_coherence_review(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("project coherence review")

        assert "route.repository_review" in _route_ids(result)

    def test_validate_pack_manifest(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("validate pack manifest")

        assert "route.pack_interface_validation" in _route_ids(result)

    def test_reference_distillation_from_source(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("distill standard into local guidance")

        assert "route.reference_distillation" in _route_ids(result)

    def test_align_docs_with_foundations(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request("align docs with foundations")

        assert "route.foundations_alignment_review" in _route_ids(result)

    def test_reconcile_schema_backed_artifacts(
        self, engine: RoutingEngine,
    ) -> None:
        result = engine.select_for_request(
            "reconcile schema backed indexes examples and validators"
        )

        assert "route.governed_artifact_reconciliation" in _route_ids(result)

    def test_adversarial_validation_harness_review_and_fix_loop(
        self, engine: RoutingEngine,
    ) -> None:
        """Full composition: adversarial + validation harness + fix loop."""
        result = engine.select_for_request(
            "adversarial validation harness review fix loop"
        )

        task_types = _task_types(result)
        assert "Validation Harness Review" in task_types
        assert "Review Remediation Loop" in task_types
        assert "workflow.adversarial_reviewer" in _workflow_ids(result)

    def test_documentation_review_and_fix_loop_with_commit(
        self, engine: RoutingEngine,
    ) -> None:
        """Doc review + fix loop + commit — three intents compose."""
        result = engine.select_for_request(
            "documentation review fix loop and commit"
        )

        task_types = _task_types(result)
        assert "Documentation Review" in task_types
        assert "Review Remediation Loop" in task_types
        assert "Commit Closeout" in task_types
