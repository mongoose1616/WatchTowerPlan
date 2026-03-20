from __future__ import annotations

import ast
from pathlib import Path

UNIT_TEST_ROOT = Path(__file__).resolve().parent


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
