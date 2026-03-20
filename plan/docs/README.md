# `plan/docs`

## Description
`This directory is the durable home for promoted plan-domain guidance. Live initiative state belongs under plan/initiatives/ or plan/projects/, not here.`

## Paths
| Path | Description |
|---|---|
| `plan/docs/README.md` | Describes the purpose of the plan docs root and its owned guidance families. |
| `plan/docs/AGENTS.md` | Defines plan-guidance-specific instructions for the `plan/docs/**` subtree. |
| `plan/docs/foundations/` | Holds the required byte-identical mirror of the authored foundations source under `core/docs/foundations/`. |
| `plan/docs/decisions/` | Holds durable decision records promoted out of live initiative work. |
| `plan/docs/patterns/` | Holds reusable patterns promoted from validated initiative outcomes. |
| `plan/docs/references/` | Holds curated plan-domain reference material promoted from initiative-local authored inputs. |
| `plan/docs/standards/` | Holds durable operational standards promoted from initiative-local guidance. |

## Notes
- `requirements.md` and `decisions.md` remain the authoritative contract while this root is being seeded and future promotion paths are still landing.
- `core/docs/foundations/` is the authored foundations source and `plan/docs/foundations/` is the required byte-identical mirror.
- Promotion into this root is governed by `plan/.wt/registries/promotion_policy_registry.json`, and the currently approved guidance inventory is published through `plan/.wt/indexes/guidance_index.json`.
- Use this root for approved, durable plan guidance once promotion support exists; do not use it as a second live planning workspace.
