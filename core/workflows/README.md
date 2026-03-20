# `core/workflows`

## Description
`This directory is the authoritative reusable-core workflow root. It holds shared routing guidance and reusable workflow modules for core implementation, review, validation, documentation, and repository-governance work.`

## Paths
| Path | Description |
|---|---|
| `core/workflows/README.md` | Describes the purpose of the core workflow root and its owned workflow surfaces. |
| `core/workflows/AGENTS.md` | Defines local instructions for future core-owned workflow guidance. |
| `core/workflows/ROUTING_TABLE.md` | Defines the reusable-core task routes and shared workflow-module selection rules. |
| `core/workflows/modules/README.md` | Explains the authoritative core workflow-module set. |

## Notes
- `requirements.md` and `decisions.md` remain authoritative for the remaining workflow split details.
- Shared reusable workflow modules live under `core/workflows/modules/`.
- Plan-domain routing lives under `plan/workflows/` and may reference shared modules from this root.
