---
id: "ref.semantic_versioning"
title: "Semantic Versioning Reference"
summary: "This document provides a working reference for Semantic Versioning as a release-versioning convention."
type: "reference"
status: "active"
tags:
  - "reference"
  - "semantic_versioning"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Semantic Versioning Reference
## Summary
This document provides a working reference for Semantic Versioning as a release-versioning convention.

## Purpose
Provide a consistent way to reason about compatibility and release impact when the repository produces versioned artifacts.

## Scope
- Covers SemVer as a versioning model.
- Does not require versioning for artifacts that do not need release semantics.

## Canonical Upstream
- `https://semver.org/` - verified 2026-03-09; Semantic Versioning 2.0.0.

## Related Standards and Sources
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

## Quick Reference or Distilled Reference
### Version Components
| Part | Meaning | Notes |
|---|---|---|
| major | breaking compatibility change | increment when older consumers may break |
| minor | backward-compatible feature addition | adds behavior without breaking existing consumers |
| patch | backward-compatible fix | no intended API or contract break |
| prerelease and build metadata | extra release context | not the same as core compatibility signals |

### Core Rules
- Apply version bumps consistently to the specific artifact or contract being versioned.
- Keep compatibility promises explicit before claiming semantic versioning.
- Use prerelease tags deliberately when stability is not yet promised.

### Common Pitfalls
- Treating every visible change as major without a compatibility definition.
- Publishing semantic-looking versions without honoring backward-compatibility meaning.

## Local Mapping in This Repository
### Current Repository Status
- Supporting authority for current repository docs, standards, commands, or control-plane surfaces.

### Current Touchpoints
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

### Why It Matters Here
- Use this reference when version fields or release workflows are added under `docs/standards/**` or `workflows/**`.
- Pair it with commit and change-control standards when release automation is introduced.

### If Local Policy Tightens
- Update the companion repository surfaces above in the same change set when this topic becomes more prescriptive locally.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- Local policy and workflow behavior should stay in the linked repository artifacts rather than being inferred from this reference alone.

## Updated At
- `2026-03-09T05:03:16Z`
