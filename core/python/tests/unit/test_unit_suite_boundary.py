from __future__ import annotations

import ast
from pathlib import Path

UNIT_TEST_ROOT = Path(__file__).resolve().parent
SHARED_TEST_ROOT = Path(__file__).resolve().parents[1]


def test_unit_suite_does_not_import_repo_fixture_materialization_helpers() -> None:
    violations: list[str] = []

    for path in sorted(UNIT_TEST_ROOT.glob("*.py")):
        if path.name in {"__init__.py", "conftest.py", "test_unit_suite_boundary.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "tests.fixture_repo_support":
                imported_names = ", ".join(sorted(alias.name for alias in node.names))
                violations.append(f"{path.name}: imports repo fixture helpers ({imported_names})")

    assert not violations, "\n".join(violations)


def test_shared_core_test_suites_do_not_import_hosted_pack_packages_directly() -> None:
    violations: list[str] = []

    for path in sorted(SHARED_TEST_ROOT.rglob("*.py")):
        if path.name in {"__init__.py", "conftest.py", "test_unit_suite_boundary.py"}:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        relative_path = path.relative_to(SHARED_TEST_ROOT).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                names = [node.module]
            else:
                continue
            for name in names:
                if not name.startswith("watchtower_"):
                    continue
                if name.startswith(("watchtower_core", "watchtower_host")):
                    continue
                violations.append(f"{relative_path}: imports hosted pack module {name}")

    assert not violations, "\n".join(violations)


def test_shared_core_test_suites_do_not_depend_on_live_plan_pack_settings_path() -> None:
    violations: list[str] = []

    for path in sorted(SHARED_TEST_ROOT.rglob("*.py")):
        if path.name in {"__init__.py", "conftest.py", "test_unit_suite_boundary.py"}:
            continue
        relative_path = path.relative_to(SHARED_TEST_ROOT).as_posix()
        if 'plan/.wt/manifests/pack_settings.json' in path.read_text(encoding="utf-8"):
            violations.append(
                f"{relative_path}: depends on live plan pack settings path "
                "instead of a fixture or pack-owned test root"
            )

    assert not violations, "\n".join(violations)


def test_shared_core_test_suites_do_not_depend_on_live_plan_rendered_surfaces() -> None:
    violations: list[str] = []
    disallowed_literals = (
        "rendered.initiative.plan",
        "rendered.plan.overview",
        "plan/.wt/indexes/initiative_index.json",
    )

    for path in sorted(SHARED_TEST_ROOT.rglob("*.py")):
        if path.name in {"__init__.py", "conftest.py", "test_unit_suite_boundary.py"}:
            continue
        relative_path = path.relative_to(SHARED_TEST_ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for literal in disallowed_literals:
            if literal in text:
                violations.append(
                    f"{relative_path}: depends on live plan-only rendered or planning surface "
                    f"{literal!r} instead of a fixture or pack-owned test root"
                )

    assert not violations, "\n".join(violations)
