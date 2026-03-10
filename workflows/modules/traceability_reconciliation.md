# Traceability Reconciliation Workflow

## Purpose
Use this workflow to reconcile traced planning and governance artifacts with their companion human trackers, family-specific indexes, and unified traceability joins so durable links do not drift silently.

## Use When
- A PRD, decision record, feature design, implementation plan, acceptance contract, or validation-evidence artifact may have invalidated a family tracker, family index, or unified traceability entry.
- A review or maintenance pass needs an explicit traceability check rather than relying only on planning workflows or handoff review.
- A task's main risk is stale identifiers, missing upstream or downstream links, or disagreement between human-readable and machine-readable planning surfaces.

## Inputs
- Scoped traceability reconciliation brief
- In-scope `trace_id` values, artifact IDs, and repository paths
- In-scope planning and governance artifacts
- In-scope human trackers, family-specific indexes, and unified traceability index entries
- Internal standards and canonical references applied
- Known authority rules for identifiers, links, and tracker or index ownership
- Known missing links, deferred follow-up work, or open questions

## Additional Files to Load
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): defines the required cross-surface links and trace-level field semantics this workflow must preserve.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): defines the machine-readable trace join surface that should match the planning corpus.
- [watchtower_core_sync_traceability_index.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_traceability_index.md): documents the command surface that rebuilds the derived traceability join.

## Workflow
1. Define the traceability boundary.
   - List the traces, artifact families, and repository paths in scope.
   - Decide which surface is authoritative for each identifier or link type when the repository already defines a source of truth.
2. Gather the current trace surfaces.
   - Read the in-scope PRDs, decisions, feature designs, implementation plans, acceptance contracts, evidence artifacts, human trackers, family indexes, and unified traceability entries.
   - Prefer explicit IDs, linked paths, and published machine-readable fields over inferred prose relationships.
3. Compare identifiers and links across the surfaces.
   - Check that stable IDs and shared `trace_id` values are present, preserved, and spelled consistently.
   - Check that human trackers and family-specific indexes agree on the current artifact set, key statuses, and linked paths.
   - Check that the unified traceability index still joins the same artifacts and related paths the family surfaces claim to cover.
   - Record missing links, stale IDs, unresolved downstream gaps, and authority conflicts explicitly.
4. Resolve or route the discrepancies.
   - Update stale trackers, indexes, and trace joins when the underlying artifacts are already correct.
   - Treat the mismatch as an upstream artifact issue when the canonical PRD, decision, design, plan, contract, or evidence surface is wrong instead.
   - Add the relevant planning workflow if the reconciliation reveals a missing durable artifact that should be created rather than merely re-linked.
5. Validate the reconciled result.
   - Re-run the narrowest meaningful checks such as path resolution, schema validation for touched indexes or contracts, and targeted tracker or index consistency checks.
   - Ensure every discrepancy is either resolved in the same change or recorded as explicit follow-up work with the missing link called out.

## Data Structure
- Reconciliation scope
- In-scope trace IDs and artifact IDs
- Authoritative planning and governance surfaces
- Human tracker surfaces
- Machine-readable traceability surfaces
- Discrepancy log with these fields:
  - trace or artifact family
  - authoritative source
  - conflicting companion surface
  - discrepancy type such as `missing_link`, `stale_identifier`, `tracker_index_drift`, `trace_join_drift`, or `authority_conflict`
  - resolution status such as `resolved_same_change`, `deferred_follow_up`, or `blocked`

## Outputs
- Updated planning trackers, family-specific indexes, or unified traceability entries for the scoped traces
- A discrepancy report for unresolved link gaps, authority conflicts, or deferred follow-up work
- Clear traceability status for the in-scope initiative or artifact family

## Done When
- The in-scope traced artifacts, trackers, and machine-readable indexes agree on the current durable links or any gaps are explicit.
- Silent disagreement between human-readable and machine-readable traceability surfaces has been removed or recorded.
- The task result makes clear whether the change updated traceability surfaces, exposed an upstream artifact issue, or deferred specific follow-up work.
