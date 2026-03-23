# `watchtower_core.evidence`

## Summary
Helpers for writing durable validation-evidence artifacts and managing pack-local evidence bundles used by readiness, review, and closeout flows.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.evidence.ValidationEvidenceRecorder`, `watchtower_core.evidence.EvidenceBundleHelper`, and their result types.
- `Non-Goals`: Repo-wide acceptance reconciliation, planning-task orchestration, or repo-local evidence workflow policy.

## Key Surfaces
- `bundles.py`: Pack-local evidence-bundle build, load, validation, and write helpers over governed bundle artifacts, with default schema resolution sourced from the active pack schema catalog.
- `validation_evidence.py`: Validation-evidence write path and record assembly helpers.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `core/control_plane/records/validation_evidence/README.md`

## Notes
- Keep reusable evidence bundle and validation-evidence helpers here.
- Resolve pack-local evidence-bundle schema IDs from the active pack schema catalog instead of hardcoding a pack-owned schema identifier in reusable core.
- Keep repo-local evidence workflow decisions outside this namespace.
