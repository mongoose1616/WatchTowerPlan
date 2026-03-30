# Traceability Reconciliation Workflow

## Purpose
Use this workflow to reconcile traced planning and governance artifacts with their companion human trackers, initiative coordination views, family-specific indexes, and unified traceability joins so durable links do not drift silently.

## Use When
- An initiative brief, decision note, design record, implementation slice, acceptance contract, or validation-evidence artifact may have invalidated a family tracker, family index, or unified traceability entry.
- A review or maintenance pass needs an explicit traceability check rather than relying only on planning workflows or handoff review.
- A task's main risk is stale identifiers, missing upstream or downstream links, or disagreement between human-readable and machine-readable planning surfaces.
- The new initiative layer may have drifted from the family-specific planning surfaces or the traceability join.
- Choose this route when the disagreement is mainly about traced IDs, links, or tracker or index projection rather than raw implementation behavior or schema shape.
- Use this route for trace links, initiative trackers, and planning-index drift; use documentation-implementation reconciliation for behavior docs and governed-artifact reconciliation for schema-backed family coherence.

## Inputs
- Scoped traceability reconciliation brief
- In-scope `trace_id` values, artifact IDs, and repository paths
- In-scope planning and governance artifacts
- In-scope human trackers, initiative coordination views, family-specific indexes, and unified traceability index entries
- Internal standards and canonical references applied
- Known authority rules for identifiers, links, and tracker or index ownership
- Known missing links, deferred follow-up work, or open questions

## Additional Files to Load
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): defines the required cross-surface links and trace-level field semantics this workflow must preserve.
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md): defines the derived initiative phase, owner, and next-step projection that should stay aligned with traceability and task state.
- [traceability_index_standard.md](/plan/docs/standards/data_contracts/traceability_index_standard.md): defines the unified machine-readable trace join surface that should match the planning corpus.
- [initiative_index_standard.md](/plan/docs/standards/data_contracts/initiative_index_standard.md): defines the machine-readable initiative projection that should stay aligned with the same traced planning state.
- [watchtower_core_sync.md](/core/docs/commands/core_python/watchtower_core_sync.md): documents the traceability, initiative-index, and initiative-tracking sync commands this workflow uses to rebuild the derived surfaces it reconciles.

## Workflow
1. Define the traceability boundary.
   - List the traces, artifact families, and repository paths in scope.
   - Decide which surface is authoritative for each identifier or link type when the repository already defines a source of truth.
2. Gather the current trace surfaces.
   - Read the in-scope initiative briefs, decision notes, design records, implementation slices, acceptance contracts, evidence artifacts, human trackers, initiative views, family indexes, and unified traceability entries.
   - Prefer explicit IDs, linked paths, and published machine-readable fields over inferred prose relationships.
3. Compare identifiers and links across the surfaces.
   - Check that stable IDs and shared `trace_id` values are present, preserved, and spelled consistently.
   - Check that human trackers, initiative views, and family-specific indexes agree on the current artifact set, key statuses, phase projection, and linked paths.
   - Check that the unified traceability index still joins the same artifacts and related paths the family surfaces claim to cover.
   - Record missing links, stale IDs, unresolved downstream gaps, and authority conflicts explicitly.
4. Resolve or route the discrepancies.
   - Update stale trackers, initiative views, indexes, and trace joins when the underlying artifacts are already correct.
   - Treat the mismatch as an upstream artifact issue when the canonical initiative brief, decision note, design record, implementation slice, contract, or evidence surface is wrong instead.
   - Add the relevant planning workflow if the reconciliation reveals a missing durable artifact that should be created rather than merely re-linked.
   - When the canonical artifacts are already correct and the drift is in derived mirrors, rebuild the affected surfaces with [watchtower_core_plan_sync_traceability_index.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_traceability_index.md), [watchtower_core_plan_sync_initiative_index.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_initiative_index.md), [watchtower_core_plan_sync_task_index.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_task_index.md), or [watchtower_core_plan_sync_github_tasks.md](/plan/docs/commands/core_python/watchtower_core_plan_sync_github_tasks.md) instead of hand-editing derived state.
5. Validate the reconciled result.
   - Re-run the narrowest meaningful checks such as path resolution, schema validation for touched indexes or contracts, and targeted tracker or index consistency checks.
   - Confirm the command-driven traceability, initiative, task, and GitHub mirrors now agree with the authoritative planning artifacts for the in-scope traces.
   - Ensure every discrepancy is either resolved in the same change or recorded as explicit follow-up work with the missing link called out.

## Data Structure
- Reconciliation scope
- In-scope trace IDs and artifact IDs
- Authoritative planning and governance surfaces
- Human tracker surfaces
- Initiative coordination surfaces
- Machine-readable traceability surfaces
- Discrepancy log with these fields:
  - trace or artifact family
  - authoritative source
  - conflicting companion surface
  - discrepancy type such as `missing_link`, `stale_identifier`, `tracker_index_drift`, `trace_join_drift`, or `authority_conflict`
  - resolution status such as `resolved_same_change`, `deferred_follow_up`, or `blocked`

## Outputs
- Updated planning trackers, initiative views, family-specific indexes, or unified traceability entries for the scoped traces
- A discrepancy report for unresolved link gaps, authority conflicts, or deferred follow-up work
- Clear traceability status for the in-scope initiative or artifact family

## Done When
- The in-scope traced artifacts, trackers, initiative views, and machine-readable indexes agree on the current durable links or any gaps are explicit.
- Silent disagreement between human-readable and machine-readable traceability or initiative surfaces has been removed or recorded.
- The task result makes clear whether the change updated traceability surfaces, exposed an upstream artifact issue, or deferred specific follow-up work.
