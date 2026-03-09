---
id: "ref.owasp_genai_security_project"
title: "OWASP GenAI Security Project Reference"
summary: "This document provides a working reference for the OWASP GenAI Security Project."
type: "reference"
status: "active"
tags:
  - "reference"
  - "owasp_genai_security_project"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# OWASP GenAI Security Project Reference
## Summary
This document provides a working reference for the OWASP GenAI Security Project.

## Purpose
Provide an external security baseline for AI- and LLM-related system risks, controls, and design review.

## Scope
- Covers the OWASP GenAI Security Project as a reference source.
- Does not by itself define the repository's AI governance policy.

## Canonical Upstream
- `https://genai.owasp.org/` - verified 2026-03-09 via official project search results; OWASP GenAI Security Project home.
- `https://genai.owasp.org/introduction/` - verified 2026-03-09 via official project search results; project introduction and scope.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### Common GenAI Security Concern Areas
| Area | Why it matters | Local implication |
|---|---|---|
| prompt injection | model instructions can be redirected | inputs and tool use need boundaries |
| data leakage | prompts, memory, or outputs can expose sensitive data | handling and retention rules matter |
| output misuse | model output can trigger unsafe downstream actions | human review and execution guards may be needed |
| supply chain and model provenance | model or plugin trust affects risk | source and update policy matter |

### Core Rules
- Use the project as a structured GenAI security reference, not as self-executing local policy.
- Translate the guidance into repository-specific safeguards, oversight, and misuse controls.
- Keep the model, prompt, tool, and output boundaries explicit.

### Common Pitfalls
- Treating generic AI security advice as automatically sufficient for this repository.
- Ignoring downstream actions and connectors while focusing only on the model itself.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repository later formalizes AI governance or bounded-agency standards.
- Pair it with NIST AI RMF and AI 600-1 when building governance-oriented policy.

### If Local Policy Tightens
- Promote any adopted repository rule into a narrower standard or workflow instead of leaving the rule only in this reference.
- Keep this file focused on upstream context and quick lookup rather than turning it into the only source of local policy.

## References
- [README.md](/home/j/WatchTowerPlan/docs/references/README.md)

## Notes
- Canonical upstream sources were rechecked on `2026-03-09` during the repository reference refresh.
- The OWASP GenAI project site rate-limited automated fetches during the refresh, so the canonical URLs were rechecked via official project search results before updating this file.
- If this topic becomes active repository policy later, move the enforceable rule into `docs/standards/**` or the relevant workflow module.

## Updated At
- `2026-03-09T05:03:16Z`
