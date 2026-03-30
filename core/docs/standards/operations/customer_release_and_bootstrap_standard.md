---
id: "std.operations.customer_release_and_bootstrap"
title: "Customer Release and Bootstrap Standard"
summary: "This standard defines the shared release and bootstrap checklist for customer-safe repository bundles and pack bundles."
type: "standard"
status: "active"
tags:
  - "standard"
  - "operations"
  - "release"
  - "bootstrap"
  - "portability"
owner: "repository_maintainer"
updated_at: "2026-03-29T04:10:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/"
  - "core/docs/"
  - "core/python/"
  - "pack_owned_docs"
  - "pack_owned_python"
aliases:
  - "customer release checklist"
  - "bootstrap checklist"
  - "portable export checklist"
---

# Customer Release and Bootstrap Standard

## Summary
This standard defines the shared release and bootstrap checklist for customer-safe repository bundles and pack bundles.

## Purpose
- Give humans and agents one canonical handoff sequence instead of spreading the release contract across several command pages.
- Keep customer release, customer bootstrap, and additive pack handoff aligned with the portability contract.
- Prevent raw donor worktrees, stale runtime residue, or partial validation passes from being mistaken for shippable artifacts.

## Scope
- Applies to core-only bootstrap bundles, core-plus-selected-pack bundles, and pack-only additive bundles.
- Covers the bounded validation, export, and post-export verification sequence for customer or downstream-repository handoff.
- Does not replace pack-specific onboarding after a pack-only bundle is copied into a compatible core repository.

## Use When
- Preparing a customer-ready handoff.
- Preparing a donor-neutral bootstrap bundle for another repository.
- Reviewing whether a release claim followed the current export and validation contract.

## Related Standards and Sources
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md): defines what a portable handoff may and may not contain.
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md): defines the broad validation baseline that should run before export.
- [schema_surface_validation_standard.md](/core/docs/standards/validations/schema_surface_validation_standard.md): defines the explicit validation path for changed `*.schema.json` files.
- [watchtower_core_release_check.md](/core/docs/commands/core_python/watchtower_core_release_check.md): runs the local fail-closed release gate in one command.
- [watchtower_core_pack_export.md](/core/docs/commands/core_python/watchtower_core_pack_export.md): stages the final repository or pack bundle.
- [watchtower_core_validate_portability.md](/core/docs/commands/core_python/watchtower_core_validate_portability.md): validates an already-staged bundle or target root read-only.
- [watchtower_core_pack_bootstrap.md](/core/docs/commands/core_python/watchtower_core_pack_bootstrap.md): reconciles shared wiring after a pack-only bundle is copied into a compatible core repository.

## Guidance
- Humans and agents should follow the same release sequence. Agents should prefer `--format json`; humans may use `human` mode for local inspection and `json` mode for recorded review evidence.
- Prefer `watchtower-core release check ... --format json` as the one-shot local release gate. It is the current fail-closed path for dirty-worktree protection, broad validation, explicit schema-definition validation, and final staged export creation.
- Treat `watchtower-core pack export` as the canonical release artifact builder. A raw repository checkout, a manually cleaned working tree, or a portability scan over a live repo is not a customer-ready deliverable.
- Run the broad repository gate before export. The normal release baseline is `watchtower-core validate all --format json`.
- When the change touched one or more `*.schema.json` files, run `watchtower-core validate schema --path <schema> --format json` for each changed schema in addition to the broad repository gate.
- Rebuild the final handoff bundle immediately before release. A working repository can accumulate telemetry, caches, or runtime residue after validation.
- Expect `pack export` to apply any selected pack's declared `export_cleanup` hook before portability validation when that pack needs pack-owned live-history scrub or clean-state derived-surface rebuilds.
- Expect the final export to omit internal acceptance-contract examples, retained validation evidence, and any traceability entry that either depends on scrubbed evidence or still points outside the staged shared-core and selected-pack roots.
- Pack-only bundles are additive handoff surfaces, not standalone repositories. After copy, the recipient still needs compatible shared core plus `watchtower-core pack bootstrap` and `watchtower-core pack validate`. If the recipient intentionally bootstraps with `--no-sync-workspace` and shared workspace wiring changed, follow immediately with the deferred pack-local `sync all` step once `uv sync` finishes.
- When the bootstrapped pack publishes a pack-owned foundations view such as `plan/docs/foundations/**`, refresh that tree from `core/docs/foundations/**` during bootstrap bring-up and adapt the pack-local wording before treating the bootstrap as complete.

## Structure or Data Model
### Execution Path Selection
| Need | Preferred Command Shape | Notes |
|---|---|---|
| One-shot local release gate | `watchtower-core release check ... --format json` | Preferred for both humans and agents when the donor worktree should fail closed if dirty. |
| Manual step-by-step review | `watchtower-core validate all ...`; `watchtower-core validate schema ...`; `watchtower-core pack export ...` | Use this when you need to inspect or record the steps separately. |

### Release Mode Selection
| Need | Command Shape | Notes |
|---|---|---|
| Shared core only | `watchtower-core pack export --output-root <path> --overwrite --format json` | Builds a scrubbed core-only bootstrap bundle. |
| Shared core plus selected pack | `watchtower-core pack export --output-root <path> --include-pack <slug> --overwrite --format json` | Builds a portable repo bundle with shared core plus the selected pack set. |
| Selected pack only | `watchtower-core pack export --output-root <path> --include-pack <slug> --pack-only --overwrite --format json` | Builds an additive pack bundle without shared core. |

### Release Checklist
| Step | Required Action | Why It Exists |
|---|---|---|
| 1 | Choose the intended handoff mode explicitly: core-only, core-plus-selected-pack, or pack-only. | The export command and the recipient instructions depend on the bundle shape. |
| 2 | Prefer `watchtower-core release check ... --format json` for the chosen handoff mode. | This is the one-shot local gate that fails closed on dirty worktrees when git metadata is available. |
| 3 | If you need to inspect or record the steps separately, run `watchtower-core validate all --format json`, then `watchtower-core validate schema --path <schema> --format json` for changed `*.schema.json` files, then `watchtower-core pack export ... --format json`. | This is the manual equivalent of the one-shot gate. |
| 4 | Review the final staged export result and require `passed: true` plus `portability.issue_count: 0`. | The staged artifact, not the donor repo, is the release surface. |
| 5 | If the handoff is pack-only, provide recipient instructions to copy the bundle into compatible shared core, then run `watchtower-core pack bootstrap` and `watchtower-core pack validate`. If the pack publishes a pack-owned foundations view such as `plan/docs/foundations/**`, also copy `core/docs/foundations/**` into that pack-owned root and adapt the pack-local wording before final validation. If bootstrap deferred shared workspace sync, include the follow-on `watchtower-core <pack-namespace> sync all --write --format json` step too. | Pack-only bundles intentionally omit shared core and shared wiring. |
| 6 | Hand off the staged output directory itself, not the donor worktree. | Prevents runtime residue or omitted-pack leaks from reappearing after the final scrub. |

## Operationalization
- `Modes`: `release`; `bootstrap`; `validation`; `documentation`
- `Operational Surfaces`: `core/docs/commands/core_python/watchtower_core_release_check.md`; `core/docs/commands/core_python/watchtower_core_pack_export.md`; `core/docs/commands/core_python/watchtower_core_validate_portability.md`; `core/docs/commands/core_python/watchtower_core_validate_all.md`; `core/docs/commands/core_python/watchtower_core_validate_schema.md`

## Validation
- Reviewers should reject customer-ready claims that are not backed by a fresh `watchtower-core pack export` result.
- Reviewers should reject release claims that bypass `watchtower-core release check` without explicit reason when the intent is a normal local handoff gate.
- Reviewers should reject release bundles that skipped `watchtower-core validate all` without an explicit bounded exception.
- Reviewers should reject schema-authoring releases that changed `*.schema.json` without direct `watchtower-core validate schema` proof.
- Reviewers should reject pack-only handoff claims that omit the required recipient bootstrap and pack-validation follow-up.

## Change Control
- Update this standard when the repository changes the release/export sequence, bundle modes, or required validation steps.
- Update the companion command docs, portability standard, validation standard, and workspace README in the same change set when this operational sequence changes materially.

## References
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md)
- [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md)
- [watchtower_core_release_check.md](/core/docs/commands/core_python/watchtower_core_release_check.md)
- [watchtower_core_pack_export.md](/core/docs/commands/core_python/watchtower_core_pack_export.md)
- [watchtower_core_validate_schema.md](/core/docs/commands/core_python/watchtower_core_validate_schema.md)

## Updated At
- `2026-03-29T04:10:00Z`
