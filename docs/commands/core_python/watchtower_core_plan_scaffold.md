# `watchtower-core plan scaffold`

## Summary
This command scaffolds one compact governed PRD, feature design, implementation plan, or decision record and refreshes derived planning surfaces in write mode.

## Use When
- You need one new planning document without copying the template by hand.
- You want the scaffold to follow current repository naming, section order, and front-matter expectations.
- You want dry-run preview before writing the document to its canonical planning path.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core plan scaffold` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/plan_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core plan scaffold --kind <prd|feature-design|implementation-plan|decision> --trace-id <trace_id> --document-id <document_id> --title <title> --summary <summary> [--owner <owner>] [--status <status>] [--applies-to <path_or_concept>] [--alias <alias>] [--file-stem <stem>] [--linked-prd <id>] [--linked-decision <id>] [--linked-design <id>] [--linked-plan <id>] [--linked-acceptance <id>] [--source-request <text>] [--reference <source>] [--updated-at <timestamp>] [--include-document] [--write] [--format <human|json>]
```

## Arguments and Options
- `--kind <...>`: Planning document family to scaffold.
- `--trace-id <trace_id>`: Stable trace identifier.
- `--document-id <document_id>`: Stable document identifier.
- `--title <title>`: Human-readable document title.
- `--summary <summary>`: One-line document summary used in trackers and indexes.
- `--owner <owner>`: Document owner recorded in front matter. Defaults to `repository_maintainer`.
- `--status <status>`: Optional explicit document status. Defaults depend on the selected kind.
- `--applies-to <path_or_concept>`: Optional applied path or concept. Repeat for multiple values.
- `--alias <alias>`: Optional retrieval alias. Repeat for multiple values.
- `--file-stem <stem>`: Optional output filename stem. Defaults to a slug derived from the title.
- `--linked-prd <id>`: Optional linked PRD ID. Repeat for multiple values.
- `--linked-decision <id>`: Optional linked decision ID. Repeat for multiple values.
- `--linked-design <id>`: Optional linked design ID. Repeat for multiple values.
- `--linked-plan <id>`: Optional linked implementation-plan ID. Repeat for multiple values.
- `--linked-acceptance <id>`: Optional linked acceptance-contract ID. Repeat for multiple values.
- `--source-request <text>`: Optional source request or driver. Repeat for multiple values.
- `--reference <source>`: Optional companion reference or source. Repeat for multiple values.
- `--updated-at <timestamp>`: Optional explicit RFC 3339 UTC timestamp. Defaults to now.
- `--include-document`: Include the rendered document content in the command output.
- `--write`: Persist the scaffolded document and refresh derived planning surfaces.
- `--format <human|json>`: Select human-readable or structured JSON output.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core plan scaffold --kind prd --trace-id trace.example --document-id prd.example --title "Example PRD" --summary "Frames the example initiative."
```

```sh
cd core/python
uv run watchtower-core plan scaffold --kind feature-design --trace-id trace.example --document-id design.features.example --title "Example Feature Design" --summary "Defines the example design boundary." --linked-prd prd.example --reference docs/planning/prds/example.md --include-document --format json
```

## Behavior and Outputs
- By default the command runs in dry-run mode and does not create files.
- Optional sections are omitted by default and the scaffold emits one compact placeholder per required section when richer inputs are not provided.
- The command rejects path collisions and front-matter or record-metadata mismatches before writing.
- In write mode, the command writes the scaffold to its canonical planning path and refreshes derived planning surfaces.
- In `json` mode, the command prints one JSON object with the scaffold metadata, target path, write state, and optional document body.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core plan` | Parent command group for planning scaffold operations. |
| `watchtower-core plan bootstrap` | Uses the same scaffold machinery to create a full traced planning chain. |
| `watchtower-core task` | Use after scaffolding when the next step is bounded task execution. |
| `watchtower-core sync all` | Rebuilds the same deterministic planning surfaces refreshed in write mode. |

## Source Surface
- `core/python/src/watchtower_core/cli/plan_family.py`
- `core/python/src/watchtower_core/cli/plan_handlers.py`
- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`

## Updated At
- `2026-03-10T23:01:32Z`
