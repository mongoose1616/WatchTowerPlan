# Root Pack Schema Catalog Contract Alignment Design Record

## Summary
Extends the reusable-core schema catalog canonical-path contract to support first-party root pack machine roots such as <pack>/.wt without donor-specific exceptions.

## Contract Change
- The canonical-path validator in `core/control_plane/schemas/artifacts/schema_catalog.schema.json` should accept schema files rooted at:
  - `core/control_plane/schemas/...`
  - `<root-pack>/.wt/schemas/...`
  - `packs/<slug>/.wt/schemas/...`
- The path rule should stay structural. It must not depend on a known list of pack names.

## Implementation Shape
- Update the schema-catalog artifact schema pattern so first-party root pack machine roots are valid.
- Add regression coverage proving:
  - `plan/.wt/...` still validates
  - `packs/example/.wt/...` still validates
  - `oversight/.wt/...` or another synthetic root-pack path validates
  - unrelated arbitrary roots still fail
- Refresh shared docs only where they help future pack authors understand the allowed schema root layouts.

## Risks
- If the new regex is too broad, schema catalogs could point to non-pack schema roots outside the supported contract.
- If the new regex is too narrow, copied root packs will continue to fail even though pack discovery and workspace-root handling already support them.

## Mitigations
- Keep the contract centered on `/.wt/schemas/` so only pack machine roots qualify.
- Add explicit negative coverage for unsupported roots.
