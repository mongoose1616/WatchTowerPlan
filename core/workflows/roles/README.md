# `core/workflows/roles`

## Description
`This directory is the authoritative shared workflow-role root. It is reserved for shared persona-oriented or reviewer-oriented workflow documents that orchestrate reusable modules without becoming pack-local exceptions.`

## Notes
- Shared reusable workflow roles live here only when the role is truly cross-pack rather than domain-specific.
- Every shared workflow role must include a `Composes Modules` section that explicitly names the reusable workflow modules the role directly orchestrates.
- The shared or pack-owned routing table remains the authority for which workflow documents become active for one task.
- The active shared role set currently includes `workflow_steward.md`, which applies the workflow-system governance lens across workflow docs, routes, indexes, validators, and command-surface parity, and `adversarial_reviewer.md`, which raises the proof bar for contradiction-oriented repository audits without making every normal review adversarial by default.
- Keep this root scoped to shared role orchestration; shared roles should document every materially distinct orchestration boundary they own and should not duplicate reusable module logic that already belongs under `core/workflows/modules/`.
