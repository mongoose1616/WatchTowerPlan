# AGENTS.md

## Role
- This file applies to the [docs/references](/home/j/WatchTowerPlan/docs/references) subtree.
- Use it for local rules that govern external reference documents.
- Keep detailed document structure in the reference template and companion documentation standards rather than expanding this file.

## Scope
- Applies to `docs/references/**`.
- If a more-specific `AGENTS.md` exists below this path, treat it as a more local overlay.
- Inherit [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) and [docs/AGENTS.md](/home/j/WatchTowerPlan/docs/AGENTS.md) first and do not weaken them here.

## Routing
- Read this file before creating or updating files in `docs/references/**`.
- Inherit repository routing from [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md).
- Do not turn this file into a second routing table.

## Local Rules
- This directory is only for references derived from internet or other externally published sources.
- Always capture the canonical source URL when the document depends on an external authority.
- Keep each reference focused on one succinct external standard, framework, specification, or published guidance topic.
- Use [reference_template.md](/home/j/WatchTowerPlan/docs/templates/reference_template.md) when creating new reference documents.

## Do
- Keep references tied to official or otherwise authoritative published sources.
- Explain how the external source is relevant to this repository without turning the file into a local policy document.
- Keep normative repository rules in `docs/standards/**` when they become local standards.

## Do Not
- Do not place repo-native standards or purely local reference notes in this directory.
- Do not omit canonical upstream links when the topic depends on an external source.
- Do not expand these files into broad multi-topic surveys when a focused reference would be clearer.
