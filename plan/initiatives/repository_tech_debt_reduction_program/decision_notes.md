# Repository Tech Debt Reduction Program Decision Notes

## Summary
Makes tech-debt reduction the active repository priority, starting with legacy residue removal, integration-tail reduction, and stale compatibility cleanup across core, host, and pack-owned code.

## Locked Decisions
- Treat technical debt as the top repository priority for the next execution tranche.
- Prefer deletion, collapse, or consolidation over another round of compatibility scaffolding.
- Keep reusable-core contracts donor-neutral and pack-neutral; remove debt by clarifying authority rather than hardcoding more repository-specific exceptions.
- Use the Python test suite runtime and the shape of duplicated or stale contract surfaces as the primary signals for ranking debt work.
- Keep one real contract-protecting end-to-end case per behavior family, but challenge repeated wrappers, migration-only residue, and redundant CLI-forwarding tests.
- Do not treat every historical edge case as sacred. Legacy cases that no longer protect an active contract should be removed or moved to a slower tier.
- Keep closeout evidence explicit: each debt-removal slice must explain what was deleted, what was narrowed, and what was intentionally retained.
