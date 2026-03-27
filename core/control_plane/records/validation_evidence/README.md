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
| `core/control_plane/records/validation_evidence/watchtower_ctf_implementation_package_preservation_handoff_readiness.json` | Durable handoff-readiness evidence for the WatchTower CTF implementation-package preservation initiative, covering source parity, canonical doc normalization, task-chain readiness, and acceptance reconciliation. |
