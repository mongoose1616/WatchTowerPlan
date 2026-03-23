# Core Governance Reference Deplanification Followup Decision Notes

## Summary
This document captures the decisions that keep shared core exportable without falsifying current `WatchTowerPlan` repository facts.

## Locked Decisions
- Shared governance, workflow, metadata, and data-contract docs under `core/**` must default to pack-neutral wording and canonical repo-relative path patterns when the rule applies to hosted packs generally.
- A `plan/**` reference may remain in shared core only when it is a true current-repository fact, a required mirror contract, or a deliberately labeled live-pack example that materially improves operator clarity.
- Shared core should prefer phrases such as `the active hosted pack`, `<pack>/docs/...`, `*/docs/...`, and `*/tracking/...` over directing users to `plan/**` for generic behavior.
- This slice is documentation-first. It should not reopen runtime or loader behavior unless a touched doc is proven false by current code.
- Validation must include the normal shared doc gates and a broad repository validation pass so doc/index reconciliation stays intact.

## Deferred Decisions
- Whether current-repository foundations should eventually be split into a separately exportable corpus distinct from donor-repo facts.
- Whether a future scaffold or bootstrap tranche should auto-generate more generic governance surfaces for newly created packs.
