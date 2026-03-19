# `core/docs/commands/core_python`

## Description
`This directory contains command pages for the core Python workspace and the watchtower-core CLI family. Use it to find the root command, the main command groups, and the highest-signal leaf pages to open before falling back to machine-readable command lookup.`

## Notes
- Start with `watchtower_core.md` for the root command and shared options.
- Use `watchtower_core_route.md` when the main question is how a request maps to workflow modules.
- Use `watchtower_core_plan.md` when the main question is how to scaffold planning artifacts, bootstrap a traced planning chain, or advance a live initiative through confirmation and approval.
- Use `watchtower_core_query.md` when the main question is which read-only lookup surface to use, then open `watchtower_core_query_foundations.md` when the question is which foundation document governs a surface or which docs cite or apply it.
- Use `watchtower_core_task.md` when the main question is how to create, update, or transition initiative-local live task records.
- Use `watchtower_core_sync.md` when the main question is which derived artifact to rebuild, then open `watchtower_core_sync_foundation_index.md` when a foundations change needs the machine-readable intent index refreshed.
- Use the command-group pages before opening individual subcommand pages.
- Use `watchtower_core_query_coordination.md` when the main question is current live planning state, next action, and active work context.
- Use `watchtower_core_query_artifacts.md` when the main question spans multiple live plan artifact families or needs canonical machine artifact paths and context metadata.
- Use `watchtower_core_query_readiness.md` when the main question is whether initiative packages are execution-ready.
- Use `watchtower_core_query_discrepancies.md` when the main question is blocking drift, mismatches, or derived-surface discrepancies.
- Use `watchtower_core_query_plan_evidence.md` when the main question is the live initiative-local evidence contract or validation bundle state.
- Use `watchtower_core_query_closeouts.md` when the main question is live closeout state, expected outcome, or promotion-review expectation.
- Use `watchtower_core_query_reviews.md` when the main question is initiative or promotion review state without stitching readiness and promotion records together manually.
- Use `watchtower_core_query_projects.md` when the main question is which project containers exist before loading a full project context.
- Use `watchtower_core_query_project_context.md` when the main question is how to load one validated project-scoped runtime context on top of the always-loaded pack context.
- Use `watchtower_core_query_authority.md` when the main question is which machine surface is canonical for a planning or governance lookup.
- Use `watchtower_core_validate_suite.md` when the main question is how to run one pack-declared validation suite with optional `pack_settings` selection.
- The family tracking sync pages describe summary-first trackers with companion terminal-history tables. Use the paired `query` commands when you need filtered machine lookup or one exact trace/task record.
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the governed machine lookup surface instead of browsing this directory.

## Files
| Path | Description |
|---|---|
| `core/docs/commands/core_python/README.md` | Describes the purpose of the core Python command-doc directory and the fastest ways to find command details. |
| `core/docs/commands/core_python/watchtower_core.md` | Human-readable page for the root `watchtower-core` command and shared CLI behavior. |
| `core/docs/commands/core_python/watchtower_core_route.md` | Entry page for advisory route preview commands. |
| `core/docs/commands/core_python/watchtower_core_plan.md` | Entry page for planning scaffold and bootstrap commands. |
| `core/docs/commands/core_python/watchtower_core_plan_confirm_inputs.md` | Confirms reviewed initiative-authored inputs into machine state before approval. |
| `core/docs/commands/core_python/watchtower_core_plan_approve.md` | Approves one live initiative package into `ready_for_execution`. |
| `core/docs/commands/core_python/watchtower_core_query.md` | Entry page for all governed query commands, including coordination, standards, references, and trace surfaces. |
| `core/docs/commands/core_python/watchtower_core_query_artifacts.md` | Query page for the live cross-family plan artifact index under `plan/.wt/indexes/artifact_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_readiness.md` | Query page for live initiative readiness and execution-gate state under `plan/.wt/indexes/readiness_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_discrepancies.md` | Query page for live plan discrepancy records under `plan/.wt/indexes/discrepancy_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_plan_evidence.md` | Query page for live initiative-local evidence bundles under `plan/.wt/indexes/evidence_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_closeouts.md` | Query page for live closeout recaps under `plan/.wt/indexes/closeout_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_reviews.md` | Query page for live initiative and promotion review state under `plan/.wt/indexes/review_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_projects.md` | Query page for pack-level project lookup under `plan/.wt/indexes/project_index.json`. |
| `core/docs/commands/core_python/watchtower_core_query_project_context.md` | Loads the explicit machine-first runtime context for one project container under `plan/projects/**`. |
| `core/docs/commands/core_python/watchtower_core_query_foundations.md` | Query foundations by topic, related surface, authority, or downstream citation or application use. |
| `core/docs/commands/core_python/watchtower_core_query_coordination.md` | Machine start-here command page for active traced initiative coordination and next-step lookup. |
| `core/docs/commands/core_python/watchtower_core_query_authority.md` | Canonical surface-discovery query page for planning and governance questions. |
| `core/docs/commands/core_python/watchtower_core_query_commands.md` | Machine-readable lookup page for finding any other current command page without scanning the directory manually. |
| `core/docs/commands/core_python/watchtower_core_task.md` | Entry page for task lifecycle commands that mutate initiative-local live task records in dry-run or write mode. |
| `core/docs/commands/core_python/watchtower_core_sync.md` | Entry page for all sync commands, including full repo rebuilds and narrower index/tracking refreshes. |
| `core/docs/commands/core_python/watchtower_core_sync_foundation_index.md` | Rebuild surface for the machine-readable foundation index derived from governed foundation docs. |
| `core/docs/commands/core_python/watchtower_core_validate.md` | Entry page for validation commands across artifacts, semantics, and repo-wide checks. |
| `core/docs/commands/core_python/watchtower_core_validate_suite.md` | Runs one pack-declared validation suite through the reusable-core suite runtime. |
| `core/docs/commands/core_python/watchtower_core_closeout.md` | Entry page for closeout commands used to terminally update traced initiative state. |
| `core/docs/commands/core_python/watchtower_core_closeout_plan_initiative.md` | Live plan-initiative closeout page for terminally updating one initiative package under `plan/**`. |
| `core/docs/commands/core_python/watchtower_core_closeout_purge_trace.md` | Governed purge page for deleting one eligible closed trace package and writing the minimal purge ledger. |
| `core/docs/commands/core_python/watchtower_core_doctor.md` | Fastest non-mutating health snapshot for the Python workspace and governed repository surfaces. |
