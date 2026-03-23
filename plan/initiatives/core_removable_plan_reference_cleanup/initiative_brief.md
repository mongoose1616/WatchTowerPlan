# Core Removable Plan Reference Cleanup

## Summary
Removes non-essential plan-specific wording and examples from shared core docs, host help, and reusable-core boundaries while preserving only references required by the current repository contract.

## Identity
- `initiative_id`: `initiative.core_removable_plan_reference_cleanup`
- `trace_id`: `trace.core_removable_plan_reference_cleanup`
- `scope_type`: `pack_wide`

## Initial Task Set
- `task.core_removable_plan_reference_cleanup.bootstrap_core_removable_plan_reference_cleanup`: Bootstrap Core Removable Plan Reference Cleanup live initiative package.

## Problem
Shared core still contains a large amount of plan-flavored wording in documentation, host CLI examples, reusable-core README surfaces, and boundary-guard messaging. Much of that residue is no longer required now that core, host, and packs have explicit boundaries and first-party root-pack support. It makes copied-core adoption harder and keeps shared guidance biased toward the donor repository.

## Desired Outcome
- Shared core documentation and help text describe pack ownership generically.
- Reusable-core boundary messaging points callers to the owning `watchtower_<pack>` package rather than to `watchtower_plan` specifically.
- Current-repository facts remain only where they are materially required: live pack registry data, current plan-owned command/index surfaces, generated indexes that mirror the live repository, and tests that intentionally prove the current internal pack contract.

## In Scope
- Shared docs under `core/docs/**` that use plan-specific wording where generic pack language is sufficient.
- Shared host help text and examples under `core/python/src/watchtower_host/**`.
- Reusable-core README and boundary-guard wording under `core/python/src/watchtower_core/**`.
- Shared tests under `core/python/tests/**` only when they need to change to match donor-neutral wording or to stop asserting plan-specific examples.
- Companion governed indexes regenerated from the changed authored surfaces.

## Out Of Scope
- Removing current live repository facts from generated machine authority when those facts are true in this repository.
- Removing the live `pack.plan` entry from `core/control_plane/registries/pack_registry.json`.
- Rehoming plan-owned schemas, commands, or runtime implementation out of their current boundaries.
- Renaming the current internal plan pack or changing CLI namespace ownership.

## Operator Requirements
- Shared help examples must not imply that `plan` is the only valid hosted-pack namespace.
- Shared documentation must remain correct if `core/` is copied into another repository with a different hosted pack.
- Current repository operator guidance may still mention the live plan pack only when the point is a concrete current-repo fact rather than a reusable rule.

## Acceptance Criteria
- Removable plan-specific wording is gone from shared core docs, host help, and reusable-core boundary messaging.
- Any remaining `plan` references in `core/**` are limited to current-repo machine authority, current-repo generated indexes, or tests that intentionally prove the current internal pack contract.
- Validation and affected tests pass after the cleanup.

## Non-Goals
- Achieving zero textual `plan` references anywhere under `core/**` regardless of correctness.
- Converting every current plan-oriented integration test into a generic synthetic-pack test in this slice.
