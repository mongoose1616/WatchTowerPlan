# `core/control_plane/indexes/traceability`

## Description
`This directory holds machine-readable traceability indexes that join planning, task, contract, validator, and evidence surfaces under shared trace IDs. Keep it as a compact derived join layer rather than a replacement for family-specific indexes.`

## Notes
- Portable customer exports may keep `core/control_plane/indexes/traceability/traceability_index.json` with `entries: []` after internal shared acceptance/evidence example lineage has been scrubbed.

## Files
| Path | Description |
|---|---|
| `core/control_plane/indexes/traceability/README.md` | Describes the purpose of the traceability index directory and its current contents. |
| `core/control_plane/indexes/traceability/traceability_index.json` | Unified machine-readable traceability index for current traced initiatives; portable exports may legitimately carry an empty `entries` array. |
