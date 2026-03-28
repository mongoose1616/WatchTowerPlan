# `watchtower-core plan sync reference-index`

## Summary
This command rebuilds the governed reference index from the authored reference documents under `core/docs/references/` plus any admitted owning-pack `docs/references/` roots.

## Use When
- You added, renamed, or materially updated a reference document.
- You want to refresh the machine-readable reference lookup surface before validation, review, or query work.
- You want a dry-run preview of the rebuilt reference index before writing it to the canonical control-plane path.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan sync reference-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `plan/python/src/watchtower_plan/cli/sync.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan sync reference-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt reference index to its canonical control-plane artifact path.
- `--output <path>`: Write the rebuilt reference index to an alternate path instead of the canonical path.
- `--include-document`: Include the rebuilt JSON document in the command output payload.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan sync reference-index
```

```sh
cd core/python
uv run watchtower-core plan sync reference-index --write
```

```sh
cd core/python
uv run watchtower-core plan sync reference-index --output /tmp/reference_index.json --format json
```

## Behavior and Outputs
- The command rebuilds the reference index from governed reference docs and validates the generated artifact against its published schema.
- Governed reference docs may live in the shared root or in an owning pack root when the reference is intentionally pack-applied.
- By default the command runs in dry-run mode and reports the rebuilt entry count without mutating the repository.
- In write mode, the command updates the canonical reference-index artifact or the requested alternate output path.
- If the authored reference docs are structurally invalid, the command exits with an error instead of writing a broken artifact.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for all derived-artifact rebuild commands. |
| `watchtower-core query references` | Reads the reference index that this command rebuilds. |
| `watchtower-core sync repository-paths` | Rebuilds the path index that complements reference lookup when engineers browse by surface instead of topic. |

## Source Surface
- `plan/python/src/watchtower_plan/cli/sync.py`
- `core/python/src/watchtower_core/sync/reference_index.py`
- `core/control_plane/indexes/references/reference_index.json`

## Updated At
- `2026-03-28T20:00:00Z`
