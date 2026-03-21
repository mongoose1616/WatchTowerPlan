"""Dependency-boundary checks for pack contracts."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from watchtower_core.validation.models import ValidationIssue

CORE_PACKAGE_RELATIVE_PATH = Path("core/python/src/watchtower_core")
HOST_PACKAGE_RELATIVE_PATH = Path("core/python/src/watchtower_host")


def dependency_boundary_issues(
    context: Any,
    runtime_manifest: Any,
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    repo_root = context.loader.repo_root
    core_package_root = repo_root / CORE_PACKAGE_RELATIVE_PATH
    pack_package_root = (
        repo_root
        / runtime_manifest.owned_roots.python_root
        / "src"
        / Path(*runtime_manifest.python_package.split("."))
    )
    if core_package_root.is_dir():
        issues.extend(
            forbidden_import_issues(
                package_root=core_package_root,
                forbidden_prefixes=(runtime_manifest.python_package,),
                code="pack_boundary_core_imports_pack",
                message_prefix="Reusable core may not import pack runtime modules",
            )
        )
        issues.extend(
            forbidden_import_issues(
                package_root=core_package_root,
                forbidden_prefixes=("watchtower_host",),
                code="pack_boundary_core_imports_host",
                message_prefix="Reusable core may not import host composition modules",
                exempt_path_suffixes=("watchtower_core/cli/main.py",),
            )
        )
        issues.extend(sys_path_mutation_issues(core_package_root))
    if pack_package_root.is_dir():
        issues.extend(
            forbidden_import_issues(
                package_root=pack_package_root,
                forbidden_prefixes=("watchtower_host",),
                code="pack_boundary_pack_imports_host",
                message_prefix="Pack runtime may not import host composition modules",
            )
        )
    return tuple(issues)


def forbidden_import_issues(
    *,
    package_root: Path,
    forbidden_prefixes: tuple[str, ...],
    code: str,
    message_prefix: str,
    exempt_path_suffixes: tuple[str, ...] = (),
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for path in sorted(package_root.rglob("*.py")):
        if any(path.as_posix().endswith(suffix) for suffix in exempt_path_suffixes):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            issues.append(
                ValidationIssue(
                    code="pack_boundary_scan_failed",
                    message=f"Could not parse Python module during boundary scan: {exc}",
                    location=path.as_posix(),
                )
            )
            continue
        for module_name in iter_import_modules(tree):
            if not module_matches_forbidden_prefix(
                module_name=module_name,
                forbidden_prefixes=forbidden_prefixes,
            ):
                continue
            issues.append(
                ValidationIssue(
                    code=code,
                    message=f"{message_prefix}: {module_name}",
                    location=path.as_posix(),
                )
            )
    return tuple(issues)


def sys_path_mutation_issues(package_root: Path) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for path in sorted(package_root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            issues.append(
                ValidationIssue(
                    code="pack_boundary_scan_failed",
                    message=f"Could not parse Python module during boundary scan: {exc}",
                    location=path.as_posix(),
                )
            )
            continue
        if not tree_mutates_sys_path(tree):
            continue
        issues.append(
            ValidationIssue(
                code="pack_boundary_core_mutates_sys_path",
                message=(
                    "Reusable core may not mutate sys.path while validating or composing "
                    "pack runtime."
                ),
                location=path.as_posix(),
            )
        )
    return tuple(issues)


def tree_mutates_sys_path(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if func.attr not in {"append", "extend", "insert", "pop", "remove"}:
            continue
        if isinstance(func.value, ast.Attribute) and func.value.attr == "path":
            if isinstance(func.value.value, ast.Name) and func.value.value.id == "sys":
                return True
    return False


def iter_import_modules(tree: ast.AST) -> tuple[str, ...]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules.append(node.module)
    return tuple(modules)


def module_matches_forbidden_prefix(
    *,
    module_name: str,
    forbidden_prefixes: tuple[str, ...],
) -> bool:
    return any(
        module_name == prefix or module_name.startswith(f"{prefix}.")
        for prefix in forbidden_prefixes
    )
