---
trace_id: trace.reference_and_reserved_surface_maturity_signaling
id: design.implementation.reference_and_reserved_surface_maturity_signaling
title: Reference and Reserved Surface Maturity Signaling Implementation Plan
summary: Breaks Reference and Reserved Surface Maturity Signaling into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-13T18:43:00Z'
audience: shared
authority: supporting
applies_to:
- docs/references/
- core/control_plane/indexes/references/
- core/control_plane/indexes/registries/
- core/control_plane/indexes/schemas/
- core/control_plane/policies/
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/query/references.py
- core/python/src/watchtower_core/cli/query_knowledge_handlers.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- docs/commands/core_python/
- docs/standards/data_contracts/reference_index_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/operations/repository_maintenance_loop_standard.md
---

# Reference and Reserved Surface Maturity Signaling Implementation Plan

## Record Metadata
- `Trace ID`: `trace.reference_and_reserved_surface_maturity_signaling`
- `Plan ID`: `design.implementation.reference_and_reserved_surface_maturity_signaling`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.reference_and_reserved_surface_maturity_signaling`
- `Linked Decisions`: `decision.reference_and_reserved_surface_maturity_signaling_direction`
- `Source Designs`: `design.features.reference_and_reserved_surface_maturity_signaling`
- `Linked Acceptance Contracts`: `contract.acceptance.reference_and_reserved_surface_maturity_signaling`
- `Updated At`: `2026-03-13T18:43:00Z`

## Summary
Breaks Reference and Reserved Surface Maturity Signaling into a bounded implementation slice.

## Source Request or Design
- Feature design: [reference_and_reserved_surface_maturity_signaling.md](/home/j/WatchTowerPlan/docs/planning/design/features/reference_and_reserved_surface_maturity_signaling.md)
- PRD: [reference_and_reserved_surface_maturity_signaling.md](/home/j/WatchTowerPlan/docs/planning/prds/reference_and_reserved_surface_maturity_signaling.md)
- Decision: [reference_and_reserved_surface_maturity_signaling_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/reference_and_reserved_surface_maturity_signaling_direction.md)

## Scope Summary
- Land the refactor slice that hardens reference maturity signaling and README-only reserved-family signaling across docs, machine-readable artifacts, query behavior, validation surfaces, and closeout tracking.
- Replace the scaffold placeholders with a real coverage map, findings ledger, and bounded task split before implementation continues.
- Deliver one reference-maturity execution task, one reserved-family execution task, and one validation-closeout task under the same trace.
- Exclude broader standards-corpus simplification, test-suite reorganization, hotspot decomposition, or removal of candidate or reserved families from this initiative.

## Assumptions and Constraints
- The live reference corpus already exposes a stable status vocabulary, so the design can derive a structured index field without editing every reference front matter block.
- The reference index, query command, command docs, standards, and tests must move together in the same slice or the result will create real lookup drift.
- Reserved-family clarification is documentation and entrypoint work only; it should not invent new machine artifact families or delete existing directory boundaries.
- The broader refactor audit remains comparative input, but the trace itself should record only the local findings, tasks, evidence, and confirmation passes needed for this bounded slice.

## Internal Standards and Canonical References Applied
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): the authored reference corpus must publish clear local-mapping and lookup semantics.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): the machine-readable reference lookup surface must reflect real touchpoints and source authority without overclaiming live support.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): README-only reserved families must be called out explicitly during maintenance and review.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): leaf command docs and CLI help must remain aligned with the implemented query semantics.

## Proposed Technical Approach
- Tighten the reference-doc contract and semantic validator around an approved `Current Repository Status` vocabulary, then derive a new `repository_status` field into the reference index from that section instead of from new front matter.
- Narrow reference `related_paths` and `uses_internal_references` to actual local mappings and explicit touchpoints so candidate references do not inherit false active-support signals from README backlinks in the generic `References` section.
- Extend reference query filtering and output to expose the new status field and support directory-descendant matching for `--related-path`, then align CLI help and command docs with that behavior.
- Update control-plane family entrypoints so README-only schema-index, registry-index, execution-policy, and validation-policy directories are explicitly reserved placeholders in both leaf and parent start-here docs.
- Refresh derived indexes, trackers, and command metadata after the authoritative docs and code change, then validate and review the entire bounded slice repeatedly before closeout.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Reference corpus and guidance | `docs/references/README.md`; reference docs under `docs/references/*_reference.md`; `docs/templates/reference_template.md`; `docs/standards/documentation/reference_md_standard.md`; `docs/standards/data_contracts/reference_index_standard.md` | Approved maturity vocabulary, touchpoint semantics, current-vs-future guidance, and authoring contract alignment |
| Reference index family | `core/control_plane/indexes/references/reference_index.v1.json`; `core/control_plane/schemas/artifacts/reference_index.v1.schema.json`; `core/control_plane/examples/valid/indexes/reference_index.v1.example.json`; `core/control_plane/examples/invalid/indexes/reference_index_missing_upstream.v1.example.json`; `core/python/src/watchtower_core/control_plane/models/planning.py`; `core/python/src/watchtower_core/repo_ops/sync/reference_index.py` | Machine-readable maturity field, touchpoint accounting, schema/example alignment, and typed loader behavior |
| Query and command surfaces | `core/python/src/watchtower_core/repo_ops/query/references.py`; `core/python/src/watchtower_core/cli/query_knowledge_family.py`; `core/python/src/watchtower_core/cli/query_knowledge_handlers.py`; `docs/commands/core_python/watchtower_core_query_references.md`; `docs/commands/core_python/watchtower_core_query.md`; `core/python/README.md` | Status-aware lookup, directory related-path behavior, human/json output, and command-doc or help alignment |
| Validation and tests | `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`; `core/python/tests/unit/test_reference_index_sync.py`; `core/python/tests/unit/test_cli_query_commands.py`; `core/python/tests/unit/test_document_semantics_validation.py`; full repo validation surfaces | Fail-closed status semantics, regression coverage, and full-repo guardrails |
| Reserved-family signaling | `core/control_plane/indexes/README.md`; `core/control_plane/indexes/registries/README.md`; `core/control_plane/indexes/schemas/README.md`; `core/control_plane/policies/README.md`; `core/control_plane/policies/execution/README.md`; `core/control_plane/policies/validation/README.md`; `docs/standards/operations/repository_maintenance_loop_standard.md`; `core/control_plane/indexes/repository_paths/repository_path_index.v1.json` | Explicit reserved-state language and adjacent start-here consistency |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.reference_and_reserved_surface_maturity_signaling.001` | `high` | `resolved` | reference docs, reference README and template, reference-index schema/examples/index, reference sync, typed models, reference query and command docs | live reference-index stats now show `readme_only_related_paths: 0`; `watchtower-core query references --query telemetry` now prints `internal=no`; targeted sync/query/semantic tests passed |
| `finding.reference_and_reserved_surface_maturity_signaling.002` | `medium` | `resolved` | reference query service, CLI help, reference command doc, related-path lookup behavior | `watchtower-core query references --related-path core/python/ --format json` now returns 7 descendant matches including `ref.uv`; CLI help and command docs publish the same directory-descendant semantics; CLI regressions passed |
| `finding.reference_and_reserved_surface_maturity_signaling.003` | `medium` | `resolved` | control-plane indexes and policies family entrypoints, repository-maintenance guidance, repository path index | family entrypoints and the repository maintenance standard now use explicit reserved-placeholder wording, and the repository path index summaries for the README-only families project the same reserved state |
| `finding.reference_and_reserved_surface_maturity_signaling.004` | `medium` | `resolved` | acceptance contract, planning catalog, coordination index, task and coordination trackers | the post-fix planning query exposed stale open-task path references after task closeout; updating the acceptance contract and rerunning `sync all --write` restored a single active closeout task and correct closed-task paths in the planning projections |
| `finding.reference_and_reserved_surface_maturity_signaling.005` | `medium` | `resolved` | adjacent reference-dependent test fixtures, governed-markdown reference resolution, standard-index sync dependency paths | the final full `pytest -q` passes exposed two neighboring reference fixtures that still used the legacy shape under `test_governed_markdown_reference_resolution.py` and `test_standard_index_sync.py`; adding the required local-mapping maturity sections restored both dependent test surfaces and their focused reruns passed |

## Work Breakdown
1. Close the bootstrap phase by replacing scaffold placeholders with the real scope, accepted direction, coverage map, findings ledger, aligned acceptance contract, and bounded execution tasks.
2. Complete `task.reference_and_reserved_surface_maturity_signaling.reference_maturity_signaling.002` by hardening reference maturity signaling across docs, validation, schema-backed artifacts, sync, query, command docs, and regression tests.
3. Complete `task.reference_and_reserved_surface_maturity_signaling.reserved_family_signaling.003` by clarifying reserved maturity across the README-only control-plane families and adjacent start-here guidance.
4. Complete `task.reference_and_reserved_surface_maturity_signaling.validation_closeout.004` by running targeted validation, full repository validation, post-fix review, second-angle review, adversarial confirmation, evidence refresh, task closeout, and initiative closeout.

## Risks
- Reference-query behavior is the main implementation risk because directory-descendant matching and status filtering need to stay deterministic while the command docs remain truthful.
- Touchpoint-accounting changes can accidentally drop legitimate local mappings if the implementation narrows `related_paths` too aggressively instead of distinguishing true touchpoints from generic backlinks.
- Reserved-family clarifications can still leave ambiguity if only the leaf READMEs change and the parent family entrypoints remain unqualified.

## Validation Plan
- Run targeted unit coverage for reference-index sync, reference query commands, and reference semantic validation while the reference-maturity slice lands.
- Rebuild the affected governed surfaces with `./.venv/bin/watchtower-core sync all --write`.
- Run full repository validation with `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/ruff check .`, and `./.venv/bin/python -m mypy src/watchtower_core`.
- Re-run the bounded refactor review from a fresh angle, then run an adversarial confirmation pass whose job is to falsify the claim that the reference and reserved-family slice is clean.
- Refresh the acceptance contract, validation evidence, task state, initiative state, and closeout surfaces with the final clean-state evidence before committing.

## References
- March 2026 refactor audit
