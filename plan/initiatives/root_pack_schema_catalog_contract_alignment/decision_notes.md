# Root Pack Schema Catalog Contract Alignment Decision Notes

## Summary
Capture the reusable-core contract decisions for widening schema-catalog canonical-path validation.

## Decisions
- Treat first-party root packs as a reusable-core operating mode, not a donor-specific exception.
- Widen the schema-catalog canonical-path contract in shared core rather than pushing this fix into an oversight-only pack workaround.
- Keep the allowed schema roots constrained to:
  - `core/control_plane/schemas/...`
  - `<pack>/.wt/schemas/...` for first-party root packs
  - `packs/<slug>/.wt/schemas/...` for nested packs
- Do not broaden the contract to arbitrary repository-relative schema locations.
- Update the shared authoring guidance in the same change set if it is ambiguous about root-pack schema publication.

## Rejected Alternatives
- Reject `oversight`-specific schema path exceptions in core because they would encode donor/consumer repository names into a shared contract.
- Reject changing the oversight pack to a nested `packs/oversight/` root only to satisfy the current core regex because reusable core already documents first-party root packs as supported.
