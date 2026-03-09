---
id: "ref.rfc_8785_json_canonicalization"
title: "RFC 8785 JSON Canonicalization Reference"
summary: "This document provides a working reference for RFC 8785 and the JSON Canonicalization Scheme (JCS)."
type: "reference"
status: "active"
tags:
  - "reference"
  - "rfc_8785_json_canonicalization"
owner: "repository_maintainer"
updated_at: "2026-03-09T05:03:16Z"
audience: "shared"
authority: "reference"
---

# RFC 8785 JSON Canonicalization Reference
## Summary
This document provides a working reference for RFC 8785 and the JSON Canonicalization Scheme (JCS).

## Purpose
Provide a canonicalization baseline when hashing, signing, or deterministic JSON comparison requires invariant serialization.

## Scope
- Covers RFC 8785 and the JSON Canonicalization Scheme.
- Does not require canonicalization for every JSON file in the repository.

## Canonical Upstream
- `https://www.rfc-editor.org/info/rfc8785` - verified 2026-03-09; Information on RFC 8785 » RFC Editor.

## Related Standards and Sources
- No narrower repository standard or workflow cites this reference directly yet.

## Quick Reference or Distilled Reference
### What Canonicalization Changes
| Concern | Canonicalization does | Why |
|---|---|---|
| whitespace | removes layout freedom | bytes become reproducible |
| object member ordering | imposes deterministic order | signatures and hashes stay stable |
| numeric serialization | normalizes representation | semantically equal values stop producing different bytes |

### Core Rules
- Use JCS only when reproducible byte output materially matters.
- Start from valid JSON first; canonicalization is not a substitute for basic correctness.
- Apply the same canonicalization policy on every producer and verifier path.

### Common Pitfalls
- Mixing canonicalized and ordinary JSON without saying which is required.
- Hashing or signing non-canonical output and expecting stable results.

## Local Mapping in This Repository
### Current Repository Status
- Candidate reference. No active standard or workflow in this repository links this file directly yet.

### Why It Matters Here
- Use this reference if future manifests, attestations, or integrity checks rely on deterministic JSON output.
- Pair it with checksum or signing standards rather than applying it everywhere by default.

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
