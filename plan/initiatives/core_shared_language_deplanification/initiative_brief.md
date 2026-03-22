# Core Shared Language Deplanification

## Summary
Removes WatchTowerPlan and plan-flavored wording from shared core standards, registries, and reusable-core READMEs so core authority stays pack-neutral.

## Identity
- `initiative_id`: `initiative.core_shared_language_deplanification`
- `trace_id`: `trace.core_shared_language_deplanification`
- `scope_type`: `pack_wide`

## Problem Statement
Several shared-core standards, registries, and reusable-core package READMEs still describe core behavior by contrast to `WatchTowerPlan` or `watchtower_plan`. Those references are partly factual because this repository currently carries an internal plan pack, but the current wording lets pack-specific language leak into reusable-core policy. That makes `watchtower_plan` read like the default shape for future packs instead of one current pack consumer.

## Goals
- Keep shared-core standards and reusable-core package docs pack-neutral in policy language.
- Retain current repository facts such as concrete path examples or mirrored documentation roots where those facts are required for operator clarity.
- Remove wording that implies core exists mainly to support `WatchTowerPlan` rather than hosted packs and reusable boundaries in general.

## In Scope
- Shared contributor guidance in `core/python/README.md`.
- Reusable-core package READMEs under `core/python/src/watchtower_core/` where the wording defines boundary policy.
- Shared engineering standards that currently over-index on the plan pack as the defining contrast for core.
- Shared registries whose notes frame mirrored or pack-owned surfaces as if they are inherently plan-specific.

## Out Of Scope
- Pack-owned docs under `plan/**` except for the machine-managed initiative package required to track this work.
- Real current-repo facts such as the existing `watchtower_plan` package name, required mirror roots, or current pack registry entries when they are serving as concrete examples rather than policy.
- Python runtime behavior, manifests, loaders, or command routing.

## Success Criteria
- Shared standards define pack-owned boundaries generically and treat `watchtower_plan` only as the current internal pack example when needed.
- Reusable-core package READMEs stop using `WatchTowerPlan` as the normative contrast for core boundaries.
- Shared registries keep current repository roots and mirrors accurate while using pack-neutral framing in summaries and notes.
- The affected docs and registries validate cleanly and any required derived indexes are refreshed in the same change set.

## Initial Task Set
- `task.core_shared_language_deplanification.bootstrap_core_shared_language_deplanification`: Bootstrap Core Shared Language Deplanification live initiative package.
