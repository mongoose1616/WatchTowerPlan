---
id: "ref.nist_ai_600_1"
title: "NIST AI 600-1 Reference"
summary: "This document provides a working reference for NIST AI 600-1, the Generative AI Profile for the AI RMF."
type: "reference"
status: "active"
tags:
  - "reference"
  - "nist_ai_600_1"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# NIST AI 600-1 Reference
## Summary
This document provides a working reference for NIST AI 600-1, the Generative AI Profile for the AI RMF.

## Purpose
Provide a GenAI-specific governance overlay when AI policy needs more specific controls than the base AI RMF alone.

## Scope
- Covers NIST AI 600-1.
- Does not by itself define repository-local AI guardrails or workflows.

## Canonical Upstream
- `https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence` - verified 2026-03-09; official upstream source.
- `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` - verified 2026-03-09; official publication PDF.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What This Adds Beyond AI RMF
- Use AI 600-1 when generative-AI-specific risks need more concrete treatment than a general AI governance framework.
- Treat it as a profile and companion, not as a replacement for AI RMF governance.
- Translate the profile into concrete review questions around misuse, output reliability, data handling, and oversight.

### Common GenAI Risk Areas
| Area | Why it matters | Local implication |
|---|---|---|
| content reliability | models can confabulate or overstate confidence | outputs need review and boundary controls |
| data exposure | prompts and outputs can carry sensitive data | handling rules must be explicit |
| misuse or abuse | capabilities can be redirected | safety and access controls matter |
| human oversight | fully automated trust is risky | review and escalation paths may be needed |

### Common Pitfalls
- Claiming "AI RMF aligned" behavior without naming the GenAI-specific controls.
- Treating a profile document as if it directly prescribed implementation details.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if the repository later formalizes GenAI-specific governance or misuse controls.
- Pair it with AI RMF and OWASP GenAI guidance when building policy.

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
