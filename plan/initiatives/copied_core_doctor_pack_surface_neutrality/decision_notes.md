# Copied Core Doctor Pack Surface Neutrality Decision Notes

## Summary
This document records the decisions that keep `watchtower-core doctor` generic across copied-core recipient repositories.

## Locked Decisions
- `watchtower-core doctor` is a shared-core health snapshot, not a `plan`-pack readiness check.
- Pack-owned live indexes such as `task_index` and `initiative_index` remain optional pack surfaces; host commands may use them only when the active pack declares them.
- Missing optional pack-owned live indexes should produce count `0` in doctor output, not a command failure.
- Broken core governed surfaces or invalid pack settings should still fail closed; this slice only removes the plan-style optional-surface assumption.
- Validation must include a copied-core root-pack proof plus the normal shared repository validation pass.

## Deferred Decisions
- Whether additional generic host commands should expose more pack-owned optional counts in the future.
- Whether `doctor` should eventually surface an explicit `optional_surfaces` section instead of only returning zero counts for absent live indexes.
