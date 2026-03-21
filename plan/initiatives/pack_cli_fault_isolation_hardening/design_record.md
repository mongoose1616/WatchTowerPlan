# Pack CLI Fault Isolation Hardening Design Record

## Summary
Keep pack validate, pack describe, and CLI startup usable when a registered hosted pack is malformed or partially bootstrapped.

## Problem
- The host command registry currently imports all registered pack integrations before dispatch and therefore lets one broken pack prevent operator-safe commands such as `pack validate` and `pack describe` from running.
- Pack-contract validation currently treats `ModuleNotFoundError` as a structured validation issue but still propagates other import-time failures, so malformed integrations can still crash validation instead of producing findings.

## Design
- Keep validation hardening first. `integration_issues()` should treat all import-time integration failures as validation findings, with `ModuleNotFoundError` remaining its own issue code and all other import-time exceptions mapped to a separate import-error issue that preserves the exception type and message.
- Remove eager host pack loading from module import time. The host should keep a core-only command surface available without importing pack integrations, and it should load pack integrations only for the selected namespace.
- Keep pack namespace discovery metadata-driven. Reading the pack registry and runtime manifests is safe; importing integration modules is not. The host should separate those responsibilities.
- Keep degraded behavior explicit. Command introspection and command-index generation should keep deterministic output while representing broken packs as unavailable namespaces rather than silently dropping them.

## Sequencing
1. Harden pack-contract validation so import-time integration failures become structured validation results.
2. Remove eager all-pack loading from host startup and make parser construction namespace-aware.
3. Update introspection and command-index generation to enumerate core commands plus pack namespaces one pack at a time.
4. Add regression coverage for broken non-selected packs, structured validation failures, and deterministic introspection behavior.

## Constraints
- The initiative package is machine-first and local to `plan/initiatives/pack_cli_fault_isolation_hardening/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
