# Ledger Retirement Contract Change Design Record

## Summary
Retire remaining ledger-authority dependencies through one governed contract change without breaking validation, command, or documentation contracts.

## Design Direction
- The repository retires `ledger` as a live governed surface family and standardizes on retained `record` families.
- Canonical retained-history roots move from `core/control_plane/ledgers/**` to `core/control_plane/records/**`.
- Artifact purposes stay the same: migration records, release records, validation-evidence records, and trace-purge records remain the surviving machine-history families.

## Key Decisions
- Prefer one hard contract cutover over a permanent alias layer. The repo should not keep both `ledgers/**` and `records/**` as active accepted roots.
- Keep existing artifact file names where they are already record-shaped, such as `*_record.json`; the main structural change is the family root and schema namespace.
- Replace `artifacts:ledgers:*` schema IDs with `artifacts:records:*` schema IDs and update every retained artifact document in the same change.
- Replace retention-policy terms such as `purge_ledger_root` and `minimal_ledger` with record-based vocabulary so the policy surface stays semantically aligned with the runtime contract.
- Preserve public behavioral seams where practical, but prefer clear record terminology in user-facing CLI output, helper constants, and human docs.

## Scope Boundaries
- In scope: control-plane retained history roots, retained artifact JSON documents, schema IDs, validator coverage, retention policy, runtime constants, purge flow, evidence helpers, command docs, standards, foundations, requirements, and tests.
- Out of scope: redesigning the underlying evidence model, removing retained history entirely, or changing initiative lifecycle policy beyond what the taxonomy shift requires.

## Validation Strategy
- Rebuild the affected derived machine surfaces after the contract change lands so indexes, trackers, and query outputs pick up the new paths.
- Run targeted validation while implementing: schema-backed artifacts, retained-history helpers, purge flow, evidence flow, and query surfaces.
- Finish with the full repository gate: `watchtower-core validate all --skip-acceptance --format json`, full unit plus integration `pytest`, and the broader `ruff` and `mypy` slices already used for this program.
