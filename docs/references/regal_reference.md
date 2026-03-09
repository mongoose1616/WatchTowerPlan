---
id: "ref.regal"
title: "Regal Reference"
summary: "This document provides a working reference for Regal as a linter and language server for Rego."
type: "reference"
status: "active"
tags:
  - "reference"
  - "regal"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# Regal Reference
## Summary
This document provides a working reference for Regal as a linter and language server for Rego.

## Purpose
Provide a quality and tooling baseline for Rego policy authoring when policy-as-code is adopted.

## Scope
- Covers Regal as a Rego tooling companion.
- Does not require Rego linting unless the repository adopts Rego.

## Canonical Upstream
- `https://www.openpolicyagent.org/projects/regal` - verified 2026-03-09; Introduction.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What Regal Adds
- Lints Rego policy for style, correctness signals, and maintainability issues before they become policy-review noise.
- Helps standardize Rego code quality separately from the policy decisions themselves.
- Works best when the enabled rule set is explicit and reviewed.

### Common Decisions
| Question | Preferred answer | Why |
|---|---|---|
| lint all Rego or only selected dirs | choose explicit scope | keeps adoption predictable |
| rule exceptions | narrow, documented suppressions | avoids silent drift |
| config location | one canonical config file | keeps rule intent visible |

### Common Pitfalls
- Treating Regal findings as policy semantics rather than code-quality guidance.
- Using broad suppressions until the lint signal loses value.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference only if the repository later adopts OPA/Rego.
- Pair it with OPA/Rego policy standards or validation workflows.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.

## Updated At
- `2026-03-09T05:03:16Z`
