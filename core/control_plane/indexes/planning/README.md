# `core/control_plane/indexes/planning`

## Description
`This directory holds the canonical planning catalog that joins trace-linked planning, task, acceptance, evidence, and per-trace coordination state into one machine-readable deep-planning surface.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/indexes/planning/README.md` | Describes the purpose of the planning-catalog directory and its current artifacts. |
| `core/control_plane/indexes/planning/planning_catalog.v1.json` | Canonical machine-readable planning catalog for deep trace-linked planning lookup with explicit status semantics. |

## Notes
- Treat this directory as a derived lookup surface, not as the source of truth for planning or task content.
- Build the planning catalog from traceability, initiative, planning-document, task, acceptance-contract, and validation-evidence sources.
- Use `watchtower-core query planning` as the canonical machine query path for deep planning lookup after `watchtower-core query coordination`.
- Keep the initiative and coordination indexes aligned as narrower projections rather than competing authorities.
