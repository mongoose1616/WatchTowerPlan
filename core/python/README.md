# `core/python`

## Description
`This directory contains the shared Python tooling, tests, reusable core package, and local environment surfaces for the repository. Keep reusable package code here under watchtower_core, keep pack-owned code only under the owning pack root, and keep authored control-plane artifacts in core/control_plane/. The shared dev environment may also install one or more hosted pack packages as editable local dependencies. Downstream WatchTower repositories may also consume this shared workspace by copying core/ and then wiring whichever hosted packs they actually carry.`

## Boundaries
`Use one local virtual environment at core/python/.venv/. Keep caches, wheels, build outputs, and egg-info directories ignored. Do not place canonical schemas, registries, contracts, manifests, or indexes in this subtree. Treat watchtower_core as reusable core, treat watchtower_<pack> packages as pack-owned boundaries, and keep live pack machine state under pack workspaces rather than in the Python workspace.`

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
| `core/python/src/watchtower_core/telemetry/README.md` | Describes the local runtime telemetry package, sink rules, and opt-out environment variables. |
| `core/python/src/watchtower_host/README.md` | Describes the host-owned CLI composition boundary for the `watchtower-core` binary. |
| `core/python/tests/` | Holds pack-neutral shared-core and host tests plus synthetic fixture data. |
| `<pack-root>/python/tests/` | Holds tests that import or exercise one hosted pack directly. |
| `core/python/tools/` | Holds small workspace-local helper scripts such as `dev_shell.sh` when they are warranted. |

## Onboarding
### Quick Start
1. `cd core/python`
2. Install `uv` if it is not already available on `PATH`.
3. `uv python install`
4. `uv sync --extra dev`
5. `uv run watchtower-core doctor`

### Install `uv`
- macOS and Linux standalone installer:
  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  uv --version
  ```
- Homebrew:
  ```sh
  brew install uv
  uv --version
  ```
- `pipx`:
  ```sh
  pipx install uv
  uv --version
  ```
- If the standalone installer updated your shell profiles but the current shell still cannot resolve `uv`, open a new shell or export the executable directory onto `PATH` before running `uv sync`. A common default on macOS and Linux is `export PATH="$HOME/.local/bin:$PATH"`.
- Use [uv_reference.md](/core/docs/references/uv_reference.md) for the upstream installation options, shell notes, and verification guidance.

### Daily Use
- Default path: run commands with `uv run ...` from `core/python/`. This uses the workspace environment without requiring manual activation.
- `uv sync --extra dev` installs `watchtower_core` and any repo-local hosted pack packages declared in the shared workspace metadata.
- `./.venv/bin/python` is useful after the workspace has already been synced, but it does not replace `uv sync` when the shared workspace metadata changes.
- In this repository, the shared workspace metadata currently includes one internal hosted pack. In a downstream repository that copies `core/`, the hosted-pack dependencies and local `tool.uv.sources` entries are repo-local configuration and should be updated to match the copied pack set instead of inheriting the donor repo's package list.
- Keep the test split explicit: `core/python/tests/` is the shared pack-neutral suite, while pack-owned tests live under the owning pack root such as `<pack-root>/python/tests/`.
- Keep the shared-core suite live-pack-neutral: if a test needs a real `watchtower_<pack>` import or depends on the live current-repository pack workspace being present, move it under the owning pack root or replace it with synthetic fixture-pack setup.
- During copied-core bring-up, `watchtower-core pack list`, `pack describe`, `pack validate`, selected pack namespaces, and `validate all` can discover a valid local pack from `<pack>/.wt/manifests/pack_settings.json` plus `<pack>/python/src` even before shared workspace wiring is persisted. Treat that as temporary bootstrap compatibility: `watchtower-core pack bootstrap --write` is the step that reconciles the shared hosted-pack registry, shared workspace metadata, and the shared command, repository-path, reference, standard, workflow, and route discovery surfaces for the copied repository.
- When a recipient repository copied `core/` exactly from a donor repository and needs to replace the donor hosted-pack wiring, run `watchtower-core pack bootstrap --pack-settings-path <recipient>/.wt/manifests/pack_settings.json --replace-hosted-packs --write --format json`. That scrub-and-reload mode removes donor pack registrations plus donor `core/python` workspace pack wiring before loading the recipient pack as the new default repository pack.
- When copying `core/` into another repo, copy source-owned files only. Do not carry over `core/python/.venv`, editable-install metadata from an existing environment, local caches, or pack `.wt/runtime/**` outputs.
- Treat shared workspace reconciliation and customer-release scrub as separate steps. `pack bootstrap` normalizes shared wiring, but portable customer artifacts still need retained records, tests, fixture packs, and other internal-only surfaces removed explicitly.
- Use `watchtower-core pack export --output-root <path> ...` when you need the curated staged bundle, not just shared host-wiring reconciliation in the donor workspace. Add `--pack-only` when you need only the scrubbed pack roots for a compatible core repository.
- Follow [customer_release_and_bootstrap_standard.md](/core/docs/standards/operations/customer_release_and_bootstrap_standard.md) for the full release and bootstrap sequence. Agents should prefer `--format json`; humans may use either output mode.
- When authoring or changing `*.schema.json` files, run `watchtower-core validate schema --path <schema>` in addition to the broad repository validation baseline.
- Package artifacts are curated deliverables, not raw repository exports. Shared `core/python/tests/**`, pack-owned `python/tests/**`, and pack-owned `watchtower_<pack>.testing` helpers are internal validation surfaces by default.
- `watchtower-core pack scaffold` now emits a starter pack-owned `workflow_metadata_registry` and wires the starter validator and validation-suite surfaces to it. Replace the starter workflow entry with the pack's real workflow IDs before relying on workflow indexing or route preview for the new pack.
- Interactive shell path: run `./tools/dev_shell.sh` when you want a shell with `.venv` activated for repeated local commands.
- Manual fallback: run `source .venv/bin/activate` if you specifically want to activate the environment in your current shell.

### Common Commands
- `uv run pytest -q`
- `./.venv/bin/python -m pytest tests/unit tests/integration -q`
- `./.venv/bin/python -m pytest ../../<pack-root>/python/tests -q`
- `./.venv/bin/python -m pytest tests/unit tests/integration ../../<pack-root>/python/tests -q`
- `uv run ruff check .`
- `uv run mypy src`
- `./core/python/.venv/bin/mypy core/python/src/watchtower_core`
- `uv run watchtower-core --help`
- `uv run watchtower-core doctor`
- `uv run watchtower-core route preview --request "review the workflow docs against the current CLI behavior"`
- `uv run watchtower-core route preview --request "do a documentation review of the command docs" --format json`
- `uv run watchtower-core route preview --task-type "Foundations Alignment Review" --format json`
- `uv run watchtower-core query commands --query coordination --format json`
- `uv run watchtower-core query foundations --query philosophy`
- `uv run watchtower-core query workflows --query validation`
- `uv run watchtower-core query references --query uv`
- `uv run watchtower-core query references --repository-status candidate_future_guidance --format json`
- `uv run watchtower-core query standards --category governance --format json`
- `uv run watchtower-core query acceptance --trace-id trace.core_python_foundation`
- `uv run watchtower-core query evidence --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core pack list --format json`
- `uv run watchtower-core pack describe --format json`
- `uv run watchtower-core pack validate --format json`
- `uv run watchtower-core pack export --output-root /tmp/customer_export --include-pack plan --overwrite --format json`
- `uv run watchtower-core pack export --output-root /tmp/customer_plan_pack --include-pack plan --pack-only --overwrite --format json`
- `uv run watchtower-core release check --output-root /tmp/customer_plan --include-pack plan --overwrite --format json`
- `uv run watchtower-core pack scaffold --pack-slug oversight --pack-root oversight --format json`
- `uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --write --format json`
- `uv run watchtower-core pack bootstrap --pack-settings-path oversight/.wt/manifests/pack_settings.json --replace-hosted-packs --write --format json`
- `uv run watchtower-core sync command-index`
- `uv run watchtower-core sync route-index`
- `uv run watchtower-core sync repository-paths`
- `uv run watchtower-core validate all --skip-acceptance`
- `uv run watchtower-core validate schema --path core/control_plane/schemas/interfaces/packs/pack_settings.schema.json --format json`
- `uv run watchtower-core validate portability --include-pack plan --format json`
- `uv run watchtower-core validate portability --root /tmp/customer_plan_pack --include-pack plan --pack-only --format json`
- `uv run watchtower-core validate suite --suite-id suite.example.validation_baseline --pack-settings-path /tmp/example_pack/.wt/manifests/pack_settings.json --format json`
- `uv run watchtower-core validate document-semantics --path core/workflows/modules/code_validation.md`
- `uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core validate artifact --path /tmp/pack_note.json --schema-id urn:watchtower:schema:external:pack-note:v1 --supplemental-schema-path /tmp/pack_schemas --format json`

## Command Docs
- Start with [README.md](/core/docs/commands/core_python/README.md) for command-doc navigation.
- Open [watchtower_core.md](/core/docs/commands/core_python/watchtower_core.md) for the root command and shared options.
- Open [watchtower_core_route.md](/core/docs/commands/core_python/watchtower_core_route.md) when you need a route preview for a request or explicit task type.
- Open [watchtower_core_validate_suite.md](/core/docs/commands/core_python/watchtower_core_validate_suite.md) when you need the pack-declared suite runtime and `--pack-settings-path` behavior.
- Use the group pages for deeper browsing:
  - [watchtower_core_query.md](/core/docs/commands/core_python/watchtower_core_query.md)
  - [watchtower_core_pack.md](/core/docs/commands/core_python/watchtower_core_pack.md)
  - [watchtower_core_sync.md](/core/docs/commands/core_python/watchtower_core_sync.md)
  - [watchtower_core_validate.md](/core/docs/commands/core_python/watchtower_core_validate.md)
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the machine-readable command lookup surface.
- Open the owning pack command-doc root when you need pack-native bootstrap, live query, task, sync, or closeout commands.
- Use the `pack` command pages below when you need the copied-core bring-up contract explained explicitly:
  - [watchtower_core_pack_list.md](/core/docs/commands/core_python/watchtower_core_pack_list.md)
  - [watchtower_core_pack_describe.md](/core/docs/commands/core_python/watchtower_core_pack_describe.md)
  - [watchtower_core_pack_export.md](/core/docs/commands/core_python/watchtower_core_pack_export.md)
  - [watchtower_core_pack_validate.md](/core/docs/commands/core_python/watchtower_core_pack_validate.md)
  - [watchtower_core_pack_bootstrap.md](/core/docs/commands/core_python/watchtower_core_pack_bootstrap.md)

### Commands Inside `./tools/dev_shell.sh`
- `watchtower-core --help`
- `watchtower-core doctor`
- `pytest -q`
- `ruff check .`
- `mypy src`

### Notes
- `uv run ...` is the default workflow for this repository.
- Runtime telemetry is default-on for `watchtower-core` commands. The default sink is `<machine_root>/runtime/telemetry/`.
- Use `WATCHTOWER_TELEMETRY=off` to disable runtime telemetry, `WATCHTOWER_TELEMETRY_STDERR=off` to suppress the one-line stderr summary, and `WATCHTOWER_TELEMETRY_DIR=<path>` to redirect the JSONL sink.
- Command payloads and exit codes remain unchanged on stdout; telemetry emits only operational JSONL files plus one concise stderr summary per invocation.
- Repo-root `./core/python/.venv/bin/mypy core/python/src` commands resolve configuration from [pyproject.toml](/home/j/WatchTowerPlan/core/python/pyproject.toml) when you do not want to `cd core/python` first.
- `uv run pytest -q` is the fast local default and collects only `core/python/tests/unit/`.
- Use `./.venv/bin/python -m pytest tests/unit tests/integration -q` for the broad shared-core Python validation pass when a change touches reusable-core, host composition, synthetic pack fixtures, or multi-surface CLI behavior.
- Use `./.venv/bin/python -m pytest ../../<pack-root>/python/tests -q` when the change touches one hosted pack directly.
- Use `./.venv/bin/python -m pytest tests/unit tests/integration ../../<pack-root>/python/tests -q` when one change spans both shared core and one hosted pack.
- `uv run watchtower-core doctor` is the fastest non-mutating baseline health snapshot before shared root sync commands, pack-owned sync-all commands, or `validate all`.
- `uv run watchtower-core pack export --output-root <staged-export> --include-pack <slug> --overwrite --format json` is the one-command repository-bundle export path for customer/bootstrap handoff.
- `uv run watchtower-core pack export --output-root <pack-bundle> --include-pack <slug> --pack-only --overwrite --format json` stages a scrubbed additive pack bundle without shared core.
- `uv run watchtower-core release check --output-root <path> ... --format json` is the preferred local release gate when you want dirty-worktree protection, the broad validation baseline, changed-schema checks, and final staged export creation in one command.
- `uv run watchtower-core validate schema --path <schema>` is the explicit schema-definition path for touched `*.schema.json` files; `validate artifact` remains the artifact-instance path.
- `uv run watchtower-core validate portability --root <staged-export> --include-pack <slug>` is the read-only scrub check after pack-bootstrap wiring is already reconciled or when you need to inspect an already-staged repository bundle independently.
- `uv run watchtower-core validate portability --root <pack-bundle> --include-pack <slug> --pack-only` is the read-only scrub check for a pack-only bundle.
- `uv run watchtower-core route preview --request "<text>"` is the fastest advisory check for how the current routing surfaces map a request onto workflow documents.
- Bounded documentation and standards review prompts now route to `Documentation Review` instead of requiring repository-review wording.
- `uv run watchtower-core route preview --task-type "Foundations Alignment Review" --format json` is the explicit preview path when a task is about keeping docs or workflow guidance aligned with repository foundations.
- The decision, design, implementation, initiative, and task tracking sync commands rebuild summary-first human trackers with companion terminal-history tables. Use the paired `query` commands when you need exact filtered machine lookup.
- `uv run watchtower-core query references --related-path core/python/ --format json` now treats trailing-slash directory paths as descendant touchpoint filters and returns only references with real current touchpoints under that directory.
- Pack-owned command namespaces remain responsible for live bootstrap, task, closeout, and pack-local state inspection behavior.
- Runtime-only discovered hosted packs are expected during copied-core bring-up. They may load and validate, but they should still report missing shared registry or workspace wiring until `watchtower-core pack bootstrap --write` persists those shared surfaces.
- `watchtower_core` is the reusable-core namespace. Push generic loaders, validators, query helpers, sync helpers, adapters, and utilities back into `watchtower_core` when they stop being pack-specific.
- Keep pack-owned namespaces narrow; do not grow them into pack-flavored mirrors of `watchtower_core`.
- Keep pack machine-state roots out of the Python workspace. Python source, workflow prose, and hand-maintained implementation logic do not belong under `.wt/`.
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
| `core/python/src/watchtower_core/validation/README.md` | `reusable_core` | Export-safe validation services, suite orchestration, and aggregate baseline helpers; pack-local document semantics stay under the owning `watchtower_<pack>.validation` package. |
| `core/python/src/watchtower_core/query/README.md` | `reusable_core` | Export-safe generic query services over governed indexes, routes, pack surfaces, knowledge docs, records, and artifact families; pack-local coordination and lifecycle queries stay under the owning `watchtower_<pack>.query` package. |
| `core/python/src/watchtower_core/sync/README.md` | `reusable_core` | Export-safe sync harness plus repo-shared command, governed-doc, workflow, route, and repository-path index rebuild services; pack-local sync orchestration stays under the owning `watchtower_<pack>.sync` package. |
| `core/python/src/watchtower_core/telemetry/README.md` | `reusable_core` | Default-on local runtime telemetry session, nested operation timing, JSONL sink writing, and stderr summary helpers. |
| `core/python/src/watchtower_core/rebuild/README.md` | `reusable_core` | Export-safe rebuild harness plus registry-backed rendered-view building and markdown reconciliation. |
| `core/python/src/watchtower_core/routing/README.md` | `reusable_core` | Export-safe route-selection runtime over governed route and workflow indexes. |
| `core/python/src/watchtower_core/workflow_execution/README.md` | `reusable_core` | Export-safe workflow execution harness over routed workflow selection and metadata. |
| `core/python/src/watchtower_core/evidence/README.md` | `reusable_core` | Validation-evidence recording plus reusable evidence-bundle helpers. |
| `core/python/src/watchtower_core/integrations/README.md` | `boundary_layer` | External-system client boundary, currently including GitHub. |
| `core/python/src/watchtower_core/closeout/README.md` | `boundary_layer` | Fail-closed compatibility guard; pack-owned closeout services live under the owning pack package root. |
| `core/python/src/watchtower_core/cli/README.md` | `boundary_guard` | Compatibility import surface plus reusable CLI support helpers while host-owned root command ownership lives under `watchtower_host`. |
| `core/python/src/watchtower_core/utils/README.md` | `reusable_core` | Narrow shared helpers that do not justify a first-class package. |

Use the nested READMEs under `integrations/github/` and the reusable-core subpackages when you need the next layer of boundary detail.

## Agent Use
- Read `core/python/AGENTS.md` before making changes under this workspace.
- Use [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md) as the authoritative guide for Python naming, module boundaries, typed interfaces, docstrings, and consolidation decisions.
- Run Python package commands from `core/python/`.
- Prefer `uv run` for tests, linting, typing, and CLI execution.
- When a command supports structured output, prefer `--format json` for agent or workflow consumption instead of parsing human-readable text.
- Keep `pyproject.toml`, `uv.lock`, and command docs aligned when the Python execution contract changes.
- Expect reusable-core packages such as `adapters`, `validation`, `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, and `utils` to satisfy a stricter `mypy` override than current pack-owned orchestration surfaces.

## Programmatic Use
- `watchtower_core.control_plane.WorkspaceConfig` supports alternate logical workspace prefixes through direct construction when a non-default repository layout is needed.
- `ControlPlaneLoader.load_pack_settings()` exposes the repository's current pack-settings load root as a typed reusable-core startup surface.
- `ControlPlaneLoader.activate_pack_settings()` is the Phase 0 bootstrap for any pack-aware runtime seam. Use it before reading the default pack runtime manifest, owned roots, or other pack-selected runtime metadata.
- `ControlPlaneLoader.load_active_pack_context()` activates and caches the full typed `PackContext` for the effective pack. Use it when the caller needs pack-governed surfaces such as the schema catalog, validator registry, validation-suite registry, or other declared governance surfaces.
- `ControlPlaneLoader.load_pack_context()` remains available for explicit-path loading, but the default pack-aware path should flow through `activate_pack_settings()` and then `load_active_pack_context()` when the consumer truly needs the full context.
- `ControlPlaneLoader.load_validation_suite_registry()` exposes the active validation-suite registry, including pack-declared suite baselines.
- `watchtower_core.control_plane.SupplementalSchemaDocument` lets external consumers register additional schemas in-memory for validation without modifying this repository's canonical schema catalog.
- `ControlPlaneLoader(... supplemental_schema_paths=...)` and `SchemaStore.from_workspace(... supplemental_schema_paths=...)` let callers load supplemental schemas from explicit files or directories for bounded external artifact validation.
- `watchtower_core.validation.suite.ValidationSuiteService` runs declared validation suites against the active pack settings surface, including pack-local schema and validator registries.
- Minimal runtime-only fixture packs may intentionally omit the full shared governance surface set. Those seams still must activate the effective pack first, but they should not require `load_active_pack_context()` unless they truly consume the declared governance surfaces.
- Keep pack-agnostic loading and validation logic out of pack-owned namespaces, and move generic behavior back into reusable-core packages when it stops being pack-specific.
- Pack-owned namespaces should be consumed through the shared workspace installation contract, not through repo-local `sys.path` mutation.
- Pack-owned namespaces are not second generic Python roots and not mirrors of `watchtower_core`; keep them narrow and pack-owned.
- The Python design target is boring, explicit, and easy to consolidate: prefer one canonical implementation, extract generic behavior before growing pack-local surfaces, and keep CLI or doc-facing modules thin.
- The default lint baseline now includes Ruff comprehension checks, and the reusable-core package subset is held to stricter `mypy` rules than current pack-owned orchestration surfaces while those domain modules continue tightening.
