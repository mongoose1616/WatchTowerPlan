# Plan Legacy History and Retention Reconciliation Design Record

## Summary
Encodes the transitional archive policy and clean-endstate purge rules for legacy `docs/planning/**` history and closed initiative packages directly in the live plan authority.

## Design Boundary
- The follow-up remains pack-wide and bounded: it publishes the machine-readable policy and linkage needed to govern legacy history and transitional archives, but it does not attempt a mass purge in the same slice.
- The live authority for this rule belongs under `plan/.wt/**`, not only in retained docs-backed standards or old purge traces.
- Existing trace-purge standards and helpers remain support-only references; the new registry must restate the active rule as live machine authority.

## Policy Model
- Use one `retention_policy_registry` artifact with the smallest field set needed to answer the current migration questions:
  - what subtree the rule covers
  - whether it applies always, only to legacy material, or only to terminal initiative archives
  - the current disposition during the transitional model
  - the intended clean-endstate disposition
  - whether the subtree should be visible in live operational queries
  - what purge gate must be satisfied before deletion
  - which surviving authority paths remain after purge
- Resolve policy by the most-specific matching root or glob so initiative-specific archive roots override broader container roots cleanly.

## Intended Outcomes
- `docs/planning/**` is explicitly marked as frozen legacy history that remains hidden from the live operational model and becomes purge-eligible only after surviving authority exists.
- `plan/initiatives/*` and `plan/projects/*/initiatives/*` gain an explicit transitional-archive rule so whole-package archive is documented as temporary rather than silently permanent.
- `plan/.wt/**`, `plan/docs/**`, and `core/control_plane/ledgers/purges/**` gain explicit surviving-authority roles in the clean endstate.
