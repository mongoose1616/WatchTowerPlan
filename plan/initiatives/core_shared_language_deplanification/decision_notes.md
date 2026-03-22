# Core Shared Language Deplanification Decision Notes

## Summary
Records the framing choices used to keep shared core policy pack-neutral without erasing real current-repository facts.

## Decision
- Keep concrete current-path examples such as `plan/python/src/watchtower_plan/` where they help contributors navigate the present repository.
- Remove wording that treats `watchtower_plan` as the defining contrast for reusable core.
- Use `pack-owned`, `pack-local`, `hosted pack`, and `current internal pack` as the default shared-core framing.

## Deferred Follow-Up
- If broader contributor docs outside this slice still use plan-first wording after this tranche, address them in a separate cleanup initiative rather than widening this documentation-only change into a repository-wide prose sweep.
