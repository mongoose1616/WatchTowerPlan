"""Repo-local bootstrap helpers for domain-owned package roots."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_plan_python_src_on_path() -> str | None:
    """Add the repo-local plan Python source root to ``sys.path`` when present."""

    repo_root = Path(__file__).resolve().parents[4]
    plan_python_src = repo_root / "plan" / "python" / "src"
    if not plan_python_src.exists():
        return None
    path_value = str(plan_python_src)
    if path_value not in sys.path:
        sys.path.insert(0, path_value)
    return path_value


__all__ = ["ensure_plan_python_src_on_path"]
