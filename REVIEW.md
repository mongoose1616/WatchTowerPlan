# Repository Review

## Findings

### High: The new task-document family is internally broken in the current worktree and cannot rebuild its own derived surfaces
- The task front matter schema adds task-specific keys such as `task_status`, `task_kind`, and `priority` in [task_front_matter.v1.schema.json](/home/j/WatchTowerPlan/core/control_plane/schemas/interfaces/documentation/task_front_matter.v1.schema.json#L6), but the shared base schema still forbids unevaluated properties in [front_matter_base.v1.schema.json](/home/j/WatchTowerPlan/core/control_plane/schemas/interfaces/documentation/front_matter_base.v1.schema.json#L112). That makes the task profile reject the very fields the task standard requires.
- The same schema also declares nested `$defs` and then references them with root-style pointers such as `#/$defs/idList` in [task_front_matter.v1.schema.json](/home/j/WatchTowerPlan/core/control_plane/schemas/interfaces/documentation/task_front_matter.v1.schema.json#L62), which breaks front-matter validation when fields like `related_ids` are present in live task docs such as [github_task_sync.md](/home/j/WatchTowerPlan/docs/planning/tasks/open/github_task_sync.md#L1).
- Task parsing is fail-closed by design: [task_documents.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/sync/task_documents.py#L123) validates task front matter before any rebuild. Because of the schema issue, both [task_index.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/sync/task_index.py#L64) and [task_tracking.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/sync/task_tracking.py#L52) fail on the current task corpus.
- That directly violates the task family’s own source-of-truth and rebuild rules in [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md#L82) and [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md#L105), and it cuts against the fail-closed validation model in [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md#L7).

### High: Governed artifact validation still covers only a small subset of the schema-backed artifact families the repo now depends on
- `watchtower-core validate artifact` only works when the target path matches an active registry validator. See [artifact.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/artifact.py#L58).
- The active JSON-artifact validators in [validator_registry.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/validators/validator_registry.v1.json#L7) still cover only acceptance contracts, the traceability index, and validation evidence. The registry does not provide artifact validators for the command index, repository path index, decision index, design-document index, PRD index, task index, schema catalog, or validator registry.
- That now leaves even more governed surfaces outside the advertised validation path, including the new task index. The gap conflicts with the companion-update and validation requirements in [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L67), [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L80), and family rules such as [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md#L92).
- I rechecked the live behavior: `validate artifact` passes for the acceptance contract and traceability index, but auto-selection still fails for the command, repository-path, decision, design-document, PRD, and task indexes plus the schema catalog and validator registry.

### Medium: Current worktree changes leave derived machine-readable lookup surfaces stale relative to the source docs
- The current worktree adds the local task-tracking feature design in [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md#L87), a task document family under [docs/planning/tasks/README.md](/home/j/WatchTowerPlan/docs/planning/tasks/README.md#L3), and traceability requirements for task records in [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md#L52).
- Dry-run rebuild comparison against the checked-in artifacts reports `repository_paths DIFF`, `design_documents DIFF`, and `traceability DIFF`. The current checked-in [repository_path_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/repository_paths/repository_path_index.v1.json), [design_document_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/design_documents/design_document_index.v1.json), and [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json) do not yet reflect the task-family additions in the worktree.
- This is exactly the kind of same-change drift the repo says to avoid in [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L74), [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md#L109), and [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md#L95).

### Medium: The CLI already exposes new task commands, but the command-doc family has not been updated to match
- The CLI now advertises and wires `watchtower-core query tasks`, `watchtower-core sync task-index`, and `watchtower-core sync task-tracking` in [main.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/main.py#L121), [main.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/main.py#L402), and [main.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/main.py#L491).
- The human command docs still describe the older command sets. [watchtower_core_query.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query.md#L25) lists only `paths`, `commands`, `prds`, `decisions`, `designs`, and `trace`, while [watchtower_core_sync.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync.md#L25) and [watchtower_core_sync.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync.md#L76) still omit the two task sync leaves.
- The command-doc directory inventory also has no pages for those three new commands in [docs/commands/core_python/README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md#L6).
- That violates the command-family requirement to update command docs, related READMEs, and lookup surfaces in the same change set in [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md#L92) and [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L79).

### Medium: The foundations now describe a domain-pack product shape that the repo still does not materially expose
- The foundations position WatchTower as a two-layer product where domain packs are the main operator-facing surface in [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md#L3), [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md#L28), and [product_narrative_brochure.md](/home/j/WatchTowerPlan/docs/foundations/product_narrative_brochure.md#L94).
- The repository itself still presents only `docs/`, `workflows/`, and `core/` at the top level in [README.md](/home/j/WatchTowerPlan/README.md#L3), and the planning corpus is still scoped to PRDs, designs, decisions, and tasks in [docs/planning/README.md](/home/j/WatchTowerPlan/docs/planning/README.md#L3).
- That means the current repo is still cohesive as a planning-and-core workspace, but it does not yet match the broader product shape the foundations now claim. This is a strategy and coherence gap rather than a code bug, but it is real if the foundations are meant to describe current direction rather than aspirational future state.

## Open Questions
- Should the new local task-tracking family block on a schema fix first, then regenerate `task_tracking.md`, `task_index.v1.json`, the repository path index, the design-document index, and the traceability index in one change?
- Do you want `watchtower-core validate artifact` to become the required validation path for every schema-backed control-plane family, or should the docs and standards be narrowed to match the smaller current validator registry?
- Are the foundations meant to describe the current repository shape or the target product shape? Right now they read closer to the latter.

## Scope
- Review target: current working tree of `/home/j/WatchTowerPlan` on `2026-03-09`.
- Review mode: code and standards review with explicit comparison to `docs/foundations/**`.
- This review includes current uncommitted workspace changes, not only the last committed snapshot.

## Checks Performed
- Ran the Python unit and integration suite with `core/python/.venv/bin/pytest -q`: passed.
- Ran `core/python/.venv/bin/mypy src`: passed.
- Ran `core/python/.venv/bin/ruff check .`: passed.
- Ran repo-wide absolute-path Markdown link resolution across `*.md` with anchor stripping: `missing_count=0`.
- Ran dry-run rebuild comparisons for the current derived surfaces:
  - `command_index`: match
  - `prd_index`: match
  - `decision_index`: match
  - `repository_path_index`: diff
  - `design_document_index`: diff
  - `traceability_index`: diff
- Ran direct task-family rebuilds:
  - `TaskIndexSyncService.build_document()`: fails on task front-matter schema validation
  - `TaskTrackingSyncService.build_document()`: fails on task front-matter schema validation
- Exercised `watchtower-core validate artifact` against representative governed artifacts to confirm actual validator coverage.

## Summary
- The existing committed Python workspace still passes its current automated checks.
- The repo’s biggest current cohesion problem is the in-flight task family: standards, schemas, docs, Python services, and derived artifacts do not yet agree, and the task schema is currently invalid for live task documents.
- The broader strategic mismatch is that the foundations now describe a domain-pack-first product, while the repository still operates primarily as a planning, workflow, and core-governance workspace.
