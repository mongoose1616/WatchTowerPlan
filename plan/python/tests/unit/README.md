# `plan/python/tests/unit`

## Description
`This directory contains the fast plan-owned unit suite. Keep tests here when they import watchtower_plan directly but still stay below repo-materialization or broad workspace orchestration.`

## Notes
- These tests may import `watchtower_plan` directly.
- Shared-core boundary guards do not apply here; this suite belongs to the plan-owned side of the split.
- If a unit-style test can be expressed against `watchtower_core` or `watchtower_host` without direct pack imports, it belongs under `core/python/tests/unit/` instead.
