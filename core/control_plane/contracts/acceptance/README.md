# `core/control_plane/contracts/acceptance`

## Description
`This directory holds machine-readable acceptance contracts derived from durable initiative or promoted guidance acceptance criteria. Use it when workflows or Python helpers need a deterministic acceptance surface without parsing source prose directly.`

## Notes
- Portable customer exports may intentionally omit the JSON artifacts in this family because the paired retained validation evidence is excluded from staged handoff bundles.

## Files
| Path | Description |
|---|---|
| `core/control_plane/contracts/acceptance/README.md` | Describes the purpose of the acceptance contracts directory and its current contents. |
| `core/control_plane/contracts/acceptance/governed_acceptance_example_acceptance.json` | Durable generic acceptance-contract example used by command docs, standards, and validation tests in the engineering repository; portable exports intentionally scrub it. |
| `core/control_plane/contracts/acceptance/watchtower_ctf_package_preservation_acceptance.json` | Durable acceptance contract for the WatchTower CTF implementation-package preservation initiative, covering preserved source parity, canonicalization, handoff tasking, and acceptance/evidence trace joins. |
