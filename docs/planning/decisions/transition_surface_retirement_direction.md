---
trace_id: trace.transition_surface_retirement
id: decision.transition_surface_retirement_direction
title: Transition Surface Retirement Direction Decision
summary: Records the initial direction decision for Transition Surface Retirement.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T19:23:51Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/
- core/python/tests/
- docs/planning/
- docs/standards/
---

# Transition Surface Retirement Direction Decision

## Record Metadata
- `Trace ID`: `trace.transition_surface_retirement`
- `Decision ID`: `decision.transition_surface_retirement_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.transition_surface_retirement`
- `Linked Designs`: `design.features.transition_surface_retirement`
- `Linked Implementation Plans`: `design.implementation.transition_surface_retirement`
- `Updated At`: `2026-03-16T19:23:51Z`

## Summary
Records the initial direction decision for Transition Surface Retirement.

## Decision Statement
Hard-retire the remaining transition facades, bridge modules, marker tests, stale discovery references, and temporary audit helpers now, and close the initiative only after the repo no longer publishes those paths anywhere in the current live surface set.

## Trigger or Source Request
- A repository-wide cleanup request asked for identification and removal of leftover issue-driven transition surfaces, with strict closeout expectations and no retained compatibility layers or historical band-aids.

## Current Context and Constraints
- The direct owners and focused replacement test suites already exist, so the remaining transition files no longer provide unique functionality.
- The product is unreleased, so preserving retired local import or test paths has no release-compatibility value.
- Current planning, acceptance, and repository-path discovery surfaces must stay aligned with the cleaned source set in the same initiative.

## Applied References and Implications
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): temporary shims should disappear once the explicit owner is stable and validated.
- [rewrite_surface_classification_standard.md](/docs/standards/governance/rewrite_surface_classification_standard.md): transition surfaces are temporary and should not remain once their replacement is proven.
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md): runtime, tests, and docs must be updated together inside the canonical workspace.

## Affected Surfaces
- core/python/src/
- core/python/tests/
- docs/planning/
- docs/standards/

## Options Considered
### Option 1
- Leave the transition files in place and rely on direct-owner docs to steer new work away from them.
- Lowest immediate churn.
- Keeps dead paths importable or discoverable and lets stale references persist.

### Option 2
- Keep temporary migration helpers and marker files until later product implementation begins.
- Preserves short-term convenience for ad hoc local callers.
- Extends rewrite debt into the implementation phase even though the replacement surfaces are already proven.

### Option 3
- Hard-cut the leftover surfaces now, rewrite current discovery outputs to live paths, and validate the final state before closeout.
- Produces the smallest and most reusable current repository surface.
- Requires coordinated source cleanup and full-repo validation in one initiative.

## Chosen Outcome
Accept option 3. The initiative will remove the remaining transition files, rename stale boundary-proof artifacts, rewrite current live discovery references, and close only after full validation and a scoped retired-path audit are clean.

## Rationale and Tradeoffs
- The repo already proved the replacement runtime owners and focused suites, so keeping alternate paths only preserves noise.
- A hard cut is safer than another temporary compatibility layer because the product is unreleased and current validation coverage is broad.
- The tradeoff is that hidden stale references will surface immediately, but that is desirable before implementation work expands the codebase again.

## Consequences and Follow-Up Impacts
- Retired import paths and hotspot filenames intentionally stop resolving.
- Current planning, acceptance, evidence, tracker, and repository-path surfaces must be regenerated from the cleaned sources.
- Any temporary audit helper introduced during the cleanup must be removed before the trace closes.

## Risks, Dependencies, and Assumptions
- Assumes the focused replacement suites still provide the necessary coverage after the marker files disappear.
- Depends on full sync and validation to catch stale references outside the immediate edited files.
- Risks a noisy follow-up pass if current planning artifacts still contain dead path references after the first cleanup sweep.

## References
- [transition_surface_retirement.md](/docs/planning/prds/transition_surface_retirement.md)
- [transition_surface_retirement.md](/docs/planning/design/features/transition_surface_retirement.md)
- [transition_surface_retirement.md](/docs/planning/design/implementation/transition_surface_retirement.md)
