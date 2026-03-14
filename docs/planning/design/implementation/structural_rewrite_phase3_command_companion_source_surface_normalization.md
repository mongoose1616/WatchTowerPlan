---
trace_id: "trace.structural_rewrite_program"
id: "design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization"
title: "Structural Rewrite Phase 3 Command Companion Source Surface Normalization"
summary: "Implements the first bounded Phase 3 slice by reconciling command-doc source surfaces to the existing registry-backed command authority model."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-14T05:41:11Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "docs/commands/core_python/"
  - "core/control_plane/indexes/commands/"
  - "core/python/src/watchtower_core/cli/"
  - "core/python/tests/"
  - "docs/planning/tasks/"
aliases:
  - "phase 3 command companion slice"
  - "command source surface normalization"
  - "rewrite command companion normalization"
---

# Structural Rewrite Phase 3 Command Companion Source Surface Normalization

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Plan ID`: `design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.structural_rewrite_program`
- `Linked Acceptance Contracts`: `contract.acceptance.structural_rewrite_program`
- `Updated At`: `2026-03-14T05:41:11Z`

## Summary
Implement the first bounded Phase 3 slice by reconciling command-doc source-surface metadata to the existing registry-backed command authority model without changing command presence, hierarchy, or public planning behavior.

## Source Request or Design
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/features/structural_rewrite_program.md)
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase3_command_authority_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md)
- [review_structural_rewrite_phase3_entry_package.md](/home/j/WatchTowerPlan/docs/planning/tasks/closed/review_structural_rewrite_phase3_entry_package.md)

## Scope Summary
- Reconcile the `Source Surface` fields in the first bounded set of command companion docs whose current source-surface metadata still points at `core/python/src/watchtower_core/cli/main.py` while the command index already points at the owning family module.
- Keep the current command-authority boundary unchanged: `registry.py` plus `parser.py` remain the only accepted machine authority for command presence and hierarchy.
- Keep the command index and command docs aligned as companion discovery surfaces rather than introducing a second durable command-authority source.
- Stop after the slice is synced, validated, and handed to an explicit follow-up review task.

## Assumptions and Constraints
- The current CLI registry and parser tree remain the only accepted machine authority for command presence and hierarchy.
- The command index remains a derived machine-readable lookup surface.
- The command docs remain the human-readable companion family and should route engineers to the responsible implementation surface.
- The first Phase 3 slice may not change command IDs, help text, flags, output payloads, or public planning-authority answers.
- The first Phase 3 slice may not widen into workflow routing, route-index, compatibility-namespace, or public planning-boundary changes.

## Current-State Context
- The bounded implementation resolved `24` command-companion drift points: the root command page's primary `## Source Surface` entry plus `23` command docs whose source-surface metadata still pointed at `core/python/src/watchtower_core/cli/main.py` while the governed command index already pointed at a parser-owned or family-owned implementation path.
- The bounded leaf-doc mismatch set remained limited to one `doctor` leaf command, `18` `sync` leaf commands, and `4` `validate` leaf commands.
- Representative mismatches include:
  - `watchtower-core doctor`: doc points at `core/python/src/watchtower_core/cli/main.py`, command index points at `core/python/src/watchtower_core/cli/doctor_family.py`
  - `watchtower-core sync command-index`: doc points at `core/python/src/watchtower_core/cli/main.py`, command index points at `core/python/src/watchtower_core/cli/sync_family.py`
  - `watchtower-core validate all`: doc points at `core/python/src/watchtower_core/cli/main.py`, command index points at `core/python/src/watchtower_core/cli/validate_family.py`
- This stayed companion-surface drift, not authority drift. The registry-backed command index already reflected the correct owning parser or family files for these commands before the slice landed.
- The slice therefore stayed inside the already-published command authority boundary instead of inventing a new command descriptor family or touching route, workflow, or compatibility surfaces.

## Internal Standards and Canonical References Applied
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): the slice must stay bounded, rollback-explicit, and tied to the current checkpoint package.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): the slice must stay within already-classified command authority and generated companion surfaces.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): the command index is the machine-readable routing aid and already points to owning implementation surfaces.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command docs must route engineers to the responsible source surface rather than to a stale entrypoint.
- [command_documentation_and_lookup.md](/home/j/WatchTowerPlan/docs/planning/design/features/command_documentation_and_lookup.md): the command docs and command index must remain aligned as human and machine companion surfaces.
- [query_family_source_surface_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/query_family_source_surface_alignment.md): provides the bounded source-surface reconciliation pattern that this Phase 3 slice follows.

## Classification Sufficiency Decision
- No additional command-adjacent workflow, route, or compatibility classification addendum is required for this first Phase 3 slice.
- The slice stays entirely inside the already-classified command authority and companion families:
  - `CLI registry plus parser tree` as `authored_authority`
  - `command index plus command docs` as `generated_projection`
- The slice does not touch `watchtower-core route`, workflow modules, compatibility namespaces, public planning queries, or planning-index projections.

## Slice Boundary
### In scope
- The root command page plus the `23` bounded `doctor`, `sync`, and `validate` command docs under `docs/commands/core_python/`
- `core/control_plane/indexes/commands/command_index.v1.json` as the current machine-readable parity oracle for command companion ownership
- `core/python/src/watchtower_core/cli/registry.py`
- `core/python/src/watchtower_core/cli/parser.py`
- `core/python/src/watchtower_core/cli/introspection.py`
- Any targeted validation or regression coverage needed to keep the affected command docs aligned with the command index for the bounded family set

### Explicitly out of scope
- Changing command presence or hierarchy authority away from the current CLI registry and parser tree
- CLI behavioral changes
- Route or workflow-family normalization
- Compatibility-namespace cleanup
- Public planning-authority changes
- Broader command-family descriptor rollout beyond the first bounded source-surface normalization slice

## Authored Truth and Derived Outputs
### Authored truth to preserve
- `core/python/src/watchtower_core/cli/registry.py`
- `core/python/src/watchtower_core/cli/parser.py`

### Derived companion outputs to keep aligned
- `core/control_plane/indexes/commands/command_index.v1.json`
- the affected command docs under `docs/commands/core_python/`

## Current Consumers
- Engineers and agents who use the command docs as the human-readable command surface
- `watchtower-core query commands`
- the command index loader and lookup handlers
- the command-doc family README and related command-reference navigation
- any targeted command-index or command-doc regression coverage added for this slice

## Proposed Technical Approach
- Treat the command index implementation-path field as the parity oracle for the affected family-owned command docs because it is already derived from the live registry-backed parser tree.
- Reconcile the affected command-doc `Source Surface` table rows and `## Source Surface` sections to the same family-owned implementation paths already published in the command index.
- Add only the narrowest targeted drift guard needed to keep the affected docs from regressing back to `main.py` where a more specific owning family file already exists.
- Keep the slice explicitly companion-only: the slice may make docs and drift checks more precise, but it may not create a second durable command-authority definition.

## Coverage Map
| Family | Affected Commands | Current Owning Implementation Path |
|---|---|---|
| `doctor` | `watchtower-core doctor` | `core/python/src/watchtower_core/cli/doctor_family.py` |
| `sync` | `watchtower-core sync command-index`; `decision-index`; `decision-tracking`; `design-document-index`; `design-tracking`; `foundation-index`; `github-tasks`; `initiative-index`; `initiative-tracking`; `prd-index`; `prd-tracking`; `reference-index`; `repository-paths`; `standard-index`; `task-index`; `task-tracking`; `traceability-index`; `workflow-index` | `core/python/src/watchtower_core/cli/sync_family.py` |
| `validate` | `watchtower-core validate acceptance`; `all`; `document-semantics`; `front-matter` | `core/python/src/watchtower_core/cli/validate_family.py` |

## Work Breakdown
1. Confirm the full affected command set by comparing command-doc `Source Surface` fields to command-index `implementation_path` values.
2. Reconcile the affected command docs to the family-owned implementation surfaces already published by the command index.
3. Add the narrowest targeted drift guard needed to fail if the affected docs drift back to stale `main.py` ownership while the command index still points to family files.
4. Rebuild the command index and validate the repo.
5. Stop with an explicit follow-up review task before any broader Phase 3 or Phase 4 work begins.

## Implementation Outcome
- The root command page's primary `## Source Surface` entry and the bounded `doctor`, `sync`, and `validate` command docs now align with the parser-owned or family-owned implementation paths already published in the command index.
- `core/python/src/watchtower_core/repo_ops/sync/command_index.py` now fails closed when a companion command doc's `Command` table or primary `## Source Surface` entry drifts from the registry-backed implementation path.
- `core/python/tests/unit/test_command_index_sync.py` now enforces that alignment directly for the current command-doc family.

## Parity Method
- Compare each affected command doc against the corresponding `implementation_path` entry in `core/control_plane/indexes/commands/command_index.v1.json`.
- Reconfirm that the command index entries remain derived from:
  - `core/python/src/watchtower_core/cli/registry.py`
  - `core/python/src/watchtower_core/cli/parser.py`
  - `core/python/src/watchtower_core/cli/introspection.py`
- Re-run:
  - `./.venv/bin/watchtower-core validate all`
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query commands --query sync --format json`
- Accept the slice only if command authority remains explicit, public planning parity remains unchanged, and the docs plus command index converge on the same owning family paths for the affected commands.

## Rollback Path
1. Revert the affected command-doc source-surface updates and any targeted drift guard added for this slice.
2. Restore the command companion surfaces to the previously published state without changing `registry.py` or `parser.py`.
3. Rebuild the command index if any helper or validation surface changed.
4. Re-run validation and the planning-authority queries before proceeding again.

## Risks
- The slice can still create hidden authority confusion if a helper or drift guard starts acting like a second command-authority registry instead of using the current parser-backed metadata.
- The mismatch set can widen mid-slice if unrelated command docs change ownership without being reconciled in the same pass.
- A seemingly documentation-only slice can still regress command discovery if the command index and docs stop agreeing about owning implementation paths.

## Validation Plan
- Re-run `./.venv/bin/watchtower-core doctor --format json`.
- Re-run `./.venv/bin/watchtower-core validate all`.
- Rebuild command companion outputs through the normal sync flow after any touched source or doc surfaces change.
- Re-run:
  - `./.venv/bin/watchtower-core query authority --domain planning --format json`
  - `./.venv/bin/watchtower-core query coordination --format json`
  - `./.venv/bin/watchtower-core query planning --trace-id trace.structural_rewrite_program --format json`
  - `./.venv/bin/watchtower-core query commands --query validate --format json`

## Stop Condition
- Stop after the bounded implementation task completes, the slice migration and evidence artifacts are published, and a successor review task is open.
- Do not widen this slice into command-presence, route-family, workflow-family, compatibility, or public-planning changes.

## References
- [structural_rewrite_phase3_command_authority_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [command_documentation_and_lookup.md](/home/j/WatchTowerPlan/docs/planning/design/features/command_documentation_and_lookup.md)
- [query_family_source_surface_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/query_family_source_surface_alignment.md)

## Updated At
- `2026-03-14T05:41:11Z`
