# Plan Rebuild Harness Export Foundation Design Record

## Summary
Exports a reusable rebuild harness and routes the existing plan and project derived-surface rebuilds through the new boundary.

## Design Boundary
- The reusable-core boundary should expose rebuild orchestration primitives only, not plan-specific document shaping or repo-local rebuild target catalogs.
- The new harness should support deterministic multi-output rebuild runs because the current plan and project callers each emit multiple JSON indexes plus multiple rendered Markdown views in one rebuild step.
- JSON outputs should remain writable through the existing artifact store while rendered Markdown outputs keep repository-relative filesystem writes with normalized trailing newlines.
- The reusable result contract should preserve per-output metadata so downstream callers can report what was rebuilt without importing repo-local services.

## Consumer Boundary
- `PlanWorkspaceService` remains responsible for loading authoritative initiative state and shaping the aggregate plan-pack outputs.
- `ProjectWorkspaceService` remains responsible for loading authoritative project state and shaping the project-pack outputs.
- Both services should delegate only the write orchestration and output accounting to the new rebuild harness.

## Validation Boundary
- Focused unit coverage should prove the new harness handles JSON and Markdown outputs deterministically and supports dry-run versus write flows.
- Boundary tests should prove `watchtower_core.rebuild` exports only the reusable harness surfaces and fails closed for repo-local rebuild services.
- Existing plan and project workspace integration tests should continue to pass against the refactored rebuild path.
