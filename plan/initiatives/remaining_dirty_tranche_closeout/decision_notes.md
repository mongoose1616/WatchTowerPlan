# Remaining Dirty Tranche Closeout Decision Notes

## Summary
This initiative exists to close out a mixed worktree, not to introduce a new architectural program. The main decisions therefore govern slice boundaries, commit hygiene, and validation expectations.

## Decisions
- Use one cleanup initiative rather than reopening the prior completed initiatives. The active need is coordinated closeout of the remaining uncommitted worktree, not further scope expansion of the already-delivered traces.
- Keep slice boundaries aligned to artifact and runtime ownership. Control-plane retained-record changes, foundations/governance updates, reusable-core refactors, and plan-runtime refactors should not be mixed into one commit.
- Prefer preserving existing public import and CLI surfaces while reducing internal concentration. Refactor behind stable facades unless a contract change is already part of the retained dirty tree.
- Validate each slice before commit using the narrowest meaningful checks, then run a full repository gate before initiative closeout.
- Treat any newly discovered unrelated drift as a separate follow-up only if it cannot be landed safely inside one of the defined slices without broadening the initiative materially.
