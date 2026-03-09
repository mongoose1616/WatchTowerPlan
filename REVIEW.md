# Repository Review

## Findings

### High: Governed artifact validation is incomplete, but the CLI and standards read as if it is broadly available
- [watchtower_core_validate_artifact.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_artifact.md#L4) and [watchtower_core_validate_artifact.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_artifact.md#L7) present `watchtower-core validate artifact` as the generic validation path for governed JSON contracts, indexes, ledgers, and similar artifacts.
- The implementation only works when the target path matches an active registry validator. See [artifact.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/artifact.py#L58) and [artifact.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/artifact.py#L87).
- The current validator registry only covers acceptance contracts, the traceability index, validation evidence, and documentation front matter. It does not cover command indexes, repository path indexes, decision indexes, design-document indexes, PRD indexes, the schema catalog, or the validator registry itself. See [validator_registry.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/validators/validator_registry.v1.json#L1).
- That conflicts with the family standards, which explicitly require those artifacts to validate against their published schemas, for example [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md#L90), [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md#L85), [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md#L84), [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md#L87), and [prd_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/prd_index_standard.md#L85).
- The repo-wide engineering rule also says new schema-backed artifact families should add any affected validators in the same change set. See [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L78).
- I verified the gap directly: `validate artifact` succeeds for the traceability index but fails with “No active schema-backed artifact validator applies” for `command_index.v1.json`, `repository_path_index.v1.json`, `decision_index.v1.json`, `design_document_index.v1.json`, `prd_index.v1.json`, `schema_catalog.v1.json`, and `validator_registry.v1.json`.

### High: The traceability standard requires design and plan trace links, but the design-document standards and templates still do not define where that metadata belongs
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md#L75) says feature designs and implementation plans should preserve upstream links explicitly, and [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md#L96) requires `trace_id` as a baseline link for both families.
- The feature-design standard does not require any trace metadata section or field. See [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md#L58).
- The implementation-plan standard has the same omission. See [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md#L57).
- The templates mirror that omission. See [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md#L8) and [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md#L8).
- Live planning docs follow the same pattern: [core_python_workspace_and_harness.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_python_workspace_and_harness.md#L1) and [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md#L1) start directly with narrative sections and do not publish `trace_id` or stable document IDs in-document.
- That leaves the new reconciliation workflow with an under-specified source surface and forces humans to recover trace data from companion indexes instead of the planning documents themselves.

### Medium: Some planning documents still describe the Python layer and schema catalog as if they were mostly unimplemented
- [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md#L21) says the schema catalog does not yet publish a governed artifact, but the live artifact exists at [schema_catalog.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/schema_catalog/schema_catalog.v1.json#L1).
- The same design doc says the consolidated package contains scaffold-only modules. See [schema_resolution_and_index_search.md](/home/j/WatchTowerPlan/docs/planning/design/features/schema_resolution_and_index_search.md#L23).
- The implementation plan still says `core/python/src/watchtower_core/control_plane/` is scaffold-only. See [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md#L24).
- That is no longer true. The control-plane loader is implemented in [loader.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/loader.py#L28), and the live loader behavior is exercised in [test_control_plane_loader.py](/home/j/WatchTowerPlan/core/python/tests/unit/test_control_plane_loader.py#L10).
- In a planning-heavy repo, stale current-state sections are a real defect because they misroute later design and implementation work.

### Medium: Validation policy is still under-specified for humans even though the repo now has multiple validation and reconciliation workflows
- The validation-standards directory is still only a placeholder. See [README.md](/home/j/WatchTowerPlan/docs/standards/validations/README.md#L1).
- At the same time, the repo now has [code_validation.md](/home/j/WatchTowerPlan/workflows/modules/code_validation.md#L1), [governed_artifact_reconciliation.md](/home/j/WatchTowerPlan/workflows/modules/governed_artifact_reconciliation.md#L1), and [traceability_reconciliation.md](/home/j/WatchTowerPlan/workflows/modules/traceability_reconciliation.md#L1), all of which assume explicit validation or reconciliation expectations.
- The repo-wide engineering standard also says validation is required and that reviewers should reject stale companion surfaces. See [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L61) and [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md#L83).
- Without actual validation standards, humans still have to infer what counts as a blocker, what can be deferred, and what evidence is sufficient for closeout.

## Open Questions
- Should `watchtower-core validate artifact` become the required validation path for every schema-backed control-plane family, or should the docs be narrowed to match the smaller current validator registry?
- Should feature designs and implementation plans publish trace metadata in front matter, in a dedicated record-metadata section, or in some other governed structure?

## Scope
- Review target: current working tree of `/home/j/WatchTowerPlan` on `2026-03-09`.
- Review mode: repo-wide coherence, documentation freshness, standards adherence, validation coverage, and human ambiguity.
- This review includes current uncommitted workspace state, not only the last committed snapshot.

## Checks Performed
- Ran the Python unit and integration suite with `core/python/.venv/bin/pytest -q`: passed.
- Ran `core/python/.venv/bin/mypy src`: passed.
- Ran `core/python/.venv/bin/ruff check .`: passed.
- Ran repo-wide absolute-path Markdown link resolution across `*.md`: `missing_count=0`.
- Rebuilt the derived command index and repository path index in dry-run mode and confirmed both match the current checked-in artifacts.
- Exercised the current CLI validation path against representative governed artifacts to confirm actual validator coverage.

## Summary
- The repo is materially cohesive and the current Python workspace passes its main executable checks.
- The biggest remaining gaps are not basic code correctness; they are governance and validation mismatches where the repo’s standards and command docs promise broader explicit validation and traceability than the current authoritative surfaces actually provide.
