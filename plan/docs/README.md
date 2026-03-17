# `plan/docs`

## Description
`This directory is the durable home for promoted plan-domain guidance. Live initiative state belongs under plan/initiatives/ or plan/projects/, not here.`

## Paths
| Path | Description |
|---|---|
| `plan/docs/README.md` | Describes the purpose of the plan docs root and its current migration boundary. |
| `plan/docs/foundations/` | Holds the duplicated foundations corpus for plan-domain guidance roots. |

## Notes
- `requirements.md` and `decisions.md` remain the authoritative contract while this root is being seeded and future promotion paths are still landing.
- `plan/docs/foundations/` and `core/docs/foundations/` intentionally duplicate the same foundation guidance and must stay aligned.
- Promotion into this root is governed by `plan/.wt/registries/promotion_policy_registry.json`, and the currently approved guidance inventory is published through `plan/.wt/indexes/guidance_index.json`.
- Use this root for approved, durable plan guidance once promotion support exists; do not use it as a second live planning workspace.
