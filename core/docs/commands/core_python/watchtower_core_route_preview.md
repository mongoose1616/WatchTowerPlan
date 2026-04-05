# `watchtower-core route preview`

## Summary
This command previews the routed workflow documents for either free-form request text or one explicit task type using the governed route and workflow indexes.

## Use When
- You want to see which workflow documents a request is likely to activate before executing the task.
- You already know the routed task type and want the exact required workflow set.
- You need structured JSON output for agent or workflow orchestration.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core route preview` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/route_family.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core route preview (--request <text> | --task-type <task_type>) [--format <human|json>]
```

## Arguments and Options
- `--request <text>`: Free-form request text to score against the governed route index.
- `--task-type <task_type>`: Exact routed task-type label from the governed route index.
- `--format <human|json>`: Select human-readable or structured JSON output. Use `json` for scripts, workflows, or agent calls.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core route preview --request "implement the feature and validate it"
```

```sh
cd core/python
uv run watchtower-core route preview --request "review code and commit the change" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "review the WatchTower report and fix the valid issues with planning, tasks, validation, and commits" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "fix the findings from this review and rerun the same review until clean" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "run a full-spectrum adversarial audit of the repository" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "run an adversarial code review" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "i want a documentation and fix loop" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "i want a adversarial telemetry, benchmark review and fix" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "do an adversarial stale test cleanup" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "i want a adversarial project coherence and fix loop" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "documentation and fix loop and commit" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "adversarial telemetry, benchmark review and fix and commit" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "validator audit and remediation loop" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "improve the workflow stuff" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "review the workflow docs against the current CLI behavior and lookup surfaces" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "reconcile command docs with current cli behavior" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "reconcile schema-backed indexes examples and validators for one artifact family" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "do a documentation review of the command docs" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --request "hand off this task from implementation to validation and create successor tasks" --format json
```

```sh
cd core/python
uv run watchtower-core route preview --task-type "Foundations Alignment Review"
```

## Behavior and Outputs
- The command is read-only and does not mutate repository state.
- Exactly one route selector is required: either `--request` or `--task-type`.
- In `human` mode, the command prints the selected routed task types, matched trigger keywords, and the merged active workflow-document set.
- In `json` mode, the command prints one JSON object with the command name, selected routes, selected workflows, any activated governed intents, any advisory `assisted_module_suggestions`, and any warnings.
- Selected workflow-role records in the JSON payload include `composes_module_paths` so explicit role-to-module orchestration remains auditable alongside the routed workflow set.
- Free-form request matching is deterministic and advisory. It scores exact phrases first, then falls back to canonicalized trigger-keyword coverage so realistic maintenance requests and adjacent-route prompts do not require verbatim routing-table phrasing.
- When one route is materially stronger than the others, the preview keeps only the dominant route plus any materially strong secondary matches instead of leaking in low-signal single-word matches. Successor-task handoff prompts stay on `Task Phase Transition` even though that workflow later opens the lifecycle rules as supporting context.
- Route preview now resolves base routes from the route index, then applies governed overlay intent rules from `route_overlay_registry.json` and governed suppression rules from `route_merge_policy_registry.json` so modifiers such as `adversarial` and `commit` stay flexible without exploding the routing table into hardcoded permutations.
- The JSON and human outputs now include `activated_intents` so companion-route attachment and modifier overlays remain auditable instead of appearing as opaque scorer side effects. The payload only keeps intents that still apply after route selection and merge-policy cleanup, so dedicated routes do not report redundant modifier overlays that never actually attach.
- When governed overlay intent explicitly asks for a companion route such as `fix loop` or `commit`, route preview now resolves dominant substantive routes first and attaches that companion route afterward instead of letting the companion route win the main score pass by itself.
- Overlay-attached companion routes can now be synthesized directly from the governed route index when the overlay intent is explicit even if the base scorer did not independently hit that companion route, so prompts such as `validator audit and remediation loop` or `workflow audit and fix loop` keep both the origin review family and the remediation loop.
- More specific governed intents can now suppress broader overlapping intents in the activated-intent set, so `fix loop` requests report the remediation-loop intent without also keeping the single-pass remediation intent active.
- This also means mixed prompts such as `adversarial refactor, standard adherence, and fix loop` can keep implementation and standards-alignment scope while still attaching the remediation loop and adversarial lens.
- Review-remediation prompts that focus on fixing findings or rerunning the same review until clean now route to dedicated remediation task types, and prompts such as `documentation and fix loop`, `benchmark review and fix loop`, or `project coherence and fix loop` can keep the paired review family in the same preview instead of collapsing to remediation alone.
- Natural-language maintenance variants such as `docs audit and fix loop`, `review and fix`, `audit and fix`, and `stale test cleanup` now score strongly enough to keep the intended remediation or optimization route instead of falling through to a generic validation match.
- Explicit commit intent now stays as a companion closeout route for substantive work such as reviews, fix loops, refactors, and benchmark remediation instead of displacing the main task family.
- Explicit adversarial audit prompts still route to `Adversarial Repository Review` when the request is repository-scoped, but an `adversarial` modifier can now overlay compatible code-review, documentation-review, workflow-governance, standards-alignment, validation-harness, benchmarking, implementation, test-optimization, and remediation routes without forcing everything through the repository-audit permutation.
- Bounded documentation and standards review prompts now route to `Documentation Review` instead of falling through to no match or a broad repository review.
- Foundations-aware documentation-alignment prompts can now select the explicit `Foundations Alignment Review` task type, which combines foundations context loading with documentation refresh.
- Adjacent route boundaries worth remembering:
  - Use `Documentation-Implementation Reconciliation` for command docs, README, example, or lookup-surface drift around live behavior.
  - Use `Governed Artifact Reconciliation` for schema, example, index, registry, or validator coherence inside one artifact family.
  - Use `Traceability Reconciliation` for traced planning links, trackers, and family-index drift.
  - Use `Task Lifecycle Management` for creating or editing task records; use `Task Phase Transition` when the main action is a handoff or successor-task boundary, including creating successor tasks for the next phase.
- The authored routing surfaces remain authoritative when a human or agent executes the task.
- Workflow-role `composes_module_paths` describe explicit role composition, but they do not activate workflow modules outside the routed workflow set.
- If no route matches the request text strongly enough, the command exits successfully with an empty selection plus a warning to refine the request or use `--task-type`; when the request still overlaps a workflow family, the JSON payload also includes advisory `assisted_module_suggestions` derived from the workflow index for agent-assisted module loading.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core route` | Parent command group for route preview operations. |
| `watchtower-core sync route-index` | Rebuilds the route index this command reads. |
| `watchtower-core query workflows` | Searches the companion workflow index for the selected workflow documents. |

## Source Surface
- `core/python/src/watchtower_host/cli/route_family.py`
- `core/python/src/watchtower_host/cli/route_handlers.py`
- `core/python/src/watchtower_core/query/routes.py`
- `core/control_plane/indexes/routes/route_index.json`
- `core/control_plane/registries/route_overlay_registry.json`
- `core/control_plane/registries/route_merge_policy_registry.json`

## Updated At
- `2026-04-05T09:05:00Z`
