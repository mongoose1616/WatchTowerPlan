# AGENTS.md

## Role
- This file applies to the [docs](/home/j/WatchTowerPlan/docs) subtree.
- Use it for documentation-specific rules that do not belong in the root [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md).
- Keep detailed task behavior in workflow modules, standards, templates, or companion docs rather than expanding this file.

## Scope
- Applies to `docs/**`.
- If a more-specific `AGENTS.md` exists below this path, treat it as a more local overlay.
- Inherit the root [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) first and do not weaken it here.

## Routing
- Read this file before working in `docs/**`.
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md) for task classification and workflow-module selection.
- Inherit repository routing from the root [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md).
- Do not turn this file into a second routing table.

## Local Rules
- Write documentation as native guidance for this repository.
- Use current repository paths, names, and terminology.
- Keep each document focused on one succinct standard, topic, or area.
- Prefer companion documents over forcing multiple concerns into one file.
- Do not describe documents as extracted from predecessor repos, external projects, imported artifacts, or filesystem snapshots.
- Do not use phrases such as `observed in`, `appears in the MVP repositories`, `based on source material from`, or references to `/home/...` source paths inside normal repository docs.
- Do not preserve predecessor project names in document titles, summaries, section headings, tables, or filenames unless the document is explicitly historical or comparative.
- When a standard or framework is relevant, present it as a current working reference for this repo or a candidate standard for this repo.
- Cite official standards or vendor documentation only when the standard itself is the subject of the document or the citation materially improves clarity.
- Prefer direct framing such as `This document defines...` or `This document provides a working reference for...` instead of lineage-based framing.

## Do
- Keep documentation scoped, current, and easy to scan.
- Use real repository paths and real repository surfaces when mapping guidance locally.
- Split documents when one file starts mixing multiple concerns heavily.

## Do Not
- Do not reintroduce predecessor-repo framing into normal docs.
- Do not turn documentation files into mixed-purpose catch-all notes.
- Do not move workflow execution procedure out of `workflows/**` unless the document is itself a workflow module.
