# `plan/docs/commands`

## Description
`This directory is the durable home for plan-owned command pages once a watchtower-core command surface is owned by the plan pack instead of reusable core.`

## Paths
| Path | Description |
|---|---|
| `plan/docs/commands/README.md` | Describes the purpose of the plan-owned command-doc root. |
| `plan/docs/commands/core_python/` | Holds plan-owned pages for the `watchtower-core plan ...` namespace. |

## Notes
- Keep shared and reusable-core command docs under `core/docs/commands/`.
- Keep pack-owned command docs here when the command namespace is owned by the plan pack.
- These command docs stay out of `plan/.wt/indexes/guidance_index.json`; they are plain command pages, not promoted guidance records.
- Do not place live initiative state or transient machine output here.
