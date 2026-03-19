# `watchtower_core.evidence`

## Summary
Helpers for writing durable validation-evidence artifacts and managing pack-local evidence bundles used by readiness, review, and closeout flows.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.evidence.ValidationEvidenceRecorder`, `watchtower_core.evidence.EvidenceBundleHelper`, and their result types.
- `Non-Goals`: Repo-wide acceptance reconciliation or planning-task orchestration.

## Key Surfaces
- `bundles.py`: Pack-local evidence-bundle build, load, validation, and write helpers over governed bundle artifacts.
- `validation_evidence.py`: Validation-evidence write path and record assembly helpers.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `core/control_plane/ledgers/validation_evidence/README.md`
