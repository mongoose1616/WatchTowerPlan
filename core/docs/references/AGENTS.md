# AGENTS.md

## Role
- This file applies to the [core/docs/references](/core/docs/references) subtree.
- Use it for local rules that govern external reference documents.
- Keep detailed document structure in the reference template and companion documentation standards rather than expanding this file.

## Scope
- Applies to `core/docs/references/**`.
- If a more-specific `AGENTS.md` exists below this path, treat it as a more local overlay.
- Inherit [AGENTS.md](/AGENTS.md) and [AGENTS.md](/core/docs/AGENTS.md) first and do not weaken them here.

## Routing
- Read this file before creating or updating files in `core/docs/references/**`.
- Inherit repository routing from the domain-owned routing tables under the shared and pack-owned workflow roots.
- Do not turn this file into a second routing table.

## Local Rules
- This directory is only for references derived from internet or other externally published sources.
- Keep shared or cross-pack reference topics here when they support reusable-core behavior, shared standards, or multiple hosted packs.
- Put pack-applied operator mappings under the owning pack `docs/references/` root, even when the upstream topic also exists here.
- Always capture the canonical source URL when the document depends on an external authority.
- Keep each reference bounded to one external standard, framework, specification, or published guidance topic, but include every materially distinct rule, default, edge case, and ambiguity the repository needs.
- Use [reference_template.md](/core/docs/templates/reference_template.md) when creating new reference documents.

## Do
- Keep references tied to official or otherwise authoritative published sources.
- Explain how the external source is relevant to this repository without turning the file into a local policy document.
- Keep the mapping here reusable across shared core or multiple packs.
- Keep normative repository rules in the shared and pack-owned standards roots when they become local standards.

## Do Not
- Do not place repo-native standards or purely local reference notes in this directory.
- Do not move pack-local operator framing into shared core just because the upstream topic is important.
- Do not omit canonical upstream links when the topic depends on an external source.
- Do not expand these files into broad multi-topic surveys when a bounded reference would be clearer.
