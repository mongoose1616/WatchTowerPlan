# `plan/docs`

## Description
`This directory is the durable home for promoted plan-domain guidance. Live initiative state belongs under plan/initiatives/ or plan/projects/, not here.`

## Paths
| Path | Description |
|---|---|
| `plan/docs/README.md` | Describes the purpose of the plan docs root and its owned guidance families. |
| `plan/docs/AGENTS.md` | Defines plan-guidance-specific instructions for the `plan/docs/**` subtree. |
| `plan/docs/foundations/` | Holds the required plan-owned foundations copy seeded from the authored foundations source under `core/docs/foundations/`. |
| `plan/docs/decisions/` | Holds durable decision records promoted out of live initiative work. |
| `plan/docs/patterns/` | Holds reusable patterns promoted from validated initiative outcomes. |
| `plan/docs/references/` | Holds curated plan-domain reference material promoted from initiative-local authored inputs. |
| `plan/docs/standards/` | Holds durable operational standards promoted from initiative-local guidance. |
| `plan/docs/commands/` | Holds pack-owned command pages when a `watchtower-core <pack> ...` surface is owned by this pack. |

## Notes
- Durable plan guidance and promotion targets are governed by `plan/docs/standards/**`, `plan/.wt/registries/promotion_policy_registry.json`, and the plan-owned foundations copy.
- `core/docs/foundations/` is the authored foundations source and `plan/docs/foundations/` is the required copied/adapted plan-owned view seeded from it.
- Promotion into this root is governed by `plan/.wt/registries/promotion_policy_registry.json`, and the currently approved guidance inventory is published through `plan/.wt/indexes/guidance_index.json`.
- `plan/docs/commands/**` is durable documentation but not part of the promoted guidance index; command docs remain plain Markdown companion pages rather than front-matter-governed guidance records.
- Use this root for approved, durable plan guidance; do not use it as a second live planning workspace.
- Keep plan-owned command docs here once a command is pack-specific and no longer a shared core surface.
