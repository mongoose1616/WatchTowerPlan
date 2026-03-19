# Plan Task Authority, Rendering, and Governance Recovery Implementation Slice

## Summary
Cuts over live task authority, restores human-readable planning renders, rewrites governance guidance, and validates the repaired operational flows.

## Initial Work Breakdown
- `task.plan_task_authority_rendering_governance_recovery.cut_over_runtime_and_cli`: Replace docs-backed task mutation paths with initiative-local live plan task state and canonical status handling.
- `task.plan_task_authority_rendering_governance_recovery.align_bootstrap_sync_and_fixtures`: Repair planning bootstrap, sync consumers, GitHub preview, and reduced fixture repos to use live plan task state.
- `task.plan_task_authority_rendering_governance_recovery.restore_human_render_depth_and_markdown`: Recover rich human-facing rendered tracker output and Markdown structure using selective patterns from main.
- `task.plan_task_authority_rendering_governance_recovery.rewrite_governance_and_command_guidance`: Update AGENTS layers, workflow modules, standards, READMEs, and command docs to the live authority model and restored human renders.
- `task.plan_task_authority_rendering_governance_recovery.validate_operational_flows`: Run end-to-end operational scenarios, close the valid report issues, and record any remaining standards gaps with evidence.

## Remaining Structural Gap
- `watchtower_core.repo_ops` is still materially broad after this remediation slice. A current workspace scan shows 93 Python source files still reference `repo_ops`, so full elimination remains a dedicated architecture tranche rather than a safe follow-on edit inside this report fix.
- This slice fixed correctness and standards gaps around live task authority, fixture/runtime-pack alignment, rendered depth, loader cache reuse, and governance drift, but it did not yet collapse the remaining repo-local orchestration namespace.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
