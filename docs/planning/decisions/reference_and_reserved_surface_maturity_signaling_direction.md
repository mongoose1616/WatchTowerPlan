---
trace_id: trace.reference_and_reserved_surface_maturity_signaling
id: decision.reference_and_reserved_surface_maturity_signaling_direction
title: Reference and Reserved Surface Maturity Signaling Direction Decision
summary: Records the initial direction decision for Reference and Reserved Surface
  Maturity Signaling.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T15:32:46Z'
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

# Reference and Reserved Surface Maturity Signaling Direction Decision

## Record Metadata
- `Trace ID`: `trace.reference_and_reserved_surface_maturity_signaling`
- `Decision ID`: `decision.reference_and_reserved_surface_maturity_signaling_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.reference_and_reserved_surface_maturity_signaling`
- `Linked Designs`: `design.features.reference_and_reserved_surface_maturity_signaling`
- `Linked Implementation Plans`: `design.implementation.reference_and_reserved_surface_maturity_signaling`
- `Updated At`: `2026-03-13T15:32:46Z`

## Summary
Records the initial direction decision for Reference and Reserved Surface Maturity Signaling.

## Decision Statement
Execute the next refactor slice by deriving structured reference maturity from the existing `Current Repository Status` section, narrowing reference touchpoint accounting to real local mappings, extending reference query behavior to expose the status and usable directory touchpoint lookup, and explicitly marking README-only control-plane families as reserved placeholders instead of treating them like live artifact families.

## Trigger or Source Request
- Perform another comprehensive internal refactor review, follow the traced task cycle, and continue the themed review loop until repeated confirmation passes find no new actionable issue.

## Current Context and Constraints
- The previous refactor trace explicitly deferred reference-lifecycle signaling and placeholder-family cleanup to later bounded traces.
- The live reference corpus already publishes a stable three-prefix status vocabulary, but the machine-readable reference index and query surfaces do not expose that distinction and currently overclaim internal support for candidate references.
- The maintenance standard already says README-only families should be treated as reserved until real artifacts exist, but the control-plane family entrypoints do not surface that maturity signal clearly enough.
- The slice should improve determinism and reduce ambiguity without forcing broad front-matter churn or deleting useful future guidance.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): simplify by tightening explicit seams and machine-readable read models instead of weakening governed families.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): docs, indexes, queries, and tests must stay aligned when a support-signal contract changes meaning.
- [reference_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/reference_md_standard.md): the reference family should keep local mapping explicit and should not hide lifecycle meaning in unrelated sections.
- [reference_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/reference_index_standard.md): the machine-readable reference lookup surface is the right place to project structured maturity and touchpoint signals.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): reserved families should be called out explicitly during maintenance and review rather than left ambiguous.

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

## Options Considered
### Option 1
- Add a new required front-matter field to every governed reference document and use that field as the only structured source for repository maturity.
- Strength: maximally explicit machine source.
- Tradeoff: broad repetitive document churn across the entire reference corpus even though the live docs already carry a stable status vocabulary.

### Option 2
- Derive a governed `repository_status` field from the existing `Current Repository Status` section, fail closed on unsupported wording, narrow touchpoint accounting to actual local mappings, and mark README-only control-plane families as reserved in their entrypoints.
- Strength: smallest deterministic repair that fixes the real user-facing and machine-facing defects without weakening authority boundaries.
- Tradeoff: requires semantic-validation rules and careful parser behavior so the section vocabulary cannot drift silently.

### Option 3
- Leave the machine surfaces unchanged and clarify the intended semantics only in docs and READMEs.
- Strength: lowest implementation cost.
- Tradeoff: leaves the misleading `internal=yes` query output, the broken directory touchpoint example, and the ambiguous reserved-family start-here surfaces untouched.

## Chosen Outcome
Adopt option 2. The trace will keep the current reference-document family and reserved directory structure, but it will harden the human/machine contract around maturity signaling. Reference docs remain the human authority for status wording, the reference index becomes the machine-readable projection for that status, reference query behavior becomes status-aware and directory-touchpoint aware, and the reserved control-plane families are labeled explicitly in the docs that surface them first.

## Rationale and Tradeoffs
- The live reference corpus already contains the raw status signal we need, so broad front-matter churn would add cost without increasing correctness proportionally.
- The actual defect is not that candidate references exist; it is that machine surfaces and query output currently blur candidate guidance with present-tense support.
- Explicit reserved-family labeling is lower risk and more foundation-aligned than removing those directories or pretending they are already active.
- The tradeoff is a small amount of section parsing and validation logic, but that is preferable to adding another parallel authority field or leaving the misleading query behavior intact.

## Consequences and Follow-Up Impacts
- The reference index schema, examples, sync builder, typed model, query service, CLI handlers, semantic validator, command docs, and tests will all change in the same bounded slice.
- The reserved-family README surfaces will become more explicit about current maturity, and adjacent derived path surfaces will refresh to match.
- Broader follow-up questions such as whether other query families should also support directory-descendant matching remain out of scope unless the post-fix review identifies a concrete same-theme defect.

## Risks, Dependencies, and Assumptions
- Assumes the current reference status vocabulary stays limited to the approved prefixes and can therefore be validated deterministically.
- Depends on same-change updates across human docs, machine artifacts, query behavior, and tests so the new status signal does not drift.
- Risks under-scoping adjacent query-family behavior if the later confirmation passes do not explicitly challenge the related-path semantics from a second angle.

## References
- March 2026 refactor audit
