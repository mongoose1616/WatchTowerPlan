# `core/control_plane/records/validation_evidence`

## Description
`This directory holds committed durable validation-evidence records. Use it for reviewable validation outcomes tied to traced initiatives, not for transient runtime logs or mutable execution output.`

## Notes
- Portable customer exports intentionally omit this retained-record family. A staged handoff bundle may therefore contain only `README.md` here.

## Files
| Path | Description |
|---|---|
| `core/control_plane/records/validation_evidence/README.md` | Describes the purpose of the validation-evidence record directory and its current contents. |
| `core/control_plane/records/validation_evidence/governed_acceptance_example_validation_baseline.json` | Durable generic validation-evidence example paired with the governed acceptance contract example in the engineering repository; portable exports intentionally scrub it. |
