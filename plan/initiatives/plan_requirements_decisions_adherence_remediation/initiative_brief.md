# Requirements And Decisions Adherence Remediation

## Summary
Retire the root docs tree, finish the initiative-package hard cutover, and restore rich machine-backed documentation surfaces.

## Identity
- `initiative_id`: `initiative.plan_requirements_decisions_adherence_remediation`
- `trace_id`: `trace.plan_requirements_decisions_adherence_remediation`
- `scope_type`: `pack_wide`

## Problem Statement
- Root `docs/**` still exists as an active documentation root even though the endstate requires durable docs to live only under `core/docs/**` and `plan/docs/**`.
- The pack-level `plan_overview.md` contract is internally inconsistent: the template and section schema require a six-section overview while the rendered-surface registry, runtime builder, tests, and current output still use the old four-section shape.
- Active routing, workflow metadata, standards, command docs, schemas, README surfaces, helper code, and tests still expose retired PRD, feature-design, implementation-plan, and `implementation_planning` terminology even though live initiative packages already use `initiative_brief.md`, `design_record.md`, `implementation_slice.md`, and optional `decision_notes.md`.
- The repo must preserve rich human-facing docs and trackers without sacrificing compact machine indexes or reintroducing docs-backed planning.

## Goals
- Retire root `docs/**` completely and re-root every active documentation family into `core/docs/**` or `plan/docs/**`.
- Make the six-section `plan_overview.md` contract authoritative and fail closed when templates, registries, renderers, or tests drift.
- Hard-cut active terminology and initiative-phase vocabulary to the endstate initiative-package model.
- Replace the remaining retired planning-document semantic helpers with initiative-package authored-input semantics.
- Restore strong Markdown structure, browseable tables, and readable navigation while keeping machine indexes compact and authoritative.
- Add validation and regression guards that prevent `domain_packs`, root `docs/**`, and other retired active surfaces from returning.

## Non-Goals
- Do not revive docs-backed planning, repo-root `workflows/`, or `repo_ops`.
- Do not preserve root `docs/**` as a compatibility root or mirror.
- Do not broaden initiative-local authored inputs into new governed front-matter families unless a current repository requirement explicitly forces it.
- Do not mass-duplicate non-foundation docs across `core/docs/**` and `plan/docs/**` just to preserve old navigation.

## Success Criteria
- No active repo navigation, schema, validator, loader, README, command doc, workflow doc, or standard depends on root `docs/**`.
- `plan_overview.md` renders the governed six-section shape and mismatches fail validation.
- Active routes, workflow docs, standards, command docs, queries, and trackers expose only initiative-package terminology and the endstate phase model.
- Machine lookup remains available through governed indexes after the doc-root move.
- Two post-cutover assessment passes find no remaining actionable gaps.

## Initial Task Set
- `task.plan_requirements_decisions_adherence_remediation.bootstrap`: Bootstrap Requirements And Decisions Adherence Remediation live initiative package.
- `task.plan_requirements_decisions_adherence_remediation.re_root_core_docs`: Move shared command pages, references, templates, and core-owned standards from root docs into `core/docs/**`.
- `task.plan_requirements_decisions_adherence_remediation.re_root_plan_docs`: Move plan-domain governance and durable plan guidance roots under `plan/docs/**` and remove root docs authority.
- `task.plan_requirements_decisions_adherence_remediation.enforce_plan_overview_contract`: Align the `plan_overview.md` template, registry, renderer, tests, and validation.
- `task.plan_requirements_decisions_adherence_remediation.hard_rename_planning_terms`: Hard-cut active planning terminology and initiative phase vocabulary.
- `task.plan_requirements_decisions_adherence_remediation.replace_planning_semantics`: Replace retired PRD and implementation-plan semantics with initiative-package authored-input semantics.
- `task.plan_requirements_decisions_adherence_remediation.restore_rich_rendering`: Restore stronger human-facing Markdown structure, trackers, and navigation.
- `task.plan_requirements_decisions_adherence_remediation.harden_residue_guards`: Add residue and `domain_packs` regression guards.
- `task.plan_requirements_decisions_adherence_remediation.run_assessment_pass_one`: Run the first full repository assessment after the main cutover slices land.
- `task.plan_requirements_decisions_adherence_remediation.run_assessment_pass_two`: Run the final confirmation-pass repository assessment.

## Constraints
- `requirements.md`, `decisions.md`, and the mirrored foundations corpus remain the governing authority when older standards or `main`-branch patterns disagree.
- `core/docs/foundations/**` remains the authored foundations source and `plan/docs/foundations/**` remains the required byte-identical mirror.
- Purge and migration ledgers may continue to mention historical `docs/**` paths, but they cannot remain active dependencies.
