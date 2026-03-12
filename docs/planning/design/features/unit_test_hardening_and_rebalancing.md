---
trace_id: trace.unit_test_hardening_and_rebalancing
id: design.features.unit_test_hardening_and_rebalancing
title: Unit Test Hardening and Rebalancing Feature Design
summary: Defines the technical design boundary for Unit Test Hardening and Rebalancing.
type: feature_design
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T02:46:38Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/planning/
aliases:
- unit_test_review_followup
- test_suite_hardening
---

# Unit Test Hardening and Rebalancing Feature Design

## Record Metadata
- `Trace ID`: `trace.unit_test_hardening_and_rebalancing`
- `Design ID`: `design.features.unit_test_hardening_and_rebalancing`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.unit_test_hardening_and_rebalancing`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.unit_test_hardening_and_rebalancing`
- `Updated At`: `2026-03-12T02:46:38Z`

## Summary
Defines the technical design boundary for strengthening low-coverage executable test surfaces, rebalancing the unit suite structure, and tightening suite-local testing guidance.

## Source Request
- Verify and operationalize the still-valid issues in the user-supplied unit-test review.

## Scope and Feature Boundary
- Covers direct unit coverage for under-tested executable surfaces in `watchtower_core`, especially GitHub integration, GitHub task sync, closeout handlers, and planning or task lifecycle handlers.
- Covers test-structure improvements under `core/python/tests/`, including shared fixture support and family-oriented CLI test modules.
- Covers updated unit-test documentation and local contributor guidance for the rebalanced suite.
- Does not redesign the repository’s broader testing philosophy outside `core/python/tests/`.
- Does not introduce live-network integration tests or external CI platform dependencies.

## Current-State Context
- The verified unit-suite review remains directionally accurate after rechecking current state: `176` unit tests pass, overall coverage remains `75%`, GitHub integration remains critically under-covered, and `test_cli.py` still carries most CLI smoke coverage.
- New workflow-operationalization code introduced additional low-coverage handler and lifecycle surfaces such as `plan_handlers.py`, `task_handlers.py`, and `planning_scaffolds.py`, so the follow-up must cover both legacy and newly added command families.
- Many tests still bind directly to the canonical repository root or inline temp-repo builders, and there is still no shared `conftest.py`.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): coverage work should improve confidence by testing the narrowest meaningful executable boundary instead of piling more broad smoke tests into one place.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable planning and machine-readable tracking surfaces need to stay aligned while the unit-suite structure changes.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): the test foundation should be reliable and maintainable before WatchTower product implementation starts consuming the exported core.

## Internal Standards and Canonical References Applied
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): feature designs should explain the concrete repository standards and references that shape the design, not only the desired outcome.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the changes stay inside the canonical Python workspace and its governed command and validation flow.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the suite should move toward smaller focused tests, deterministic fixtures, and same-change documentation or tracker updates.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the initiative keeps its planning, task, and acceptance surfaces synchronized while execution slices land.

## Design Goals and Constraints
- Move expensive behavior checks down to the handler or service layer whenever broad parser smoke tests are not the best assertion point.
- Preserve realistic repository-governed behavior by continuing to use authored fixtures where they add confidence, but centralize their construction and reuse.
- Keep all new GitHub tests fully local and deterministic through mocks or fake clients; no live network use is allowed.
- Avoid introducing a second incompatible testing pattern while refactoring the current CLI suite.

## Options Considered
### Option 1
- Add a few more smoke tests to the existing unit suite without restructuring it.
- Strength: minimal file movement.
- Tradeoff: leaves the oversized CLI file, fixture duplication, and handler-level blind spots in place.

### Option 2
- Split the work into direct handler or service tests, focused CLI-family smoke tests, and a small shared fixture support layer.
- Strength: improves coverage quality, maintenance cost, and failure localization in the same change set.
- Tradeoff: requires coordinated file moves and more deliberate test layering.

### Option 3
- Reclassify large parts of the current unit suite as integration tests without adding the missing executable coverage.
- Strength: makes naming more honest quickly.
- Tradeoff: does not solve the real confidence gaps in the most mutation-heavy code paths.

## Recommended Design
### Architecture
- Keep three complementary layers inside `core/python/tests`:
  1. focused service tests for branch-heavy behavior such as GitHub sync and initiative closeout
  2. direct handler tests for CLI payload and human-output branches
  3. a smaller top-level CLI smoke layer for parser and command-registration coverage
- Add shared test support through `tests/conftest.py` and helper modules for temporary repo subsets, JSON loading, and output capture patterns.
- Split monolithic CLI tests into family-oriented files so each file maps to one command area and can use only the helpers it needs.

### Data and Interface Impacts
- Affected Python surfaces include `integrations/github`, `repo_ops/sync/github_tasks.py`, `closeout/initiative.py`, handler modules under `cli/`, and lifecycle services under `repo_ops/`.
- Affected test surfaces include `tests/unit/README.md`, new shared helpers, and new CLI-family test modules.
- No schema or control-plane artifact family changes are required beyond the planning trace artifacts for this initiative.

### Execution Flow
1. Add shared fixture helpers and split the CLI suite into family-oriented test modules while preserving command-surface coverage.
2. Add direct handler and service tests for the most under-covered executable surfaces, starting with GitHub client and sync plus closeout and lifecycle handlers.
3. Expand aggregate failure-path coverage for sync, validate, and coordination or initiative derivation, then update suite-local docs to match the new structure.

### Invariants and Failure Cases
- The unit suite must stay deterministic and must not make live network calls.
- Shared helpers must not hide authoritative repository behavior behind unrealistic fixtures.
- Handler tests must cover both JSON and human-output branches where the handler owns output behavior.
- Failure-path tests must assert meaningful error conditions rather than only non-zero exit codes.

## Affected Surfaces
- core/python/tests/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/planning/

## Design Guardrails
- Do not expand `test_cli.py` further; new family-specific CLI coverage belongs in smaller focused files.
- Do not solve low coverage by only adding more `main()`-level smoke tests when a direct handler or service test is cheaper and more precise.
- Do not add live GitHub credentials, network calls, or environment-coupled flake sources to the suite.

## Risks
- Test moves can temporarily reduce confidence if command-family smoke coverage is deleted before direct handler coverage is in place.
- Helper extraction can over-abstract the suite if it hides important authored fixture details instead of centralizing only repeated mechanics.

## References
- User-supplied WatchTower unit-test review dated `2026-03-10`

## Updated At
- `2026-03-12T02:46:38Z`
