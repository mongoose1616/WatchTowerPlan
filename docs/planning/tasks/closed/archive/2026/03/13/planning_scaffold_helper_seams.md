---
id: task.planning_authoring_hotspot_regression_hardening.scaffold_modularity.002
trace_id: trace.planning_authoring_hotspot_regression_hardening
title: Refactor planning scaffold helper seams and specs
summary: Extract declarative scaffold specs, focused rendering helpers, bootstrap
  artifact builders, and planning-surface refresh seams while preserving plan command
  behavior.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T17:36:16Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/repo_ops/planning_scaffold_models.py
- core/python/src/watchtower_core/repo_ops/planning_scaffold_rendering.py
- core/python/src/watchtower_core/repo_ops/planning_scaffold_specs.py
- core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py
- core/python/src/watchtower_core/repo_ops/planning_bootstrap_support.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_planning_scaffold_specs.py
- core/python/tests/
- docs/commands/core_python/
related_ids:
- prd.planning_authoring_hotspot_regression_hardening
- design.features.planning_authoring_hotspot_regression_hardening
- design.implementation.planning_authoring_hotspot_regression_hardening
- decision.planning_authoring_hotspot_regression_hardening_direction
- contract.acceptance.planning_authoring_hotspot_regression_hardening
---

# Refactor planning scaffold helper seams and specs

## Summary
Extract declarative scaffold specs, focused rendering helpers, bootstrap artifact builders, and planning-surface refresh seams while preserving plan command behavior.

## Scope
- Extract declarative plan-kind contract helpers from the scaffold support layer.
- Move scaffold rendering, bootstrap artifact generation, and planning-surface refresh into helper-backed seams.
- Keep plan handlers, docs, and scaffold regressions aligned with the split.

## Done When
- The planning scaffold hotspot files are materially smaller and helper-backed.
- Plan command behavior and generated artifact shapes remain stable under targeted tests.
- Adjacent docs and runtime-boundary surfaces stay aligned.
