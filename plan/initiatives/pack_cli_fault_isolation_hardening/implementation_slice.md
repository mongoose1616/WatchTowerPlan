# Pack CLI Fault Isolation Hardening Implementation Slice

## Summary
Keep pack validate, pack describe, and CLI startup usable when a registered hosted pack is malformed or partially bootstrapped.

## Work Breakdown
- `task.pack_cli_fault_isolation_hardening.bootstrap_pack_cli_fault_isolation_hardening`: Bootstrap Pack CLI Fault Isolation Hardening live initiative package.
- `task.pack_cli_fault_isolation_hardening.harden_pack_cli_fault_isolation`
  Reproduce the current failures, harden pack-contract validation so import-time integration errors become findings, remove eager all-pack host loading, update introspection and command-index generation for lazy loading, add regression coverage, run the full validation gate, and close the slice.

## Implementation Phases
- Phase 1: Update `watchtower_core.validation._pack_contract.runtime.integration_issues()` so missing integration modules and other import-time failures both return structured validation issues instead of propagating exceptions.
- Phase 2: Remove import-time eager loading from `watchtower_host.cli.registry`, keep core commands always available, and load pack integrations only for the namespace actually being invoked.
- Phase 3: Update `watchtower_host.cli.introspection` and `watchtower_host.cli.command_index` to enumerate pack namespaces one pack at a time and emit explicit unavailable-pack records for broken integrations.
- Phase 4: Add regression tests for broken non-selected packs, broken selected packs, structured validation import errors, and deterministic command-index behavior under degraded pack conditions.

## Validation Plan
- Targeted reproductions for the two verified failures before and after the fix.
- `./core/python/.venv/bin/pytest core/python/tests/unit/test_pack_integration_runtime.py -q`
- `./core/python/.venv/bin/pytest core/python/tests/unit/test_validation_suite_service.py -q`
- `./core/python/.venv/bin/pytest core/python/tests/unit/test_cli_pack_commands.py -q`
- `./core/python/.venv/bin/pytest core/python/tests/integration/test_cli_sync_commands.py -q`
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_core core/python/src/watchtower_host core/python/tests/unit core/python/tests/integration`
- `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
- `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration -q`

## Additional Improvement Targets To Watch
- The current bootstrap and confirmation commands still show the lingering-process behavior after work completes; avoid expanding that surface in this slice, but keep an eye out for any host lazy-loading changes that make that operational issue easier to isolate later.
- Keep command-index output explicit about broken packs rather than silently hiding them, because silent omission would undermine operator trust in the introspection surfaces.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
