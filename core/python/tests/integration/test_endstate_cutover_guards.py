from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

ACTIVE_SURFACE_ROOTS = (
    REPO_ROOT / ".github",
    REPO_ROOT / "core/control_plane/AGENTS.md",
    REPO_ROOT / "core/docs",
    REPO_ROOT / "plan/docs",
    REPO_ROOT / "core/workflows",
    REPO_ROOT / "plan/workflows",
    REPO_ROOT / "core/python/src/watchtower_core",
    REPO_ROOT / "core/control_plane/indexes",
    REPO_ROOT / "core/control_plane/registries",
    REPO_ROOT / "core/control_plane/schemas",
    REPO_ROOT / "README.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "core/python/AGENTS.md",
    REPO_ROOT / "plan/AGENTS.md",
    REPO_ROOT / "plan/python/AGENTS.md",
)
TEXT_SUFFIXES = {".json", ".md", ".py", ".yaml", ".yml"}
BANNED_LITERALS = (
    "docs/planning",
    "prd_generation",
    "feature_design_planning",
    "implementation_planning",
    "planning_scaffolds.py",
    "watchtower_core.repo_ops",
)
BANNED_PATTERNS = (
    re.compile(r"\bPRDs?\b"),
    re.compile(r"feature design", flags=re.IGNORECASE),
    re.compile(r"implementation plan", flags=re.IGNORECASE),
    re.compile(r"plan scaffold", flags=re.IGNORECASE),
    re.compile(r"\(\?:docs\|core/docs\|plan/docs"),
    re.compile(r"current migration boundary", flags=re.IGNORECASE),
    re.compile(r"until the migration is complete", flags=re.IGNORECASE),
    re.compile(r"for the current migration", flags=re.IGNORECASE),
    re.compile(r"active migration", flags=re.IGNORECASE),
    re.compile(r"workflow-root migration", flags=re.IGNORECASE),
    re.compile(r"filled out to the endstate", flags=re.IGNORECASE),
    re.compile(r"being seeded and future promotion paths are still landing", flags=re.IGNORECASE),
    re.compile(r"will later carry", flags=re.IGNORECASE),
    re.compile(r"once promotion support exists", flags=re.IGNORECASE),
)
REMOVED_TEST_PATHS = (
    REPO_ROOT / "core/python/tests/fixture_repo_support.py",
    REPO_ROOT / "core/python/tests/integration/initiative_package_integration_cases.py",
    REPO_ROOT / "core/python/tests/integration/plan_workspace_integration_cases.py",
    REPO_ROOT / "core/python/tests/integration/test_acceptance_reconciliation.py",
    REPO_ROOT / "core/python/tests/integration/test_all_sync.py",
    REPO_ROOT / "core/python/tests/integration/test_all_validation.py",
    REPO_ROOT / "core/python/tests/integration/test_cli_dry_run_authoring_commands.py",
    REPO_ROOT / "core/python/tests/integration/test_cli_planning_query_commands.py",
    REPO_ROOT / "core/python/tests/integration/test_cli_sync_commands.py",
    REPO_ROOT / "core/python/tests/integration/test_coordination_index_sync.py",
    REPO_ROOT / "core/python/tests/integration/test_coordination_tracking_sync.py",
    REPO_ROOT / "core/python/tests/integration/test_evidence_bundle_helper.py",
    REPO_ROOT / "core/python/tests/integration/test_github_task_sync.py",
    REPO_ROOT / "core/python/tests/integration/test_guidance_promotion_integration.py",
    REPO_ROOT / "core/python/tests/integration/test_initiative_bootstrap.py",
    REPO_ROOT / "core/python/tests/integration/test_initiative_closeout.py",
    REPO_ROOT / "core/python/tests/integration/test_initiative_readiness.py",
    REPO_ROOT / "core/python/tests/integration/test_pack_externalization.py",
    REPO_ROOT / "core/python/tests/integration/test_plan_workspace_coordination.py",
    REPO_ROOT / "core/python/tests/integration/test_plan_workspace_indexes.py",
    REPO_ROOT / "core/python/tests/integration/test_plan_workspace_rendering.py",
    REPO_ROOT / "core/python/tests/integration/test_project_scoped_initiatives.py",
    REPO_ROOT / "core/python/tests/integration/test_project_workspace_service.py",
    REPO_ROOT / "core/python/tests/integration/test_runtime_telemetry_integration.py",
    REPO_ROOT / "core/python/tests/integration/test_task_lifecycle.py",
    REPO_ROOT / "core/python/tests/integration/test_task_lifecycle_service.py",
    REPO_ROOT / "core/python/tests/integration/test_task_workflow_end_to_end.py",
    REPO_ROOT / "core/python/tests/integration/test_trace_purge.py",
    REPO_ROOT / "core/python/tests/integration/test_traceability_index_sync.py",
    REPO_ROOT / "core/python/tests/integration/test_workspace_injection.py",
    REPO_ROOT / "core/python/tests/unit/test_cli.py",
    REPO_ROOT / "core/python/tests/unit/test_cli_pack_commands.py",
    REPO_ROOT / "core/python/tests/unit/test_closeout_handlers.py",
    REPO_ROOT / "core/python/tests/unit/test_document_semantics_reference_rules.py",
    REPO_ROOT / "core/python/tests/unit/test_document_semantics_standard_rules.py",
    REPO_ROOT / "core/python/tests/unit/test_document_semantics_validator_selection.py",
    REPO_ROOT / "core/python/tests/unit/test_initiative_package_closeout_helper.py",
    REPO_ROOT / "core/python/tests/unit/test_pack_integration_runtime.py",
    REPO_ROOT / "core/python/tests/unit/test_plan_and_task_handlers.py",
    REPO_ROOT / "core/python/tests/unit/test_plan_python_boundary.py",
    REPO_ROOT / "core/python/tests/unit/test_plan_query_handlers.py",
    REPO_ROOT / "core/python/tests/unit/test_plan_query_service_runtime_guards.py",
    REPO_ROOT / "core/python/tests/unit/test_project_query_handlers.py",
    REPO_ROOT / "core/python/tests/unit/test_validation_suite_service.py",
)
REMOVED_PLACEHOLDER_PATHS = (
    REPO_ROOT / "core/control_plane/indexes/registries",
    REPO_ROOT / "core/control_plane/indexes/schemas",
)


def _iter_active_surface_files() -> tuple[Path, ...]:
    paths: list[Path] = []
    for root in ACTIVE_SURFACE_ROOTS:
        if root.is_file():
            paths.append(root)
            continue
        paths.extend(
            path
            for path in sorted(root.rglob("*"))
            if path.is_file() and path.suffix in TEXT_SUFFIXES
        )
    return tuple(paths)


def _iter_paths_table_duplicates(path: Path) -> tuple[tuple[str, int, int], ...]:
    duplicates: list[tuple[str, int, int]] = []
    in_paths_section = False
    seen: dict[str, int] = {}

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            in_paths_section = line.strip() == "## Paths"
            seen = {}
            continue
        if not in_paths_section or not line.startswith("| `"):
            continue

        path_literal = line.split("`", 2)[1]
        if path_literal in seen:
            duplicates.append((path_literal, seen[path_literal], line_number))
            continue
        seen[path_literal] = line_number

    return tuple(duplicates)


def test_root_docs_and_domain_packs_paths_are_gone() -> None:
    assert not (REPO_ROOT / "docs").exists()
    assert not (REPO_ROOT / "domain_packs").exists()


def test_removed_repo_fixture_helpers_and_repo_aware_unit_paths_stay_gone() -> None:
    violations = [
        path.relative_to(REPO_ROOT).as_posix() for path in REMOVED_TEST_PATHS if path.exists()
    ]
    assert not violations, "\n".join(violations)


def test_removed_placeholder_index_roots_stay_gone() -> None:
    violations = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in REMOVED_PLACEHOLDER_PATHS
        if path.exists()
    ]
    assert not violations, "\n".join(violations)


def test_cli_main_compatibility_shim_stays_thin_and_host_forwarding_only() -> None:
    shim_path = REPO_ROOT / "core/python/src/watchtower_core/cli/main.py"
    text = shim_path.read_text(encoding="utf-8")

    assert "from watchtower_host.cli.main import main" in text
    assert "raise SystemExit(main())" in text
    assert "ArgumentParser" not in text
    assert "load_command_group_specs" not in text


def test_instruction_layers_publish_current_core_plan_boundaries() -> None:
    expectations = {
        REPO_ROOT / "AGENTS.md": ("core/control_plane/", "plan/.wt/", "plan/python/**"),
        REPO_ROOT / "plan/AGENTS.md": ("plan/.wt/", "plan/docs/**", "plan/python/**"),
        REPO_ROOT / "core/python/AGENTS.md": (
            "watchtower_core/**",
            "plan/python/**",
            "plan/.wt/**",
        ),
        REPO_ROOT / "plan/python/AGENTS.md": (
            "core/python/src/watchtower_core/**",
            "watchtower_plan",
            "plan-domain runtime under `watchtower_core.plan_runtime`",
        ),
        REPO_ROOT / "core/control_plane/AGENTS.md": (
            "core/control_plane/**",
            "owning pack machine root",
            "schemas",
        ),
    }

    violations: list[str] = []
    for path, required_fragments in expectations.items():
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                violations.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()}: "
                    f"missing expected boundary fragment {fragment!r}"
                )

    assert not violations, "\n".join(violations)


def test_readme_layers_publish_current_core_plan_boundaries() -> None:
    expectations = {
        REPO_ROOT / "README.md": (
            "core/control_plane/README.md",
            "plan/.wt/indexes/coordination_index.json",
            "plan/python/README.md",
        ),
        REPO_ROOT / "plan/README.md": ("plan/.wt/**", "plan/python/", "machine state only"),
        REPO_ROOT / "core/control_plane/README.md": (
            "authored machine authority",
            "<pack>/.wt/**",
            "live pack machine state",
        ),
        REPO_ROOT / "core/python/README.md": (
            "watchtower_core",
            "watchtower_<pack>",
            "pack workspaces",
        ),
        REPO_ROOT / "plan/python/README.md": (
            "approved plan-owned Python boundary",
            "plan/.wt/**",
            "watchtower_plan",
        ),
        REPO_ROOT / "plan/python/src/watchtower_plan/README.md": (
            "watchtower_core",
            "plan/.wt/**",
            "plan-flavored duplicates",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/README.md": (
            "watchtower_<pack>",
            "reusable-core",
            "pack-owned logic",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/control_plane/README.md": (
            "pack workspace",
            "machine authority",
            "repo-local pack behavior",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/rebuild/README.md": (
            "reusable_core",
            "Plan-specific rebuild target catalogs",
            "reusable rebuild primitives",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/query/README.md": (
            "watchtower_<pack>.query",
            "pack-flavored duplicates",
            "generic governed-surface query helpers",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/documentation/README.md": (
            "watchtower_<pack>.validation",
            "repo-shared governed-document helpers",
            "repo-local semantic validators",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/evidence/README.md": (
            "repo-local evidence workflow policy",
            "reusable evidence bundle",
            "validation-evidence",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/routing/README.md": (
            "pack-flavored routing wrappers",
            "governed route selection",
            "repo-local route narration",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/sync/README.md": (
            "watchtower_<pack>.sync",
            "pack-flavored copies",
            "reusable harness behavior",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/validation/README.md": (
            "watchtower_<pack>.validation",
            "pack-flavored duplicates",
            "reusable suite orchestration",
        ),
        REPO_ROOT / "core/python/src/watchtower_core/workflow_execution/README.md": (
            "reusable workflow execution semantics",
            "repo-local planning mutations",
            "pack-specific event persistence",
        ),
        REPO_ROOT / "plan/python/src/watchtower_plan/query/README.md": (
            "plan/.wt/**",
            "watchtower_core.query",
            "plan-flavored duplicates",
        ),
        REPO_ROOT / "plan/python/src/watchtower_plan/sync/README.md": (
            "plan/.wt/**",
            "watchtower_core.sync",
            "plan-flavored duplicates",
        ),
        REPO_ROOT / "plan/python/src/watchtower_plan/validation/README.md": (
            "watchtower_core.validation",
            "generic validators",
            "repo-local semantic validation",
        ),
        REPO_ROOT / "plan/python/src/watchtower_plan/closeout/README.md": (
            "machine-state root",
            "reusable core",
            "live plan state",
        ),
        REPO_ROOT / "core/docs/README.md": (
            "authored foundations source",
            "byte-identical mirror",
            "Root `docs/` is retired",
        ),
        REPO_ROOT / "plan/docs/README.md": (
            "authored foundations source",
            "byte-identical mirror",
            "second live planning workspace",
        ),
    }

    violations: list[str] = []
    for path, required_fragments in expectations.items():
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                violations.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()}: "
                    f"missing expected README fragment {fragment!r}"
                )

    assert not violations, "\n".join(violations)


def test_specific_active_readmes_do_not_use_stale_future_boundary_wording() -> None:
    expectations = {
        REPO_ROOT / "core/workflows/README.md": ("future core-owned workflow guidance",),
        REPO_ROOT / "core/control_plane/schemas/interfaces/packs/README.md": (
            "future domain packs",
            "future pack artifact index",
        ),
    }

    violations: list[str] = []
    for path, banned_fragments in expectations.items():
        text = path.read_text(encoding="utf-8")
        for fragment in banned_fragments:
            if fragment in text:
                violations.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()}: "
                    f"contains stale fragment {fragment!r}"
                )

    assert not violations, "\n".join(violations)


def test_active_readme_paths_tables_do_not_repeat_entries() -> None:
    violations: list[str] = []
    for path in _iter_active_surface_files():
        if path.name != "README.md":
            continue
        for duplicated_path, first_line, duplicate_line in _iter_paths_table_duplicates(path):
            violations.append(
                f"{path.relative_to(REPO_ROOT).as_posix()}: "
                f"duplicate ## Paths entry {duplicated_path!r} "
                f"at lines {first_line} and {duplicate_line}"
            )

    assert not violations, "\n".join(violations)


def test_active_endstate_surfaces_do_not_publish_retired_planning_residue() -> None:
    violations: list[str] = []

    for path in _iter_active_surface_files():
        relative_path = path.relative_to(REPO_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for literal in BANNED_LITERALS:
            if literal in text:
                violations.append(f"{relative_path}: contains retired literal {literal!r}")
        for pattern in BANNED_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                violations.append(
                    f"{relative_path}: contains retired pattern {pattern.pattern!r} "
                    f"via {match.group(0)!r}"
                )

    assert not violations, "\n".join(violations)
