---
trace_id: trace.versionless_governed_artifact_filenames
id: decision.versionless_governed_artifact_filenames_direction
title: Versionless Governed Artifact Filenames Direction Decision
summary: Records the decision to remove filename-embedded major-version tokens from
  governed artifacts and keep compatibility signaling inside artifact content.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T17:55:05Z'
audience: shared
authority: supporting
applies_to:
- core/control_plane/
- core/python/
- docs/standards/
- docs/planning/
---

# Versionless Governed Artifact Filenames Direction Decision

## Record Metadata
- `Trace ID`: `trace.versionless_governed_artifact_filenames`
- `Decision ID`: `decision.versionless_governed_artifact_filenames_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.versionless_governed_artifact_filenames`
- `Linked Designs`: `design.features.versionless_governed_artifact_filenames`
- `Linked Implementation Plans`: `design.implementation.versionless_governed_artifact_filenames`
- `Updated At`: `2026-03-16T17:55:05Z`

## Summary
Records the decision to remove filename-embedded major-version tokens from governed artifacts and keep compatibility signaling inside artifact content.

## Decision Statement
Governed artifact filenames will stop carrying `.v1` or similar major-version tokens, and compatibility signaling will remain inside artifact content through schema URNs, `$schema` references, and stable machine-readable IDs.

## Trigger or Source Request
- User request to stop using `v1` in governed filenames and enforce a repository standard where compatibility information lives inside the artifact content rather than the path.

## Current Context and Constraints
- The current naming standard explicitly requires versioned governed filenames and the control-plane tree now contains `209` physical `.v1` files.
- Runtime code, tests, registries, and planning docs encode those paths directly, so the repository must migrate them together if the convention changes.
- The product is not released, so a breaking internal rename is acceptable as long as the repository ends in one coherent post-change state.

## Applied References and Implications
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md): must change because it currently mandates version tokens in governed filenames.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): still requires explicit contract metadata and reviewable schema identity even after filenames become versionless.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): same-change alignment across code, docs, and governed artifacts is required for a migration this broad.

## Affected Surfaces
- core/control_plane/
- core/python/
- docs/standards/
- docs/planning/

## Options Considered
### Option 1
- Keep versioned governed filenames and rely on current standards.
- Lowest migration cost.
- Rejected because it conflicts directly with the requested repository policy.

### Option 2
- Allow versionless filenames only for new artifacts while leaving existing `.v1` filenames in place.
- Avoids a large immediate rename.
- Rejected because it would permanently preserve mixed conventions and duplicated review overhead.

### Option 3
- Rename governed files to versionless names repo-wide and update the standards to make that the only accepted convention.
- Produces one clear rule and one coherent tree.
- Chosen because the repository prefers concise reusable surfaces over backward-compatibility baggage.

## Chosen Outcome
- Update the naming and schema standards to prohibit filename-embedded major-version tokens for governed artifacts.
- Rename governed files under `core/control_plane/` to versionless filenames and repair every in-repo path reference in code, tests, docs, registries, and planning records.
- Keep schema URNs and other in-content identifiers versioned where compatibility semantics still matter.

## Rationale and Tradeoffs
- This removes redundant path noise while preserving explicit compatibility semantics inside the artifact itself.
- The migration is broad, but it is cheaper now than after external release, and it prevents future mixed conventions from spreading.

## Consequences and Follow-Up Impacts
- Future governed artifacts must use versionless filenames by default.
- Any generator, loader, validator, or test fixture that derives governed filenames must be updated to emit the new path form.

## Risks, Dependencies, and Assumptions
- The decision depends on a repo-wide path rewrite and full validation pass; missing even one active consumer will surface as broken validation or stale links.

## References
- [versionless_governed_artifact_filenames.md](/docs/planning/prds/versionless_governed_artifact_filenames.md)
- [versionless_governed_artifact_filenames.md](/docs/planning/design/features/versionless_governed_artifact_filenames.md)
