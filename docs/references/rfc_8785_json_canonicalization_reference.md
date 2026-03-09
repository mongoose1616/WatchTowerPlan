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
updated: "2026-03-09"
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
- `https://www.rfc-editor.org/info/rfc8785`

## Related Standards and Sources
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Quick Reference or Distilled Reference
### Rules or Decision Points
- Use canonicalization only when reproducible bytes materially matter.
- Keep baseline JSON validity separate from canonicalized serialization rules.
- Document where canonicalized JSON is required instead of assuming it implicitly.

## Local Mapping in This Repository
- Use this reference if future manifests, attestations, or integrity checks rely on deterministic JSON output.
- Pair it with checksum or signing standards rather than applying it everywhere by default.

## Process or Workflow
1. Read this reference before codifying RFC 8785 JSON Canonicalization Reference into repository standards, workflows, templates, or automation.
2. Map only the parts that materially improve clarity, correctness, or consistency in this repository.
3. If the repository adopts the reference as policy, move the normative rule into `docs/standards/**` and keep this file as supporting context.

## Examples
- Use this reference when deciding how deterministic JSON hashing and signing should be expressed in repository docs, standards, or automation.
- Use this reference as a supporting source when drafting a focused standards document under `docs/standards/**`.

## References
- [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md)

## Notes
- This file is a working external reference, not a mandatory policy by itself.
- Repository-specific rules should live in `docs/standards/**` when they become normative.

## Last Synced
- `2026-03-09`
