# Pack CLI Fault Isolation Hardening

## Summary
Keep pack validate, pack describe, and CLI startup usable when a registered hosted pack is malformed or partially bootstrapped.

## Identity
- `initiative_id`: `initiative.pack_cli_fault_isolation_hardening`
- `trace_id`: `trace.pack_cli_fault_isolation_hardening`
- `scope_type`: `pack_wide`

## Verified Current State
- The host still eagerly loads every registered pack integration in `watchtower_host.cli.registry`, and it still does so at module import time through `COMMAND_GROUP_SPECS`.
- `watchtower_host.cli.parser.build_parser()` still reloads the full command-group registry and therefore still requires every registered pack integration to import successfully before dispatch.
- `watchtower_core.validation._pack_contract.runtime.integration_issues()` still converts only `ModuleNotFoundError` into a structured finding and still propagates other import-time exceptions.
- Reproduction 1: importing `watchtower_host.cli.main` from a temporary repo whose pack runtime manifest points at `watchtower_plan.missing_integration` still fails with `ModuleNotFoundError` before `main(["pack", "validate", ...])` can run.
- Reproduction 2: patching `watchtower_core.validation._pack_contract.runtime.importlib.import_module` to raise `RuntimeError("boom")` still causes `PackContractValidationService.validate()` to raise instead of returning a failed validation result.

## Goal
- Keep `watchtower-core pack list`, `watchtower-core pack describe`, and `watchtower-core pack validate` usable even when some other registered hosted pack is broken.
- Keep `watchtower-core <pack namespace> ...` fail-local to the selected pack instead of bricking the entire host CLI at startup.
- Keep pack-contract validation structured and operator-readable by returning validation issues for import-time integration failures instead of tracebacks.

## Non-Goals
- Do not change pack manifest semantics, pack registry semantics, or the external hosted-pack authoring contract beyond the new failure-reporting behavior.
- Do not weaken pack-contract validation; malformed integrations should still fail, but they should fail as findings rather than as host crashes.
- Do not introduce a silent-drop behavior for broken packs in command introspection or command-index generation.

## Initial Task Set
- `task.pack_cli_fault_isolation_hardening.bootstrap_pack_cli_fault_isolation_hardening`: Bootstrap Pack CLI Fault Isolation Hardening live initiative package.
- `task.pack_cli_fault_isolation_hardening.harden_pack_cli_fault_isolation`: Harden pack validation, host parser composition, and command introspection so broken packs fail locally instead of taking down the CLI.

## Acceptance Criteria
- `watchtower-core pack list`, `watchtower-core pack describe`, and `watchtower-core pack validate` still run when a non-selected registered pack has a broken integration module.
- `watchtower-core pack validate` returns structured failed results for import-time integration errors instead of propagating tracebacks.
- `watchtower-core <pack namespace> ...` imports only the selected pack namespace rather than eagerly importing all registered pack integrations.
- Command introspection and command-index generation remain deterministic under broken-pack conditions and report broken packs explicitly rather than silently dropping them.
