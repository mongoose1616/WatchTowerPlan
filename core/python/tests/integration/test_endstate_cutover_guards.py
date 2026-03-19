from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

ACTIVE_SURFACE_ROOTS = (
    REPO_ROOT / ".github",
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


def test_root_docs_and_domain_packs_paths_are_gone() -> None:
    assert not (REPO_ROOT / "docs").exists()
    assert not (REPO_ROOT / "domain_packs").exists()


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
