# Planning Author Role

## Purpose
Use this role to orchestrate end-to-end planning authoring so initiative intake, technical design, and implementation slicing hand off cleanly without duplicating module logic or carrying unresolved ambiguity forward.

## Use When
- One request spans initiative brief authoring, design planning, and implementation-slice planning together.
- The task needs a thin orchestration layer that sequences the planning artifacts and their handoff boundaries explicitly.
- The planning package should stay coherent across multiple planning modules instead of being produced as disconnected documents.

## Inputs
- Scoped planning-package request
- Current initiative context, repository state, and applicable foundations or standards
- Any existing initiative brief, design notes, or implementation-planning fragments that must be reconciled

## Composes Modules
- [initiative_brief_authoring.md](../modules/initiative_brief_authoring.md): establishes the authoritative intake boundary, scope, and acceptance seeds for the initiative package.
- [design_record_planning.md](../modules/design_record_planning.md): turns the scoped initiative into a review-ready technical design with explicit implementation guardrails.
- [implementation_slice_planning.md](../modules/implementation_slice_planning.md): turns the settled scope and design into execution slices with a task-management handoff.

## Workflow
1. Confirm whether the request really spans multiple planning artifacts rather than one narrow planning module.
2. Establish the upstream boundary with `initiative_brief_authoring.md` before allowing design work to settle scope implicitly.
3. Move into `design_record_planning.md` only after the intake boundary is explicit enough to support technical tradeoff analysis.
4. Move into `implementation_slice_planning.md` only after the design boundary is explicit enough to support stable execution slicing.
5. Escalate to `decision_capture.md` or clarification when unresolved tradeoffs or missing inputs would otherwise leak ambiguity into downstream planning artifacts.

## Data Structure
- Ordered planning-artifact chain from initiative brief through design record to implementation slice
- Explicit escalation points for clarification or decision capture when planning cannot advance cleanly

## Outputs
- A coherent planning package with explicit handoff boundaries between brief, design, and implementation slice
- Explicit escalation notes when unresolved ambiguity blocked one stage of planning

## Done When
- Each planning artifact has a clear upstream input boundary and downstream handoff boundary.
- Scope, design, and execution slicing no longer rely on implied context between documents.
- The role has orchestrated the planning chain without copying the module procedures into role prose.
