# Core Pack Neutrality Followup

## Summary
Removes remaining donor-style plan assumptions from shared core tests, fixtures, and core-owned standards while keeping legitimate current-repo pack facts scoped to plan-owned boundaries.

## Identity
- `initiative_id`: `initiative.core_pack_neutrality_followup`
- `trace_id`: `trace.core_pack_neutrality_followup`
- `scope_type`: `pack_wide`

## Problem
Shared reusable-core still carries a small but important tail of `plan`-shaped assumptions in three places:
- shared-core Python fixture support still uses a donor-style plan fixture template and replacement map
- a few tests under `core/python/tests/**` still rely on live `plan/**` rendered surfaces or initiative artifacts instead of pack-neutral fixtures or plan-owned test placement
- several core-owned references and standards still operationalize through `plan/**` paths when the intent is generic hosted-pack behavior rather than current-repository fact

Those assumptions no longer break the `WatchTowerPlan` repo itself, but they remain copy-forward portability debt and they are still the exact class of drift highlighted by the `WatchTowerOversight` core-swap assessment.

## Desired Outcome
- shared-core fixture and test support becomes pack-neutral by default
- tests that require a live `plan/**` workspace run under `plan/python/tests/**`, not `core/python/tests/**`
- core-owned standards and references describe generic pack-owned workflow or command surfaces using canonical repo-relative patterns or neutral prose instead of donor `plan/**` paths
- current-repository facts that are truly about the live `plan` pack stay scoped to plan-owned docs or to the few shared foundations that intentionally describe this repository as it exists today

## In Scope
- `core/python/tests/**` fixture and boundary support
- relocation of any remaining live-plan-only tests into `plan/python/tests/**`
- `core/docs/references/**` and `core/docs/standards/**` entries where `plan/**` is used as accidental shared-core operationalization rather than necessary current-repo fact
- companion boundary docs that explain how future developers and agents should preserve the split

## Out Of Scope
- changing the live `plan` runtime, commands, or pack-owned docs for non-boundary reasons
- removing current-repo `plan` facts from authored shared foundations when those facts are intentionally descriptive of this repository
- changing `WatchTowerOversight/**` directly in this initiative
- registry, workspace, or bootstrap mutations for a second hosted pack in this repository

## Operator Requirements
- `core/python/tests/**` must remain runnable without a hidden dependency on live `watchtower_plan` imports or live `plan/**` rendered surfaces
- copied-core consumers must not inherit parser-visible `plan/**` path metadata from shared references or standards when the intended contract is generic pack ownership
- future contributors must have explicit guidance on when a test belongs under `core/python/tests/**` versus `plan/python/tests/**`

## Acceptance Criteria
- no shared-core unit or integration test requires the live `plan/**` workspace when the behavior under test is reusable-core only
- synthetic hosted-pack fixture support no longer uses `pack.plan`, `suite.plan.*`, or `watchtower_plan.integration` as its template contract
- core-owned references and standards touched by this slice validate with canonical repo-relative paths and use pack-neutral operationalization where intended
- `ruff`, `mypy`, targeted pytest, and `watchtower-core validate all --skip-acceptance --format json` pass after the cleanup

## Non-Goals
- proving that zero `plan` strings remain anywhere under `core/**`
- rewriting shared foundations that intentionally describe the live `WatchTowerPlan` repository
- introducing a second generic pack test framework beyond what is needed for this cleanup slice

## Task Set
- `task.core_pack_neutrality_followup.bootstrap_core_pack_neutrality_followup`: Bootstrap, confirm, approve, and close the initiative package.
- `task.core_pack_neutrality_followup.neutralize_shared_fixture_templates`: Replace donor-style shared fixture-pack templates and helper assumptions with pack-neutral template data.
- `task.core_pack_neutrality_followup.split_live_plan_only_tests_from_core`: Move or rewrite remaining live-plan-only tests so shared-core tests do not depend on the live `plan/**` workspace.
- `task.core_pack_neutrality_followup.generalize_core_owned_guidance`: Remove donor-style `plan/**` operationalization and applies-to metadata from shared references and standards where the contract is generic pack behavior.
- `task.core_pack_neutrality_followup.validate_and_closeout`: Run targeted and broad validation, refresh any derived surfaces required by the touched docs, then close and commit the initiative.
