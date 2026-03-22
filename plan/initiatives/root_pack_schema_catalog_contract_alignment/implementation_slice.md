# Root Pack Schema Catalog Contract Alignment Implementation Slice

## Summary
Extends the reusable-core schema catalog canonical-path contract to support first-party root pack machine roots such as <pack>/.wt without donor-specific exceptions.

## Work Breakdown
- `task.root_pack_schema_catalog_contract_alignment.capture_and_approve_contract_delta`
  - Finish authored inputs, confirm them, and approve the initiative for execution.
- `task.root_pack_schema_catalog_contract_alignment.widen_schema_catalog_root_pack_contract`
  - Update the reusable-core schema-catalog artifact schema to accept first-party root pack schema roots.
- `task.root_pack_schema_catalog_contract_alignment.add_regression_coverage_and_refresh_docs`
  - Add root-pack and negative-path regression coverage and refresh shared docs where the contract is ambiguous.
- `task.root_pack_schema_catalog_contract_alignment.validate_and_close`
  - Run lint, type, targeted tests, repo validation, and close the initiative.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.

## Validation Plan
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/tests/unit core/python/tests/integration`
- `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
- targeted `pytest` for schema-catalog and pack-root contract coverage
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Commit Plan
- Commit 1: initiative package capture and approval
- Commit 2: reusable-core schema contract plus regression coverage and any required shared doc updates
- Commit 3: closeout state if it is not folded into the implementation commit
