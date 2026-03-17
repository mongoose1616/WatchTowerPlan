# `workflows`

## Description
`This directory is now a thin compatibility surface for older root-level workflow references. Authoritative shared workflow routing lives under core/workflows/, and authoritative plan-domain workflow routing lives under plan/workflows/.`

## Paths
| Path | Description |
|---|---|
| `workflows/README.md` | Describes the purpose of the workflows directory and the main workflow entrypoints stored here. |
| `workflows/ROUTING_TABLE.md` | Compatibility note pointing readers to the split workflow roots. |
| `workflows/modules/` | Compatibility copies retained for older links while core/workflows/ and plan/workflows/ own current workflow authority. |

## Notes
- Reusable shared workflow start-here: `core/workflows/README.md`
- Plan-domain workflow start-here: `plan/workflows/README.md`
- Do not treat this root as the authoritative routing backend for new work.
