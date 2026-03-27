# Phase 7: Release And Portability Proof

## Purpose

Prove that the resulting offensive-security pack can be exported, bootstrapped into the target repository, validated, and handed off through the shared release contract.

## In-Scope Surfaces

- shared core export from donor repo
- copy into target repo
- `pack bootstrap`
- `pack validate`
- `validate all`
- changed-schema validation
- portability proof
- handoff-mode selection

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- donor export from `/home/j/WatchTowerPlan/core`
- target bootstrap in `/home/j/WatchTower/core/python`
- `watchtower-core pack bootstrap --replace-hosted-packs --write` when the copied repository must replace donor pack wiring
- `watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- `watchtower-core validate all --format json`
- `watchtower-core validate schema --path <schema> --format json` for changed schemas
- `watchtower-core pack export` or `watchtower-core release check` for final portability-clean output

## Dependencies

- Phases 0 through 6 complete
- target repository ready to receive exported core and pack roots

## Upstream Assumptions

- export remains the canonical shared-core transfer path
- pack-only bundles still require compatible shared core and bootstrap in the recipient repo

## Validation And Acceptance Criteria

- donor and recipient roles are explicit
- all handoff modes are documented: `core-only`, `core-plus-pack`, `pack-only`
- portability proof uses staged export, not raw repo snapshots
- target bootstrap sequence is explicit and reproducible

## Risks And Unresolved Questions

- target repo may need replacement bootstrap if multiple hosted packs exist later
- omitted release scrub steps can invalidate otherwise-correct bootstrap wiring

## Exit Criteria

- the package defines the full bootstrap, validation, and portability proof path into `/home/j/WatchTower`
