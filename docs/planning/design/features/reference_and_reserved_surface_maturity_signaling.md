---
trace_id: trace.reference_and_reserved_surface_maturity_signaling
id: design.features.reference_and_reserved_surface_maturity_signaling
title: Reference and Reserved Surface Maturity Signaling Feature Design
summary: Defines the technical design boundary for Reference and Reserved Surface
  Maturity Signaling.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-13T15:32:46Z'
audience: shared
authority: authoritative
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

# Reference and Reserved Surface Maturity Signaling Feature Design

## Record Metadata
- `Trace ID`: `trace.reference_and_reserved_surface_maturity_signaling`
- `Design ID`: `design.features.reference_and_reserved_surface_maturity_signaling`
- `Design Status`: `active`
- `Linked PRDs`: `prd.reference_and_reserved_surface_maturity_signaling`
- `Linked Decisions`: `decision.reference_and_reserved_surface_maturity_signaling_direction`
- `Linked Implementation Plans`: `design.implementation.reference_and_reserved_surface_maturity_signaling`
- `Updated At`: `2026-03-13T15:32:46Z`

## Summary
Defines the technical design boundary for Reference and Reserved Surface Maturity Signaling.

## Source Request
- Perform another comprehensive internal refactor review, follow the traced task cycle, and keep reviewing under the same theme until repeated confirmation passes find no new actionable issue.

## Scope and Feature Boundary
- Covers the open refactor follow-up around reference-corpus maturity signaling: reference docs, the family README and template, reference standards, semantic validation, the reference-index schema and examples, sync and query behavior, typed models, CLI help, command docs, and adjacent regression coverage.
- Covers the README-only reserved-family follow-up around control-plane schema-index, registry-index, execution-policy, and validation-policy directories plus their parent start-here entrypoints and adjacent maintenance guidance.
- Covers the same-change derived surfaces that must stay aligned when the governing docs or query behavior changes, including the reference index, command index, repository path index, planning trackers, and traceability joins touched by the task lifecycle.
- Excludes broader standards-corpus boilerplate reduction, test-suite decomposition, repo-local hotspot modularity, and policy-threshold tuning from the refactor audit.
- Excludes deleting candidate future references or retiring reserved families; the slice is about explicit maturity signaling, not authority-family removal.

## Current-State Context
- The discovery pass confirmed that the live reference corpus already uses a small status vocabulary in `Current Repository Status`: 40 reference docs say `Candidate reference`, 22 say `Supporting authority`, and 1 says `Active support`.
- The reference-index sync path currently derives `related_paths` from both `Local Mapping in This Repository` and `References`, which means many candidate references inherit only `docs/references/README.md` as a repo-local path and still appear in query output as `internal=yes`.
- `watchtower-core query references --related-path core/python/ --format json` currently returns zero results even though the command docs and parser examples present directory-style related-path lookup as a normal usage pattern.
- The repository-maintenance standard already distinguishes README-only reserved families from active families, but the control-plane family entrypoints still describe the README-only schema-index, registry-index, execution-policy, and validation-policy directories in the same tone as live artifact families.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): preserve explicit governed surfaces and deterministic lookup behavior while tightening the seams that currently overstate present-tense support.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep the authored docs, derived indexes, query behavior, and tests aligned in the same change set when a support-signal contract changes.
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): keep the slice inside repository-maintenance and governance-support boundaries rather than turning it into future product policy work.

## Internal Standards and Canonical References Applied
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): reference docs should stay focused on durable lookup content with explicit local mapping rather than generic bibliography links or hidden lifecycle signals.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): the reference index is the machine-readable lookup surface for repository touchpoints and upstream authority, so its fields must reflect the real local-mapping boundary.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): maintenance reviews should call out whether a family is active, reserved, or ambiguous in maturity, and README-only reserved families should be treated as future scope.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command pages should stay aligned with live CLI behavior and avoid examples that do not match the implemented lookup semantics.

## Design Goals and Constraints
- Make maturity signaling explicit enough that humans and machines can tell active support, supporting authority, candidate future guidance, and reserved placeholders apart without browsing raw prose manually.
- Preserve the current reference-document family and the reserved control-plane-family boundaries instead of replacing them with a new meta-surface or deleting useful future guidance.
- Prefer the smallest deterministic implementation that can be validated locally; avoid wide front-matter churn if the live reference corpus already has a stable machine-derivable status vocabulary.
- Fail closed when a reference document drifts from the approved status wording or omits required touchpoint structure for a non-candidate entry.

## Options Considered
### Option 1
- Add a new required front-matter field to every governed reference document and treat that field as the only source of machine-readable maturity status.
- Strength: status parsing becomes trivial and explicit.
- Tradeoff: forces broad repetitive document churn across the full reference corpus even though the live docs already publish a stable, repeated status vocabulary.

### Option 2
- Derive a governed `repository_status` index field from the existing `Current Repository Status` section, tighten semantic validation around the approved phrases, narrow `related_paths` to actual local mapping surfaces, and mark README-only control-plane families as reserved in their entrypoints.
- Strength: fixes the real signaling defect with the smallest authority-preserving change and keeps the live docs, machine index, and query behavior aligned around the corpus the repository already has.
- Tradeoff: requires careful semantic-validation rules and deterministic parsing so the section wording cannot drift silently.

### Option 3
- Leave the machine surfaces unchanged and only rewrite the README pages to explain the intended meaning more clearly.
- Strength: smallest documentation-only change.
- Tradeoff: does not fix the false `internal=yes` query output, does not add machine-readable maturity filtering, and leaves the misleading directory query example unaddressed.

## Recommended Design
### Architecture
- Treat `Current Repository Status` as the authoritative human-readable source for reference maturity while adding a derived `repository_status` field to the reference index.
- Tighten reference semantics so reference docs must publish an approved repository-status phrase and non-candidate entries must keep explicit current touchpoints or equivalent local mapping paths.
- Build `related_paths` and `uses_internal_references` from `applies_to` plus `Local Mapping in This Repository`, not from generic repo-local links in the `References` section.
- Extend `watchtower-core query references` so it can filter by repository status, emit that field in JSON and human output, and treat directory-form related-path filters as descendant matches instead of file-only exact equality.
- Mark the README-only schema-index, registry-index, execution-policy, and validation-policy directories as reserved placeholders in both their leaf READMEs and their parent family entrypoints.

### Data and Interface Impacts
- `core/control_plane/schemas/artifacts/reference_index.v1.schema.json`, `core/control_plane/examples/valid/indexes/reference_index.v1.example.json`, `core/control_plane/indexes/references/reference_index.v1.json`, and the typed `ReferenceIndexEntry` model gain the derived `repository_status` field.
- `core/python/src/watchtower_core/repo_ops/sync/reference_index.py`, `core/python/src/watchtower_core/repo_ops/query/references.py`, `core/python/src/watchtower_core/cli/query_knowledge_family.py`, and `core/python/src/watchtower_core/cli/query_knowledge_handlers.py` change together for the status derivation, related-path behavior, and query output.
- `docs/references/README.md`, `docs/templates/reference_template.md`, `docs/standards/documentation/reference_md_standard.md`, `docs/standards/data_contracts/reference_index_standard.md`, `docs/commands/core_python/watchtower_core_query_references.md`, and nearby workspace command guidance change together for the human-facing contract.
- `core/control_plane/indexes/README.md`, `core/control_plane/indexes/registries/README.md`, `core/control_plane/indexes/schemas/README.md`, `core/control_plane/policies/README.md`, `core/control_plane/policies/execution/README.md`, `core/control_plane/policies/validation/README.md`, and the repository-maintenance standard change together for reserved-family signaling.

### Execution Flow
1. Publish the bounded coverage map and findings ledger for reference maturity and reserved-family signaling before touching implementation.
2. Tighten the reference-document contract, then update reference-index sync, schema, examples, models, and query behavior so maturity status and touchpoint accounting are deterministic.
3. Refresh reference command docs, workspace guidance, and regression coverage so the new query behavior and approved directory-touchpoint semantics stay aligned.
4. Rewrite the control-plane family entrypoints so the README-only families are explicitly reserved placeholders rather than ambiguous live families.
5. Run targeted validation, then full validation, then repeated post-fix and adversarial review passes; if a new issue appears inside the same slice, add it to the findings ledger and repeat.

### Invariants and Failure Cases
- Candidate references must not look like live repository support because of README backlinks alone.
- Reference query behavior must stay deterministic and inspectable; directory lookup support must not degrade into fuzzy substring matching.
- Reserved-family clarification must not hide real live artifacts if any of those directories later gain governed documents; the wording should make the current boundary explicit, not hard-code permanent absence.
- The implementation must fail closed if a reference doc omits the required status section or uses unsupported maturity wording.

## Affected Surfaces
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

## Design Guardrails
- Do not create a second competing authority for reference maturity outside the existing reference docs and derived reference index.
- Do not treat generic repo-local links in `References` as the same thing as present-tense local touchpoints.
- Do not retire the reserved control-plane directories; label them accurately as reserved until real governed artifacts exist there.

## Risks
- The most likely implementation mistake is overfitting the status parser to ad hoc prose instead of the stable approved prefixes already present in the corpus.
- Directory-descendant related-path matching could become inconsistent with other query families if it is implemented as a one-off heuristic rather than a small explicit rule.
- Some candidate references may currently rely on README backlinks to stay discoverable, so the query output and docs must make the new status field visible enough that the loss of those false-positive touchpoints does not reduce real usability.

## References
- March 2026 refactor audit
