# AGENTS.md

## Role
- Treat this file as the instruction layer for `plan/docs/**`.
- Use it for durable plan-domain guidance rules that apply after live initiative work is promoted.
- Keep task execution behavior in workflow modules rather than expanding this file into a procedure catalog.

## Scope
- Applies to `plan/docs/**`.
- If a more-specific `AGENTS.md` exists below this path, treat it as a more local overlay.
- Inherit [AGENTS.md](/AGENTS.md) and [AGENTS.md](/plan/AGENTS.md) first and do not weaken them here.

## Routing
- Read this file before working in `plan/docs/**`.
- Use [ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md) for plan-domain promotion, traceability, and governance work.
- Use [ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) only for shared documentation or governed-artifact reconciliation modules the plan route explicitly needs.
- Do not turn this file into a second routing table.

## Local Rules
- Treat [requirements.md](/requirements.md) and [decisions.md](/decisions.md) as the controlling contract for promotion targets, durable plan guidance, and endstate document boundaries.
- `plan/docs/**` holds approved durable guidance, not live initiative state.
- Use current initiative-package terminology and current repository paths.
- Keep each document focused on one durable plan-domain guidance concern.
- Keep promoted guidance self-contained and readable without turning it into a live tracker or execution log.
- Keep mirrored foundations under `plan/docs/foundations/**` byte-identical with `core/docs/foundations/**`.

## Do
- Keep durable plan guidance scoped, current, and easy to scan.
- Use `plan/docs/decisions/**`, `plan/docs/patterns/**`, `plan/docs/references/**`, and `plan/docs/standards/**` according to ownership.
- Keep promotion indexes and companion machine-readable surfaces aligned when durable guidance changes materially.

## Do Not
- Do not recreate live initiative or task state under `plan/docs/**`.
- Do not use retired planning-model terminology on active surfaces when the initiative-package terms apply.
- Do not turn promoted guidance into a second execution workspace.
