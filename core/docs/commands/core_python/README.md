# `core/docs/commands/core_python`

## Description
`This directory contains shared and reusable-core command pages for the core Python workspace and the watchtower-core CLI family. Use it to find the root command, shared command groups, and the highest-signal shared leaf pages before falling back to machine-readable command lookup.`

## Notes
- Start with `watchtower_core.md` for the root command and shared options.
- Use `watchtower_core_benchmark.md` when the main question is deliberate performance benchmarking rather than operational telemetry.
- Use `watchtower_core_telemetry.md` when the main question is runtime telemetry cleanup or sink hygiene.
- Use `watchtower_core_route.md` when the main question is how a request maps to workflow documents.
- Use `watchtower_core_git.md` when the main question is stale branch review, worktree cleanup, or local git hygiene automation.
- Use `watchtower_core_query.md` when the main question is which shared read-only lookup surface to use.
- Use `watchtower_core_query_authority.md` when the first question is which governed surface is canonical.
- Use `watchtower_core_query_templates.md` before drafting or materially restructuring governed docs whose shape is already defined.
- Use `watchtower_core_release.md` when the main question is the local release-gate or staged customer handoff flow.
- Use `watchtower_core_sync.md` when the main question is which shared derived artifact to rebuild.
- For pack-owned command groups and leaf pages, start in the owning pack command-doc root such as `<pack-root>/docs/commands/core_python/`.
- Use the command-group pages before opening individual subcommand pages.
- Use `watchtower_core_validate_suite.md` when the main question is how to run one pack-declared validation suite with optional `pack_settings` selection.
- Use `watchtower_core_validate_schema.md` when the main question is how to validate a `*.schema.json` definition file directly.
- Use `watchtower_core_pack_extract_core.md` when the main question is engineering repo-to-repo `core/` refresh rather than customer-safe export.
- Use `watchtower_core_pack_apply_core.md` when the main question is how to replace the local `core/` tree from a staged engineering extract without deleting `.venv` or caches.
- Use `watchtower_core_pack_bootstrap.md` when the main question is copied-core startup, donor-pack scrub and reload, or the shared hosted-pack registry and workspace wiring flow.
- Prefer `uv run watchtower-core query authority --query <question> --format json` when you need the canonical lookup surface before scanning docs or indexes directly.
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the governed machine lookup surface instead of browsing this directory.

## Files
| Path | Description |
|---|---|
| `core/docs/commands/core_python/README.md` | Describes the purpose of the core Python command-doc directory and the fastest ways to find command details. |
| `core/docs/commands/core_python/watchtower_core.md` | Human-readable page for the root `watchtower-core` command and shared CLI behavior. |
| `core/docs/commands/core_python/watchtower_core_benchmark.md` | Entry page for governed reusable-core benchmark commands. |
| `core/docs/commands/core_python/watchtower_core_benchmark_run.md` | Runs one governed benchmark suite and can retain the resulting benchmark record. |
| `core/docs/commands/core_python/watchtower_core_git.md` | Entry page for local branch and worktree hygiene commands. |
| `core/docs/commands/core_python/watchtower_core_git_hygiene.md` | Evaluates local branch and worktree old-state status and can apply conservative cleanup. |
| `core/docs/commands/core_python/watchtower_core_telemetry.md` | Entry page for local runtime telemetry cleanup commands. |
| `core/docs/commands/core_python/watchtower_core_telemetry_delete.md` | Deletes or previews retained runtime telemetry files under one telemetry root. |
| `core/docs/commands/core_python/watchtower_core_route.md` | Entry page for advisory route preview commands. |
| `core/docs/commands/core_python/watchtower_core_query.md` | Entry page for shared governed query commands such as authority resolution, command discovery, repository paths, templates, standards, references, foundations, workflows, acceptance, evidence, and benchmarks. |
| `core/docs/commands/core_python/watchtower_core_query_benchmarks.md` | Searches retained benchmark records captured by the reusable-core benchmarking runtime. |
| `core/docs/commands/core_python/watchtower_core_query_authority.md` | Resolves which shared governed surface is canonical for a recurring governance question. |
| `core/docs/commands/core_python/watchtower_core_query_templates.md` | Searches the governed template catalog for required sections, allowed roots, and authoring guidance. |
| `core/docs/commands/core_python/watchtower_core_release.md` | Entry page for the local release-gate command family. |
| `core/docs/commands/core_python/watchtower_core_release_check.md` | Runs the local release gate and stages one final export. |
| `core/docs/commands/core_python/watchtower_core_query_foundations.md` | Query foundations by topic, related surface, authority, or downstream citation or application use. |
| `core/docs/commands/core_python/watchtower_core_query_commands.md` | Machine-readable lookup page for finding any other current command page without scanning the directory manually. |
| `core/docs/commands/core_python/watchtower_core_sync.md` | Entry page for reusable-core sync commands such as command, route, and repository-path rebuilds. |
| `core/docs/commands/core_python/watchtower_core_validate.md` | Entry page for validation commands across artifacts, semantics, and repo-wide checks. |
| `core/docs/commands/core_python/watchtower_core_validate_schema.md` | Validates one JSON Schema definition file against the Draft 2020-12 metaschema. |
| `core/docs/commands/core_python/watchtower_core_validate_suite.md` | Runs one pack-declared validation suite through the reusable-core suite runtime. |
| `core/docs/commands/core_python/watchtower_core_pack_extract_core.md` | Stages a donor-neutral shared-core extract for engineering repo-to-repo reuse. |
| `core/docs/commands/core_python/watchtower_core_pack_apply_core.md` | Applies a staged engineering shared-core extract into the local repository core/ tree. |
| `core/docs/commands/core_python/watchtower_core_doctor.md` | Fastest non-mutating health snapshot for the Python workspace and governed repository surfaces. |
