# `core/python`

## Description
`This directory contains the shared Python tooling, tests, reusable core package, and local environment surfaces for the repository. Keep reusable package code here under watchtower_core, keep only narrow plan-owned repo-local code under plan/python/, and keep authored control-plane artifacts in core/control_plane/. The shared dev environment also installs the plan-owned package from plan/python/ as an editable local dependency.`

## Boundaries
`Use one local virtual environment at core/python/.venv/. Keep caches, wheels, build outputs, and egg-info directories ignored. Do not place canonical schemas, registries, contracts, manifests, or indexes in this subtree. Treat watchtower_core as reusable core, treat watchtower_plan as the narrow repo-local plan boundary, and keep live plan machine state under plan/.wt/ rather than in the Python workspace.`

## Paths
| Path | Description |
|---|---|
| `core/python/AGENTS.md` | Defines Python-workspace-specific instructions for agents working under this subtree. |
| `core/python/README.md` | Describes the purpose of the Python workspace and the standard onboarding flow. |
| `core/python/.gitignore` | Ignores the local virtual environment, caches, and build outputs. |
| `core/python/pyproject.toml` | Canonical Python project and tool configuration for the core helper and harness package. |
| `core/python/uv.lock` | Locked dependency graph used for repeatable local onboarding. |
| `core/python/src/` | Holds the `watchtower_core` reusable-core package source tree. |
| `core/python/src/watchtower_core/**/README.md` | Package-level runtime boundary docs for the reusable-core namespaces. |
| `core/python/src/watchtower_host/README.md` | Describes the host-owned CLI composition boundary for the `watchtower-core` binary. |
| `core/python/tests/` | Holds Python tests and fixtures for package behavior, validation, and sync/query flows. |
| `core/python/tools/` | Holds small workspace-local helper scripts such as `dev_shell.sh` when they are warranted. |

## Onboarding
### Quick Start
1. `cd core/python`
2. `uv python install`
3. `uv sync --extra dev`
4. `uv run watchtower-core doctor`

### Daily Use
- Default path: run commands with `uv run ...` from `core/python/`. This uses the workspace environment without requiring manual activation.
- `uv sync --extra dev` installs both `watchtower_core` and the local `watchtower_plan` package into the shared workspace environment.
- Interactive shell path: run `./tools/dev_shell.sh` when you want a shell with `.venv` activated for repeated local commands.
- Manual fallback: run `source .venv/bin/activate` if you specifically want to activate the environment in your current shell.

### Common Commands
- `uv run pytest -q`
- `./.venv/bin/python -m pytest tests/unit tests/integration -q`
- `uv run ruff check .`
- `uv run mypy src`
- `uv run watchtower-core --help`
- `uv run watchtower-core doctor`
- `uv run watchtower-core route preview --request "review the workflow docs against the current CLI behavior"`
- `uv run watchtower-core route preview --request "do a documentation review of the command docs" --format json`
- `uv run watchtower-core route preview --task-type "Foundations Alignment Review" --format json`
- `uv run watchtower-core plan bootstrap --trace-id trace.example --title "Example Initiative" --summary "Bootstraps the example initiative." --format json`
- `uv run watchtower-core plan confirm-inputs --initiative-slug example_initiative --format json`
- `uv run watchtower-core plan approve --initiative-slug example_initiative --format json`
- `uv run watchtower-core query coordination --format json`
- `uv run watchtower-core query artifacts --artifact-family initiative_state --format json`
- `uv run watchtower-core query readiness --ready-for-execution true --format json`
- `uv run watchtower-core query projects --slug watchtower --format json`
- `uv run watchtower-core query project-context --project-slug watchtower --format json`
- `uv run watchtower-core query authority --domain planning --format json`
- `uv run watchtower-core query commands --query coordination --format json`
- `uv run watchtower-core query foundations --query philosophy`
- `uv run watchtower-core query workflows --query validation`
- `uv run watchtower-core query references --query uv`
- `uv run watchtower-core query references --repository-status candidate_future_guidance --format json`
- `uv run watchtower-core query standards --category governance --format json`
- `uv run watchtower-core query tasks --task-status planned`
- `uv run watchtower-core query tasks --blocked-only --include-dependency-details`
- `uv run watchtower-core plan task transition --task-id task.example.001 --task-status completed --format json`
- `uv run watchtower-core query acceptance --trace-id trace.core_python_foundation`
- `uv run watchtower-core query evidence --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core query initiatives --current-phase capture`
- `uv run watchtower-core sync all`
- `uv run watchtower-core sync coordination`
- `uv run watchtower-core sync route-index`
- `uv run watchtower-core sync initiative-index`
- `uv run watchtower-core sync task-index`
- `uv run watchtower-core sync github-tasks --repo owner/repo`
- `uv run watchtower-core sync github-tasks --repo owner/repo --no-label-sync`
- `uv run watchtower-core closeout plan-initiative --initiative-slug plan_example --initiative-status completed --closure-reason "Delivered and validated" --write`
- `uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Closed the retained traced planning package"`
- `uv run watchtower-core closeout purge-trace --trace-id trace.example --retained-authority-path plan/docs/standards/governance/planning_retention_and_purge_standard.md`
- `uv run watchtower-core validate all --skip-acceptance`
- `uv run watchtower-core validate suite --suite-id suite.example.validation_baseline --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json --format json`
- `uv run watchtower-core validate document-semantics --path core/workflows/modules/code_validation.md`
- `uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core validate artifact --path /tmp/pack_note.json --schema-id urn:watchtower:schema:external:pack-note:v1 --supplemental-schema-path /tmp/pack_schemas --format json`

## Command Docs
- Start with [README.md](/core/docs/commands/core_python/README.md) for command-doc navigation.
- Open [watchtower_core.md](/core/docs/commands/core_python/watchtower_core.md) for the root command and shared options.
- Open [watchtower_core_route.md](/core/docs/commands/core_python/watchtower_core_route.md) when you need a route preview for a request or explicit task type.
- Open [watchtower_core_plan.md](/core/docs/commands/core_python/watchtower_core_plan.md) when you need live initiative bootstrap or readiness-gate commands.
- Open [watchtower_core_validate_suite.md](/core/docs/commands/core_python/watchtower_core_validate_suite.md) when you need the pack-declared suite runtime and `--pack-settings-path` behavior.
- Use the group pages for deeper browsing:
  - [watchtower_core_plan.md](/core/docs/commands/core_python/watchtower_core_plan.md)
  - [watchtower_core_query.md](/core/docs/commands/core_python/watchtower_core_query.md)
  - [watchtower_core_plan_task.md](/core/docs/commands/core_python/watchtower_core_plan_task.md)
  - [watchtower_core_sync.md](/core/docs/commands/core_python/watchtower_core_sync.md)
  - [watchtower_core_validate.md](/core/docs/commands/core_python/watchtower_core_validate.md)
  - [watchtower_core_closeout.md](/core/docs/commands/core_python/watchtower_core_closeout.md)
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the machine-readable command lookup surface.

### Commands Inside `./tools/dev_shell.sh`
- `watchtower-core --help`
- `watchtower-core doctor`
- `pytest -q`
- `ruff check .`
- `mypy src`

### Notes
- `uv run ...` is the default workflow for this repository.
- `uv run pytest -q` is the fast local default and collects only `core/python/tests/unit/`.
- Use `./.venv/bin/python -m pytest tests/unit tests/integration -q` for the broad Python validation pass when a change touches repo-materialization, workspace orchestration, or multi-surface CLI behavior.
- `uv run watchtower-core doctor` is the fastest non-mutating baseline health snapshot before a full `sync all` or `validate all` run.
- `uv run watchtower-core route preview --request "<text>"` is the fastest advisory check for how the current routing surfaces map a request onto workflow modules.
- Bounded documentation and standards review prompts now route to `Documentation Review` instead of requiring repository-review wording.
- `uv run watchtower-core route preview --task-type "Foundations Alignment Review" --format json` is the explicit preview path when a task is about keeping docs or workflow guidance aligned with repository foundations.
- `plan/.wt/indexes/coordination_index.json` is the live machine-readable current-state entrypoint for the plan workspace.
- `uv run watchtower-core query project-context --project-slug <slug> --format json` is the explicit runtime proof path for loading `project_context` on top of always-loaded `pack_context` for project-scoped work.
- `uv run watchtower-core query coordination --format json` is the live plan-workspace machine start-here command backed by `plan/.wt/indexes/coordination_index.json`.
- `uv run watchtower-core query artifacts --format json` exposes the cross-family live artifact lookup under `plan/.wt/indexes/artifact_index.json`.
- `uv run watchtower-core query readiness --format json`, `query discrepancies --format json`, and `query projects --format json` expose the live readiness, discrepancy, and project indexes under `plan/.wt/indexes/`.
- Use `uv run watchtower-core query coordination --initiative-status <status> --format json` or `uv run watchtower-core query initiatives --initiative-status <status> --format json` when you need explicit non-active initiative lookup without treating the default coordination payload as a full history surface.
- The decision, design, implementation, initiative, and task tracking sync commands rebuild summary-first human trackers with companion terminal-history tables. Use the paired `query` commands when you need exact filtered machine lookup.
- `uv run watchtower-core plan bootstrap --include-decision --write ...` seeds a live initiative package in pre-execution review and leaves bootstrap-only traces in `capture` until non-bootstrap active work exists.
- `uv run watchtower-core plan confirm-inputs --write ...` records maintainer confirmation of the current initiative-authored inputs before execution approval.
- `uv run watchtower-core plan approve --write ...` is the explicit live readiness gate that moves one initiative package into `ready_for_execution` before execution-status task transitions are allowed.
- `uv run watchtower-core closeout plan-initiative --write ...` is the default live closeout path for `plan/**` initiative packages and refreshes the initiative-local artifacts plus the pack and project coordination surfaces in the same slice.
- `uv run watchtower-core closeout initiative --write ...` is compatibility-only and must fail closed back to `closeout plan-initiative` for live `plan/**` initiatives.
- `uv run watchtower-core closeout purge-trace --write ...` deletes one eligible closed trace package, writes the minimal purge ledger, and then refreshes all derived governed surfaces.
- `uv run watchtower-core plan task create|update|transition --write ...` writes initiative-local live task state under `plan/**/.wt/tasks/**`, refreshes the live plan indexes and rendered views, still requires `--trace-id` when traced `related_ids` are present, and fails closed if an execution-starting status is requested before the initiative package is approved into `ready_for_execution`.
- `uv run watchtower-core query authority --domain planning --format json` resolves which planning or governance surface is canonical when routing is still unclear.
- `uv run watchtower-core query references --related-path core/python/ --format json` now treats trailing-slash directory paths as descendant touchpoint filters and returns only references with real current touchpoints under that directory.
- `uv run watchtower-core sync coordination` now refreshes the derived coordination index in the same deterministic slice as task, traceability, and initiative surfaces.
- `watchtower_core` is the reusable-core namespace. Push generic loaders, validators, query helpers, sync helpers, adapters, and utilities back into `watchtower_core` when they stop being plan-specific.
- `watchtower_plan` is the narrow repo-local plan boundary under `plan/python/`; do not grow it into a plan-flavored mirror of `watchtower_core`.
- `plan/.wt/` is live plan machine state only. Keep Python source, workflow prose, and hand-maintained implementation logic out of that tree.
- `source .venv/bin/activate` is optional and mainly useful for interactive shell sessions.
- `./tools/dev_shell.sh` is for interactive use and does not require `uv` once the shell is active.
- If you used `./tools/dev_shell.sh`, leave the activated shell with `exit`.
- If you activated the environment manually, leave it with `deactivate`.

## Runtime Architecture
Start with `core/python/src/watchtower_core/README.md` when you need the runtime package map before reading code.

| Package README | Classification | Notes |
|---|---|---|
| `core/python/src/watchtower_core/README.md` | `runtime_architecture_start_here` | Top-level reusable-core package map and navigation. |
| `core/python/src/watchtower_host/README.md` | `host_composition` | Host-owned CLI parser, registry, and entrypoint composition for the `watchtower-core` binary. |
| `core/python/src/watchtower_core/control_plane/README.md` | `reusable_core` | Workspace, loader, schema, and typed artifact boundary. |
| `core/python/src/watchtower_core/documentation/README.md` | `reusable_core` | Repo-shared governed-document semantics, front-matter path normalization, and standard/reference helper logic. |
| `core/python/src/watchtower_core/validation/README.md` | `reusable_core` | Export-safe validation services, suite orchestration, and aggregate baseline helpers; repo-local document semantics stay under `watchtower_plan.validation`. |
| `core/python/src/watchtower_core/query/README.md` | `reusable_core` | Export-safe generic query services over governed indexes, routes, pack surfaces, knowledge docs, records, and artifact families; live plan coordination and task queries stay under `watchtower_plan.query`. |
| `core/python/src/watchtower_core/sync/README.md` | `reusable_core` | Export-safe sync harness plus repo-shared command, route, and repository-path index rebuild services; live plan sync orchestration stays under `watchtower_plan.sync`. |
| `core/python/src/watchtower_core/rebuild/README.md` | `reusable_core` | Export-safe rebuild harness plus registry-backed rendered-view building and markdown reconciliation. |
| `core/python/src/watchtower_core/routing/README.md` | `reusable_core` | Export-safe route-selection runtime over governed route and workflow indexes. |
| `core/python/src/watchtower_core/workflow_execution/README.md` | `reusable_core` | Export-safe workflow execution harness over routed workflow selection and metadata. |
| `core/python/src/watchtower_core/evidence/README.md` | `reusable_core` | Validation-evidence recording plus reusable evidence-bundle helpers. |
| `core/python/src/watchtower_core/integrations/README.md` | `boundary_layer` | External-system client boundary, currently including GitHub. |
| `core/python/src/watchtower_core/closeout/README.md` | `boundary_layer` | Fail-closed compatibility guard; plan-domain closeout services live under `plan/python/src/watchtower_plan/closeout/`. |
| `plan/python/src/watchtower_plan/README.md` | `repo_local_orchestration` | WatchTowerPlan-specific repo-local plan orchestration under the approved plan-owned Python boundary. |
| `core/python/src/watchtower_core/cli/README.md` | `boundary_guard` | Compatibility import surface plus remaining family and handler modules while host-owned CLI composition lives under `watchtower_host`. |
| `core/python/src/watchtower_core/utils/README.md` | `reusable_core` | Narrow shared helpers that do not justify a first-class package. |

Use the nested READMEs under `plan/python/src/watchtower_plan/`, `integrations/github/`, and the reusable-core subpackages when you need the next layer of boundary detail.

## Agent Use
- Read `core/python/AGENTS.md` before making changes under this workspace.
- Use [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md) as the authoritative guide for Python naming, module boundaries, typed interfaces, docstrings, and consolidation decisions.
- Run Python package commands from `core/python/`.
- Prefer `uv run` for tests, linting, typing, and CLI execution.
- When a command supports structured output, prefer `--format json` for agent or workflow consumption instead of parsing human-readable text.
- Keep `pyproject.toml`, `uv.lock`, and command docs aligned when the Python execution contract changes.
- Expect reusable-core packages such as `adapters`, `validation`, `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, and `utils` to satisfy a stricter `mypy` override than plan-owned repo-local surfaces.

## Programmatic Use
- `watchtower_core.control_plane.WorkspaceConfig` supports alternate logical workspace prefixes through direct construction when a non-default repository layout is needed.
- `ControlPlaneLoader.load_pack_settings()` exposes the repository's current pack-settings load root as a typed reusable-core startup surface.
- `ControlPlaneLoader.load_pack_context()` materializes a reusable `PackContext` by loading pack settings and the surfaces declared there.
- `ControlPlaneLoader.load_validation_suite_registry()` exposes the active validation-suite registry, including pack-declared suite baselines.
- `watchtower_core.control_plane.SupplementalSchemaDocument` lets external consumers register additional schemas in-memory for validation without modifying this repository's canonical schema catalog.
- `ControlPlaneLoader(... supplemental_schema_paths=...)` and `SchemaStore.from_workspace(... supplemental_schema_paths=...)` let callers load supplemental schemas from explicit files or directories for bounded external artifact validation.
- `watchtower_core.validation.suite.ValidationSuiteService` runs declared validation suites against the active pack settings surface, including pack-local schema and validator registries.
- `watchtower_plan` is the approved internal plan-pack consumer boundary under `plan/python/src/watchtower_plan/`; keep pack-agnostic loading and validation logic out of that namespace, and move generic behavior back into reusable-core packages when it stops being plan-specific.
- `watchtower_plan` should be consumed through the shared workspace installation contract, not through repo-local `sys.path` mutation.
- `watchtower_plan` is not a second generic Python root and not a mirror of `watchtower_core`; keep it narrow and repo-local.
- The Python design target is boring, explicit, and easy to consolidate: prefer one canonical implementation, extract generic behavior before growing repo-local plan-only surfaces, and keep CLI or doc-facing modules thin.
- The default lint baseline now includes Ruff comprehension checks, and the reusable-core package subset is held to stricter `mypy` rules than the plan-owned repo-local surfaces while those domain modules continue tightening.
