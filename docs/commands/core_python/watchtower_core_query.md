# `watchtower-core query`

## Summary
This command group provides read-only lookup over governed repository indexes and narrow runtime context loads. Use it to route from a current-state question to the smallest useful command or machine-readable surface.

## Use When
- You need to choose the correct lookup path before opening raw JSON or scanning docs manually.
- You want one read-only command group for current planning state, deep planning joins, command discovery, standards lookup, or trace-linked records.
- You need structured JSON output for scripts, workflows, or agent use.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core query` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_core/cli/query_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core query <query_command> [args]
```

## Arguments and Options
- `<query_command>`: Choose a leaf command such as `coordination`, `initiatives`, `tasks`, `artifacts`, `readiness`, `discrepancies`, `plan-evidence`, `closeouts`, `reviews`, `projects`, `project-context`, `planning`, `authority`, `commands`, `paths`, `standards`, `workflows`, `references`, `prds`, `decisions`, `designs`, `acceptance`, `evidence`, `foundations`, or `trace`.
- `-h`, `--help`: Show the query-group help text.
- Pass filters, limits, and output-mode flags to the selected leaf command.

## Examples
```sh
cd core/python
uv run watchtower-core query --help
```

```sh
cd core/python
uv run watchtower-core query coordination --format json
```

```sh
cd core/python
uv run watchtower-core query artifacts --artifact-family initiative_state --format json
```

```sh
cd core/python
uv run watchtower-core query readiness --ready-for-execution true --format json
```

```sh
cd core/python
uv run watchtower-core query projects --slug watchtower --format json
```

```sh
cd core/python
uv run watchtower-core query project-context --project-slug watchtower --format json
```

```sh
cd core/python
uv run watchtower-core query planning --trace-id trace.core_python_foundation --format json
```

```sh
cd core/python
uv run watchtower-core query initiatives --initiative-status completed --format json
```

```sh
cd core/python
uv run watchtower-core query authority --domain planning --format json
```

## Behavior and Outputs
- With no leaf command, the group prints help and exits successfully.
- Every leaf command is read-only and supports `--format human` or `--format json`.
- Use `plan/.wt/indexes/coordination_index.json` as the live plan-workspace machine start-here path for current planning state and next action.
- Use `plan/.wt/indexes/artifact_index.json` when the question spans multiple live plan artifact families or you need canonical machine artifact paths and context metadata.
- Use `plan/.wt/indexes/readiness_index.json` for execution-gate lookup, `plan/.wt/indexes/discrepancy_index.json` for blocking drift, `plan/.wt/indexes/evidence_index.json` for live validation bundles, `plan/.wt/indexes/closeout_index.json` for closeout recaps, `plan/.wt/indexes/review_index.json` for review state, and `plan/.wt/indexes/project_index.json` for project-container browse.
- Use `project-context` when the operation is project-scoped and you need the validated project record, initiative root, and linked repositories on top of always-loaded `pack_context`.
- Use `coordination` when you need the live machine start-here planning payload.
- Use `artifacts` when you need cross-family live plan artifact lookup without opening raw JSON manually.
- Use `readiness` when the question is whether an initiative package may start or resume execution.
- Use `discrepancies` when you need mismatch, drift, or stale-surface records without opening one initiative directly.
- Use `plan-evidence` when you need the live initiative-local validation-bundle contract rather than durable validation evidence under `core/control_plane/ledgers/`.
- Use `closeouts` when you need the current closeout recap contract or terminal closeout summary for one live initiative.
- Use `reviews` when you need initiative review and promotion approval state on one joined machine surface.
- Use `projects` when you need project lookup without loading the full project context payload.
- Filterless `planning` and `initiatives` browse calls now default to `initiative_status=active`; pass explicit `--initiative-status` for terminal history and `--trace-id` when you already know the closed trace.
- Use `planning` after coordination when you need the canonical deep machine-readable record for one trace.
- Use `initiatives` when you need broader initiative-family browsing, filtered terminal history, or explicit non-active status lookup.
- Use `authority` when the main question is which planning or governance surface is canonical.
- Use `commands` or `paths` when the main task is discovery rather than planning-state inspection.
- Use `references --repository-status <status>` when you need only active-support, supporting-authority, or candidate-future guidance from the governed reference corpus.
- For exact filters and field behavior, open the leaf command page or CLI help for the selected query command.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core query coordination` | Live machine start-here planning lookup surface. |
| `watchtower-core query artifacts` | Cross-family machine artifact lookup surface for live `plan/**` state. |
| `watchtower-core query readiness` | Live readiness-gate lookup surface for initiative execution state. |
| `watchtower-core query discrepancies` | Live mismatch and drift lookup surface for plan discrepancies. |
| `watchtower-core query plan-evidence` | Live initiative-local evidence-bundle lookup surface. |
| `watchtower-core query closeouts` | Live initiative-local closeout recap lookup surface. |
| `watchtower-core query reviews` | Live initiative and promotion review-state lookup surface. |
| `watchtower-core query projects` | Live project-container browse surface. |
| `watchtower-core query project-context` | Explicit project-scoped runtime context load on top of pack context. |
| `watchtower-core query planning` | Canonical deep planning join for one trace. |
| `watchtower-core query initiatives` | Broader initiative-family and historical-status lookup. |
| `watchtower-core query authority` | Canonical-surface resolver for planning and governance questions. |
| `watchtower-core` | Root command that dispatches to this group. |

## Source Surface
- `core/python/src/watchtower_core/cli/query_family.py`
- `core/python/src/watchtower_core/cli/query_discovery_family.py`
- `core/python/src/watchtower_core/cli/query_knowledge_family.py`
- `core/python/src/watchtower_core/cli/query_records_family.py`
- `core/python/src/watchtower_core/cli/query_coordination_family.py`
- `core/python/src/watchtower_core/repo_ops/query/`
- `core/python/src/watchtower_core/repo_ops/project_context.py`

## Updated At
- `2026-03-17T22:39:20Z`
