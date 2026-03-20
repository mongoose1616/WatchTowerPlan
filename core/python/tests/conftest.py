from __future__ import annotations

import sys
from pathlib import Path


def _ensure_plan_python_src_on_path() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    plan_python_src = repo_root / "plan" / "python" / "src"
    if not plan_python_src.exists():
        return
    path_value = str(plan_python_src)
    if path_value not in sys.path:
        sys.path.insert(0, path_value)


_ensure_plan_python_src_on_path()
