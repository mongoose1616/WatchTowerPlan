# `watchtower_core.evidence`

## Summary
Helpers for writing durable validation-evidence artifacts from validation and closeout flows.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.evidence.ValidationEvidenceRecorder` and its result types.
- `Non-Goals`: Repo-wide acceptance reconciliation or planning-task orchestration.

## Key Surfaces
- `validation_evidence.py`: Validation-evidence write path and record assembly helpers.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `core/control_plane/ledgers/validation_evidence/README.md`
