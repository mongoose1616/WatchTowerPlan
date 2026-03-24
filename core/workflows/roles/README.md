# `core/workflows/roles`

## Description
`This directory is the authoritative shared workflow-role root. It is reserved for shared persona-oriented or reviewer-oriented workflow documents that orchestrate reusable modules without becoming pack-local exceptions.`

## Notes
- Shared reusable workflow roles live here only when the role is truly cross-pack rather than domain-specific.
- Every shared workflow role must include a `Composes Modules` section that explicitly names the reusable workflow modules the role directly orchestrates.
- The shared or pack-owned routing table remains the authority for which workflow documents become active for one task.
- Most current shared reusable execution guidance still belongs under `core/workflows/modules/`.
- Keep this root intentionally sparse until a role surface is reused across packs without domain-local assumptions.
