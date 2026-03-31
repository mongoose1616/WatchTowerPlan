from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

SHARED_CORE_SURFACES = (
    "core/control_plane/registries/validation_suite_registry.json",
    "core/docs/commands/core_python/watchtower_core_pack_bootstrap.md",
    "core/docs/foundations/customer_story.md",
    "core/docs/foundations/engineering_stack_direction.md",
    "core/docs/standards/documentation/README.md",
    "core/docs/standards/engineering/README.md",
    "core/docs/standards/operations/customer_release_and_bootstrap_standard.md",
    "core/docs/standards/workflows/README.md",
)

DISALLOWED_SHARED_CORE_STRINGS = (
    "planning repository",
    "plan-pack orchestration",
    "live plan-pack baseline",
    "`WatchTowerPlan` is preparing",
    "plan/docs/foundations/**",
    "plan/.wt/manifests/pack_runtime_manifest.json",
)


def test_shared_core_docs_and_registry_stay_portable() -> None:
    violations: list[str] = []
    for relative_path in SHARED_CORE_SURFACES:
        text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        for disallowed in DISALLOWED_SHARED_CORE_STRINGS:
            if disallowed in text:
                violations.append(f"{relative_path}: {disallowed}")

    assert violations == []
