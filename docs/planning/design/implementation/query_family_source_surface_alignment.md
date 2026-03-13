---
trace_id: trace.query_family_source_surface_alignment
id: design.implementation.query_family_source_surface_alignment
title: Query Family Source Surface Alignment Implementation Plan
summary: Breaks Query Family Source Surface Alignment into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T22:12:37Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/
- docs/commands/core_python/
- core/control_plane/indexes/commands/
aliases:
- query source surface alignment
---

# Query Family Source Surface Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.query_family_source_surface_alignment`
- `Plan ID`: `design.implementation.query_family_source_surface_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.query_family_source_surface_alignment`
- `Linked Decisions`: `decision.query_family_source_surface_alignment_direction`
- `Source Designs`: `design.features.query_family_source_surface_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.query_family_source_surface_alignment`
- `Updated At`: `2026-03-13T22:12:37Z`

## Summary
Breaks Query Family Source Surface Alignment into a bounded implementation slice.

## Source Request or Design
- Comprehensive refactor review slice for query-family source-surface authority, command docs, and command index drift.

## Scope Summary
- Cover the query-family implementation-path authority seam, the affected command docs, the
  derived command index, direct loader or CLI consumers, and the planning closeout surfaces
  required for repeated confirmation.
- Exclude behavioral changes to query results, non-query command families, and speculative
  runtime handler splitting unless later passes find a new same-theme issue.

## Coverage Map
- Registry-backed CLI group metadata and parser introspection:
  `core/python/src/watchtower_core/cli/registry.py`;
  `core/python/src/watchtower_core/cli/introspection.py`
- Direct query-family registration and runtime boundaries:
  `core/python/src/watchtower_core/cli/query_family.py`;
  `core/python/src/watchtower_core/cli/query_discovery_family.py`;
  `core/python/src/watchtower_core/cli/query_knowledge_family.py`;
  `core/python/src/watchtower_core/cli/query_records_family.py`;
  `core/python/src/watchtower_core/cli/query_coordination_family.py`;
  `core/python/src/watchtower_core/cli/query_coordination_handlers.py`
- Human and machine command lookup surfaces:
  `docs/commands/core_python/watchtower_core_query*.md`;
  `core/control_plane/indexes/commands/command_index.v1.json`
- Direct consumers and regression coverage:
  `core/python/tests/unit/test_command_index_sync.py`;
  `core/python/tests/unit/test_control_plane_loader.py`;
  `core/python/tests/unit/test_cli_knowledge_query_commands.py`
- Adjacent governed planning and closeout surfaces:
  traced PRD, design, decision, task docs, acceptance contract, evidence ledger, and derived
  planning trackers for this trace

## Findings Ledger
| Finding | Severity | Status | Affected Surfaces | Verification Target |
|---|---|---|---|---|
| `finding.001` | `high` | `resolved` | `core/python/src/watchtower_core/cli/introspection.py`; `core/python/src/watchtower_core/cli/registry.py`; `core/control_plane/indexes/commands/command_index.v1.json` | Query leaf command specs and the rebuilt command index expose the correct split family implementation paths. |
| `finding.002` | `medium` | `resolved` | `docs/commands/core_python/watchtower_core_query*.md` | Affected query command pages stop pointing at stale `main.py` or umbrella `query_family.py` surfaces. |
| `finding.003` | `medium` | `resolved` | `core/python/tests/unit/test_command_index_sync.py`; `core/python/tests/unit/test_control_plane_loader.py`; `core/python/tests/unit/test_cli_knowledge_query_commands.py` | Direct consumers fail if discovery, loader, or command-index surfaces drift back to coarse query-family ownership. |
| `finding.004` | `medium` | `resolved` | `docs/planning/tasks/closed/validate_and_close_query_family_source_surface_alignment.md`; `core/control_plane/contracts/acceptance/query_family_source_surface_alignment_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/query_family_source_surface_alignment_planning_baseline.v1.json` | Acceptance-aware validation covers the final closed validation task path and all five acceptance IDs without bootstrap-only drift. |

## Assumptions and Constraints
- The fix must preserve command IDs, help text, query payloads, and deterministic command-index
  regeneration.
- The current split query family files are the intended long-lived registration boundaries, so
  the implementation should align metadata to them rather than re-collapsing the family.

## Internal Standards and Canonical References Applied
- `docs/standards/data_contracts/command_index_standard.md`: the command index is a lookup
  surface and must point to the owning implementation files when they exist.
- `docs/standards/documentation/command_md_standard.md`: command docs must record the current
  source surface for operators and engineers.
- `docs/standards/engineering/python_workspace_standard.md`: runtime code, CLI tests, and
  validation commands stay in the canonical Python workspace.

## Proposed Technical Approach
- Extend `CommandGroupSpec` so split families can declare leaf-specific implementation-path
  overrides in the same registry metadata that already defines the top-level family.
- Update parser introspection to consume those overrides for leaf commands while leaving the
  root `query` group entry unchanged.
- Reconcile all affected query command pages, direct tests, and the rebuilt command index to
  the new authoritative mapping.
- Re-review `query_coordination_handlers.py` from an adjacent angle, record the accepted
  bounded recommendation, and keep the trace focused on source-surface authority unless a new
  actionable issue appears.

## Work Breakdown
1. Implement and verify the registry-backed query leaf implementation-path mapping plus direct
   unit coverage.
2. Reconcile query command pages and rebuild the command index so human and machine lookup
   surfaces agree.
3. Run targeted tests, then full validation, then repeated confirmation and adversarial probes;
   reopen the loop if a new same-theme issue appears.

## Risks
- A stale query command page or omitted leaf override could leave one part of the family
  misaligned even if representative spot checks look correct.
- Acceptance or evidence coverage could drift if the trace closeout artifacts are left in their
  bootstrap-only state.

## Validation Plan
- Run targeted pytest for command-index sync, loader command-index consumption, and query
  command discovery output.
- Rebuild the command index from the live parser tree and inspect `watchtower-core query
  commands --tag query --limit 20 --format json`.
- Run a stale-reference sweep over query command docs and the command index to confirm only the
  root query group still points at `query_family.py`.
- Run full repo validation plus a post-fix review, a second-angle confirmation pass, and an
  adversarial probe that tries to falsify the cleaned-state claim.

## References
- REFACTOR.md RF-PY-004
