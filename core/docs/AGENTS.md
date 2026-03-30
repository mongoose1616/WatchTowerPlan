# AGENTS.md

## Role
- Treat this file as the instruction layer for `core/docs/**`.
- Use it for documentation-specific rules that govern shared and core-owned durable docs.
- Keep detailed task behavior in workflow modules, standards, templates, or companion docs rather than expanding this file.

## Scope
- Applies to `core/docs/**`.
- If a more-specific `AGENTS.md` exists below this path, treat it as a more local overlay.
- Inherit the root [AGENTS.md](/AGENTS.md) first and do not weaken it here.

## Routing
- Read this file before working in `core/docs/**`.
- Use [ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) for documentation, reconciliation, and engineering routes.
- Use a pack-owned routing table only when pack-domain governance work happens to touch `core/docs/**`.
- Do not turn this file into a second routing table.

## Local Rules
- Treat the authored foundations under [core/docs/foundations/](/core/docs/foundations/) and the current documentation standards under [core/docs/standards/](/core/docs/standards/) as the controlling contract for documentation roots and endstate behavior.
- Use `watchtower-core query authority` to resolve canonical documentation and standards surfaces before broad scanning, and use `watchtower-core query templates` before drafting or materially restructuring governed docs whose family shape already exists.
- Write documentation as native guidance for this repository.
- Use current repository paths, names, and terminology.
- Keep each document focused on one standard, topic, or area.
- Prefer companion documents over mixed-purpose catch-all files.
- Do not describe documents as extracted from predecessor repos, imported snapshots, or filesystem copies.
- Do not preserve predecessor project names in titles, summaries, headings, tables, or filenames unless the document is explicitly historical or comparative.
- Keep shared command docs, references, templates, and shared or core-owned standards under `core/docs/**`.
- Keep authored shared foundations under `core/docs/foundations/**`.
- Keep pack-owned mirrors, promoted guidance, and pack-specific documentation roots under the owning pack docs root and pack-local registries instead of encoding them into shared-core path rules.

## Do
- Keep documentation scoped, current, and easy to scan.
- Use real repository paths and real repository surfaces when mapping guidance locally.
- Keep observed facts, local interpretation, and normative repository policy distinguishable when a document depends on external or multi-surface authority.
- Split documents when one file starts mixing multiple concerns heavily.

## Do Not
- Do not reintroduce predecessor-repo framing into normal docs.
- Do not turn documentation files into mixed-purpose catch-all notes.
- Do not move pack-owned durable guidance into `core/docs/**` when an owning pack docs root owns it.
