"""Dependency-boundary checks for pack contracts."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from watchtower_core.validation.models import ValidationIssue

CORE_PACKAGE_RELATIVE_PATH = Path("core/python/src/watchtower_core")
HOST_PACKAGE_RELATIVE_PATH = Path("core/python/src/watchtower_host")


@dataclass(frozen=True, slots=True)
class PythonModuleBoundaryFact:
    """Parsed import and mutation facts for one Python module."""

    path: str
    imported_modules: tuple[str, ...]
    mutates_sys_path: bool
    scan_error: str | None = None


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
        core_facts = scan_python_boundary_facts(core_package_root)
        issues.extend(scan_failure_issues(core_facts))
        issues.extend(
            forbidden_import_issues(
                facts=core_facts,
                forbidden_prefixes=(runtime_manifest.python_package,),
                code="pack_boundary_core_imports_pack",
                message_prefix="Reusable core may not import pack runtime modules",
            )
        )
        issues.extend(
            forbidden_import_issues(
                facts=core_facts,
                forbidden_prefixes=("watchtower_host",),
                code="pack_boundary_core_imports_host",
                message_prefix="Reusable core may not import host composition modules",
                exempt_path_suffixes=("watchtower_core/cli/main.py",),
            )
        )
        issues.extend(sys_path_mutation_issues(core_facts))
    if pack_package_root.is_dir():
        pack_facts = scan_python_boundary_facts(pack_package_root)
        issues.extend(scan_failure_issues(pack_facts))
        issues.extend(
            forbidden_import_issues(
                facts=pack_facts,
                forbidden_prefixes=("watchtower_host",),
                code="pack_boundary_pack_imports_host",
                message_prefix="Pack runtime may not import host composition modules",
            )
        )
    return tuple(issues)


def forbidden_import_issues(
    *,
    facts: tuple[PythonModuleBoundaryFact, ...],
    forbidden_prefixes: tuple[str, ...],
    code: str,
    message_prefix: str,
    exempt_path_suffixes: tuple[str, ...] = (),
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for fact in facts:
        if fact.scan_error is not None:
            continue
        if any(fact.path.endswith(suffix) for suffix in exempt_path_suffixes):
            continue
        for module_name in fact.imported_modules:
            if not module_matches_forbidden_prefix(
                module_name=module_name,
                forbidden_prefixes=forbidden_prefixes,
            ):
                continue
            issues.append(
                ValidationIssue(
                    code=code,
                    message=f"{message_prefix}: {module_name}",
                    location=fact.path,
                )
            )
    return tuple(issues)


def sys_path_mutation_issues(
    facts: tuple[PythonModuleBoundaryFact, ...],
) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    for fact in facts:
        if fact.scan_error is not None:
            continue
        if not fact.mutates_sys_path:
            continue
        issues.append(
            ValidationIssue(
                code="pack_boundary_core_mutates_sys_path",
                message=(
                    "Reusable core may not mutate sys.path while validating or composing "
                    "pack runtime."
                ),
                location=fact.path,
            )
        )
    return tuple(issues)


@cache
def scan_python_boundary_facts(package_root: Path) -> tuple[PythonModuleBoundaryFact, ...]:
    facts: list[PythonModuleBoundaryFact] = []
    for path in sorted(package_root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            facts.append(
                PythonModuleBoundaryFact(
                    path=path.as_posix(),
                    imported_modules=(),
                    mutates_sys_path=False,
                    scan_error=str(exc),
                )
            )
            continue
        facts.append(
            PythonModuleBoundaryFact(
                path=path.as_posix(),
                imported_modules=iter_import_modules(tree),
                mutates_sys_path=tree_mutates_sys_path(tree),
            )
        )
    return tuple(facts)


def scan_failure_issues(
    facts: tuple[PythonModuleBoundaryFact, ...],
) -> tuple[ValidationIssue, ...]:
    return tuple(
        ValidationIssue(
            code="pack_boundary_scan_failed",
            message=f"Could not parse Python module during boundary scan: {fact.scan_error}",
            location=fact.path,
        )
        for fact in facts
        if fact.scan_error is not None
    )


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
