# Core Removable Plan Reference Cleanup Decision Notes

## Summary
This initiative removes removable plan-specific wording from shared core while preserving only references that are materially required by the live repository contract.

## Locked Decisions
- Shared core docs, help text, and reusable-core messaging should prefer generic `watchtower_<pack>`, `<pack>`, or hosted-pack wording over `watchtower_plan`.
- Current-repository data surfaces may keep plan references when they are factual current state, such as the active pack registry entry, generated command/index records, and plan-owned paths referenced by current-governed artifacts.
- Current-repository examples in shared host help should be replaced with donor-neutral examples where possible instead of using `--pack plan` or `watchtower-core plan ...` as the default pattern.
- Shared tests may keep plan references only when they intentionally prove the current internal pack contract or the generated current-repo authority.
- This slice does not move plan-owned implementation out of `plan/**`; it only removes shared-core residue that overstates plan as the reusable baseline.
