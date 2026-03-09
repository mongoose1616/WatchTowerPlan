# `watchtower-core sync foundation-index`

## Summary
This command rebuilds the governed foundation index from the governed foundation documents under `docs/foundations/`.

## Use When
- You changed a foundation doc and need the machine-readable foundation index to reflect the current intent corpus.
- You want to audit where foundation docs are cited or explicitly applied across standards, workflows, and planning docs.
- You want a controlled way to regenerate one intent-layer index without rebuilding unrelated derived artifacts.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core sync foundation-index` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/main.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core sync foundation-index [--write] [--output <path>] [--include-document] [--format <human|json>]
```

## Arguments and Options
- `--write`: Write the rebuilt artifact to the canonical foundation-index path in `core/control_plane/`.
- `--output <path>`: Optional explicit output path for the rebuilt artifact.
- `--include-document`: Include the rebuilt document in JSON output for inspection or downstream tooling.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core sync foundation-index
```

```sh
cd core/python
uv run watchtower-core sync foundation-index --write
```

```sh
cd core/python
uv run watchtower-core sync foundation-index --output /tmp/foundation_index.v1.json --format json
```

## Behavior and Outputs
- The command reads the governed foundation docs under `docs/foundations/` and rebuilds the machine-readable foundation index deterministically.
- The rebuild validates foundation front matter, enforces required `References` and `Updated At` sections, and captures downstream citation or application use from standards, workflows, and planning docs.
- By default the command runs in dry-run mode and does not mutate the canonical artifact.
- In `human` mode, the command prints whether it ran in dry-run or write mode and how many foundation entries were rebuilt.
- In `json` mode, the command prints one JSON object with the command name, status, entry count, write flag, and output path when one was written.
- If `--include-document` is used, the JSON payload includes the rebuilt foundation-index document.
- The command exits with status code `0` when the rebuild succeeds and non-zero if the source documents or rebuilt artifact are invalid.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core sync` | Parent command group for governed artifact rebuild operations. |
| `watchtower-core query foundations` | Reads the foundation index that this command rebuilds. |
| `watchtower-core sync reference-index` | Rebuilds the companion reference index used to normalize downstream external authority. |
| `watchtower-core sync all` | Rebuilds the foundation index together with the other local deterministic sync surfaces. |

## Source Surface
- `core/python/src/watchtower_core/cli/main.py`
- `core/python/src/watchtower_core/sync/foundation_index.py`
- `core/control_plane/indexes/foundations/foundation_index.v1.json`

## Updated At
- `2026-03-09T23:22:09Z`
