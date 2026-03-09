---
id: "ref.opa_rego"
title: "OPA and Rego Reference"
summary: "This document provides a working reference for Open Policy Agent and the Rego policy language."
type: "reference"
status: "active"
tags:
  - "reference"
  - "opa_rego"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# OPA and Rego Reference
## Summary
This document provides a working reference for Open Policy Agent and the Rego policy language.

## Purpose
Provide a policy-as-code baseline when repository controls need declarative, testable policy rules.

## Scope
- Covers OPA and Rego together as a policy engine and language pair.
- Does not define the repository's policy model by itself.

## Canonical Upstream
- `https://www.openpolicyagent.org/docs` - verified 2026-03-09; Open Policy Agent (OPA).
- `https://www.openpolicyagent.org/docs/policy-language` - verified 2026-03-09; Policy Language.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Core Rego Concepts
| Concept | Role | Notes |
|---|---|---|
| package | policy namespace | keeps modules organized |
| input | data supplied for evaluation | contract should be explicit |
| data | external or contextual data | separate from request-time input |
| rules | derived decisions or facts | often used for allow or deny outcomes |
| default | fallback behavior | useful for fail-closed patterns |

### Core Rules
- Use OPA and Rego when policy logic should be explicit, reviewable, and testable.
- Make input shape and decision outputs explicit before writing many rules.
- Prefer fail-closed defaults when policy governs sensitive behavior.

### Common Pitfalls
- Hiding policy meaning in implicit inputs or external data.
- Letting rule names or outputs drift away from the decision they control.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repository later adds policy-as-code controls under `docs/standards/governance/**` or validation workflows.
- Pair it with Regal when linting or style enforcement for Rego matters.

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
