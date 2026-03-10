# Governed Artifact Reconciliation Workflow

## Purpose
Use this workflow to reconcile schema-backed governed artifacts with their companion schemas, examples, registries, indexes, loaders, validators, and lookup surfaces so artifact families stay internally coherent.

## Use When
- A schema, registry, index, contract, policy, ledger, or other governed artifact family may have drifted from its companion machine-readable or implementation-facing surfaces.
- A review or maintenance pass needs an explicit control-plane coherence check rather than relying only on generic code validation.
- A task's main risk is stale schema IDs, stale canonical paths, broken examples, or hidden loader and validator assumptions about governed artifacts.

## Inputs
- Scoped governed-artifact reconciliation brief
- In-scope artifact families, live artifacts, and repository paths
- Companion schemas, examples, registries, indexes, validators, loaders, or command surfaces that depend on the in-scope artifacts
- Internal standards and canonical references applied
- Known source-of-truth rules for the artifact families in scope
- Known discrepancies, resolution constraints, or open questions

## Additional Files to Load
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): defines the schema-backed artifact constraints and same-change-set expectations this workflow should reconcile.
- [watchtower_core_validate_artifact.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate_artifact.md): documents the command surface for schema-backed governed-artifact validation.
- [watchtower_core_sync_all.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_all.md): documents the broad rebuild path when multiple governed indexes or catalogs changed together.

## Workflow
1. Define the artifact-family boundary.
   - List the artifact families, canonical files, and dependent surfaces in scope.
   - Decide which surface is authoritative for schema identity, canonical paths, lookup records, and behavioral assumptions.
2. Gather the current governed surfaces.
   - Read the live artifacts, their companion schemas, example sets, registries or indexes, and any loader, validator, or command surfaces that resolve or validate them.
   - Prefer published artifact fields such as `$id`, canonical paths, stable identifiers, and governed examples over inferred descriptions.
3. Compare the companion surfaces for coherence.
   - Check that schema IDs, canonical paths, and artifact-family fields agree across schemas, catalogs, registries, and live artifacts.
   - Check that valid and invalid examples still represent the intended acceptance boundary.
   - Check that loaders, validators, indexes, and command surfaces point to real files and still match the current artifact shape or lookup rules.
   - Record schema drift, example drift, lookup drift, loader-assumption drift, and missing companion surfaces explicitly.
4. Resolve or route the discrepancies.
   - Update stale schemas, examples, indexes, registries, loaders, validators, or documentation when the authoritative artifact family is already correct.
   - Treat the issue as an artifact-design or implementation problem when the canonical schema or live artifact is wrong instead.
   - Add the narrower implementation, validation, or documentation workflow when the discrepancy cannot be resolved inside reconciliation alone.
5. Validate the reconciled result.
   - Re-run the narrowest meaningful checks such as schema validation, path checks, example validation, targeted tests, and index or registry validation.
   - Ensure every discrepancy is either resolved in the same change or recorded as explicit follow-up work with the affected artifact family named.

## Data Structure
- Reconciliation scope
- In-scope artifact families and canonical files
- Companion validation and lookup surfaces
- Authoritative source map
- Discrepancy log with these fields:
  - artifact family
  - authoritative source
  - conflicting companion surface
  - discrepancy type such as `schema_drift`, `example_drift`, `lookup_drift`, `loader_assumption_drift`, or `missing_companion_surface`
  - resolution status such as `resolved_same_change`, `deferred_follow_up`, or `blocked`

## Outputs
- Updated governed artifacts or companion schemas, examples, registries, indexes, loaders, or validators for the scoped families
- A discrepancy report for unresolved artifact-family drift or deferred follow-up work
- Clear coherence status for the in-scope governed artifact families

## Done When
- The in-scope governed artifact families and their companion surfaces agree on current schema identity, lookup, and acceptance boundaries or the gaps are explicit.
- Silent disagreement between live artifacts and their companion validation or lookup surfaces has been removed or recorded.
- The task result makes clear whether the change updated companion surfaces, exposed an upstream artifact issue, or deferred specific follow-up work.
