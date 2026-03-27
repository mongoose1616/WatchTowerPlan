# Phase 1: Scaffold And Integrate The Pack

## Purpose

Create the first runnable hosted-pack root, register it through shared bootstrap, and replace scaffold placeholders with the first real offensive-security workflow and machine-contract surfaces.

## In-Scope Surfaces

- scaffold command
- generated pack roots and starter manifests
- bootstrap and pack validation commands
- path and id generation baseline
- starter workflow metadata replacement
- immediate next slice after scaffold

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- `offensive_security/.wt/manifests/pack_settings.json`
- `offensive_security/.wt/manifests/pack_runtime_manifest.json`
- `offensive_security/.wt/registries/workflow_metadata_registry.json`
- `offensive_security/docs/commands/core_python/README.md`
- `offensive_security/docs/commands/core_python/watchtower_core_offsec.md`
- `offensive_security/workflows/modules/*.md`
- `offensive_security/workflows/roles/*.md`
- `offensive_security/python/src/watchtower_offensivesecurity/integration.py`

## Dependencies

- Phase 0 baseline
- current `watchtower-core pack scaffold`, `pack bootstrap`, and `pack validate`
- shared `core/python/pyproject.toml` bootstrap behavior

## Upstream Assumptions

- `pack bootstrap --write` still reconciles shared registry, workspace metadata, and shared discovery indexes together
- the scaffold-compatible `offensivesecurity` slug plus `watchtower-offensivesecurity` and `watchtower_offensivesecurity` python naming proof is the locked current-compatible baseline, even though older Step 1 prose explored alternate normalization
- pack-owned path and typed-id rules still need to be explicit even though shared core owns the generic naming machinery

## Validation And Acceptance Criteria

- scaffold, bootstrap, and direct pack validation commands are captured exactly as rerun on `2026-03-26`
- manifest examples match the current-compatible proof
- path normalization, typed ids, placeholder segments, and collision handling are locked before any real challenge root is created
- starter workflow metadata replacement is defined as mandatory before route/index reliance
- the pack command-doc directory entrypoint `offensive_security/docs/commands/core_python/README.md` is explicitly authored before authority-map command lookup depends on it
- immediate next slice is explicit and minimal
- the immediate next slice is a thin vertical slice on the real pack root through the real pack CLI, not an internal-helper-only proof
- that thin slice uses real schemas and validators for the included surfaces rather than temporary placeholders

## Risks And Unresolved Questions

- upstream slug normalization may change generated python names later
- older optional-segment path notes can cause drift unless the v1 placeholder policy is stated explicitly
- route preview will be misleading if starter workflow metadata is not replaced immediately

## Exit Criteria

- the package shows exactly how to get from empty target pack root to a bootstrap-valid starter pack with no hidden steps
