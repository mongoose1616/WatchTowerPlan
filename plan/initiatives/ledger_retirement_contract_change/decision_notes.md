# Ledger Retirement Contract Change Decision Notes

## Summary
Retire `ledger` as a live repository taxonomy and standardize retained machine history on `record` families.

## Decisions
- Replace the canonical retained-history root `core/control_plane/ledgers/` with `core/control_plane/records/`.
- Replace the schema namespace segment `artifacts:ledgers:*` with `artifacts:records:*`.
- Keep migration, release, validation-evidence, and trace-purge families as retained records rather than deleting them.
- Reject a permanent compatibility alias that keeps the retired ledger root or ledger schema namespace active.
- Update machine-readable contracts, retained artifacts, runtime helpers, docs, and tests in the same tranche so no mixed terminology survives.
